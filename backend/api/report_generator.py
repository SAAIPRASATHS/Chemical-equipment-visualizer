"""
PDF Report Generator using ReportLab.
"""
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.graphics.shapes import Drawing
from reportlab.graphics.charts.barcharts import VerticalBarChart
from reportlab.graphics.charts.piecharts import Pie
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from io import BytesIO
from datetime import datetime


class ReportGenerator:
    """Generates PDF reports for equipment analysis."""
    
    def __init__(self, dataset, equipment_list):
        self.dataset = dataset
        self.equipment_list = equipment_list
        self.buffer = BytesIO()
        self.styles = getSampleStyleSheet()
        self._add_custom_styles()
    
    def _add_custom_styles(self):
        """Add custom paragraph styles."""
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#1a237e'),
            spaceAfter=30,
            alignment=TA_CENTER
        ))
        
        self.styles.add(ParagraphStyle(
            name='SectionHeader',
            parent=self.styles['Heading2'],
            fontSize=16,
            textColor=colors.HexColor('#283593'),
            spaceAfter=12,
            spaceBefore=12
        ))
    
    def _create_header(self):
        """Create report header."""
        elements = []
        
        # Title
        title = Paragraph(
            "Chemical Equipment Health Intelligence Report",
            self.styles['CustomTitle']
        )
        elements.append(title)
        elements.append(Spacer(1, 0.2*inch))
        
        # Report metadata
        metadata = [
            ['Report Generated:', datetime.now().strftime('%Y-%m-%d %H:%M:%S')],
            ['Dataset:', self.dataset.filename],
            ['Upload Date:', self.dataset.upload_date.strftime('%Y-%m-%d %H:%M:%S')],
            ['Uploaded By:', self.dataset.uploaded_by.username],
        ]
        
        metadata_table = Table(metadata, colWidths=[2*inch, 4*inch])
        metadata_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#e3f2fd')),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))
        
        elements.append(metadata_table)
        elements.append(Spacer(1, 0.3*inch))
        
        return elements
    
    def _create_executive_summary(self):
        """Create executive summary section."""
        elements = []
        
        elements.append(Paragraph("Executive Summary", self.styles['SectionHeader']))
        elements.append(Spacer(1, 0.1*inch))
        
        summary_text = Paragraph(self.dataset.executive_summary, self.styles['BodyText'])
        elements.append(summary_text)
        elements.append(Spacer(1, 0.2*inch))
        
        return elements
    
    def _create_summary_statistics(self):
        """Create summary statistics section."""
        elements = []
        
        elements.append(Paragraph("Summary Statistics", self.styles['SectionHeader']))
        elements.append(Spacer(1, 0.1*inch))
        
        stats_data = [
            ['Metric', 'Value'],
            ['Total Equipment', str(self.dataset.total_equipment)],
            ['Average Flowrate', f"{self.dataset.avg_flowrate:.2f}"],
            ['Average Pressure', f"{self.dataset.avg_pressure:.2f}"],
            ['Average Temperature', f"{self.dataset.avg_temperature:.2f}°C"],
            ['Healthy Equipment', str(self.dataset.healthy_count)],
            ['Warning Equipment', str(self.dataset.warning_count)],
            ['Critical Equipment', str(self.dataset.critical_count)],
        ]
        
        stats_table = Table(stats_data, colWidths=[3*inch, 2*inch])
        stats_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1a237e')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f5f5f5')]),
        ]))
        
        elements.append(stats_table)
        elements.append(Spacer(1, 0.3*inch))
        
        return elements
    
    def _create_risk_distribution_chart(self):
        """Create risk distribution pie chart using ReportLab."""
        elements = []
        
        elements.append(Paragraph("Risk Distribution", self.styles['SectionHeader']))
        elements.append(Spacer(1, 0.1*inch))
        
        # Create ReportLab pie chart
        drawing = Drawing(400, 200)
        pie = Pie()
        pie.x = 150
        pie.y = 50
        pie.width = 100
        pie.height = 100
        
        pie.data = [self.dataset.healthy_count, self.dataset.warning_count, self.dataset.critical_count]
        pie.labels = ['Healthy', 'Warning', 'Critical']
        pie.slices.strokeWidth = 0.5
        pie.slices[0].fillColor = colors.HexColor('#4caf50')
        pie.slices[1].fillColor = colors.HexColor('#ff9800')
        pie.slices[2].fillColor = colors.HexColor('#f44336')
        
        drawing.add(pie)
        elements.append(drawing)
        elements.append(Spacer(1, 0.3*inch))
        
        return elements
    
    def _create_critical_equipment_list(self):
        """Create critical equipment list."""
        elements = []
        
        critical_equipment = [eq for eq in self.equipment_list if eq.risk_level == 'Critical']
        
        if critical_equipment:
            elements.append(Paragraph("Critical Equipment List", self.styles['SectionHeader']))
            elements.append(Spacer(1, 0.1*inch))
            
            critical_data = [['Equipment Name', 'Type', 'Health Score', 'Recommendations']]
            
            for eq in critical_equipment[:10]:  # Limit to top 10
                critical_data.append([
                    eq.name,
                    eq.equipment_type,
                    f"{eq.health_score:.1f}",
                    eq.recommendations[:100] + '...' if len(eq.recommendations) > 100 else eq.recommendations
                ])
            
            critical_table = Table(critical_data, colWidths=[1.5*inch, 1*inch, 1*inch, 3*inch])
            critical_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#f44336')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 8),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#ffebee')]),
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ]))
            
            elements.append(critical_table)
            elements.append(Spacer(1, 0.3*inch))
        
        return elements
    
    def _create_equipment_type_distribution(self):
        """Create equipment type distribution chart using ReportLab."""
        elements = []
        
        elements.append(Paragraph("Equipment Type Distribution", self.styles['SectionHeader']))
        elements.append(Spacer(1, 0.1*inch))
        
        # Create ReportLab bar chart
        type_dist = self.dataset.type_distribution
        
        if type_dist:
            drawing = Drawing(400, 200)
            bc = VerticalBarChart()
            bc.x = 50
            bc.y = 50
            bc.height = 125
            bc.width = 300
            bc.data = [list(type_dist.values())]
            bc.categoryAxis.categoryNames = list(type_dist.keys())
            bc.valueAxis.valueMin = 0
            bc.bars[0].fillColor = colors.HexColor('#2196f3')
            
            drawing.add(bc)
            elements.append(drawing)
            elements.append(Spacer(1, 0.3*inch))
        
        return elements
    
    def generate(self):
        """Generate the complete PDF report."""
        doc = SimpleDocTemplate(self.buffer, pagesize=letter,
                               rightMargin=0.75*inch, leftMargin=0.75*inch,
                               topMargin=0.75*inch, bottomMargin=0.75*inch)
        
        # Build report elements
        elements = []
        elements.extend(self._create_header())
        elements.extend(self._create_executive_summary())
        elements.extend(self._create_summary_statistics())
        elements.extend(self._create_risk_distribution_chart())
        elements.extend(self._create_critical_equipment_list())
        elements.extend(self._create_equipment_type_distribution())
        
        # Build PDF
        doc.build(elements)
        
        # Get PDF data
        pdf_data = self.buffer.getvalue()
        self.buffer.close()
        
        return pdf_data
