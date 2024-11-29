import os
import unittest
from datetime import datetime, timedelta
from io import StringIO
from unittest.mock import patch

import mysql.connector
from dotenv import load_dotenv

from backend.auth import AuthHandler


class TestAuthHandler(unittest.TestCase):
    """
    Test suite for the AuthHandler class.

    This test class includes tests for:
    - User registration (successful registration and various error scenarios).
    - User login (successful login, handling of incorrect passwords, account lockout, and account unlocking).
    - Password hashing and verification.
    - Account lockout mechanics and unlocking after the lockout period.

    The tests ensure that the authentication system works as expected and handles edge cases properly.
    """

    @classmethod
    def setUpClass(cls):
        """
        Class-level setup method that initializes the test environment.

        - Loads environment variables for database configuration.
        - Establishes a connection to the MySQL server.
        - Creates a test database to avoid affecting the production database.
        - Initializes an instance of AuthHandler with the test configuration.
        """
        load_dotenv()  # Load environment variables from .env file
        cls.test_config = {
            'user': os.getenv('DB_USER'),
            'password': os.getenv('DB_PASSWORD'),
            'host': os.getenv('DB_HOST'),
            'database': 'test_cine_mood',
            'raise_on_warnings': True
        }
        try:
            # Connect to MySQL server
            # This connection is used to manage the test database
            cls.conn = mysql.connector.connect(
                user=cls.test_config['user'],
                password=cls.test_config['password'],
                host=cls.test_config['host']
            )
            cls.cursor = cls.conn.cursor()
            # Create a test database for isolated testing to avoid modifying production data
            cls.cursor.execute("CREATE DATABASE IF NOT EXISTS test_cine_mood")
            cls.conn.commit()
            # Initialize AuthHandler instance with test configuration
            # This will also create the necessary 'users' table
            cls.auth = AuthHandler(cls.test_config)
        except mysql.connector.Error as err:
            # Print the error and re-raise it to be handled by the test framework
            print(err)
            raise

    @classmethod
    def tearDownClass(cls):
        """
        Class-level teardown method that cleans up after all tests have run.

        - Closes the AuthHandler's database connection.
        - Drops the test database to ensure no residual data is left.
        - Closes the cursor and MySQL connection.
        """
        # Close AuthHandler's connection to properly clean up resources
        cls.auth.close_connection()
        # Drop the test database to ensure no residual data is left
        cls.cursor.execute("DROP DATABASE test_cine_mood")
        cls.conn.commit()
        # Close cursor and MySQL connection
        cls.cursor.close()
        cls.conn.close()

    def test_register_user_success(self):
        """
        Test successful registration of a new user.

        - Registers a user with valid credentials.
        - Verifies that the user is correctly inserted into the database.
        """
        username = "testuser"
        password = "Test@1234"
        self.auth.register_user(username, password)
        # Verify that the user was correctly inserted into the database
        self.auth.cursor.execute("SELECT username FROM users WHERE username = %s", (username,))
        result = self.auth.cursor.fetchone()
        self.assertIsNotNone(result)  # Check if user exists
        self.assertEqual(result['username'], username)  # Verify correct username was inserted

    def test_register_user_duplicate(self):
        """
        Test registration of a duplicate user.

        - Registers a user.
        - Attempts to register the same user again.
        - Verifies that an appropriate error message is displayed.
        """
        username = "duplicateuser"
        password = "Test@1234"
        self.auth.register_user(username, password)
        # Attempt to register the same user again
        with self.assertRaises(Exception) as context:
            self.auth.register_user(username, password)
        # Check that the correct error message is printed
        self.assertIn("Username is already taken. Please choose another one.", str(context.exception))

    def test_register_user_invalid_username(self):
        """
        Test registration with an invalid username.

        - Tries to register a user with a username that's too short.
        - Verifies that an appropriate error message is displayed.
        """
        username = "ab"  # Too short
        password = "Test@1234"
        with self.assertRaises(Exception) as context:
            self.auth.register_user(username, password)
        # Check that the correct error message is printed
        self.assertIn("Invalid username.", str(context.exception))

    def test_register_user_invalid_password(self):
        """
        Test registration with an invalid password.

        - Tries to register a user with a password lacking a special character.
        - Verifies that an appropriate error message is displayed.
        """
        username = "validuser"
        password = "password"  # No special character
        with self.assertRaises(Exception) as context:
            self.auth.register_user(username, password)
        # Check that the correct error message is printed
        self.assertIn("Invalid password.", str(context.exception))

    def test_login_user_success(self):
        """
        Test successful user login.

        - Registers a user with valid credentials.
        - Logs in with the correct username and password.
        - Verifies that the user is successfully logged in and failed_attempts are reset.
        """
        username = "loginuser"
        password = "Login@1234"
        self.auth.register_user(username, password)
        # Attempt to log in with correct credentials
        user_info = self.auth.login_user(username, password)
        # Check that the login was successful
        self.assertEqual(user_info['username'], username)
        self.assertFalse(user_info['is_guest'])
        # Check if failed_attempts reset to 0 after successful login
        self.auth.cursor.execute("SELECT failed_attempts FROM users WHERE username = %s", (username,))
        result = self.auth.cursor.fetchone()
        self.assertEqual(result['failed_attempts'], 0)

    def test_login_user_failure(self):
        """
        Test user login with incorrect password leading to account lockout.

        - Registers a user.
        - Attempts to log in with an incorrect password multiple times.
        - Verifies that the account becomes locked after exceeding max failed attempts.
        """
        username = "failuser"
        password = "Fail@1234"
        self.auth.register_user(username, password)
        wrong_password = "Wrong@1234"
        # Attempt to log in with the wrong password until account is locked
        for attempt in range(AuthHandler.MAX_FAILED_ATTEMPTS):
            with  self.assertRaises(Exception) as context:
                self.auth.login_user(username, wrong_password)
            if attempt < AuthHandler.MAX_FAILED_ATTEMPTS - 1:
                self.assertIn("Invalid username or password.", str(context.exception))
            else:
                self.assertIn(f"Too many failed attempts. Account '{username}' is locked for", str(context.exception))

        # Check if account is locked by verifying lockout_time is set
        self.auth.cursor.execute("SELECT lockout_time FROM users WHERE username = %s", (username,))
        result = self.auth.cursor.fetchone()
        self.assertIsNotNone(result['lockout_time'])

    def test_password_hashing(self):
        """
        Test password hashing and verification.

        - Hashes a password.
        - Verifies that the original password matches the hash.
        - Verifies that an incorrect password does not match the hash.
        """
        password = "Hash@1234"
        hashed = self.auth.hash_password(password)
        # Verify that the correct password matches the hash
        self.assertTrue(self.auth.verify_password(password, hashed))
        # Verify that an incorrect password does not match the hash
        self.assertFalse(self.auth.verify_password("WrongPass", hashed))

    def test_account_unlock(self):
        """
        Test unlocking an account after the lockout period has passed.

        - Registers a user and locks the account by entering the wrong password multiple times.
        - Simulates the passage of time beyond the lockout duration.
        - Attempts to log in again with the correct password.
        - Verifies that the user can log in and failed_attempts are reset.
        """
        # Register a user and lock the account by entering the wrong password multiple times.
        username = "unlockuser"
        password = "Unlock@1234"
        self.auth.register_user(username, password)
        wrong_password = "Wrong@1234"
        for _ in range(AuthHandler.MAX_FAILED_ATTEMPTS):
            with self.assertRaises(Exception) as context:
                self.auth.login_user(username, wrong_password)

        # Verify that the account is locked
        self.auth.cursor.execute("SELECT lockout_time FROM users WHERE username = %s", (username,))
        result = self.auth.cursor.fetchone()
        self.assertIsNotNone(result['lockout_time'])

        # Simulate time after lockout duration to ensure account unlock works
        future_time = datetime.now() + timedelta(minutes=16)
        with patch('backend.auth.datetime') as mock_datetime:
            # Mock datetime.now() to return a future time
            mock_datetime.now.return_value = future_time
            # Ensure other datetime functions work normally
            mock_datetime.side_effect = lambda *args, **kwargs: datetime(*args, **kwargs)
            # Attempt to login again with correct password
            user_info = self.auth.login_user(username, password)
            self.assertEqual(user_info['username'], username)
            self.assertFalse(user_info['is_guest'])

        # Verify that failed_attempts counter is reset after successful login
        self.auth.cursor.execute("SELECT failed_attempts FROM users WHERE username = %s", (username,))
        result = self.auth.cursor.fetchone()
        self.assertEqual(result['failed_attempts'], 0)

    def test_login_guest(self):
        """
        Test logging in as a guest.

        - Logs in as a guest.
        - Verifies that the returned guest information is correct.
        - Confirms that `is_guest` is True.
        """
        guest_info = self.auth.login_guest()
        self.assertEqual(guest_info['username'], 'Guest')
        self.assertTrue(guest_info['is_guest'])

    def test_guest_does_not_create_user_in_db(self):
        """
        Ensure that logging in as a guest does not create a user in the database.

        - Logs in as a guest.
        - Checks that no user with username 'Guest' exists in the database.
        """
        # Log in as guest
        guest_info = self.auth.login_guest()
        self.assertEqual(guest_info['username'], 'Guest')
        self.assertTrue(guest_info['is_guest'])

        # Verify that 'Guest' does not exist in the users table
        self.auth.cursor.execute("SELECT * FROM users WHERE username = %s", ('Guest',))
        result = self.auth.cursor.fetchone()
        self.assertIsNone(result)


if __name__ == '__main__':
    unittest.main()
