from datetime import datetime, timedelta

import bcrypt
import mysql.connector
from mysql.connector import errorcode


class AuthHandler:
    # Maximum allowed failed login attempts before account lockout
    MAX_FAILED_ATTEMPTS = 5
    # Duration of account lockout after reaching max failed attempts
    LOCKOUT_DURATION = timedelta(minutes=15)  # Lockout duration after max failed attempts

    def __init__(self, config):
        """
        Initializes the connection to the MySQL database and creates the users table if it doesn't exist.

        :param config: Dictionary containing MySQL connection configuration.
        """
        try:
            # Establish connection to the MySQL database using provided configuration
            self.conn = mysql.connector.connect(**config)
            # Create a cursor for executing queries, with results as dictionaries
            self.cursor = self.conn.cursor(dictionary=True)
            # Ensure the users table exists
            self.create_users_table()
        except mysql.connector.Error as err:
            # Handle common connection errors
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Incorrect MySQL username or password.")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist.")
            else:
                print(err)
            # Do not exit; raise the exception instead
            raise

    def create_users_table(self):
        """
        Creates the 'users' table if it does not already exist.
        The table includes fields for user credentials and login attempt tracking.
        """
        create_table_query = """
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(50) UNIQUE NOT NULL,
            password BINARY(60) NOT NULL,
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
                # Re-raise any other exception
                raise

    def register_user(self, username, password):
        """
        Registers a new user after validating the username and password.

        :param username: The desired username.
        :param password: The desired password.
        """
        # Validate the username
        if not self.validate_username(username):
            print(
                "Invalid username. It must be at least 3 characters long and contain only letters, numbers, "
                "underscores, or hyphens.")
            return

        # Validate the password
        if not self.validate_password(password):
            print("Invalid password. It must be at least 8 characters long and include at least one special character.")
            return

        # Hash the password using bcrypt
        hashed_password = self.hash_password(password)
        try:
            # Insert the new user into the database
            insert_query = "INSERT INTO users (username, password) VALUES (%s, %s)"
            self.cursor.execute(insert_query, (username, hashed_password))
            self.conn.commit()
            print(f"User '{username}' has been registered.")
        except mysql.connector.IntegrityError:
            # Handle case where username is already taken (violates UNIQUE constraint)
            print("Username is already taken. Please choose another one.")

    def login_user(self, username, password):
        """
        Logs in an existing user with security checks, including account lockout handling.

        :param username: The username.
        :param password: The password.
        """
        # Retrieve the user from the database
        user = self.get_user(username)
        if not user:
            # User does not exist
            print("Invalid username or password.")
            return

        # Check if the account is locked due to too many failed attempts
        if self.is_locked_out(user):
            # Calculate remaining lockout time
            remaining = user['lockout_time'] - datetime.now()
            minutes, seconds = divmod(remaining.total_seconds(), 60)
            print(f"Account is locked. Try again in {int(minutes)} minutes and {int(seconds)} seconds.")
            return

        # Verify the password
        if self.verify_password(password, user['password']):
            # Successful login; reset failed attempts and lockout time
            self.reset_failed_attempts(username)
            print(f"User '{username}' has been logged in.")
            # Proceed with post-login actions (e.g., navigate to main menu)
        else:
            # Incorrect password; increment failed attempts
            self.increment_failed_attempts(user)
            # Calculate attempts left before account lockout
            attempts_left = self.MAX_FAILED_ATTEMPTS - (user['failed_attempts'] + 1)
            if attempts_left > 0:
                print(f"Invalid username or password. You have {attempts_left} attempts left.")
            else:
                # Lock the account after exceeding max failed attempts
                self.lock_account(username)
                lockout_minutes = int(self.LOCKOUT_DURATION.total_seconds() / 60)
                print(f"Too many failed attempts. Account '{username}' is locked for {lockout_minutes} minutes.")

    def logout_user(self):
        """
        Logs out the user.

        Note: Implementation depends on how user sessions are managed in the application.
        """
        print("You have been logged out.")
        # Implement logout logic here (e.g., clear session data)

    def hash_password(self, password):
        """
        Hashes the password using bcrypt.

        :param password: The plain-text password.
        :return: The hashed password as bytes.
        """
        # Generate a salt and hash the password
        return bcrypt.hashpw(password.encode(), bcrypt.gensalt())

    def verify_password(self, password, hashed):
        """
        Verifies that the provided password matches the hashed password.

        :param password: The password entered by the user.
        :param hashed: The hashed password from the database.
        :return: True if the password is correct, False otherwise.
        """
        # Compare the provided password with the stored hashed password
        return bcrypt.checkpw(password.encode(), hashed)

    def get_user(self, username):
        """
        Retrieves a user's data from the database.

        :param username: The username to look up.
        :return: A dictionary with user data or None if user does not exist.
        """
        select_query = "SELECT * FROM users WHERE username = %s"
        self.cursor.execute(select_query, (username,))
        # Fetch one user record
        return self.cursor.fetchone()

    def increment_failed_attempts(self, user):
        """
        Increments the failed login attempts for a user.

        :param user: The user dictionary.
        """
        # Increment the failed_attempts count
        new_attempts = user['failed_attempts'] + 1
        update_query = "UPDATE users SET failed_attempts = %s WHERE username = %s"
        self.cursor.execute(update_query, (new_attempts, user['username']))
        self.conn.commit()

    def reset_failed_attempts(self, username):
        """
        Resets the failed login attempts and lockout time for a user.

        :param username: The username.
        """
        update_query = "UPDATE users SET failed_attempts = 0, lockout_time = NULL WHERE username = %s"
        self.cursor.execute(update_query, (username,))
        self.conn.commit()

    def lock_account(self, username):
        """
        Locks a user's account by setting the lockout_time to a future timestamp.

        :param username: The username.
        """
        # Calculate the lockout time as current time plus the lockout duration
        lockout_time = datetime.now() + self.LOCKOUT_DURATION
        update_query = "UPDATE users SET lockout_time = %s WHERE username = %s"
        self.cursor.execute(update_query, (lockout_time, username))
        self.conn.commit()

    def is_locked_out(self, user):
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

    def validate_username(self, username):
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

    def validate_password(self, password):
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
                pass # Suppress any exception during cursor close
        if hasattr(self, 'conn') and self.conn:
            try:
                self.conn.close()
            except Exception:
                pass # Suppress any exception during connection close

    def __del__(self):
        """
        Destructor to ensure the database connection is closed when the object is deleted.
        """
        try:
            self.close_connection()
        except Exception:
            pass  # Suppress any exception during object deletion
