import datetime

from flask_jwt_extended import create_access_token

from tests.utilities.status_codes import StatusCodes
from tests.utilities.utility_functions import generate_token_for_person_id_1, \
    generate_token_for_recruiter, post_request_applications_endpoint, \
    remove_users_from_db, \
    setup_application_status_for_user1_in_db, \
    setup_availabilities_for_user1_in_db, \
    setup_user1_in_db


def test_valid_token(app_with_client):
    app, test_client = app_with_client
    setup_user1_in_db(app)
    setup_availabilities_for_user1_in_db(app)
    setup_application_status_for_user1_in_db(app)

    valid_token = generate_token_for_recruiter(app)

    response = post_request_applications_endpoint(test_client, valid_token)
    assert response.status_code == StatusCodes.OK
    remove_users_from_db(app)


def test_invalid_token(app_with_client):
    app, test_client = app_with_client
    setup_user1_in_db(app)
    valid_token = generate_token_for_person_id_1(app)
    invalid_token = valid_token + 'invalid'

    response = post_request_applications_endpoint(test_client,
                                                  invalid_token)
    assert response.status_code == StatusCodes.UNAUTHORIZED
    assert response.json['error'] == 'INVALID_TOKEN'


def test_expired_token(app_with_client):
    app, test_client = app_with_client
    setup_user1_in_db(app)

    with app.app_context():
        expired_token = create_access_token(
                identity=None,
                additional_claims={'id': 1},
                expires_delta=datetime.timedelta(days=-1))

    response = post_request_applications_endpoint(test_client,
                                                  expired_token)
    assert response.status_code == StatusCodes.UNAUTHORIZED
    assert response.json['error'] == 'TOKEN_EXPIRED'
    remove_users_from_db(app)


def test_unauthorized_request(app_with_client):
    app, test_client = app_with_client
    response = test_client.get('/api/applications/')
    assert response.status_code == StatusCodes.UNAUTHORIZED
    assert response.json['error'] == 'UNAUTHORIZED'
