import unittest
from auth import AuthHandler
import mysql.connector
from mysql.connector import errorcode
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta
from io import StringIO
from unittest.mock import patch


class TestAuthHandler(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        load_dotenv()  # Load environment variables
        cls.test_config = {
            'user': os.getenv('DB_USER'),
            'password': os.getenv('DB_PASSWORD'),
            'host': os.getenv('DB_HOST'),
            'database': 'test_cine_mood',
            'raise_on_warnings': True
        }
        try:
            cls.conn = mysql.connector.connect(
                user=cls.test_config['user'],
                password=cls.test_config['password'],
                host=cls.test_config['host']
            )
            cls.cursor = cls.conn.cursor()
            cls.cursor.execute("CREATE DATABASE IF NOT EXISTS test_cine_mood")
            cls.cursor.execute("USE test_cine_mood")
            cls.cursor.execute("""
                   CREATE TABLE IF NOT EXISTS users (
                       id INT AUTO_INCREMENT PRIMARY KEY,
                       username VARCHAR(50) UNIQUE NOT NULL,
                       password BINARY(60) NOT NULL,
                       failed_attempts INT DEFAULT 0,
                       lockout_time DATETIME NULL
                   )
               """)
            cls.conn.commit()
        except mysql.connector.Error as err:
            print(err)
            exit(1)
        cls.auth = AuthHandler(cls.test_config)

    @classmethod
    def tearDownClass(cls):
        cls.cursor.execute("DROP DATABASE test_cine_mood")
        cls.cursor.close()
        cls.conn.close()

    def test_register_user_success(self):
        username = "testuser"
        password = "Test@1234"
        self.auth.register_user(username, password)
        self.auth.cursor.execute("SELECT username FROM users WHERE username = %s", (username,))
        result = self.auth.cursor.fetchone()
        self.assertIsNotNone(result)
        self.assertEqual(result['username'], username)

    def test_register_user_duplicate(self):
        username = "duplicateuser"
        password = "Test@1234"
        self.auth.register_user(username, password)
        # Attempt to register the same user again
        with self.assertLogs(level='INFO') as log:
            self.auth.register_user(username, password)
            self.assertIn("Username is already taken. Please choose another one.", log.output[0])

    def test_register_user_invalid_username(self):
        username = "ab"  # Too short
        password = "Test@1234"
        with self.assertLogs(level='INFO') as log:
            self.auth.register_user(username, password)
            self.assertIn("Invalid username.", log.output[0])

    def test_register_user_invalid_password(self):
        username = "validuser"
        password = "password"  # No special character
        with self.assertLogs(level='INFO') as log:
            self.auth.register_user(username, password)
            self.assertIn("Invalid password.", log.output[0])

    def test_login_user_success(self):
        username = "loginuser"
        password = "Login@1234"
        self.auth.register_user(username, password)
        self.auth.login_user(username, password)
        # Check if failed_attempts reset to 0
        self.auth.cursor.execute("SELECT failed_attempts FROM users WHERE username = %s", (username,))
        result = self.auth.cursor.fetchone()
        self.assertEqual(result['failed_attempts'], 0)

    def test_login_user_failure(self):
        username = "failuser"
        password = "Fail@1234"
        self.auth.register_user(username, password)
        wrong_password = "Wrong@1234"
        for _ in range(AuthHandler.MAX_FAILED_ATTEMPTS):
            self.auth.login_user(username, wrong_password)
        # Check if account is locked
        self.auth.cursor.execute("SELECT lockout_time FROM users WHERE username = %s", (username,))
        result = self.auth.cursor.fetchone()
        self.assertIsNotNone(result['lockout_time'])

    def test_password_hashing(self):
        password = "Hash@1234"
        hashed = self.auth.hash_password(password)
        self.assertTrue(self.auth.verify_password(password, hashed))
        self.assertFalse(self.auth.verify_password("WrongPass", hashed))


if __name__ == '__main__':
    unittest.main()
