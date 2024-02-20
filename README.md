# Applications Endpoint

`GET /api/applications/`

## Additional requirements

* The user must be logged in when calling this API
* The user's JWT token must be included in the `Authorization` header

## Successful Response Body

#### `OK` (200 OK)

All applications were fetched successfully. The response body contains an array of applications.

```json
[
  {
    "personal_info": {
      "name": "user1",
      "surname": "tester",
      "pnr": "123123123",
      "email": "hello@kth.se"
    },
    "competences": [
      {
        "competence_id": 1,
        "years_of_experience": 1.00
      },
      {
        "competence_id": 1,
        "years_of_experience": 4.00
      }
    ],
    "availabilities": [
      {
        "from_date": "2024-03-01",
        "to_date": "2024-03-02"
      },
      {
        "from_date": "2024-03-04",
        "to_date": "2024-03-05"
      }
    ],
    "status": "UNHANDLED"
  },
  ...
]
```

## Partially Successful Response Body

#### `PARTIAL_CONTENT` (206 Partial Content)

Some applications were fetched successfully, but there were errors with others. The response body contains an array of
applications and an array of errors.

```json
{
  "applications": [
    {
      "personal_info": {
        "name": "user2",
        "surname": "tester",
        "pnr": "1231231232",
        "email": "hello@kth.se"
      },
      "competences": [
        {
          "competence_id": 2,
          "years_of_experience": 2.00
        }
      ],
      "availabilities": [
        {
          "from_date": "2024-03-02",
          "to_date": "2024-03-03"
        }
      ],
      "status": "UNHANDLED"
    },
    ...
  ],
  "errors": [
    {
      "error": "NO_AVAILABILITIES_FOUND_FOR_PERSON: 1"
    },
    ...
  ]
}
```

## Error Response Body

#### `INTERNAL_SERVER_ERROR` (500 Internal Server Error)

There was an issue with the database operation when trying to fetch the applications. The response body contains an
error message.

```json
{
  "error": "COULD_NOT_FETCH_APPLICATIONS"
}
```

## Error responses

#### `UNAUTHORIZED` (401 Unauthorized)

User is not logged in (JWT token was not provided or is invalid)

#### `COULD_NOT_FETCH_APPLICATIONS` (500 Internal Server Error)

There was an issue with the database operation when trying to fetch the applications

#### `NOT_FOUND` (404 Not Found)

No applications were found in the database

#### `PARTIAL_CONTENT` (206 Partial Content)

Some applications were fetched successfully, but there were errors with others

#### `INTERNAL_SERVER_ERROR` (500 Internal Server Error)

An unexpected error occurred

#### `INVALID_TOKEN` (401 Unauthorized)

The provided JWT token is invalid (e.g., it is expired, not yet valid, or does not contain the required claims)

#### `TOKEN_EXPIRED` (401 Unauthorized)

The provided JWT token has expired

#### `UNAUTHORIZED` (401 Unauthorized)

Unauthorized request