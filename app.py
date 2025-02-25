'''
app.py - Entry Point for the Application
'''
import sys
from main import Main

if __name__ == "__main__":
    # Create an instance of the Main application class
    app = Main()
    # Check if there are any users in the system before allowing login
    app.check_for_users()

    # Loop until the user logs in successfully
    while True:
        # Save what login() retern
        CHECK, full_name = app.login()
        # Check if login was successful
        if CHECK:
            app.log_file(full_name)
            break
        # Exits the program with a status code of 0
        sys.exit()

    # Start the main application loop to manage user interactions
    app.run()
