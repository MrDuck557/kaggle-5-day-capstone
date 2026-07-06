import sys
from models import Debate, Side, Issue, Argument, ChatMessage
from agents import MockDebateAgent, BaseDebateAgent

def test_debate_model_validation():
    print("Testing data models & serialization...")
    # Validate side
    side = Side(id="pro", name="Pro-Side", description="Stance description", persona="Persona instructions")
    assert side.id == "pro"
    
    # Validate issue
    issue = Issue(id="cost", name="Cost Issue", description="Cost aspect")
    assert issue.id == "cost"
    
    # Validate argument
    argument = Argument(side_id="pro", issue_id="cost", text="Mock argument text")
    assert argument.text == "Mock argument text"
    
    # Validate debate
    debate = Debate(
        topic="Test topic",
        sides=[side],
        issues=[issue],
        arguments=[argument]
    )
    assert debate.topic == "Test topic"
    assert len(debate.sides) == 1
    print("OK: Data structures are correct.")

def test_mock_data_retrieval(agent: BaseDebateAgent):
    print("Testing mock data generation...")
    # Pre-packaged: remote work
    debate_remote = agent.generate_debate_structure("Should remote work be default?")
    assert isinstance(debate_remote, Debate)
    assert len(debate_remote.sides) == 3
    assert len(debate_remote.issues) == 4
    assert len(debate_remote.arguments) == 12
    print("OK: Pre-packaged remote work mock retrieved successfully.")
    
    # Pre-packaged: nuclear energy
    debate_nuclear = agent.generate_debate_structure("Is nuclear energy good?")
    assert isinstance(debate_nuclear, Debate)
    assert len(debate_nuclear.sides) == 2
    assert len(debate_nuclear.issues) == 4
    assert len(debate_nuclear.arguments) == 8
    print("OK: Pre-packaged nuclear energy mock retrieved successfully.")
    
    # Generic generator fallback
    debate_generic = agent.generate_debate_structure("Should space travel be funded?")
    assert isinstance(debate_generic, Debate)
    assert len(debate_generic.sides) == 2
    assert len(debate_generic.issues) == 3
    assert len(debate_generic.arguments) == 6
    assert debate_generic.topic == "Should space travel be funded?"
    print("OK: Generic fallback structure generated successfully.")

def test_mock_agent_q_and_a(agent: BaseDebateAgent):
    print("Testing mock agent Q&A response generation...")
    debate_remote = agent.generate_debate_structure("remote work")
    side = debate_remote.sides[0]  # remote_first
    issue = debate_remote.issues[0]  # productivity
    
    # Standard response
    resp_std = agent.ask_about_issue(side, issue, debate_remote)
    assert resp_std is not None
    assert side.name in resp_std
    print("OK: Standard agent response generated.")
    
    # Custom follow-up response
    history = [ChatMessage(role="user", content="What about networking?")]
    resp_custom = agent.ask_about_issue(side, issue, debate_remote, chat_history=history)
    assert resp_custom is not None
    assert "networking" in resp_custom.lower()
    print("OK: Custom follow-up agent response generated.")

def test_generate_arguments_for_issue(agent: BaseDebateAgent):
    print("Testing custom issue argument generation...")
    debate_remote = agent.generate_debate_structure("remote work")
    new_issue = Issue(id="security", name="Information Security", description="How company files and data are secured.")
    new_args = agent.generate_arguments_for_issue(debate_remote, new_issue)
    assert len(new_args) == len(debate_remote.sides)
    for arg in new_args:
        assert arg.issue_id == "security"
        assert arg.text is not None
        assert len(arg.text) > 0
    print("OK: Custom issue argument generation successful.")

def run_all_tests():
    # Instantiate MockDebateAgent to inject into the tests
    agent = MockDebateAgent()
    
    try:
        test_debate_model_validation()
        test_mock_data_retrieval(agent)
        test_mock_agent_q_and_a(agent)
        test_generate_arguments_for_issue(agent)
        print("\nAll automated tests PASSED successfully!")
        sys.exit(0)
    except AssertionError as e:
        print(f"\nAssertion Error: Test failed! {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\nError: Tests failed with exception: {e}")
        sys.exit(1)

if __name__ == "__main__":
    run_all_tests()
