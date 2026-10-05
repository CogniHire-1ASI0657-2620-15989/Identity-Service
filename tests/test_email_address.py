import pytest

from app.domain.model.value_objects.email_address import EmailAddress


def test_email_address_is_normalized_to_lowercase():
    # Arrange
    raw_email = "  Jeremy@UPC.EDU.PE  "

    # Act
    email = EmailAddress(raw_email)

    # Assert
    assert email.value == "jeremy@upc.edu.pe"
    assert str(email) == "jeremy@upc.edu.pe"


@pytest.mark.parametrize("raw_email", ["", "   ", "correo-sin-arroba"])
def test_email_address_rejects_empty_or_malformed_values(raw_email: str):
    # Arrange
    invalid_email = raw_email

    # Act / Assert
    with pytest.raises(ValueError):
        EmailAddress(invalid_email)
