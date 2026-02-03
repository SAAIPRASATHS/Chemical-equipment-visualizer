"""
API Views for Chemical Equipment Intelligence system.
"""
from rest_framework import status, viewsets
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from django.http import HttpResponse
from django.conf import settings
from django.contrib.auth import get_user_model
import pandas as pd
import io

from .models import Dataset, Equipment, TrendComparison
from .serializers import (
    UserSerializer, UserRegistrationSerializer, DatasetSerializer,
    DatasetDetailSerializer, EquipmentSerializer, TrendComparisonSerializer,
    SummarySerializer, HistorySerializer
)
from .analysis import EquipmentAnalyzer
from .report_generator import ReportGenerator

User = get_user_model()


@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    """Register a new user."""
    serializer = UserRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        return Response({
            'message': 'User registered successfully',
            'user': UserSerializer(user).data
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def upload_csv(request):
    """
    Upload and analyze CSV file.
    Validates structure, calculates health scores, and stores data.
    """
    if 'file' not in request.FILES:
        return Response({'error': 'No file provided'}, status=status.HTTP_400_BAD_REQUEST)
    
    csv_file = request.FILES['file']
    
    # Validate file extension
    if not csv_file.name.endswith('.csv'):
        return Response({'error': 'File must be a CSV'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        # Read CSV into DataFrame
        df = pd.read_csv(csv_file)
        
        # Initialize analyzer
        analyzer = EquipmentAnalyzer()
        
        # Validate CSV structure
        is_valid, error_message = analyzer.validate_csv(df)
        if not is_valid:
            return Response({'error': error_message}, status=status.HTTP_400_BAD_REQUEST)
        
        # Analyze dataset
        summary, analyzed_df = analyzer.analyze_dataset(df)
        
        # Create Dataset record
        dataset = Dataset.objects.create(
            uploaded_by=request.user,
            filename=csv_file.name,
            total_equipment=summary['total_equipment'],
            avg_flowrate=summary['avg_flowrate'],
            avg_pressure=summary['avg_pressure'],
            avg_temperature=summary['avg_temperature'],
            healthy_count=summary['healthy_count'],
            warning_count=summary['warning_count'],
            critical_count=summary['critical_count'],
            executive_summary=summary['executive_summary'],
            type_distribution=summary['type_distribution']
        )
        
        # Create Equipment records
        equipment_records = []
        for _, row in analyzed_df.iterrows():
            equipment_records.append(Equipment(
                dataset=dataset,
                name=row['Equipment Name'],
                equipment_type=row['Type'],
                flowrate=row['Flowrate'],
                pressure=row['Pressure'],
                temperature=row['Temperature'],
                health_score=row['health_score'],
                risk_level=row['risk_level'],
                recommendations=row['recommendations']
            ))
        
        Equipment.objects.bulk_create(equipment_records)
        
        # Compare with previous dataset if exists
        previous_datasets = Dataset.objects.filter(
            uploaded_by=request.user
        ).exclude(id=dataset.id).order_by('-upload_date')
        
        if previous_datasets.exists():
            previous_dataset = previous_datasets.first()
            previous_df = pd.DataFrame(list(
                previous_dataset.equipment.values(
                    'name', 'equipment_type', 'flowrate', 'pressure', 'temperature'
                )
            ))
            previous_df.columns = ['Equipment Name', 'Type', 'Flowrate', 'Pressure', 'Temperature']
            
            # Analyze previous dataset to get risk levels
            _, previous_analyzed_df = analyzer.analyze_dataset(previous_df)
            
            # Compare trends
            trend_data = analyzer.compare_trends(analyzed_df, previous_analyzed_df)
            
            # Create TrendComparison record
            TrendComparison.objects.create(
                current_dataset=dataset,
                previous_dataset=previous_dataset,
                pressure_change=trend_data['pressure_change'],
                temperature_change=trend_data['temperature_change'],
                flowrate_change=trend_data['flowrate_change'],
                new_critical_equipment=trend_data['new_critical_equipment']
            )
        
        # Maintain only last 5 datasets
        all_datasets = Dataset.objects.filter(uploaded_by=request.user).order_by('-upload_date')
        if all_datasets.count() > settings.MAX_DATASET_HISTORY:
            datasets_to_delete = all_datasets[settings.MAX_DATASET_HISTORY:]
            for ds in datasets_to_delete:
                ds.delete()
        
        return Response({
            'message': 'CSV uploaded and analyzed successfully',
            'dataset': DatasetDetailSerializer(dataset).data
        }, status=status.HTTP_201_CREATED)
    
    except Exception as e:
        return Response({
            'error': f'Error processing CSV: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_summary(request):
    """
    Get summary of the most recent dataset.
    Includes current dataset, trend comparison, and critical equipment.
    """
    try:
        # Get most recent dataset
        current_dataset = Dataset.objects.filter(
            uploaded_by=request.user
        ).order_by('-upload_date').first()
        
        if not current_dataset:
            return Response({
                'message': 'No datasets found. Please upload a CSV file first.'
            }, status=status.HTTP_404_NOT_FOUND)
        
        # Get trend comparison
        trend_comparison = TrendComparison.objects.filter(
            current_dataset=current_dataset
        ).first()
        
        # Get critical equipment
        critical_equipment = Equipment.objects.filter(
            dataset=current_dataset,
            risk_level='Critical'
        ).order_by('health_score')
        
        # Build risk distribution
        risk_distribution = {
            'Healthy': current_dataset.healthy_count,
            'Warning': current_dataset.warning_count,
            'Critical': current_dataset.critical_count
        }
        
        # Build parameter trends
        parameter_trends = {
            'avg_flowrate': current_dataset.avg_flowrate,
            'avg_pressure': current_dataset.avg_pressure,
            'avg_temperature': current_dataset.avg_temperature
        }
        
        response_data = {
            'current_dataset': DatasetDetailSerializer(current_dataset).data,
            'trend_comparison': TrendComparisonSerializer(trend_comparison).data if trend_comparison else None,
            'critical_equipment': EquipmentSerializer(critical_equipment, many=True).data,
            'risk_distribution': risk_distribution,
            'parameter_trends': parameter_trends
        }
        
        return Response(response_data, status=status.HTTP_200_OK)
    
    except Exception as e:
        return Response({
            'error': f'Error retrieving summary: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_history(request):
    """
    Get history of last 5 datasets.
    """
    try:
        datasets = Dataset.objects.filter(
            uploaded_by=request.user
        ).order_by('-upload_date')[:settings.MAX_DATASET_HISTORY]
        
        response_data = {
            'datasets': DatasetSerializer(datasets, many=True).data,
            'total_count': datasets.count()
        }
        
        return Response(response_data, status=status.HTTP_200_OK)
    
    except Exception as e:
        return Response({
            'error': f'Error retrieving history: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def generate_report(request, dataset_id):
    """
    Generate and download PDF report for a specific dataset.
    """
    try:
        dataset = Dataset.objects.get(id=dataset_id, uploaded_by=request.user)
        equipment_list = Equipment.objects.filter(dataset=dataset)
        
        # Generate PDF
        report_gen = ReportGenerator(dataset, equipment_list)
        pdf_data = report_gen.generate()
        
        # Create HTTP response
        response = HttpResponse(pdf_data, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="equipment_report_{dataset_id}.pdf"'
        
        return response
    
    except Dataset.DoesNotExist:
        return Response({
            'error': 'Dataset not found'
        }, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({
            'error': f'Error generating report: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_dataset_detail(request, dataset_id):
    """Get detailed information about a specific dataset."""
    try:
        dataset = Dataset.objects.get(id=dataset_id, uploaded_by=request.user)
        return Response(
            DatasetDetailSerializer(dataset).data,
            status=status.HTTP_200_OK
        )
    except Dataset.DoesNotExist:
        return Response({
            'error': 'Dataset not found'
        }, status=status.HTTP_404_NOT_FOUND)
