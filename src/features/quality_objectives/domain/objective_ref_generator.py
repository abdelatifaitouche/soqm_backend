from src.core.shared.domain.exceptions import DomainValidationException


class ObjectiveRefGenerator:
    @staticmethod
    def _seq2ref(seq: int) -> str:
        if seq <= 0:
            raise DomainValidationException("Sequence Number must be greater than 0.")

        result = ""
        temp_seq = seq

        while temp_seq > 0:
            temp_seq -= 1
            remainder = temp_seq % 26
            result = (
                chr(ord("A") + remainder) + result
            )  # ✅ Prepend to fix the overwrite bug
            temp_seq //= 26

        # Enforce your custom casing requirement: 'aaA', 'a', etc.
        if len(result) == 1:
            return result.lower()
        return result[:-1].lower() + result[-1]

    @staticmethod
    def generate_objective_ref(component_order: int, seq: int) -> str:
        alpha_seq = ObjectiveRefGenerator._seq2ref(seq)
        return f"{component_order}{alpha_seq}"
