import os
from abc import ABC, abstractmethod
from typing import Dict, List
from models import Debate, Side, Issue, Argument, ChatMessage

# ==========================================
# Abstract Base Class (Interface)
# ==========================================
class BaseDebateAgent(ABC):
    @abstractmethod
    def generate_debate_structure(self, topic: str) -> Debate:
        """
        Stage 1: Analyzes the topic and returns a structured Debate object.
        """
        pass

    @abstractmethod
    def ask_about_issue(self, side: Side, issue: Issue, debate_context: Debate, chat_history: List[ChatMessage] = None) -> str:
        """
        Stage 2: Generates a response from a specific side's persona regarding a chosen issue, using chat history.
        """
        pass

    @abstractmethod
    def generate_arguments_for_issue(self, debate_context: Debate, new_issue: Issue) -> List[Argument]:
        """
        Generates arguments for each side on a newly added issue.
        """
        pass


# ==========================================
# Mock Debate Agent Implementation
# ==========================================
class MockDebateAgent(BaseDebateAgent):
    def __init__(self):
        self.mock_debates: Dict[str, Debate] = {}
        self._initialize_mock_data()

    def _initialize_mock_data(self):
        # 1. Remote Work Debate
        remote_sides = [
            Side(
                id="remote_first",
                name="Remote-First Advocacy",
                description="Believes work is an activity, not a place. Focuses on autonomy, flexibility, and productivity.",
                persona="You are a passionate Remote-First Advocate. You focus on individual autonomy, work-life balance, lack of commutes, and global talent. Speak in a modern, forward-thinking, and worker-centric tone. Keep it concise."
            ),
            Side(
                id="office_first",
                name="Office-First Advocacy",
                description="Believes physical proximity is essential for collaboration, mentorship, security, and company culture.",
                persona="You are a dedicated Office-First Advocate. You emphasize the power of face-to-face meetings, spontaneous whiteboard ideas, corporate culture, onboarding of junior staff, and separating home from work. Speak in an executive, team-oriented, and structured tone. Keep it concise."
            ),
            Side(
                id="hybrid_balance",
                name="Hybrid-Work Pragmatism",
                description="Believes in a compromise: structured office days for collaborative tasks and remote days for deep execution.",
                persona="You are a Hybrid-Work Pragmatist. You believe in balance: using the office for collaboration/relationship building and home for focus. Speak in a sensible, managerial, and realistic tone. Keep it concise."
            )
        ]

        remote_issues = [
            Issue(
                id="productivity",
                name="Productivity & Deep Work",
                description="Where do employees perform tasks most efficiently and with the best concentration?"
            ),
            Issue(
                id="collaboration",
                name="Collaboration & Innovation",
                description="How does team location affect brainstorming, mentoring, and spontaneous connection?"
            ),
            Issue(
                id="wellbeing",
                name="Work-Life Balance & Burnout",
                description="The impact of commutes, work hours, isolation, and flexibility on employee health."
            ),
            Issue(
                id="infrastructure",
                name="Costs & Office Real Estate",
                description="The financial impact on corporate office rent, home office utilities, and regional economies."
            )
        ]

        remote_arguments = [
            Argument(
                side_id="remote_first",
                issue_id="productivity",
                text="Individual contributors experience far fewer interruptions at home. Deep focus time is maximized, leading to higher quality work without office distractions."
            ),
            Argument(
                side_id="office_first",
                issue_id="productivity",
                text="While individuals feel productive, team throughput suffers. Physical proximity allows instant resolution of blockers and keeps everyone aligned without endless Zoom calls."
            ),
            Argument(
                side_id="hybrid_balance",
                issue_id="productivity",
                text="The best approach is splitting tasks. Independent writing, coding, and analysis are most productive at home, while alignment and planning are best in the office."
            ),
            Argument(
                side_id="remote_first",
                issue_id="collaboration",
                text="Collaboration in a remote setting is more structured, documented, and inclusive. Asynchronous tools ensure that introverted team members and different timezones can collaborate equally."
            ),
            Argument(
                side_id="office_first",
                issue_id="collaboration",
                text="Serendipitous encounters at the watercooler and physical brainstorming sessions yield the highest innovation. Junior staff learn via osmosis by observing senior colleagues in-person."
            ),
            Argument(
                side_id="hybrid_balance",
                issue_id="collaboration",
                text="We should coordinate office days specifically for collaboration, workshops, and team-building, and leave remote days entirely for distraction-free execution."
            ),
            Argument(
                side_id="remote_first",
                issue_id="wellbeing",
                text="Eliminating daily commutes saves hours of stress every week, allows healthier eating, and gives parents the flexibility to manage family life, reducing overall burnout."
            ),
            Argument(
                side_id="office_first",
                issue_id="wellbeing",
                text="Working from home blurs the boundary between personal life and work, causing people to work longer hours. Going to an office provides a healthy mental boundary and routine."
            ),
            Argument(
                side_id="hybrid_balance",
                issue_id="wellbeing",
                text="Hybrid work offers the 'best of both worlds'. You get the flexibility to work from home two days a week, but also the vital social interaction and human connection on office days."
            ),
            Argument(
                side_id="remote_first",
                issue_id="infrastructure",
                text="Companies save millions on premium real estate and facilities. Workers save on commuting costs. It also distributes wealth away from congested cities to suburban and rural areas."
            ),
            Argument(
                side_id="office_first",
                issue_id="infrastructure",
                text="Empty offices hurt local small businesses and public transit systems. Additionally, companies must bear security risks and pay for redundant IT/home-office equipment."
            ),
            Argument(
                side_id="hybrid_balance",
                issue_id="infrastructure",
                text="Companies can downsize office footprints by using hot-desking, reducing overhead while maintaining a physical base for core gatherings."
            )
        ]

        self.mock_debates["remote work"] = Debate(
            topic="Should Remote Work be the Default?",
            sides=remote_sides,
            issues=remote_issues,
            arguments=remote_arguments
        )

        # 2. Nuclear Energy Debate
        nuclear_sides = [
            Side(
                id="pro_nuclear",
                name="Pro-Nuclear Coalition",
                description="Views nuclear power as a clean, reliable, and high-density baseload energy source crucial for deep decarbonization.",
                persona="You are a Pro-Nuclear Advocate. You rely on statistical safety data, energy density facts, and grid reliability arguments. Speak in a scientific, objective, and optimistic tone. Keep it concise."
            ),
            Side(
                id="anti_nuclear",
                name="Anti-Nuclear / Renewables First",
                description="Believes nuclear is too slow, too expensive, safety-risky, and detracts from rapid deployment of wind and solar.",
                persona="You are an Anti-Nuclear Advocate. You highlight radiation risks, unresolved waste storage, catastrophic accidents, construction delays, and weapon proliferation. Speak in an urgent, risk-conscious, and environmentalist tone. Keep it concise."
            )
        ]

        nuclear_issues = [
            Issue(
                id="climate",
                name="Decarbonization & Climate Change",
                description="How effectively and rapidly does the energy source reduce greenhouse gas emissions?"
            ),
            Issue(
                id="safety",
                name="Safety & Radioactive Waste",
                description="The risks of reactor meltdowns, weapons proliferation, and storing toxic waste for thousands of years."
            ),
            Issue(
                id="cost_time",
                name="Economics & Grid Connection Time",
                description="Is the construction cost-effective, and can reactors be built fast enough to meet near-term climate goals?"
            ),
            Issue(
                id="reliability",
                name="Baseload & Grid Stability",
                description="Can the source provide stable, 24/7 power regardless of weather or season?"
            )
        ]

        nuclear_arguments = [
            Argument(
                side_id="pro_nuclear",
                issue_id="climate",
                text="Nuclear plants produce zero greenhouse gases during operation. Their extremely high energy density means they require very little land compared to massive wind or solar farms."
            ),
            Argument(
                side_id="anti_nuclear",
                issue_id="climate",
                text="Although operating emissions are low, the carbon footprint of uranium mining, refining, and concrete-heavy construction is high. Renewables provide faster, cleaner carbon reduction."
            ),
            Argument(
                side_id="pro_nuclear",
                issue_id="safety",
                text="Modern Generation III+ and IV reactors have passive cooling systems that prevent meltdowns. Statistically, nuclear has fewer deaths per TWh than even wind and solar."
            ),
            Argument(
                side_id="anti_nuclear",
                issue_id="safety",
                text="A single nuclear accident (like Chernobyl or Fukushima) is globally catastrophic. No country has a long-term, fully operational deep geological repository for high-level waste."
            ),
            Argument(
                side_id="pro_nuclear",
                issue_id="cost_time",
                text="While initial capital costs are high, reactors run for 60 to 80 years. Over their lifespan, they supply stable electricity prices unaffected by fuel price spikes."
            ),
            Argument(
                side_id="anti_nuclear",
                issue_id="cost_time",
                text="Nuclear projects are notorious for massive budget overruns and taking 10-15 years to build. Wind, solar, and battery storage can be deployed in a fraction of the time and cost."
            ),
            Argument(
                side_id="pro_nuclear",
                issue_id="reliability",
                text="Nuclear provides constant, high-output baseload power. It is unaffected by weather, unlike wind and solar, which require expensive, non-existent grid-scale battery storage."
            ),
            Argument(
                side_id="anti_nuclear",
                issue_id="reliability",
                text="A modern smart grid does not need inflexible baseload. Mixing solar, wind, geothermal, smart demand-response, and battery storage is safer and more flexible than nuclear."
            )
        ]

        self.mock_debates["nuclear energy"] = Debate(
            topic="Is Nuclear Energy a Sustainable Solution?",
            sides=nuclear_sides,
            issues=nuclear_issues,
            arguments=nuclear_arguments
        )

    def _get_generic_debate(self, topic: str) -> Debate:
        sides = [
            Side(
                id="pro",
                name=f"Pro-'{topic}' Perspective",
                description=f"Supports the adoption, expansion, or positive view of: {topic}.",
                persona=f"You represent the supportive side of the debate: '{topic}'. You highlight progress, benefits, potential, and constructive solutions. Speak in an encouraging, hopeful, and logical tone."
            ),
            Side(
                id="con",
                name=f"Con-'{topic}' Perspective",
                description=f"Raises critical questions, highlights risks, or opposes: {topic}.",
                persona=f"You represent the critical/opposing side of the debate: '{topic}'. You highlight risks, costs, safety, unintended consequences, and ethical considerations. Speak in a cautious, analytical, and critical tone."
            )
        ]
        
        issues = [
            Issue(
                id="feasibility",
                name="Feasibility & Economic Cost",
                description="Is it financially viable, practical to implement, and worth the resources?"
            ),
            Issue(
                id="social_impact",
                name="Social & Ethical Impact",
                description="How does this affect communities, equity, daily life, and human values?"
            ),
            Issue(
                id="safety_risks",
                name="Safety & Unintended Consequences",
                description="What are the potential negative side effects, safety hazards, or long-term risks?"
            )
        ]
        
        arguments = [
            Argument(
                side_id="pro",
                issue_id="feasibility",
                text=f"Investing in '{topic}' creates long-term efficiencies and economic growth. The initial setup cost is offset by future dividends and societal progress."
            ),
            Argument(
                side_id="con",
                issue_id="feasibility",
                text=f"The financial burden of '{topic}' is disproportionate. It requires massive resources that would yield better results if directed toward existing, proven solutions."
            ),
            Argument(
                side_id="pro",
                issue_id="social_impact",
                text=f"It fosters connection, reduces inequality, and empowers individuals to achieve better outcomes, enhancing general human well-being."
            ),
            Argument(
                side_id="con",
                issue_id="social_impact",
                text=f"It risks creating new divides, disrupting community trust, or raising deep ethical questions about autonomy and fairness."
            ),
            Argument(
                side_id="pro",
                issue_id="safety_risks",
                text=f"Modern oversight and smart regulation can easily manage any hazards. The potential gains far outweigh any controlled risks."
            ),
            Argument(
                side_id="con",
                issue_id="safety_risks",
                text=f"We cannot predict the cascading risks or system failures that could occur. Proceeding without absolute safety guarantees is irresponsible."
            )
        ]
        
        return Debate(
            topic=topic,
            sides=sides,
            issues=issues,
            arguments=arguments
        )

    def generate_debate_structure(self, topic: str) -> Debate:
        normalized = topic.lower()
        if "remote" in normalized or "office" in normalized or "wfh" in normalized:
            return self.mock_debates["remote work"]
        elif "nuclear" in normalized or "fission" in normalized or "reactor" in normalized:
            return self.mock_debates["nuclear energy"]
        else:
            return self._get_generic_debate(topic)

    def ask_about_issue(self, side: Side, issue: Issue, debate_context: Debate, chat_history: List[ChatMessage] = None) -> str:
        # Find the predefined argument
        base_argument = None
        for arg in debate_context.arguments:
            if arg.side_id == side.id and arg.issue_id == issue.id:
                base_argument = arg.text
                break
                
        if not base_argument:
            base_argument = f"We believe our stance on '{issue.name}' is the most reasonable and beneficial."

        if not chat_history:
            return f"[{side.name} Response on {issue.name}]:\n\"{base_argument}\""
        else:
            # Last user message is the latest user question
            user_messages = [msg.content for msg in chat_history if msg.role == "user"]
            last_user_msg = user_messages[-1] if user_messages else "Please explain your argument on this issue."
            return (
                f"[{side.name} Response to your question on {issue.name}]:\n"
                f"\"Addressing your question: '{last_user_msg}'. As a defender of our stance, we must emphasize: "
                f"{base_argument[:-1] if base_argument.endswith('.') else base_argument}. "
                f"We believe this directly resolves the concern you raised.\""
            )

    def generate_arguments_for_issue(self, debate_context: Debate, new_issue: Issue) -> List[Argument]:
        generated_arguments = []
        for side in debate_context.sides:
            text = (
                f"For the new issue '{new_issue.name}', we emphasize that our core stance "
                f"({side.description[:-1] if side.description.endswith('.') else side.description}) "
                f"provides the most optimal approach. We focus heavily on resolving {new_issue.description}."
            )
            generated_arguments.append(
                Argument(side_id=side.id, issue_id=new_issue.id, text=text)
            )
        return generated_arguments


# ==========================================
# LLM (Gemini) Debate Agent Implementation
# ==========================================
class LLMDebateAgent(BaseDebateAgent):
    def __init__(self, api_key: str):
        self.api_key = api_key
        
        # Initialize the new google-genai Client
        from google import genai
        self.client = genai.Client(api_key=self.api_key)
        self.model_name = "gemini-2.5-flash"

    def generate_debate_structure(self, topic: str) -> Debate:
        from google.genai import types
        
        prompt = f"""
        Analyze the debate topic: "{topic}".
        Provide a comprehensive, structured breakdown of the debate:
        1. Identify 2 to 3 distinct sides or perspectives (e.g. Pro, Anti, Hybrid, etc.). For each, write a concise name, description, and persona guidelines.
        2. Identify 3 to 4 core issues or sub-topics of the debate (e.g., Cost, Safety, Culture).
        3. For every combination of side and issue, provide a brief, high-quality, representative argument text (1-2 sentences). You must supply exactly one Argument per side-issue pair.
        
        You must output JSON matching the required schema.
        """
        
        response = self.client.models.generate_content(
            model=self.model_name,
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=Debate
            )
        )
        return response.parsed

    def ask_about_issue(self, side: Side, issue: Issue, debate_context: Debate, chat_history: List[ChatMessage] = None) -> str:
        # Find the pre-defined argument first to use as context
        base_argument = None
        for arg in debate_context.arguments:
            if arg.side_id == side.id and arg.issue_id == issue.id:
                base_argument = arg.text
                break
                
        if not base_argument:
            base_argument = f"We believe our stance on '{issue.name}' is the most reasonable and beneficial."

        # Format conversation history
        history_str = ""
        if chat_history:
            for msg in chat_history:
                sender = "User" if msg.role == "user" else side.name
                history_str += f"{sender}: {msg.content}\n"

        prompt = f"""
        You are representing the side "{side.name}" in a debate about "{debate_context.topic}".
        Your core stance: {side.description}
        Your persona guidelines: {side.persona}

        The issue being discussed is: "{issue.name}" ({issue.description}).
        Your base argument on this issue is: "{base_argument}"
        
        Below is the conversation history so far:
        {history_str}
        
        Respond to the latest user question. Keep your response concise (2-4 sentences), highly persuasive, and strictly in-character. Do not start with phrases like "Sure, as a..." or refer to yourself as an AI. Respond directly.
        """
        
        response = self.client.models.generate_content(
            model=self.model_name,
            contents=prompt
        )
        return response.text.strip()

    def generate_arguments_for_issue(self, debate_context: Debate, new_issue: Issue) -> List[Argument]:
        from google.genai import types
        from pydantic import BaseModel
        
        class ArgumentList(BaseModel):
            arguments: List[Argument]
            
        sides_str = "\n".join([f"- ID: {side.id}, Name: {side.name}, Stance: {side.description}" for side in debate_context.sides])
        
        prompt = f"""
        We are adding a new issue to an ongoing debate.
        Debate Topic: "{debate_context.topic}"
        
        Here are the sides involved:
        {sides_str}
        
        The new issue to generate arguments for is:
        Name: "{new_issue.name}"
        Description: "{new_issue.description}"
        
        For each of the sides listed above, generate a representative, concise argument (1-2 sentences) explaining their stance on this new issue.
        
        You must return a JSON list of Argument objects matching the schema. Ensure that you generate exactly one argument for each side, using the exact Side ID provided.
        """
        
        response = self.client.models.generate_content(
            model=self.model_name,
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=ArgumentList
            )
        )
        parsed = response.parsed.arguments
        
        # Guarantee alignment of side_id and issue_id for all sides
        final_arguments = []
        for i, side in enumerate(debate_context.sides):
            found_arg = None
            for arg in parsed:
                if arg.side_id.strip().lower() == side.id.strip().lower():
                    found_arg = arg
                    break
            
            if found_arg:
                found_arg.side_id = side.id
                found_arg.issue_id = new_issue.id
                final_arguments.append(found_arg)
            else:
                if i < len(parsed):
                    arg = parsed[i]
                    arg.side_id = side.id
                    arg.issue_id = new_issue.id
                    final_arguments.append(arg)
                else:
                    final_arguments.append(
                        Argument(
                            side_id=side.id,
                            issue_id=new_issue.id,
                            text=f"Regarding '{new_issue.name}', we believe that our perspective supports this by focusing on our core stance."
                        )
                    )
        return final_arguments
