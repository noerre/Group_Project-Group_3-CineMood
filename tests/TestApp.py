import unittest
from unittest.mock import patch

from backend.auth import AuthHandler
from backend.app import create_app


class MyTestCase(unittest.TestCase):
    """
        Test suite for the main Flask application endpoints.
        """

    def setUp(self):
        """
        Set up the test client and configure the application for testing.
        """
        # Create a test configuration dictionary
        self.test_config = {
            'TESTING': True,
            'JWT_SECRET_KEY': 'test_secret_key',
        }

        # Create the Flask app with the test configuration
        self.app = create_app(self.test_config)
        self.client = self.app.test_client()

        # Sample data for testing
        self.valid_user = {
            'username': 'testuser',
            'password': 'Test@1234'
        }

        self.invalid_user = {
            'username': 'ab',  # Too short
            'password': 'pass'  # Too short and no special character
        }

    @patch.object(AuthHandler, 'register_user')
    def test_register_success(self, mock_register):
        """
        Test successful user registration.
        """
        mock_register.return_value = None  # Simulate successful registration

        response = self.client.post('/register', json=self.valid_user)
        data = response.get_json()

        self.assertEqual(response.status_code, 201)
        self.assertIn('username', data)
        self.assertIn('access_token', data)
        self.assertFalse(data['is_guest'])
        mock_register.assert_called_once_with(self.valid_user['username'], self.valid_user['password'])

    @patch.object(AuthHandler, 'register_user')
    def test_register_duplicate_username(self, mock_register):
        """
        Test registration with a duplicate username.
        """
        mock_register.side_effect = Exception("Username is already taken. Please choose another one.")

        response = self.client.post('/register', json=self.valid_user)
        data = response.get_json()

        self.assertEqual(response.status_code, 400)
        self.assertIn('error', data)
        self.assertEqual(data['error'], "Username is already taken. Please choose another one.")
        mock_register.assert_called_once_with(self.valid_user['username'], self.valid_user['password'])

    @patch.object(AuthHandler, 'register_user')
    def test_register_invalid_input(self, mock_register):
        """
        Test registration with invalid input data.
        """
        response = self.client.post('/register', json=self.invalid_user)
        data = response.get_json()

        self.assertEqual(response.status_code, 400)
        self.assertIn('errors', data)
        self.assertTrue(len(data['errors']) > 0)
        mock_register.assert_not_called()

    @patch.object(AuthHandler, 'login_user')
    def test_login_success(self, mock_login):
        """
        Test successful user login.
        """
        mock_login.return_value = {'is_guest': False}

        response = self.client.post('/login', json=self.valid_user)
        data = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertIn('username', data)
        self.assertIn('access_token', data)
        self.assertFalse(data['is_guest'])
        mock_login.assert_called_once_with(self.valid_user['username'], self.valid_user['password'])

    @patch.object(AuthHandler, 'login_user')
    def test_login_invalid_credentials(self, mock_login):
        """
        Test login with invalid credentials.
        """
        mock_login.side_effect = Exception("Invalid username or password.")

        response = self.client.post('/login', json=self.valid_user)
        data = response.get_json()

        self.assertEqual(response.status_code, 401)
        self.assertIn('error', data)
        self.assertEqual(data['error'], "Invalid username or password.")
        mock_login.assert_called_once_with(self.valid_user['username'], self.valid_user['password'])

    def test_protected_endpoint_without_token(self):
        """
        Test accessing the protected endpoint without a JWT token.
        """
        response = self.client.get('/protected')
        data = response.get_json()

        self.assertEqual(response.status_code, 401)
        self.assertIn('msg', data)
        self.assertEqual(data['msg'], 'Missing Authorization Header')

    @patch.object(AuthHandler, 'is_token_revoked')
    def test_protected_endpoint_with_valid_token(self, mock_is_revoked):
        """
        Test accessing the protected endpoint with a valid JWT token.
        """
        mock_is_revoked.return_value = False

        # First, login to get a token
        with patch.object(AuthHandler, 'login_user', return_value={'is_guest': False}):
            login_response = self.client.post('/login', json=self.valid_user)
            token = login_response.get_json()['access_token']

        # Access the protected endpoint with the token
        response = self.client.get('/protected', headers={
            'Authorization': f'Bearer {token}'
        })
        data = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertIn('msg', data)
        self.assertIn(self.valid_user['username'], data['msg'])

    @patch.object(AuthHandler, 'logout_user')
    def test_logout_success(self, mock_logout):
        """
        Test successful user logout.
        """
        mock_logout.return_value = None

        # First, login to get a token
        with patch.object(AuthHandler, 'login_user', return_value={'is_guest': False}):
            login_response = self.client.post('/login', json=self.valid_user)
            token = login_response.get_json()['access_token']

        # Logout with the token
        response = self.client.post('/logout', headers={
            'Authorization': f'Bearer {token}'
        })
        data = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertIn('msg', data)
        self.assertEqual(data['msg'], "Successfully logged out.")
        mock_logout.assert_called_once()

    @patch.object(AuthHandler, 'login_guest')
    def test_login_guest_success(self, mock_login_guest):
        """
        Test successful guest login.
        """
        mock_login_guest.return_value = {'username': 'Guest', 'is_guest': True}

        response = self.client.post('/login_guest')
        data = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertIn('username', data)
        self.assertIn('access_token', data)
        self.assertTrue(data['is_guest'])
        mock_login_guest.assert_called_once()


if __name__ == '__main__':
    unittest.main()
