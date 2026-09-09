from dataclasses import dataclass

@dataclass(frozen=True)
class EmailAddress:
    value: str

    def __post_init__(self):
        normalized = self.value.strip().lower()

        if not normalized:
            raise ValueError("El email no puede estar vacío.")

        if "@" not in normalized:
            raise ValueError("El email no tiene un formato válido.")

        object.__setattr__(self, 'value', normalized)

    def __str__(self) -> str:
        return self.value