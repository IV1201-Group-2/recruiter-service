class StatusCodes:
    """
    Represents the HTTP status codes that can be returned by the API.

    :ivar OK: The request was successful.
    :ivar PARTIAL_CONTENT: The request was partially successful.
    :ivar UNAUTHORIZED: The request was unauthorized.
    :ivar NOT_FOUND: The resource was not found.
    :ivar INTERNAL_SERVER_ERROR: An internal server error occurred.
    """

    OK = 200
    PARTIAL_CONTENT = 206
    UNAUTHORIZED = 401
    NOT_FOUND = 404
    INTERNAL_SERVER_ERROR = 500
