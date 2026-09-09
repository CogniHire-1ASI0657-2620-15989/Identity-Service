from enum import Enum


class UserSegment(str, Enum):
    INTERN = "practicante"
    WORKER = "trabajador"

    @classmethod
    def from_value(cls, value: str) -> "UserSegment":
        normalized = value.strip().lower()

        for segment in cls:
            if segment.value == normalized:
                return segment

        raise ValueError(
            f"Segmento inválido: {value}. "
            f"Valores permitidos: practicante, trabajador."
        )