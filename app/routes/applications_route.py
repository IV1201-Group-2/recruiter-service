import logging

from flask import Blueprint, Response, jsonify, request
from flask_jwt_extended import get_jwt, jwt_required
from sqlalchemy.exc import NoResultFound, SQLAlchemyError

from app.services.applications_service import compile_applications
from app.utilities.status_codes import StatusCodes

applications_bp = Blueprint('applications', __name__)


@applications_bp.route('/', methods=['GET'])
@jwt_required()
def get_applications() -> tuple[Response, int]:
    """
    Retrieves applications information.

    This function fetches the applications information. It checks if the
    current user is authorized. If the user is, it fetches the applications.

    :returns: A tuple containing the response and the status code.
    """

    requester_ip = request.remote_addr

    if get_jwt()['role'] != 1:
        logging.warning(
                f'{requester_ip} - Unauthorized access attempt to '
                f'applications.')
        return jsonify({'error': 'UNAUTHORIZED'}), StatusCodes.UNAUTHORIZED

    try:
        errors, applications = compile_applications()

        if not errors:
            logging.info(f'{requester_ip} - Responding with applications.')
            return jsonify(applications), StatusCodes.OK
        elif 0 < len(errors) < len(applications):
            logging.warning(f'{requester_ip} - Responding with applications '
                            f'and errors.')
            return (jsonify({'applications': applications, 'errors': errors}),
                    StatusCodes.PARTIAL_CONTENT)
        else:
            logging.critical(f'{requester_ip} - Could not fetch applications.')
            return (jsonify({'error': 'COULD_NOT_FETCH_APPLICATIONS'}),
                    StatusCodes.INTERNAL_SERVER_ERROR)

    except NoResultFound as exception:
        logging.error(f'{requester_ip} - {exception.args[0]}')
        return (jsonify({'error': exception.args[0]}),
                StatusCodes.NOT_FOUND)
    except SQLAlchemyError:
        logging.critical(f'{requester_ip} - Could not fetch applications.')
        return (jsonify({'error': 'COULD_NOT_FETCH_APPLICATIONS'}),
                StatusCodes.INTERNAL_SERVER_ERROR)
