from dataclasses import dataclass


@dataclass(frozen=True)
class ClosureReasonDTO:
    code: str
    title: str
    user_comment: str
