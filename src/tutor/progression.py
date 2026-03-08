from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

ProgressionAction = Literal["remind", "ask_confirm", "advance", "stay"]


@dataclass(frozen=True)
class ProgressionDecision:
    action: ProgressionAction
    message: str


def decide_progression(
    user_intent: str,
    key_points_covered: bool,
    pending_gaps: list[str],
    user_confirmation: bool | None,
) -> ProgressionDecision:
    if user_intent != "next_lesson":
        return ProgressionDecision(action="stay", message="")

    if key_points_covered or user_confirmation is True:
        return ProgressionDecision(
            action="advance",
            message="Proceeding to the next lesson.",
        )

    if user_confirmation is False:
        return ProgressionDecision(
            action="stay",
            message="We'll stay on this lesson. Let's close the remaining gaps first.",
        )

    gap_summary = ", ".join(pending_gaps) if pending_gaps else "a few key points"
    return ProgressionDecision(
        action="ask_confirm",
        message=f"Before moving on, we still need to cover: {gap_summary}. Do you still want to continue to the next lesson?",
    )
