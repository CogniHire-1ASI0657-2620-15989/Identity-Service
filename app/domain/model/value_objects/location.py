from dataclasses import dataclass


@dataclass(frozen=True)
class Location:
    city: str
    country: str

    def __post_init__(self):
        city = self.city.strip()
        country = self.country.strip()

        if not city:
            raise ValueError("La ciudad no puede estar vacía.")

        if not country:
            raise ValueError("El país no puede estar vacío.")

        object.__setattr__(self, "city", city)
        object.__setattr__(self, "country", country)

    def __str__(self) -> str:
        return f"{self.city}, {self.country}"