import unittest
from unittest.mock import MagicMock, patch
from database_handler import DatabaseHandler


class TestDatabaseHandler(unittest.TestCase):

    @patch('mysql.connector.connect')
    def setUp(self, mock_connect):
        self.mock_connection = MagicMock()
        mock_connect.return_value = self.mock_connection

        self.db_config = {
            "host": "localhost",
            "user": "test_user",
            "password": "test_password",
            "database": "test_db"
        }
        self.db_handler = DatabaseHandler(self.db_config)

    def test_add_director_existing(self):
        self.db_handler.check_record = MagicMock(return_value=1)

        director_id = 1
        director_name = "Existing Director"

        result = self.db_handler.add_director(director_id, director_name)

        self.assertEqual(result, 1)
        print("Director already exists test passed.")

    def test_add_director_new(self):
        self.db_handler.check_record = MagicMock(return_value=None)

        director_id = 2
        director_name = "New Director"

        result = self.db_handler.add_director(director_id, director_name)

        self.mock_connection.cursor().execute.assert_called_with(
            "INSERT INTO director (id, d_name) VALUES (%s, %s)",
            (director_id, director_name)
        )

        self.assertEqual(result, director_id)
        print("Director new test passed.")

    def test_add_director_no_connection(self):
        self.db_handler.connection = None

        director_id = 3
        director_name = "Director Without Connection"

        result = self.db_handler.add_director(director_id, director_name)

        self.assertIsNone(result)
        print("Director no connection test passed.")


if __name__ == "__main__":
    unittest.main()