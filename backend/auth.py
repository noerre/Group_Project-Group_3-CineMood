from datetime import datetime, timedelta
from typing import Optional

import bcrypt
import mysql.connector
# Import JWT functionalities from Flask-JWT-Extended
from flask_jwt_extended import decode_token
from mysql.connector import errorcode


class AuthHandler:
    """
    Handles user authentication, including registration and login functionalities.
    """

    # Maximum allowed failed login attempts before account lockout
    MAX_FAILED_ATTEMPTS = 5
    # Duration of account lockout after reaching max failed attempts
    LOCKOUT_DURATION = timedelta(minutes=15)  # Lockout duration after max failed attempts

    def __init__(self, config):
        """
        Initializes the connection to the MySQL database and creates the users table if it doesn't exist.

        :param config: Dictionary containing MySQL connection configuration.
        """
        if not isinstance(config, dict):
            raise TypeError("config must be a dictionary")
        try:
            # Establish connection to the MySQL database using provided configuration
            self.conn = mysql.connector.connect(**config)
            # Create a cursor for executing queries, with results as dictionaries
            self.cursor = self.conn.cursor(dictionary=True)
            # Ensure the users table exists
            self.create_users_table()
            # Initialize an in-memory set to store revoked tokens
            self.revoked_tokens = set()
        except mysql.connector.Error as err:
            # Handle common connection errors
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                raise Exception("Incorrect MySQL username or password.")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                raise Exception("Database does not exist.")
            else:
                raise Exception(str(err))

    def create_users_table(self):
        """
        Creates the 'users' table if it does not already exist.
        The table includes fields for user credentials and login attempt tracking.
        """
        create_table_query = """
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(50) UNIQUE NOT NULL,
            password VARCHAR(255) NOT NULL,
            failed_attempts INT DEFAULT 0,
            lockout_time DATETIME NULL
        )
        """
        try:
            # Execute the table creation query
            self.cursor.execute(create_table_query)
            # Commit the changes to the database
            self.conn.commit()
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                # Table already exists, ignore the error
                pass
            else:
                raise Exception(str(err))

    def register_user(self, username, password):
        """
        Registers a new user after validating the username and password.

        :param username: The desired username.
        :param password: The desired password.
        """
        # Validate the username
        if not self.validate_username(username):
            raise Exception(
                "Invalid username. It must be at least 3 characters long and contain only letters, numbers, "
                "underscores, or hyphens.")

        # Validate the password
        if not self.validate_password(password):
            raise Exception(
                "Invalid password. It must be at least 8 characters long and include at least one special character.")

        # Hash the password using bcrypt
        hashed_password = self.hash_password(password).decode('utf-8')

        try:
            # Insert the new user into the database
            insert_query = ("INSERT INTO users (username, password, , failed_attempts, lockout_time) "
                            "VALUES (%s, %s, 0, NULL)")
            self.cursor.execute(insert_query, (username, hashed_password))
            self.conn.commit()
        except mysql.connector.IntegrityError:
            # Handle case where username is already taken (violates UNIQUE constraint)
            raise Exception("Username is already taken. Please choose another one.")

    def login_guest(self):
        """
        Logs in the user in guest mode.
        Creates a temporary user profile without saving it to the database.

        :return: Dictionary containing guest user information.
        """
        return {
            'username': 'Guest',
            'is_guest': True
        }

    def login_user(self, username, password):
        """
        Logs in an existing user with security checks, including account lockout handling.

        :param username: The username.
        :param password: The password.
        :return: Dictionary containing user information.
        :raises Exception: If login fails due to invalid credentials or account lockout.
        """
        # Retrieve the user from the database
        user = self.get_user(username)
        if not user:
            # User does not exist
            raise Exception("Invalid username or password.")

        # Check if the account is locked due to too many failed attempts
        if self.is_locked_out(user):
            # Calculate remaining lockout time
            remaining = user['lockout_time'] - datetime.now()
            minutes, seconds = divmod(remaining.total_seconds(), 60)
            raise Exception(f"Account is locked. Try again in {minutes} minutes and {seconds} seconds.")

        # Verify the password
        stored_hashed_password = user['password'].encode('utf-8')
        if self.verify_password(password, stored_hashed_password):
            # Successful login; reset failed attempts and lockout time
            self.reset_failed_attempts(username)
            return {
                'username': username,
                'is_guest': False
            }
        else:
            # Incorrect password; increment failed attempts
            self.increment_failed_attempts(user)
            # Calculate attempts left before account lockout
            attempts_left = self.MAX_FAILED_ATTEMPTS - (user['failed_attempts'] + 1)
            if attempts_left > 0:
                raise Exception(f"Invalid username or password. You have {attempts_left} attempts left.")
            else:
                # Lock the account after exceeding max failed attempts
                self.lock_account(username)
                lockout_minutes = int(self.LOCKOUT_DURATION.total_seconds() / 60)
                raise Exception(
                    f"Too many failed attempts. Account '{username}' is locked for {lockout_minutes} minutes.")

    def logout_user(self, token: str):
        """
        Logs out the user by revoking their JWT token.

        :param token: The JWT access token to revoke.
        """
        try:
            # Decode the token to ensure it's valid and extract its unique identifier (jti)
            decoded_token = decode_token(token)
            jti = decoded_token['jti']
            # Add the jti to the revoked tokens set
            self.revoked_tokens.add(jti)
            print("User has been logged out and the token has been revoked.")
        except Exception as e:
            print(f"Error during logout: {e}")
            raise Exception("Invalid token. Logout failed.")

    def is_token_revoked(self, jti: str) -> bool:
        """
        Checks if a token's jti is in the revoked tokens set.

        :param jti: The unique identifier of the token.
        :return: True if the token is revoked, False otherwise.
        """
        return jti in self.revoked_tokens

    def hash_password(self, password: str) -> bytes:
        """
        Hashes the password using bcrypt.

        :param password: The plain-text password.
        :return: The hashed password as bytes.
        """
        # Generate a salt and hash the password
        return bcrypt.hashpw(password.encode(), bcrypt.gensalt())

    def verify_password(self, password: str, hashed: bytes) -> bool:
        """
        Verifies that the provided password matches the hashed password.

        :param password: The password entered by the user.
        :param hashed: The hashed password from the database.
        :return: True if the password is correct, False otherwise.
        """
        # Compare the provided password with the stored hashed password
        return bcrypt.checkpw(password.encode(), hashed)

    def get_user(self, username: str) -> Optional[dict]:
        """
        Retrieves a user's data from the database.

        :param username: The username to look up.
        :return: A dictionary with user data or None if user does not exist.
        """
        select_query = "SELECT * FROM users WHERE username = %s"
        self.cursor.execute(select_query, (username,))
        # Fetch one user record
        return self.cursor.fetchone()

    def increment_failed_attempts(self, user: dict):
        """
        Increments the failed login attempts for a user.

        :param user: The user dictionary.
        """
        # Increment the failed_attempts count
        new_attempts = user['failed_attempts'] + 1
        update_query = "UPDATE users SET failed_attempts = %s WHERE username = %s"
        self.cursor.execute(update_query, (new_attempts, user['username']))
        self.conn.commit()

    def reset_failed_attempts(self, username: str):
        """
        Resets the failed login attempts and lockout time for a user.

        :param username: The username.
        """
        update_query = "UPDATE users SET failed_attempts = 0, lockout_time = NULL WHERE username = %s"
        self.cursor.execute(update_query, (username,))
        self.conn.commit()

    def lock_account(self, username: str):
        """
        Locks a user's account by setting the lockout_time to a future timestamp.

        :param username: The username.
        """
        # Calculate the lockout time as current time plus the lockout duration
        lockout_time = datetime.now() + self.LOCKOUT_DURATION
        update_query = "UPDATE users SET lockout_time = %s WHERE username = %s"
        self.cursor.execute(update_query, (lockout_time, username))
        self.conn.commit()

    def is_locked_out(self, user: dict) -> bool:
        """
        Checks if a user's account is currently locked.

        :param user: The user dictionary.
        :return: True if the account is locked, False otherwise.
        """
        if user['lockout_time']:
            if datetime.now() < user['lockout_time']:
                # Account is still locked
                return True
            else:
                # Lockout period has expired; reset failed attempts and lockout time
                self.reset_failed_attempts(user['username'])
        # Account is not locked
        return False

    def validate_username(self, username: str) -> bool:
        """
        Validates the username based on length and allowed characters.

        :param username: The username to validate.
        :return: True if valid, False otherwise.
        """
        if len(username) < 3:
            # Username too short
            return False
        if not all(c.isalnum() or c in ('_', '-') for c in username):
            # Username contains invalid characters
            return False
        return True

    def validate_password(self, password: str) -> bool:
        """
        Validates the password for minimum length and presence of special characters.

        :param password: The password to validate.
        :return: True if valid, False otherwise.
        """
        if len(password) < 8:
            # Password too short
            return False
        if not any(c in '!@#$%^&*()-_=+[]{}|;:",.<>?/' for c in password):
            # Password lacks special characters
            return False
        return True

    def close_connection(self):
        """
        Closes the database cursor and connection.
        """
        if hasattr(self, 'cursor') and self.cursor:
            try:
                self.cursor.close()
            except Exception:
                pass  # Suppress any exception during cursor close
        if hasattr(self, 'conn') and self.conn:
            try:
                self.conn.close()
            except Exception:
                pass  # Suppress any exception during connection close

    def __del__(self):
        """
        Destructor to ensure the database connection is closed when the object is deleted.
        """
        try:
            self.close_connection()
        except Exception:
            pass  # Suppress any exception during object deletion
