from dataclasses import dataclass


@dataclass(frozen=True)
class PersonName:
    value: str

    def __post_init__(self):
        normalized = self.value.strip()

        if not normalized:
            raise ValueError("El nombre no puede estar vacío.")

        if len(normalized) > 150:
            raise ValueError("El nombre no puede superar los 150 caracteres.")

        object.__setattr__(self, "value", normalized)

    def __str__(self) -> str:
        return self.value