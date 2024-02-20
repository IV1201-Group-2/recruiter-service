import datetime as dt

from flask_jwt_extended import create_access_token

from app.extensions import database
from app.models.application import ApplicationStatus
from app.models.availability import Availability
from app.models.competence_profile import CompetenceProfile
from app.models.person import Person


def setup_user1_in_db(app):
    with (app.app_context()):
        database.session.add(Person(name='user1', surname='s1', pnr=1))
        database.session.commit()


def setup_user2_in_db(app):
    with (app.app_context()):
        database.session.add(Person(name='user2', surname='s2', pnr=2))
        database.session.commit()


def setup_user3_in_db(app):
    with (app.app_context()):
        database.session.add(Person(name='user3', surname='s3', pnr=3))
        database.session.commit()


def remove_users_from_db(app):
    with app.app_context():
        Person.query.delete()
        database.session.commit()


def setup_competence_profile_for_user1_in_db(app):
    with app.app_context():
        database.session.add(CompetenceProfile(person_id=1, competence_id=1,
                                               years_of_experience=1))
        database.session.add(CompetenceProfile(person_id=1, competence_id=1,
                                               years_of_experience=4))
        database.session.commit()


def setup_competence_profile_for_user2_in_db(app):
    with app.app_context():
        database.session.add(CompetenceProfile(person_id=2, competence_id=2,
                                               years_of_experience=2))
        database.session.commit()


def remove_competence_profiles_from_db(app):
    with app.app_context():
        CompetenceProfile.query.delete()
        database.session.commit()


def setup_availabilities_for_user1_in_db(app):
    with app.app_context():
        database.session.add(Availability(person_id=1,
                                          from_date=dt.datetime(2024, 3, 1),
                                          to_date=dt.datetime(2024, 3, 2)))
        database.session.add(Availability(person_id=1,
                                          from_date=dt.datetime(2024, 3, 4),
                                          to_date=dt.datetime(2024, 3, 5)))
        database.session.commit()


def setup_availability_for_user2_in_db(app):
    with app.app_context():
        database.session.add(Availability(person_id=2,
                                          from_date=dt.datetime(2024, 3, 2),
                                          to_date=dt.datetime(2024, 3, 3)))
        database.session.commit()


def setup_availability_for_user3_in_db(app):
    with app.app_context():
        database.session.add(Availability(person_id=3,
                                          from_date=dt.datetime(2024, 3, 3),
                                          to_date=dt.datetime(2024, 3, 4)))
        database.session.commit()


def remove_availabilities_from_db(app):
    with app.app_context():
        Availability.query.delete()
        database.session.commit()


def setup_application_status_for_user1_in_db(app):
    with app.app_context():
        database.session.add(ApplicationStatus(person_id=1))
        database.session.commit()


def setup_application_status_for_user2_in_db(app):
    with app.app_context():
        database.session.add(ApplicationStatus(person_id=2))
        database.session.commit()


def setup_application_status_for_user3_in_db(app):
    with app.app_context():
        database.session.add(ApplicationStatus(person_id=3))
        database.session.commit()


def remove_application_statuses_from_db(app):
    with app.app_context():
        ApplicationStatus.query.delete()
        database.session.commit()


def generate_token_for_person_id_1(app) -> tuple[str, str]:
    with app.app_context():
        return create_access_token(identity=None,
                                   additional_claims={'id': 1, 'role': 2},
                                   expires_delta=dt.timedelta(days=1))


def generate_token_for_recruiter(app) -> tuple[str, str]:
    with app.app_context():
        return create_access_token(identity=None,
                                   additional_claims={'id': 2, 'role': 1},
                                   expires_delta=dt.timedelta(days=1))


def setup_three_users(app):
    setup_user1_in_db(app)
    setup_user2_in_db(app)
    setup_user3_in_db(app)


def setup_application_statuses_for_all_users(app):
    setup_application_status_for_user1_in_db(app)
    setup_application_status_for_user2_in_db(app)
    setup_application_status_for_user3_in_db(app)


def setup_availabilities_for_all_users(app):
    setup_availabilities_for_user1_in_db(app)
    setup_availability_for_user2_in_db(app)
    setup_availability_for_user3_in_db(app)


def setup_competence_profiles_for_all_users(app):
    setup_competence_profile_for_user1_in_db(app)
    setup_competence_profile_for_user2_in_db(app)


def assert_application_details(application, name, surname, person_id, status,
                               competences, availabilities):
    assert application['personal_info']['name'] == name
    assert application['personal_info']['surname'] == surname
    assert application['personal_info']['person_id'] == person_id
    assert application['status'] == status
    assert application['competences'] == competences
    assert application['availabilities'] == availabilities


def cleanup_db(app):
    remove_users_from_db(app)
    remove_application_statuses_from_db(app)
    remove_competence_profiles_from_db(app)
    remove_availabilities_from_db(app)


def post_request_applications_endpoint(test_client, token):
    return test_client.get('/api/applications/',
                           headers={'Authorization': f'Bearer {token}'})
