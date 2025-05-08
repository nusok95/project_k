from typing import Optional, List, Any, Dict
from pydantic import BaseModel

class Prompt(BaseModel):
    goal: Optional[str] = None
    return_format: Optional[str] = None
    warnings: Optional[str] = None
    context_dump: Optional[str] = None

    def _format_section(self, title: str, content: Optional[str]) -> Optional[str]:
        if content:
            return f"### {title} ###\n{content}"
        return None

    def to_str(self) -> str:
        parts = []
        
        goal_section = self._format_section("Goal", self.goal)
        if goal_section:
            parts.append(goal_section)

        format_section = self._format_section("Desired Return Format", self.return_format)
        if format_section:
            parts.append(format_section)

        context_section = self._format_section("Context", self.context_dump)
        if context_section:
            parts.append(context_section)

        warnings_section = self._format_section("Important Warnings/Considerations", self.warnings)
        if warnings_section:
            parts.append(warnings_section)

        return "\n\n".join(parts).strip()

class PromptBuilderService:

    def __init__(self):
        pass 

    def create_prompt(
        self,
        goal: Optional[str] = None,
        return_format: Optional[str] = None,
        warnings: Optional[str] = None,
        context_dump: Optional[str] = None
    ) -> Prompt:
        return Prompt(
            goal=goal,
            return_format=return_format,
            warnings=warnings,
            context_dump=context_dump
        )
