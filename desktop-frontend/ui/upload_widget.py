"""
Upload Widget for Desktop Application.
"""
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QFileDialog, QMessageBox, QGroupBox, QTextEdit)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont


class UploadWidget(QWidget):
    """Widget for uploading CSV files."""
    
    def __init__(self, api_client, on_upload_success=None):
        super().__init__()
        self.api_client = api_client
        self.on_upload_success = on_upload_success
        self.selected_file = None
        self.init_ui()
    
    def init_ui(self):
        """Initialize the user interface."""
        self.setStyleSheet("""
            QWidget {
                background-color: #0a0e27;
                color: #e8eaf6;
            }
            QLabel {
                color: #e8eaf6;
            }
            QPushButton {
                background-color: #3f51b5;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 12px 20px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #5c6bc0;
            }
            QPushButton:disabled {
                background-color: #555;
                color: #999;
            }
            QGroupBox {
                border: 2px solid #283593;
                border-radius: 8px;
                margin-top: 10px;
                padding: 15px;
                font-weight: bold;
                color: #e8eaf6;
            }
            QTextEdit {
                background-color: #1a1f3a;
                color: #e8eaf6;
                border: 1px solid #283593;
                border-radius: 5px;
                padding: 10px;
            }
        """)
        
        layout = QVBoxLayout()
        
        # Title
        title = QLabel('📤 Upload Equipment Data')
        title_font = QFont()
        title_font.setPointSize(18)
        title_font.setBold(True)
        title.setFont(title_font)
        layout.addWidget(title)
        
        # Instructions
        instructions_group = QGroupBox('📋 CSV Format Requirements')
        instructions_layout = QVBoxLayout()
        
        instructions = QTextEdit()
        instructions.setReadOnly(True)
        instructions.setMaximumHeight(150)
        instructions.setText(
            "Required CSV Columns:\n\n"
            "• Equipment Name - Unique identifier for equipment\n"
            "• Type - Equipment type (e.g., Pump, Valve, Reactor)\n"
            "• Flowrate - Flow rate measurement (numeric)\n"
            "• Pressure - Pressure measurement (numeric)\n"
            "• Temperature - Temperature measurement in °C (numeric)\n\n"
            "Note: All numeric columns must contain valid numbers."
        )
        
        instructions_layout.addWidget(instructions)
        instructions_group.setLayout(instructions_layout)
        layout.addWidget(instructions_group)
        
        # File selection
        file_group = QGroupBox('📁 Select File')
        file_layout = QVBoxLayout()
        
        self.file_label = QLabel('No file selected')
        self.file_label.setStyleSheet("""
            background-color: #1a1f3a;
            border: 2px dashed #283593;
            border-radius: 8px;
            padding: 20px;
            text-align: center;
            color: #9fa8da;
        """)
        self.file_label.setAlignment(Qt.AlignCenter)
        
        select_btn = QPushButton('📂 Browse Files')
        select_btn.clicked.connect(self.select_file)
        
        file_layout.addWidget(self.file_label)
        file_layout.addWidget(select_btn)
        file_group.setLayout(file_layout)
        layout.addWidget(file_group)
        
        # Upload button
        self.upload_btn = QPushButton('🚀 Upload & Analyze')
        self.upload_btn.setEnabled(False)
        self.upload_btn.clicked.connect(self.upload_file)
        self.upload_btn.setStyleSheet("""
            QPushButton {
                background-color: #4caf50;
                font-size: 16px;
                padding: 15px;
            }
            QPushButton:hover {
                background-color: #66bb6a;
            }
            QPushButton:disabled {
                background-color: #555;
            }
        """)
        layout.addWidget(self.upload_btn)
        
        layout.addStretch()
        self.setLayout(layout)
    
    def select_file(self):
        """Open file dialog to select CSV file."""
        file_path, _ = QFileDialog.getOpenFileName(
            self, 'Select CSV File', '', 'CSV Files (*.csv)'
        )
        
        if file_path:
            self.selected_file = file_path
            self.file_label.setText(f'Selected: {file_path.split("/")[-1]}')
            self.file_label.setStyleSheet("""
                background-color: #1a1f3a;
                border: 2px solid #4caf50;
                border-radius: 8px;
                padding: 20px;
                text-align: center;
                color: #4caf50;
                font-weight: bold;
            """)
            self.upload_btn.setEnabled(True)
    
    def upload_file(self):
        """Upload the selected file."""
        if not self.selected_file:
            QMessageBox.warning(self, 'Error', 'Please select a file first')
            return
        
        self.upload_btn.setEnabled(False)
        self.upload_btn.setText('⏳ Uploading & Analyzing...')
        
        try:
            result = self.api_client.upload_csv(self.selected_file)
            QMessageBox.information(self, 'Success', 'CSV uploaded and analyzed successfully!')
            
            # Reset UI
            self.selected_file = None
            self.file_label.setText('No file selected')
            self.file_label.setStyleSheet("""
                background-color: #1a1f3a;
                border: 2px dashed #283593;
                border-radius: 8px;
                padding: 20px;
                text-align: center;
                color: #9fa8da;
            """)
            
            if self.on_upload_success:
                self.on_upload_success()
        
        except Exception as e:
            QMessageBox.critical(self, 'Upload Failed', str(e))
        
        finally:
            self.upload_btn.setEnabled(True)
            self.upload_btn.setText('🚀 Upload & Analyze')
