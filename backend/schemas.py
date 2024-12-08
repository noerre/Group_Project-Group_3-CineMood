from marshmallow import Schema, fields, validate, ValidationError


# ======================================================================
# Schema Definitions using Marshmallow
# ======================================================================

def validate_special_char(value):
    if not any(c in '!@#$%^&*()-_=+[]{}|;:",.<>?/' for c in value):
        raise ValidationError("Password must include at least one special character.")


class RegisterRequestSchema(Schema):
    """
    Schema for validating user registration requests.

    Fields:
        username (str):
            - Required.
            - Must be at least 3 characters long.
            - Can contain letters, numbers, underscores, or hyphens.
        password (str):
            - Required.
            - Must be at least 8 characters long.
            - Should include at least one special character.
    """
    username = fields.Str(
        required=True,
        validate=validate.Length(min=3, error="Username must be at least 3 characters long.")
    )
    password = fields.Str(
        required=True,
        validate=[
            validate.Length(min=8, error="Password must be at least 8 characters long."),
            validate_special_char
        ]
    )


class LoginRequestSchema(Schema):
    """
    Schema for validating user login requests.

    Fields:
        username (str):
            - Required.
        password (str):
            - Required.
    """
    username = fields.Str(
        required=True,
        error_messages={"required": "Username is required."}
    )
    password = fields.Str(
        required=True,
        error_messages={"required": "Password is required."}
    )


class AuthResponseSchema(Schema):
    """
    Schema for structuring authentication responses.

    Fields:
        username (str):
            - Required.
            - The username of the authenticated user.
        is_guest (bool):
            - Required.
            - Indicates whether the user is a guest.
        access_token (str):
            - Required.
            - JWT access token for authenticated sessions.
    """
    username = fields.Str(
        required=True,
        error_messages={"required": "Username is required in the response."}
    )
    is_guest = fields.Bool(
        required=True,
        error_messages={"required": "is_guest flag is required in the response."}
    )
    access_token = fields.Str(
        required=True,
        error_messages={"required": "Access token is required in the response."}
    )

