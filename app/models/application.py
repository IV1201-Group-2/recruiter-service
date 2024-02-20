from app.extensions import database


class ApplicationStatus(database.Model):  # type: ignore
    """
    Represents the status of an application in the database.

    :ivar application_status_id: The unique ID of the application status.
    :ivar person_id: The unique ID of the person associated with this
          application status.
    :ivar status: The current status of the application.
    """

    __tablename__ = 'application_status'

    application_status_id = database.Column(
            database.BigInteger, primary_key=True, autoincrement=True)
    person_id = database.Column(
            database.BigInteger, database.ForeignKey('person.person_id'),
            nullable=False)
    status = database.Column(database.String)

    def __init__(self, person_id: int) -> None:
        """
        Initializes a new ApplicationStatus object.

        :param person_id: The ID of the user associated with this
        application status.
        """

        self.person_id = person_id
        self.status = 'Pending'

    def to_dict(self) -> dict:
        """
        Convert the application status to a dictionary.

        :returns: A dictionary representation of the application status.
        """
        return {
            'application_status_id': self.application_status_id,
            'status': self.status
        }
