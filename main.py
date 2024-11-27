# main.py

from dotenv import load_dotenv
from auth import AuthHandler
from config import db_config


def run():
    load_dotenv()
    print("Welcome to the CineMood application.")
    try:
        auth = AuthHandler(db_config)
    except Exception as e:
        print(f"Error initializing AuthHandler: {e}")
        return

    while True:
        print("\n1. Login")
        print("2. Register")
        print("3. Exit")
        choice = input("Choose an option: ").strip()

        if choice == '1':
            username = input("Enter username: ").strip()
            password = input("Enter password: ").strip()
            if not username or not password:
                print("Username and password cannot be empty.")
                continue
            try:
                auth.login_user(username, password)
            except Exception as e:
                print(f"Error during login: {e}")
        elif choice == '2':
            username = input("Enter username: ").strip()
            password = input("Enter password: ").strip()
            if not username or not password:
                print("Username and password cannot be empty.")
                continue
            try:
                auth.register_user(username, password)
            except Exception as e:
                print(f"Error during registration: {e}")
        elif choice == '3':
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    run()
