"""
Main Window for Desktop Application.
"""
from PyQt5.QtWidgets import QMainWindow, QTabWidget, QMessageBox
from PyQt5.QtCore import Qt
from .dashboard_widget import DashboardWidget
from .upload_widget import UploadWidget


class MainWindow(QMainWindow):
    """Main application window."""
    
    def __init__(self, api_client):
        super().__init__()
        self.api_client = api_client
        self.init_ui()
    
    def init_ui(self):
        """Initialize the user interface."""
        self.setWindowTitle('Chemical Equipment Health Intelligence')
        self.setGeometry(100, 100, 1200, 800)
        
        self.setStyleSheet("""
            QMainWindow {
                background-color: #0a0e27;
            }
            QTabWidget::pane {
                border: 1px solid #283593;
                background-color: #0a0e27;
            }
            QTabBar::tab {
                background-color: #151932;
                color: #9fa8da;
                padding: 12px 24px;
                border: 1px solid #283593;
                font-size: 14px;
                font-weight: bold;
            }
            QTabBar::tab:selected {
                background-color: #3f51b5;
                color: white;
            }
            QTabBar::tab:hover {
                background-color: #252b4a;
            }
        """)
        
        # Create tab widget
        tabs = QTabWidget()
        
        # Dashboard tab
        self.dashboard = DashboardWidget(self.api_client)
        tabs.addTab(self.dashboard, '📊 Dashboard')
        
        # Upload tab
        self.upload = UploadWidget(self.api_client, on_upload_success=self.on_upload_success)
        tabs.addTab(self.upload, '📤 Upload')
        
        self.setCentralWidget(tabs)
    
    def on_upload_success(self):
        """Handle successful upload."""
        # Refresh dashboard
        self.dashboard.load_data()
    
    def closeEvent(self, event):
        """Handle window close event."""
        reply = QMessageBox.question(
            self, 'Confirm Exit',
            'Are you sure you want to exit?',
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()
