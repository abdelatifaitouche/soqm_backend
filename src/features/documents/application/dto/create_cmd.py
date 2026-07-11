from dataclasses import dataclass
from typing import BinaryIO


@dataclass(frozen=True)
class CreateDocument:
    title: str
    description: str
    document_type: str
    filesize: int
    filename: str
    content_type: str
    file: BinaryIO
