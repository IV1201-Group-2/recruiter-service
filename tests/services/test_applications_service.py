from unittest.mock import patch

import pytest
from sqlalchemy.exc import NoResultFound, SQLAlchemyError

from app.services.applications_service import compile_applications
from tests.utilities.utility_functions import cleanup_db, \
    setup_application_statuses_for_all_users, \
    setup_availabilities_for_all_users, \
    setup_competence_profiles_for_all_users, setup_three_users, \
    setup_user1_in_db, setup_user2_in_db


def test_compile_applications_only_success(app_with_client):
    app, _ = app_with_client
    setup_application_statuses_for_all_users(app)
    setup_availabilities_for_all_users(app)
    setup_competence_profiles_for_all_users(app)
    setup_three_users(app)

    with app.app_context():
        errors, applications = compile_applications()
        assert len(errors) == 0
        assert len(applications) == 3

    cleanup_db(app)


def test_compile_applications_partial_success(app_with_client):
    app, _ = app_with_client
    setup_user1_in_db(app)
    setup_user2_in_db(app)
    setup_application_statuses_for_all_users(app)
    setup_availabilities_for_all_users(app)
    setup_competence_profiles_for_all_users(app)

    with app.app_context():
        errors, applications = compile_applications()
        assert len(errors) == 1
        assert len(applications) == 2

    cleanup_db(app)


def test_compile_applications_only_errors(app_with_client):
    app, _ = app_with_client
    setup_three_users(app)
    setup_application_statuses_for_all_users(app)
    setup_competence_profiles_for_all_users(app)

    with app.app_context():
        errors, applications = compile_applications()
        assert len(errors) == 3
        assert len(applications) == 0

    cleanup_db(app)


@patch('app.services.applications_service.get_application_statuses_from_db')
def test_compile_applications_no_applications(mock_fetch, app_with_client):
    app, _ = app_with_client
    mock_fetch.side_effect = NoResultFound

    with app.app_context():
        with pytest.raises(NoResultFound) as exception:
            compile_applications()

        assert isinstance(exception.value, NoResultFound)
        assert mock_fetch.call_count == 1


@patch('app.services.applications_service.get_application_statuses_from_db')
def test_compile_applications_sqlalchemy_error_on_application_status(
        mock_fetch, app_with_client):
    app, _ = app_with_client
    mock_fetch.side_effect = SQLAlchemyError

    with app.app_context():
        with pytest.raises(SQLAlchemyError) as exception:
            compile_applications()

        assert isinstance(exception.value, SQLAlchemyError)
        assert mock_fetch.call_count == 1
