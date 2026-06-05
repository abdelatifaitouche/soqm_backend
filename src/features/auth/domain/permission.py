from dataclasses import dataclass


@dataclass
class Permission:
    resource: str
    action: str
