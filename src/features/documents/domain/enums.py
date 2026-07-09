from enum import StrEnum


class DocumentStatus(StrEnum):
    ACTIVE = "active"
    ARCHIVED = "archived"
    DELETED = "deleted"


class DocumentProcessingStatus(StrEnum):
    UPLOADING = "uploading"
    UPLOADED = "uploaded"
    SCANNING = "scanning"
    READY = "ready"
    FAILED = "failed"


class DocumentType(StrEnum):
    POLICY = "policy"
    PROCEDURE = "procedure"
    TEMPLATE = "template"
    FORM = "form"
    GUIDANCE = "guidance"
    EVIDENCE = "evidence"
    STANDARD = "standard"
    OTHER = "other"
