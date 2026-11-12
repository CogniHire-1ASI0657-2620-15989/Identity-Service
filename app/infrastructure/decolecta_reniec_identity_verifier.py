import httpx

from app.application.ports.reniec_identity_verifier import (
    ReniecIdentity,
    ReniecIdentityNotFound,
    ReniecIdentityUnavailable,
    ReniecIdentityVerifier,
)
from app.observability import outbound_headers


class DecolectaReniecIdentityVerifier(ReniecIdentityVerifier):
    """Adapter for Decolecta's RENIEC DNI lookup endpoint."""

    def __init__(self, base_url: str, api_key: str, timeout_seconds: float):
        self._base_url = base_url.rstrip("/")
        self._api_key = api_key
        self._timeout_seconds = timeout_seconds

    def find_by_dni(self, dni: str) -> ReniecIdentity:
        try:
            with httpx.Client(timeout=self._timeout_seconds) as client:
                response = client.get(
                    f"{self._base_url}/v1/reniec/dni",
                    params={"numero": dni},
                    headers=outbound_headers({"Authorization": f"Bearer {self._api_key}", "Accept": "application/json"}),
                )
        except httpx.HTTPError as exc:
            raise ReniecIdentityUnavailable("RENIEC validation is temporarily unavailable.") from exc

        if response.status_code == 404:
            raise ReniecIdentityNotFound("DNI not found.")
        if response.status_code >= 400:
            raise ReniecIdentityUnavailable("RENIEC validation is temporarily unavailable.")

        try:
            data = response.json()
            identity = ReniecIdentity(
                first_name=str(data["first_name"]),
                first_last_name=str(data["first_last_name"]),
                second_last_name=str(data["second_last_name"]),
                document_number=str(data["document_number"]),
            )
        except (KeyError, TypeError, ValueError) as exc:
            raise ReniecIdentityUnavailable("RENIEC validation returned an invalid response.") from exc

        if identity.document_number != dni:
            raise ReniecIdentityUnavailable("RENIEC validation returned an inconsistent response.")
        return identity
