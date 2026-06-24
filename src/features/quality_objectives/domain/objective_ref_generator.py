from src.core.exceptions import ValidationError


class ObjectiveRefGenerator:
    @staticmethod
    def seq2ref(seq: int):
        """
        input : seq integer
        returns :
            - aaA
        """
        if seq < 0:
            raise ValidationError(
                "Sequence Number cannot be negative",
            )

        result = ""

        while seq:
            seq -= 1
            result = chr(ord("A") + seq % 26)
            seq //= 26

        if len(result) == 1:
            return result.lower()
        return result[:-1].lower() + result[-1]

    @staticmethod
    def generate_objective_ref(component_order: int, seq: int) -> str:
        alpha_seq: str = ObjectiveRefGenerator.seq2ref(seq)
        return f"{component_order}{alpha_seq}"
