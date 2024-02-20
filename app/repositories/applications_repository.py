from flask import current_app
from sqlalchemy.exc import NoResultFound, SQLAlchemyError

from app.models.application import ApplicationStatus
from app.models.availability import Availability
from app.models.competence_profile import CompetenceProfile
from app.models.person import Person


def get_application_statuses_from_db() -> list[ApplicationStatus]:
    """
    Retrieves application statuses from the database.

    This function fetches all application statuses from the database. It
    raises an exception if there is a database issue or if no application
    statuses are found.

    :returns: A list of ApplicationStatus objects.
    :raises SQLAlchemyError: If there is a database issue.
    :raises NoResultFound: If no application statuses are found.
    """

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
    """
    Retrieves personal information of a user from the database.

    This function fetches the personal information of a user with the given
    person_id from the database. It raises an exception if there is a database
    issue or if no user is found.

    :param person_id: The id of the user to retrieve information for.
    :returns: A Person object representing the user.
    :raises SQLAlchemyError: If there is a database issue.
    :raises NoResultFound: If no user is found.
    """

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
    """
    Retrieves competences of a user from the database.

    This function fetches the competences of a user with the given person_id
    from the database. It raises an exception if there is a database issue.

    :param person_id: The id of the user to retrieve competences for.
    :returns: A list of CompetenceProfile objects representing the user's
              competences.
    :raises SQLAlchemyError: If there is a database issue.
    """

    try:
        return CompetenceProfile.query.filter_by(person_id=person_id).all()
    except SQLAlchemyError as exception:
        current_app.logger.error(exception)
        raise SQLAlchemyError(f'COULD_NOT_FETCH_COMPETENCES: {person_id}')


def get_availabilities_from_db(person_id: int) -> list[CompetenceProfile]:
    """
    Retrieves availabilities of a user from the database.

    This function fetches the availabilities of a user with the given person_id
    from the database. It raises an exception if there is a database issue or
    if no availabilities are found.

    :param person_id: The id of the user to retrieve availabilities for.
    :returns: A list of Availability objects representing the user's
              availabilities.
    :raises SQLAlchemyError: If there is a database issue.
    :raises NoResultFound: If no availabilities are found.
    """

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
