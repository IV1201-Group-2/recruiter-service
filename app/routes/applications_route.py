from flask import Blueprint, Response, current_app, jsonify
from flask_jwt_extended import get_jwt, jwt_required
from sqlalchemy.exc import NoResultFound, SQLAlchemyError

from app.services.applications_service import compile_applications
from app.utilities.status_codes import StatusCodes

applications_bp = Blueprint('applications', __name__)


@applications_bp.route('/', methods=['GET'])
@jwt_required()
def get_applications() -> tuple[Response, int]:
    if get_jwt()['role'] != 1:
        return jsonify({'error': 'UNAUTHORIZED'}), StatusCodes.UNAUTHORIZED

    try:
        errors, applications = compile_applications()

        if not errors:
            current_app.logger.info('Responding with applications.')
            return jsonify(applications), StatusCodes.OK
        elif 0 < len(errors) < len(applications):
            current_app.logger.info('Responding with applications and errors.')
            return (jsonify({'applications': applications, 'errors': errors}),
                    StatusCodes.PARTIAL_CONTENT)
        else:
            current_app.logger.error('Could not fetch applications.')
            return (jsonify({'error': 'COULD_NOT_FETCH_APPLICATIONS'}),
                    StatusCodes.INTERNAL_SERVER_ERROR)

    except NoResultFound as exception:
        return (jsonify({'error': exception.args[0]}),
                StatusCodes.NOT_FOUND)
    except SQLAlchemyError:
        return (jsonify({'error': 'COULD_NOT_FETCH_APPLICATIONS'}),
                StatusCodes.INTERNAL_SERVER_ERROR)
