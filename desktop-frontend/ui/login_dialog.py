"""
Login Dialog for Desktop Application.
"""
from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                             QLineEdit, QPushButton, QMessageBox, QTabWidget, QWidget, QComboBox)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont


class LoginDialog(QDialog):
    """Login and registration dialog."""
    
    def __init__(self, api_client):
        super().__init__()
        self.api_client = api_client
        self.init_ui()
    
    def init_ui(self):
        """Initialize the user interface."""
        self.setWindowTitle('Chemical Equipment Intelligence - Login')
        self.setFixedSize(450, 400)
        self.setStyleSheet("""
            QDialog {
                background-color: #1a1f3a;
            }
            QLabel {
                color: #e8eaf6;
                font-size: 14px;
            }
            QLineEdit {
                background-color: #151932;
                color: #e8eaf6;
                border: 1px solid #283593;
                border-radius: 5px;
                padding: 8px;
                font-size: 13px;
            }
            QLineEdit:focus {
                border: 2px solid #3f51b5;
            }
            QPushButton {
                background-color: #3f51b5;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 10px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #5c6bc0;
            }
            QPushButton:pressed {
                background-color: #283593;
            }
            QTabWidget::pane {
                border: 1px solid #283593;
                background-color: #1a1f3a;
            }
            QTabBar::tab {
                background-color: #151932;
                color: #9fa8da;
                padding: 10px 20px;
                border: 1px solid #283593;
            }
            QTabBar::tab:selected {
                background-color: #3f51b5;
                color: white;
            }
            QComboBox {
                background-color: #151932;
                color: #e8eaf6;
                border: 1px solid #283593;
                border-radius: 5px;
                padding: 8px;
            }
        """)
        
        layout = QVBoxLayout()
        
        # Title
        title = QLabel('🧪 Chemical Equipment Intelligence')
        title.setAlignment(Qt.AlignCenter)
        title_font = QFont()
        title_font.setPointSize(16)
        title_font.setBold(True)
        title.setFont(title_font)
        layout.addWidget(title)
        
        # Tab widget for login/register
        tabs = QTabWidget()
        
        # Login tab
        login_tab = QWidget()
        login_layout = QVBoxLayout()
        
        self.login_username = QLineEdit()
        self.login_username.setPlaceholderText('Username')
        self.login_password = QLineEdit()
        self.login_password.setPlaceholderText('Password')
        self.login_password.setEchoMode(QLineEdit.Password)
        
        login_btn = QPushButton('Login')
        login_btn.clicked.connect(self.handle_login)
        
        login_layout.addWidget(QLabel('Username:'))
        login_layout.addWidget(self.login_username)
        login_layout.addWidget(QLabel('Password:'))
        login_layout.addWidget(self.login_password)
        login_layout.addWidget(login_btn)
        login_layout.addStretch()
        
        login_tab.setLayout(login_layout)
        
        # Register tab
        register_tab = QWidget()
        register_layout = QVBoxLayout()
        
        self.register_username = QLineEdit()
        self.register_username.setPlaceholderText('Username')
        self.register_email = QLineEdit()
        self.register_email.setPlaceholderText('Email')
        self.register_password = QLineEdit()
        self.register_password.setPlaceholderText('Password (min 8 characters)')
        self.register_password.setEchoMode(QLineEdit.Password)
        self.register_role = QComboBox()
        self.register_role.addItems(['viewer', 'admin'])
        
        register_btn = QPushButton('Register')
        register_btn.clicked.connect(self.handle_register)
        
        register_layout.addWidget(QLabel('Username:'))
        register_layout.addWidget(self.register_username)
        register_layout.addWidget(QLabel('Email:'))
        register_layout.addWidget(self.register_email)
        register_layout.addWidget(QLabel('Password:'))
        register_layout.addWidget(self.register_password)
        register_layout.addWidget(QLabel('Role:'))
        register_layout.addWidget(self.register_role)
        register_layout.addWidget(register_btn)
        register_layout.addStretch()
        
        register_tab.setLayout(register_layout)
        
        tabs.addTab(login_tab, 'Login')
        tabs.addTab(register_tab, 'Register')
        
        layout.addWidget(tabs)
        self.setLayout(layout)
    
    def handle_login(self):
        """Handle login button click."""
        username = self.login_username.text().strip()
        password = self.login_password.text()
        
        if not username or not password:
            QMessageBox.warning(self, 'Error', 'Please enter username and password')
            return
        
        try:
            self.api_client.login(username, password)
            self.accept()
        except Exception as e:
            QMessageBox.critical(self, 'Login Failed', str(e))
    
    def handle_register(self):
        """Handle register button click."""
        username = self.register_username.text().strip()
        email = self.register_email.text().strip()
        password = self.register_password.text()
        role = self.register_role.currentText()
        
        if not username or not email or not password:
            QMessageBox.warning(self, 'Error', 'Please fill in all fields')
            return
        
        if len(password) < 8:
            QMessageBox.warning(self, 'Error', 'Password must be at least 8 characters')
            return
        
        try:
            self.api_client.register(username, email, password, role)
            QMessageBox.information(self, 'Success', 'Registration successful! Please login.')
        except Exception as e:
            QMessageBox.critical(self, 'Registration Failed', str(e))
