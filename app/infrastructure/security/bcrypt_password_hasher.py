import bcrypt

from app.application.ports.password_hasher import PasswordHasher


class BcryptPasswordHasher(PasswordHasher):

    def hash(
        self,
        password: str
    ) -> str:

        password_bytes = password.encode("utf-8")

        hashed = bcrypt.hashpw(
            password_bytes,
            bcrypt.gensalt(),
        )

        return hashed.decode("utf-8")

    def verify(
        self,
        password: str,
        password_hash: str
    ) -> bool:

        return bcrypt.checkpw(
            password.encode("utf-8"),
            password_hash.encode("utf-8"),
        )