from src.core.exceptions import ValidationError


class ResponseRefGenerator:
    @staticmethod
    def _get_component_abbrv(component_name: str) -> str:
        ref: str = ""
        parts = component_name.split()
        if len(parts) == 1:
            return parts[0][0]
        ref = "".join(l[0] for l in parts[:3]).upper()
        return ref

    @classmethod
    def generate(cls, component_name: str, sequence_number: int) -> str:

        if not component_name or component_name.strip() == "":
            raise ValidationError(
                message="Invalid component name",
                details={
                    "component_name": component_name,
                },
            )

        if sequence_number < 0:
            raise ValidationError(
                message="Invalid sequence number",
                details={
                    "sequence": sequence_number,
                },
            )

        ref: str = cls._get_component_abbrv(component_name) + f"-{sequence_number}"

        return ref
