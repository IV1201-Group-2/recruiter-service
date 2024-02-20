from unittest.mock import patch

from sqlalchemy.exc import SQLAlchemyError

from tests.utilities.status_codes import StatusCodes
from tests.utilities.utility_functions import assert_application_details, \
    generate_token_for_person_id_1, generate_token_for_recruiter, \
    post_request_applications_endpoint, \
    setup_application_statuses_for_all_users, \
    setup_availabilities_for_all_users, setup_availability_for_user2_in_db, \
    setup_availability_for_user3_in_db, \
    setup_competence_profiles_for_all_users, setup_three_users


def test_get_applications_success(app_with_client):
    app, test_client = app_with_client
    setup_three_users(app)
    setup_application_statuses_for_all_users(app)
    setup_availabilities_for_all_users(app)
    setup_competence_profiles_for_all_users(app)

    token = generate_token_for_recruiter(app)
    response = post_request_applications_endpoint(test_client, token)

    assert response.status_code == StatusCodes.OK

    applications = response.json
    assert len(applications) == 3

    assert_application_details(
            applications[0], 'user1', 's1', 1, 'Pending',
            [{'competence_id': 1, 'years_of_experience': '1.00'},
             {'competence_id': 1, 'years_of_experience': '4.00'}],
            [{'from_date': '2024-03-01', 'to_date': '2024-03-02'},
             {'from_date': '2024-03-04', 'to_date': '2024-03-05'}])

    assert_application_details(
            applications[1], 'user2', 's2', 2, 'Pending',
            [{'competence_id': 2, 'years_of_experience': '2.00'}],
            [{'from_date': '2024-03-02', 'to_date': '2024-03-03'}])

    assert_application_details(
            applications[2], 'user3', 's3', 3, 'Pending',
            [],
            [{'from_date': '2024-03-03', 'to_date': '2024-03-04'}])


def test_get_applications_partial_success(app_with_client):
    app, test_client = app_with_client
    setup_three_users(app)
    setup_application_statuses_for_all_users(app)
    setup_availability_for_user2_in_db(app)
    setup_availability_for_user3_in_db(app)
    setup_competence_profiles_for_all_users(app)

    token = generate_token_for_recruiter(app)
    response = post_request_applications_endpoint(test_client, token)

    assert response.status_code == StatusCodes.PARTIAL_CONTENT

    applications = response.json
    assert len(applications) == 2

    successfully_fetched = applications['applications']
    assert len(successfully_fetched) == 2

    assert_application_details(
            successfully_fetched[0], 'user2', 's2', 2, 'Pending',
            [{'competence_id': 2, 'years_of_experience': '2.00'}],
            [{'from_date': '2024-03-02', 'to_date': '2024-03-03'}])

    assert_application_details(
            successfully_fetched[1], 'user3', 's3', 3, 'Pending',
            [],
            [{'from_date': '2024-03-03', 'to_date': '2024-03-04'}])

    failed_to_fetch = applications['errors']
    assert len(failed_to_fetch) == 1
    assert failed_to_fetch[0][
               'error'] == 'NO_AVAILABILITIES_FOUND_FOR_PERSON: 1'


def test_get_applications_not_found(app_with_client):
    app, test_client = app_with_client
    setup_three_users(app)
    setup_availabilities_for_all_users(app)
    setup_competence_profiles_for_all_users(app)

    token = generate_token_for_recruiter(app)
    response = post_request_applications_endpoint(test_client, token)

    assert response.status_code == StatusCodes.NOT_FOUND
    assert response.json['error'] == 'NO_APPLICATION_STATUSES_FOUND'


def test_get_applications_only_errors(app_with_client):
    app, test_client = app_with_client
    setup_three_users(app)
    setup_competence_profiles_for_all_users(app)
    setup_application_statuses_for_all_users(app)

    token = generate_token_for_recruiter(app)
    response = post_request_applications_endpoint(test_client, token)

    assert response.status_code == StatusCodes.INTERNAL_SERVER_ERROR
    assert response.json['error'] == 'COULD_NOT_FETCH_APPLICATIONS'


def test_get_applications_unauthorized(app_with_client):
    app, test_client = app_with_client
    token = generate_token_for_person_id_1(app)

    response = post_request_applications_endpoint(test_client, token)
    assert response.status_code == StatusCodes.UNAUTHORIZED


@patch('app.routes.applications_route.compile_applications')
def test_get_applications_sqlalchemy_error(mock_fetch, app_with_client):
    app, test_client = app_with_client
    token = generate_token_for_recruiter(app)

    mock_fetch.side_effect = SQLAlchemyError

    response = post_request_applications_endpoint(test_client, token)

    assert response.status_code == StatusCodes.INTERNAL_SERVER_ERROR
    assert response.json['error'] == 'COULD_NOT_FETCH_APPLICATIONS'
