from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field

class IntentDetail(BaseModel):
    """
    Represents a single recognized intent and its associated information.
    """
    type: str = Field(..., description="The type of intent recognized.")
    attributes: Optional[List[str]] = Field(default_factory=list)
    entities: Optional[Dict[str, Any]] = Field(default_factory=dict)
    missing_info: Optional[List[str]] = Field(default_factory=list)
    details: Optional[Any] = None

class UserIntentionResponse(BaseModel):
    """
    Represents the structured response from the first LLM call,
    detailing the user's intents.
    """
    intents: List[IntentDetail] = Field(..., description="List of intents recognized from the user's message.") 