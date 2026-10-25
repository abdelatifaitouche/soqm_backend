from dataclasses import dataclass


@dataclass(frozen=True)
class ClosureReason:
    closure_code: str
    closure_title: str
    closure_reason_comment: str
