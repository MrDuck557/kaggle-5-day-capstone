import sys
import time
import os
from typing import Dict
from dotenv import load_dotenv
from models import Debate, Side, Issue, Argument, ChatMessage, ConversationLog
from agents import BaseDebateAgent, MockDebateAgent, LLMDebateAgent

# Colors for terminal styling (ANSI Escape Codes)
BLUE = "\033[94m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
BOLD = "\033[1m"
UNDERLINE = "\033[4m"
RESET = "\033[0m"
CYAN = "\033[96m"

def print_header(text: str):
    print(f"\n{BOLD}{BLUE}{'=' * 60}{RESET}")
    print(f"{BOLD}{BLUE} {text.upper()}{RESET}")
    print(f"{BOLD}{BLUE}{'=' * 60}{RESET}")

def print_subheader(text: str):
    print(f"\n{BOLD}{CYAN}--- {text} ---{RESET}")

def show_spinner(duration: float = 1.5, message: str = "Analyzing"):
    chars = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
    end_time = time.time() + duration
    i = 0
    sys.stdout.write(f" {message} ")
    sys.stdout.flush()
    while time.time() < end_time:
        sys.stdout.write(f"\r {message} {chars[i % len(chars)]}")
        sys.stdout.flush()
        time.sleep(0.1)
        i += 1
    sys.stdout.write("\r" + " " * (len(message) + 10) + "\r")
    sys.stdout.flush()

def display_debate_overview(debate: Debate):
    print_header("Debate Overview")
    print(f"{BOLD}Topic:{RESET} {debate.topic}")
    
    print_subheader("Sides / Perspectives Discovered")
    for i, side in enumerate(debate.sides, 1):
        print(f" {BOLD}{i}. {side.name}{RESET}")
        print(f"    Stance: {side.description}")
        
    print_subheader("Core Issues Identified")
    for i, issue in enumerate(debate.issues, 1):
        print(f" {BOLD}{i}. {issue.name}{RESET}")
        print(f"    Aspect: {issue.description}")

def view_argument_matrix(debate: Debate):
    print_header("Argument Matrix")
    for issue in debate.issues:
        print_subheader(issue.name)
        print(f"{UNDERLINE}Question:{RESET} {issue.description}\n")
        
        for side in debate.sides:
            # Find argument
            arg_text = "No argument found."
            for arg in debate.arguments:
                if arg.side_id == side.id and arg.issue_id == issue.id:
                    arg_text = arg.text
                    break
            print(f"  {BOLD}{side.name}:{RESET}")
            print(f"    \"{arg_text}\"\n")

def ask_specific_side(debate: Debate, agent: BaseDebateAgent, conversations: Dict[str, ConversationLog]):
    print_header("Talk with a Specific Side")
    
    # 1. Select Issue
    print("\nSelect an Issue to discuss:")
    for i, issue in enumerate(debate.issues, 1):
        print(f"  [{i}] {issue.name}")
    
    try:
        issue_choice = int(input("\nEnter choice (number): ")) - 1
        if issue_choice < 0 or issue_choice >= len(debate.issues):
            print(f"{RED}Invalid issue selection.{RESET}")
            return
    except ValueError:
        print(f"{RED}Please enter a valid number.{RESET}")
        return
        
    selected_issue = debate.issues[issue_choice]
    
    # 2. Select Side
    print(f"\nWhich perspective would you like to speak to about '{selected_issue.name}'?")
    for i, side in enumerate(debate.sides, 1):
        print(f"  [{i}] {side.name}")
        
    try:
        side_choice = int(input("\nEnter choice (number): ")) - 1
        if side_choice < 0 or side_choice >= len(debate.sides):
            print(f"{RED}Invalid side selection.{RESET}")
            return
    except ValueError:
        print(f"{RED}Please enter a valid number.{RESET}")
        return
        
    selected_side = debate.sides[side_choice]
    
    # 3. Chat Loop for this side
    print(f"\n{GREEN}Connecting you with '{selected_side.name}'...{RESET}")
    print(f"Context: {selected_side.description}")
    print(f"Issue: {selected_issue.description}\n")
    
    conv_key = f"{selected_side.id}_{selected_issue.id}"
    if conv_key not in conversations:
        conversations[conv_key] = ConversationLog(side_id=selected_side.id, issue_id=selected_issue.id, history=[])
    
    conv_log = conversations[conv_key]
    
    # Initial statement or resume history
    if not conv_log.history:
        show_spinner(1.0, f"Retrieving opening argument from {selected_side.name}")
        response = agent.ask_about_issue(selected_side, selected_issue, debate)
        conv_log.history.append(ChatMessage(role="agent", content=response))
        print(response)
    else:
        print(f"{YELLOW}[Resuming previous conversation]{RESET}")
        for msg in conv_log.history:
            sender = selected_side.name if msg.role == "agent" else "User"
            print(f"{BOLD}{sender}:{RESET} {msg.content}")
    
    while True:
        print(f"\n{BOLD}Options:{RESET} [1] Ask follow-up question, [2] Back to main menu")
        opt = input("Select option: ").strip()
        if opt == "2":
            break
        elif opt == "1":
            question = input(f"\nAsk '{selected_side.name}' a follow-up: ").strip()
            if not question:
                print(f"{YELLOW}Empty question. Returning to options.{RESET}")
                continue
            conv_log.history.append(ChatMessage(role="user", content=question))
            show_spinner(1.5, f"Agent '{selected_side.name}' is formulating response")
            response = agent.ask_about_issue(selected_side, selected_issue, debate, chat_history=conv_log.history)
            conv_log.history.append(ChatMessage(role="agent", content=response))
            print(f"\n{response}")
        else:
            print(f"{RED}Invalid choice.{RESET}")

def ask_all_sides(debate: Debate, agent: BaseDebateAgent, conversations: Dict[str, ConversationLog]):
    print_header("Compare All Sides")
    
    # 1. Select Issue
    print("\nSelect an Issue to discuss:")
    for i, issue in enumerate(debate.issues, 1):
        print(f"  [{i}] {issue.name}")
    
    try:
        issue_choice = int(input("\nEnter choice (number): ")) - 1
        if issue_choice < 0 or issue_choice >= len(debate.issues):
            print(f"{RED}Invalid issue selection.{RESET}")
            return
    except ValueError:
        print(f"{RED}Please enter a valid number.{RESET}")
        return
        
    selected_issue = debate.issues[issue_choice]
    
    question = input(f"\nEnter question/prompt to send to ALL sides (Press Enter to request their standard stance): ").strip()
    custom_q = question if question else None
    
    print_subheader(f"Querying all sides on: {selected_issue.name}")
    if custom_q:
        print(f"{BOLD}Question:{RESET} {custom_q}\n")
    
    for side in debate.sides:
        conv_key = f"{side.id}_{selected_issue.id}"
        if conv_key not in conversations:
            conversations[conv_key] = ConversationLog(side_id=side.id, issue_id=selected_issue.id, history=[])
        
        conv_log = conversations[conv_key]
        
        if custom_q:
            conv_log.history.append(ChatMessage(role="user", content=custom_q))
            show_spinner(0.8, f"Querying {side.name}")
            response = agent.ask_about_issue(side, selected_issue, debate, chat_history=conv_log.history)
            conv_log.history.append(ChatMessage(role="agent", content=response))
        else:
            # Get standard opening response
            show_spinner(0.8, f"Querying {side.name}")
            response = agent.ask_about_issue(side, selected_issue, debate)
            if not conv_log.history:
                conv_log.history.append(ChatMessage(role="agent", content=response))
        
        print(f"\n{BOLD}{side.name}:{RESET}")
        print(response)
        print("-" * 40)

def add_custom_issue(debate: Debate, agent: BaseDebateAgent):
    print_header("Add a Custom Issue")
    name = input("\nEnter the name of the new issue (e.g. 'Data Privacy'): ").strip()
    if not name:
        print(f"{RED}Issue name cannot be empty.{RESET}")
        return
        
    description = input("Enter a brief description of this issue: ").strip()
    if not description:
        print(f"{RED}Issue description cannot be empty.{RESET}")
        return
        
    issue_id = name.lower().replace(" ", "_")
    for existing in debate.issues:
        if existing.id == issue_id:
            print(f"{RED}An issue with this name already exists.{RESET}")
            return
            
    new_issue = Issue(id=issue_id, name=name, description=description)
    
    show_spinner(2.0, "Generating arguments for each side on the new issue")
    try:
        new_arguments = agent.generate_arguments_for_issue(debate, new_issue)
        debate.issues.append(new_issue)
        debate.arguments.extend(new_arguments)
        print(f"\n{GREEN}Success! The issue '{name}' has been added to the debate.{RESET}")
    except Exception as e:
        print(f"\n{RED}Error generating arguments: {e}{RESET}")

def main():
    # Load env variables
    load_dotenv()

    # Enable ANSI terminal colors on Windows if possible
    if os.name == 'nt':
        os.system('color')
        
    print_header("Welcome to Debate Explorer")
    
    # Instantiate the agent dependency based on environment configuration
    api_key = os.getenv("GEMINI_API_KEY")
    if api_key:
        agent = LLMDebateAgent(api_key=api_key)
        print(f"{GREEN}Mode: GEMINI LLM ACTIVE{RESET}")
        print(" -> Real-time topic analysis & persona generation enabled.")
    else:
        agent = MockDebateAgent()
        print(f"{YELLOW}Mode: SIMULATED MOCK DATA{RESET}")
        print(" -> Using pre-set responses to save tokens/keys.")
        print(" -> Provide `GEMINI_API_KEY` in `.env` to enable real-time Gemini LLM analysis.")
        
    print("-" * 60)
    
    debate_ctx = None
    debate_conversations: Dict[str, ConversationLog] = {}
    
    while True:
        if not debate_ctx:
            print_subheader("Stage 1: Define Debate Topic")
            print("Pre-packaged topics for instant mock testing: 'Remote Work', 'Nuclear Energy'.")
            topic = input("Enter a debate topic (or 'exit' to quit): ").strip()
            
            if not topic:
                continue
            if topic.lower() == 'exit':
                print(f"\n{BOLD}Goodbye!{RESET}")
                break
                
            show_spinner(2.0, "Analyzing topic and generating stances")
            debate_ctx = agent.generate_debate_structure(topic)
            debate_conversations = {} # Reset conversation logs for the new topic
            
            display_debate_overview(debate_ctx)
            
        print_header("Interactive Debate Menu")
        print(" 1. View Argument Matrix (Compare predefined stances)")
        print(" 2. Converse with a Specific Side (Interactive follow-up)")
        print(" 3. Ask All Sides (Compare custom questions)")
        print(" 4. Add a Custom Issue to the Debate")
        print(" 5. Start a New Debate Topic")
        print(" 6. Exit")
        
        choice = input("\nEnter choice [1-6]: ").strip()
        
        if choice == "1":
            view_argument_matrix(debate_ctx)
        elif choice == "2":
            ask_specific_side(debate_ctx, agent, debate_conversations)
        elif choice == "3":
            ask_all_sides(debate_ctx, agent, debate_conversations)
        elif choice == "4":
            add_custom_issue(debate_ctx, agent)
        elif choice == "5":
            debate_ctx = None
        elif choice == "6":
            print(f"\n{BOLD}Goodbye!{RESET}")
            break
        else:
            print(f"{RED}Invalid choice. Please enter 1-5.{RESET}")
            
        if debate_ctx:
            input(f"\n{CYAN}Press Enter to return to main menu...{RESET}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{BOLD}Program interrupted. Goodbye!{RESET}")
        sys.exit(0)
