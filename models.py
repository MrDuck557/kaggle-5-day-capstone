from typing import List
from pydantic import BaseModel, Field

class Side(BaseModel):
    id: str = Field(description="Unique short identifier for the side, e.g., 'pro', 'con', 'hybrid'")
    name: str = Field(description="Display name of the side, e.g., 'Pro-Nuclear Power'")
    description: str = Field(description="Brief summary of this side's core stance")
    persona: str = Field(description="Instructions on how an agent representing this side should speak, its tone, values, and perspective")

class Issue(BaseModel):
    id: str = Field(description="Unique short identifier for the issue, e.g., 'safety', 'cost', 'environment'")
    name: str = Field(description="Short display name of the issue, e.g., 'Safety & Waste Management'")
    description: str = Field(description="Brief description of the core question or aspect of this issue")

class Argument(BaseModel):
    side_id: str = Field(description="The ID of the side presenting this argument")
    issue_id: str = Field(description="The ID of the issue this argument addresses")
    text: str = Field(description="The core argument text explaining the side's stance on this issue")

class Debate(BaseModel):
    topic: str = Field(description="The main topic of the debate, e.g., 'Should remote work be the default?'")
    sides: List[Side] = Field(description="The different sides or perspectives involved in the debate")
    issues: List[Issue] = Field(description="The key issues or dimensions of the debate")
    arguments: List[Argument] = Field(description="The pre-defined arguments of each side for each issue")

class ChatMessage(BaseModel):
    role: str = Field(description="The role of the sender: 'user' or 'agent'")
    content: str = Field(description="The text content of the message")

class ConversationLog(BaseModel):
    side_id: str = Field(description="The ID of the side this conversation is with")
    issue_id: str = Field(description="The ID of the issue being discussed")
    history: List[ChatMessage] = Field(default_factory=list, description="Chronological list of chat messages in this conversation")
