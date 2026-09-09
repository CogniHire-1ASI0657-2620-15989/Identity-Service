from sqlalchemy.orm import Session

from app.domain.model.aggregates.user import User
from app.domain.model.value_objects.email_address import EmailAddress
from app.domain.model.value_objects.location import Location
from app.domain.model.value_objects.person_name import PersonName
from app.domain.model.value_objects.user_segment import UserSegment
from app.domain.repositories.user_repository import UserRepository

from app.infrastructure.persistence.sqlalchemy.models.user_model import UserModel


class SQLAlchemyUserRepository(UserRepository):

    def __init__(self, db: Session):
        self._db = db

    def find_by_id(
        self,
        user_id: int
    ) -> User | None:

        model = (
            self._db
            .query(UserModel)
            .filter(UserModel.id == user_id)
            .first()
        )

        if model is None:
            return None

        return self._to_domain(model)

    def find_by_email(
        self,
        email: EmailAddress
    ) -> User | None:

        model = (
            self._db
            .query(UserModel)
            .filter(UserModel.email == email.value)
            .first()
        )

        if model is None:
            return None

        return self._to_domain(model)

    def save(
        self,
        user: User
    ) -> User:

        model = UserModel(
            name=user.name.value,
            email=user.email.value,
            password_hash=user.password_hash,
            segment=user.segment.value,
            city=user.location.city if user.location else None,
            country=user.location.country if user.location else None,
            target_position=user.target_position,
            expected_city=user.expected_city,
            expected_country=user.expected_country,
            work_modality=user.work_modality,
            hard_skills=user.hard_skills,
            soft_skills=user.soft_skills,
            education=user.education,
            experience=user.experience,
            languages=user.languages,
            professional_summary=user.professional_summary,
            created_at=user.created_at,
        )

        self._db.add(model)
        self._db.commit()
        self._db.refresh(model)

        return self._to_domain(model)

    def update(
        self,
        user: User
    ) -> User:

        model = (
            self._db
            .query(UserModel)
            .filter(UserModel.id == user.id)
            .first()
        )

        if model is None:
            raise ValueError("Usuario no encontrado.")

        model.name = user.name.value
        model.email = user.email.value
        model.password_hash = user.password_hash
        model.segment = user.segment.value
        model.target_position = user.target_position
        model.expected_city = user.expected_city
        model.expected_country = user.expected_country
        model.work_modality = user.work_modality
        model.hard_skills = user.hard_skills
        model.soft_skills = user.soft_skills
        model.education = user.education
        model.experience = user.experience
        model.languages = user.languages
        model.professional_summary = user.professional_summary

        if user.location:
            model.city = user.location.city
            model.country = user.location.country
        else:
            model.city = None
            model.country = None

        self._db.commit()
        self._db.refresh(model)

        return self._to_domain(model)

    def delete(
        self,
        user: User
    ) -> None:

        model = (
            self._db
            .query(UserModel)
            .filter(UserModel.id == user.id)
            .first()
        )

        if model is None:
            raise ValueError("Usuario no encontrado.")

        self._db.delete(model)
        self._db.commit()

    @staticmethod
    def _to_domain(
        model: UserModel
    ) -> User:

        location = None

        if model.city and model.country:
            location = Location(
                city=model.city,
                country=model.country,
            )

        return User(
            user_id=model.id,
            name=PersonName(model.name),
            email=EmailAddress(model.email),
            password_hash=model.password_hash,
            segment=UserSegment.from_value(model.segment),
            location=location,
            target_position=model.target_position,
            expected_city=model.expected_city,
            expected_country=model.expected_country,
            work_modality=model.work_modality,
            hard_skills=model.hard_skills or [],
            soft_skills=model.soft_skills or [],
            education=model.education or [],
            experience=model.experience or [],
            languages=model.languages or [],
            professional_summary=model.professional_summary,
            created_at=model.created_at,
        )