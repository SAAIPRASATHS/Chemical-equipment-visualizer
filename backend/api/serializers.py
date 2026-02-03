"""
DRF Serializers for API responses.
"""
from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Dataset, Equipment, TrendComparison

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model."""
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role', 'created_at']
        read_only_fields = ['id', 'created_at']


class UserRegistrationSerializer(serializers.ModelSerializer):
    """Serializer for user registration."""
    password = serializers.CharField(write_only=True, min_length=8)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'role']
    
    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password'],
            role=validated_data.get('role', 'viewer')
        )
        return user


class EquipmentSerializer(serializers.ModelSerializer):
    """Serializer for Equipment model."""
    
    class Meta:
        model = Equipment
        fields = [
            'id', 'name', 'equipment_type', 'flowrate', 'pressure', 
            'temperature', 'health_score', 'risk_level', 'recommendations'
        ]
        read_only_fields = ['id', 'health_score', 'risk_level', 'recommendations']


class DatasetSerializer(serializers.ModelSerializer):
    """Serializer for Dataset model."""
    uploaded_by = UserSerializer(read_only=True)
    equipment_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Dataset
        fields = [
            'id', 'filename', 'uploaded_by', 'upload_date',
            'total_equipment', 'avg_flowrate', 'avg_pressure', 'avg_temperature',
            'healthy_count', 'warning_count', 'critical_count',
            'executive_summary', 'type_distribution', 'equipment_count'
        ]
        read_only_fields = ['id', 'upload_date']
    
    def get_equipment_count(self, obj):
        return obj.equipment.count()


class DatasetDetailSerializer(DatasetSerializer):
    """Detailed serializer for Dataset with equipment list."""
    equipment = EquipmentSerializer(many=True, read_only=True)
    
    class Meta(DatasetSerializer.Meta):
        fields = DatasetSerializer.Meta.fields + ['equipment']


class TrendComparisonSerializer(serializers.ModelSerializer):
    """Serializer for TrendComparison model."""
    current_dataset = DatasetSerializer(read_only=True)
    previous_dataset = DatasetSerializer(read_only=True)
    
    class Meta:
        model = TrendComparison
        fields = [
            'id', 'current_dataset', 'previous_dataset',
            'pressure_change', 'temperature_change', 'flowrate_change',
            'new_critical_equipment', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']


class SummarySerializer(serializers.Serializer):
    """Serializer for summary statistics."""
    current_dataset = DatasetDetailSerializer()
    trend_comparison = TrendComparisonSerializer(allow_null=True)
    critical_equipment = EquipmentSerializer(many=True)
    risk_distribution = serializers.DictField()
    parameter_trends = serializers.DictField()


class HistorySerializer(serializers.Serializer):
    """Serializer for dataset history."""
    datasets = DatasetSerializer(many=True)
    total_count = serializers.IntegerField()
