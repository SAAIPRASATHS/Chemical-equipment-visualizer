"""
Database models for Chemical Equipment Intelligence system.
"""
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


class User(AbstractUser):
    """Extended user model with role-based access."""
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('viewer', 'Viewer'),
    ]
    
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='viewer')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'users'
    
    def __str__(self):
        return f"{self.username} ({self.role})"


class Dataset(models.Model):
    """Stores metadata and analysis results for uploaded CSV datasets."""
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='datasets')
    upload_date = models.DateTimeField(default=timezone.now)
    filename = models.CharField(max_length=255)
    
    # Summary statistics
    total_equipment = models.IntegerField(default=0)
    avg_flowrate = models.FloatField(default=0.0)
    avg_pressure = models.FloatField(default=0.0)
    avg_temperature = models.FloatField(default=0.0)
    
    # Risk classification counts
    healthy_count = models.IntegerField(default=0)
    warning_count = models.IntegerField(default=0)
    critical_count = models.IntegerField(default=0)
    
    # Executive summary
    executive_summary = models.TextField(blank=True)
    
    # Equipment type distribution (stored as JSON string)
    type_distribution = models.JSONField(default=dict)
    
    class Meta:
        db_table = 'datasets'
        ordering = ['-upload_date']
    
    def __str__(self):
        return f"{self.filename} - {self.upload_date.strftime('%Y-%m-%d %H:%M')}"


class Equipment(models.Model):
    """Individual equipment records from uploaded CSV."""
    dataset = models.ForeignKey(Dataset, on_delete=models.CASCADE, related_name='equipment')
    
    # CSV columns
    name = models.CharField(max_length=255)
    equipment_type = models.CharField(max_length=100)
    flowrate = models.FloatField()
    pressure = models.FloatField()
    temperature = models.FloatField()
    
    # Calculated fields
    health_score = models.FloatField(default=0.0)
    risk_level = models.CharField(max_length=20, default='Unknown')  # Healthy, Warning, Critical
    recommendations = models.TextField(blank=True)
    
    class Meta:
        db_table = 'equipment'
        ordering = ['name']
    
    def __str__(self):
        return f"{self.name} ({self.equipment_type}) - Score: {self.health_score:.1f}"


class TrendComparison(models.Model):
    """Stores trend comparison between consecutive datasets."""
    current_dataset = models.ForeignKey(Dataset, on_delete=models.CASCADE, related_name='trend_as_current')
    previous_dataset = models.ForeignKey(Dataset, on_delete=models.CASCADE, related_name='trend_as_previous')
    
    # Percentage changes
    pressure_change = models.FloatField(default=0.0)
    temperature_change = models.FloatField(default=0.0)
    flowrate_change = models.FloatField(default=0.0)
    
    # New critical equipment
    new_critical_equipment = models.JSONField(default=list)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'trend_comparisons'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Comparison: {self.previous_dataset.filename} → {self.current_dataset.filename}"
