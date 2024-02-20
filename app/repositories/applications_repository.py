from flask import current_app
from sqlalchemy.exc import NoResultFound, SQLAlchemyError

from app.models.application import ApplicationStatus
from app.models.availability import Availability
from app.models.competence_profile import CompetenceProfile
from app.models.person import Person


def get_application_statuses_from_db() -> list[ApplicationStatus]:
    try:
        application_statuses = ApplicationStatus.query.all()
    except SQLAlchemyError as exception:
        current_app.logger.error(exception)
        raise SQLAlchemyError

    if not application_statuses:
        current_app.logger.error('NO_APPLICATION_STATUSES_FOUND')
        raise NoResultFound('NO_APPLICATION_STATUSES_FOUND')
    return application_statuses


def get_personal_info_from_db(person_id: int) -> Person:
    try:
        applicant = Person.query.filter_by(person_id=person_id).first()
    except SQLAlchemyError as exception:
        current_app.logger.error(exception)
        raise SQLAlchemyError(f'COULD_NOT_FETCH_PERSON: {person_id}')

    if not applicant:
        current_app.logger.error(f'PERSON_NOT_FOUND: {person_id}')
        raise NoResultFound(f'PERSON_NOT_FOUND: {person_id}')
    return applicant


def get_competences_from_db(person_id: int) -> list[CompetenceProfile]:
    try:
        return CompetenceProfile.query.filter_by(person_id=person_id).all()
    except SQLAlchemyError as exception:
        current_app.logger.error(exception)
        raise SQLAlchemyError(f'COULD_NOT_FETCH_COMPETENCES: {person_id}')


def get_availabilities_from_db(person_id: int) -> list[CompetenceProfile]:
    try:
        availabilities = Availability.query.filter_by(
                person_id=person_id).all()

    except SQLAlchemyError as exception:
        current_app.logger.error(exception)
        raise SQLAlchemyError(f'COULD_NOT_FETCH_AVAILABILITIES: {person_id}')

    if not availabilities:
        current_app.logger.error(
                f'NO_AVAILABILITIES_FOUND_FOR_PERSON: {person_id}')
        raise NoResultFound(
                f'NO_AVAILABILITIES_FOUND_FOR_PERSON: {person_id}')
    return availabilities
