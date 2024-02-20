from unittest.mock import patch

import pytest
from sqlalchemy.exc import NoResultFound, SQLAlchemyError

from app.repositories.applications_repository import \
    get_application_statuses_from_db, get_availabilities_from_db, \
    get_competences_from_db, \
    get_personal_info_from_db
from tests.utilities.utility_functions import cleanup_db, \
    setup_application_status_for_user1_in_db, \
    setup_availabilities_for_user1_in_db, \
    setup_competence_profile_for_user2_in_db, setup_user1_in_db


def test_get_application_statuses_from_db_success(app_with_client):
    app, _ = app_with_client
    setup_application_status_for_user1_in_db(app)

    with app.app_context():
        application_statuses = get_application_statuses_from_db()
        assert len(application_statuses) == 1
        assert application_statuses[0].person_id == 1
        assert application_statuses[0].status == 'UNHANDLED'

    cleanup_db(app)


def test_get_application_statuses_from_db_no_statuses(app_with_client):
    app, _ = app_with_client

    with app.app_context():
        try:
            get_application_statuses_from_db()
            assert False
        except NoResultFound:
            assert True


def test_get_application_statuses_from_db_sqlalchemy_error(app_with_client):
    app, _ = app_with_client
    setup_application_status_for_user1_in_db(app)

    with (app.app_context()):
        with patch('app.models.application.ApplicationStatus.query') as mock:
            mock.all.side_effect = SQLAlchemyError
            with pytest.raises(SQLAlchemyError) as exception_info:
                get_application_statuses_from_db()

            assert isinstance(exception_info.value, SQLAlchemyError)
            mock.all.assert_called_once()


def test_get_personal_info_from_db_success(app_with_client):
    app, _ = app_with_client
    setup_user1_in_db(app)

    with app.app_context():
        personal_info = get_personal_info_from_db(1)
        assert personal_info.person_id == 1
        assert personal_info.name == 'user1'
        assert personal_info.surname == 's1'
        assert personal_info.pnr == '1'

    cleanup_db(app)


def test_get_personal_info_from_db_no_result(app_with_client):
    app, _ = app_with_client

    with app.app_context():
        with pytest.raises(NoResultFound) as exception_info:
            get_personal_info_from_db(1)
        assert exception_info.type == NoResultFound


def test_get_person_from_db_sqlalchemy_error(app_with_client):
    app, _ = app_with_client

    with app.app_context():
        with patch('app.models.person.Person.query',
                   side_effect=SQLAlchemyError) as mock:
            with pytest.raises(SQLAlchemyError) as exception_info:
                mock.filter_by.return_value.first.side_effect = SQLAlchemyError
                get_personal_info_from_db(1)

            assert isinstance(exception_info.value, SQLAlchemyError)
            mock.filter_by.return_value.first.assert_called_once()
            mock.filter_by.assert_called_once_with(person_id=1)


def test_get_competences_from_db_success(app_with_client):
    app, _ = app_with_client
    setup_competence_profile_for_user2_in_db(app)

    with app.app_context():
        competences = get_competences_from_db(2)
        assert len(competences) == 1
        assert competences[0].person_id == 2
        assert competences[0].competence_id == 2
        assert competences[0].years_of_experience == float(2)

    cleanup_db(app)


def test_get_competences_from_db_sqlalchemy_error(app_with_client):
    app, _ = app_with_client

    with app.app_context():
        with patch('app.models.competence_profile.CompetenceProfile.query',
                   side_effect=SQLAlchemyError) as mock:
            with pytest.raises(SQLAlchemyError) as exception_info:
                mock.filter_by.return_value.all.side_effect = SQLAlchemyError
                get_competences_from_db(1)

            assert isinstance(exception_info.value, SQLAlchemyError)
            mock.filter_by.return_value.all.assert_called_once()


def test_get_availabilities_from_db_success(app_with_client):
    app, _ = app_with_client
    setup_availabilities_for_user1_in_db(app)

    with app.app_context():
        availabilities = get_availabilities_from_db(1)
        assert len(availabilities) == 2
        assert availabilities[0].person_id == 1
        assert availabilities[0].from_date.strftime('%Y-%m-%d') == '2024-03-01'
        assert availabilities[0].to_date.strftime('%Y-%m-%d') == '2024-03-02'
        assert availabilities[1].person_id == 1
        assert availabilities[1].from_date.strftime('%Y-%m-%d') == '2024-03-04'
        assert availabilities[1].to_date.strftime('%Y-%m-%d') == '2024-03-05'

    cleanup_db(app)


def test_get_availabilities_from_db_sqlalchemy_error(app_with_client):
    app, _ = app_with_client

    with app.app_context():
        with patch('app.models.availability.Availability.query',
                   side_effect=SQLAlchemyError) as mock:
            with pytest.raises(SQLAlchemyError) as exception_info:
                mock.filter_by.return_value.all.side_effect = SQLAlchemyError
                get_availabilities_from_db(1)

            assert isinstance(exception_info.value, SQLAlchemyError)
            mock.filter_by.return_value.all.assert_called_once()
