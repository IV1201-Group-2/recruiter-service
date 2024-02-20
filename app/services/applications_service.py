from sqlalchemy.exc import NoResultFound, SQLAlchemyError

from app.repositories.applications_repository import \
    get_application_statuses_from_db, get_availabilities_from_db, \
    get_competences_from_db, get_personal_info_from_db


def compile_applications() -> tuple[list, list]:
    """
    Compiles applications information.

    This function fetches the applications information from the database. It
    checks each application status and compiles the personal information,
    competences, and availabilities related to each application.

    :returns: A tuple containing a list of errors and the compiled applications
    :raises NoResultFound: If no application statuses are found.
    :raises SQLAlchemyError: If there is a database issue.
    """

    application_statuses = get_application_statuses_from_db()
    compiled_applications = []
    errors = []

    for entry in application_statuses:
        try:
            person_id = entry.person_id
            personal_info = get_personal_info_from_db(person_id).to_dict()
            competences = get_competences_from_db(person_id)
            availabilities = get_availabilities_from_db(person_id)

            compiled_application = {
                'personal_info': personal_info,
                'competences': [competence.to_dict() for competence in
                                competences],
                'availabilities': [availability.to_dict() for availability in
                                   availabilities],
                'status': entry.status
            }

            compiled_applications.append(compiled_application)

        except (NoResultFound, SQLAlchemyError) as exception:
            errors.append({'error': exception.args[0]})
            continue

    return errors, compiled_applications
