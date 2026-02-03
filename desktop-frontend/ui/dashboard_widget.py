"""
Dashboard Widget for Desktop Application.
Displays summary statistics, charts, and critical equipment.
"""
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QTableWidget, QTableWidgetItem, QScrollArea,
                             QMessageBox, QFileDialog, QGroupBox, QGridLayout)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


class DashboardWidget(QWidget):
    """Dashboard widget showing equipment health data."""
    
    def __init__(self, api_client):
        super().__init__()
        self.api_client = api_client
        self.summary_data = None
        self.init_ui()
        self.load_data()
    
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
                padding: 10px 15px;
                font-size: 13px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #5c6bc0;
            }
            QTableWidget {
                background-color: #1a1f3a;
                color: #e8eaf6;
                gridline-color: #283593;
                border: 1px solid #283593;
            }
            QTableWidget::item {
                padding: 5px;
            }
            QHeaderView::section {
                background-color: #151932;
                color: #9fa8da;
                padding: 8px;
                border: 1px solid #283593;
                font-weight: bold;
            }
            QGroupBox {
                border: 2px solid #283593;
                border-radius: 8px;
                margin-top: 10px;
                padding: 15px;
                font-weight: bold;
                color: #e8eaf6;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
            }
        """)
        
        main_layout = QVBoxLayout()
        
        # Header
        header_layout = QHBoxLayout()
        title = QLabel('📊 Equipment Health Dashboard')
        title_font = QFont()
        title_font.setPointSize(18)
        title_font.setBold(True)
        title.setFont(title_font)
        
        refresh_btn = QPushButton('🔄 Refresh')
        refresh_btn.clicked.connect(self.load_data)
        
        download_btn = QPushButton('📄 Download Report')
        download_btn.clicked.connect(self.download_report)
        
        header_layout.addWidget(title)
        header_layout.addStretch()
        header_layout.addWidget(refresh_btn)
        header_layout.addWidget(download_btn)
        
        main_layout.addLayout(header_layout)
        
        # Scroll area for content
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll_widget = QWidget()
        scroll_layout = QVBoxLayout()
        
        # Executive Summary
        self.summary_label = QLabel()
        self.summary_label.setWordWrap(True)
        self.summary_label.setStyleSheet("""
            background-color: #1a1f3a;
            border: 2px solid #3f51b5;
            border-radius: 8px;
            padding: 15px;
            font-size: 13px;
            line-height: 1.6;
        """)
        summary_group = QGroupBox('📋 Executive Summary')
        summary_layout = QVBoxLayout()
        summary_layout.addWidget(self.summary_label)
        summary_group.setLayout(summary_layout)
        scroll_layout.addWidget(summary_group)
        
        # Statistics Cards
        stats_group = QGroupBox('📈 Summary Statistics')
        stats_layout = QGridLayout()
        
        self.total_label = self.create_stat_card('Total Equipment', '0', '#3f51b5')
        self.healthy_label = self.create_stat_card('Healthy', '0', '#4caf50')
        self.warning_label = self.create_stat_card('Warning', '0', '#ff9800')
        self.critical_label = self.create_stat_card('Critical', '0', '#f44336')
        
        stats_layout.addWidget(self.total_label, 0, 0)
        stats_layout.addWidget(self.healthy_label, 0, 1)
        stats_layout.addWidget(self.warning_label, 0, 2)
        stats_layout.addWidget(self.critical_label, 0, 3)
        
        stats_group.setLayout(stats_layout)
        scroll_layout.addWidget(stats_group)
        
        # Charts
        charts_group = QGroupBox('📊 Visualizations')
        charts_layout = QHBoxLayout()
        
        # Create matplotlib figures
        self.fig1 = Figure(figsize=(5, 4), facecolor='#0a0e27')
        self.canvas1 = FigureCanvas(self.fig1)
        self.ax1 = self.fig1.add_subplot(111)
        
        self.fig2 = Figure(figsize=(5, 4), facecolor='#0a0e27')
        self.canvas2 = FigureCanvas(self.fig2)
        self.ax2 = self.fig2.add_subplot(111)
        
        charts_layout.addWidget(self.canvas1)
        charts_layout.addWidget(self.canvas2)
        
        charts_group.setLayout(charts_layout)
        scroll_layout.addWidget(charts_group)
        
        # Critical Equipment Table
        table_group = QGroupBox('🚨 Critical Equipment')
        table_layout = QVBoxLayout()
        
        self.equipment_table = QTableWidget()
        self.equipment_table.setColumnCount(5)
        self.equipment_table.setHorizontalHeaderLabels([
            'Equipment Name', 'Type', 'Health Score', 'Risk Level', 'Recommendations'
        ])
        self.equipment_table.horizontalHeader().setStretchLastSection(True)
        
        table_layout.addWidget(self.equipment_table)
        table_group.setLayout(table_layout)
        scroll_layout.addWidget(table_group)
        
        scroll_widget.setLayout(scroll_layout)
        scroll.setWidget(scroll_widget)
        main_layout.addWidget(scroll)
        
        self.setLayout(main_layout)
    
    def create_stat_card(self, label, value, color):
        """Create a statistics card widget."""
        card = QLabel()
        card.setAlignment(Qt.AlignCenter)
        card.setStyleSheet(f"""
            background-color: #1a1f3a;
            border: 2px solid {color};
            border-radius: 8px;
            padding: 20px;
            font-size: 14px;
        """)
        card.setText(f'<div style="text-align: center;">'
                    f'<div style="font-size: 32px; font-weight: bold; color: {color};">{value}</div>'
                    f'<div style="color: #9fa8da; margin-top: 5px;">{label}</div>'
                    f'</div>')
        return card
    
    def update_stat_card(self, card, label, value, color):
        """Update a statistics card."""
        card.setText(f'<div style="text-align: center;">'
                    f'<div style="font-size: 32px; font-weight: bold; color: {color};">{value}</div>'
                    f'<div style="color: #9fa8da; margin-top: 5px;">{label}</div>'
                    f'</div>')
    
    def load_data(self):
        """Load dashboard data from API."""
        try:
            self.summary_data = self.api_client.get_summary()
            self.update_ui()
        except Exception as e:
            QMessageBox.warning(self, 'Error', f'Failed to load data: {str(e)}')
    
    def update_ui(self):
        """Update UI with loaded data."""
        if not self.summary_data:
            return
        
        current_dataset = self.summary_data['current_dataset']
        critical_equipment = self.summary_data['critical_equipment']
        risk_distribution = self.summary_data['risk_distribution']
        
        # Update summary
        self.summary_label.setText(current_dataset['executive_summary'])
        
        # Update statistics
        self.update_stat_card(self.total_label, 'Total Equipment', 
                            str(current_dataset['total_equipment']), '#3f51b5')
        self.update_stat_card(self.healthy_label, 'Healthy', 
                            str(current_dataset['healthy_count']), '#4caf50')
        self.update_stat_card(self.warning_label, 'Warning', 
                            str(current_dataset['warning_count']), '#ff9800')
        self.update_stat_card(self.critical_label, 'Critical', 
                            str(current_dataset['critical_count']), '#f44336')
        
        # Update charts
        self.plot_type_distribution(current_dataset['type_distribution'])
        self.plot_risk_distribution(risk_distribution)
        
        # Update table
        self.update_equipment_table(critical_equipment)
    
    def plot_type_distribution(self, type_dist):
        """Plot equipment type distribution."""
        self.ax1.clear()
        
        types = list(type_dist.keys())
        counts = list(type_dist.values())
        
        self.ax1.bar(types, counts, color='#3f51b5')
        self.ax1.set_title('Equipment Type Distribution', color='#e8eaf6', fontsize=12, fontweight='bold')
        self.ax1.set_xlabel('Equipment Type', color='#9fa8da')
        self.ax1.set_ylabel('Count', color='#9fa8da')
        self.ax1.tick_params(colors='#9fa8da', labelsize=9)
        plt.setp(self.ax1.xaxis.get_majorticklabels(), rotation=45, ha='right')
        self.ax1.set_facecolor('#0a0e27')
        self.ax1.grid(True, alpha=0.2, color='#283593')
        
        self.fig1.tight_layout()
        self.canvas1.draw()
    
    def plot_risk_distribution(self, risk_dist):
        """Plot risk distribution pie chart."""
        self.ax2.clear()
        
        labels = ['Healthy', 'Warning', 'Critical']
        sizes = [risk_dist.get('Healthy', 0), risk_dist.get('Warning', 0), risk_dist.get('Critical', 0)]
        colors = ['#4caf50', '#ff9800', '#f44336']
        
        self.ax2.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', 
                    startangle=90, textprops={'color': '#e8eaf6'})
        self.ax2.set_title('Risk Distribution', color='#e8eaf6', fontsize=12, fontweight='bold')
        
        self.fig2.tight_layout()
        self.canvas2.draw()
    
    def update_equipment_table(self, equipment_list):
        """Update the critical equipment table."""
        self.equipment_table.setRowCount(len(equipment_list))
        
        for row, eq in enumerate(equipment_list):
            self.equipment_table.setItem(row, 0, QTableWidgetItem(eq['name']))
            self.equipment_table.setItem(row, 1, QTableWidgetItem(eq['equipment_type']))
            self.equipment_table.setItem(row, 2, QTableWidgetItem(f"{eq['health_score']:.1f}"))
            self.equipment_table.setItem(row, 3, QTableWidgetItem(eq['risk_level']))
            self.equipment_table.setItem(row, 4, QTableWidgetItem(eq['recommendations']))
    
    def download_report(self):
        """Download PDF report."""
        if not self.summary_data:
            QMessageBox.warning(self, 'Error', 'No data available')
            return
        
        dataset_id = self.summary_data['current_dataset']['id']
        
        file_path, _ = QFileDialog.getSaveFileName(
            self, 'Save Report', f'equipment_report_{dataset_id}.pdf', 'PDF Files (*.pdf)'
        )
        
        if file_path:
            try:
                self.api_client.download_report(dataset_id, file_path)
                QMessageBox.information(self, 'Success', 'Report downloaded successfully!')
            except Exception as e:
                QMessageBox.critical(self, 'Error', f'Failed to download report: {str(e)}')
