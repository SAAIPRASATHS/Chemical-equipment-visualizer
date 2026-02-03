"""
Main entry point for Desktop Application.
Chemical Equipment Health Intelligence & Predictive Monitoring System
"""
import sys
from PyQt5.QtWidgets import QApplication, QMessageBox
from ui.login_dialog import LoginDialog
from ui.main_window import MainWindow
from services.api_client import APIClient


def main():
    """Main application entry point."""
    app = QApplication(sys.argv)
    
    # Set application style
    app.setStyle('Fusion')
    
    # Create API client
    api_client = APIClient()
    
    # Show login dialog
    login_dialog = LoginDialog(api_client)
    
    if login_dialog.exec_() == login_dialog.Accepted:
        # Login successful, show main window
        main_window = MainWindow(api_client)
        main_window.show()
        sys.exit(app.exec_())
    else:
        # Login cancelled
        sys.exit(0)


if __name__ == '__main__':
    main()
