from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Dataset, Equipment, TrendComparison


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Admin interface for User model."""
    list_display = ('username', 'email', 'role', 'is_staff', 'created_at')
    list_filter = ('role', 'is_staff', 'is_active')
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Custom Fields', {'fields': ('role',)}),
    )


@admin.register(Dataset)
class DatasetAdmin(admin.ModelAdmin):
    """Admin interface for Dataset model."""
    list_display = ('filename', 'uploaded_by', 'upload_date', 'total_equipment', 'critical_count')
    list_filter = ('upload_date', 'uploaded_by')
    search_fields = ('filename',)
    readonly_fields = ('upload_date',)


@admin.register(Equipment)
class EquipmentAdmin(admin.ModelAdmin):
    """Admin interface for Equipment model."""
    list_display = ('name', 'equipment_type', 'health_score', 'risk_level', 'dataset')
    list_filter = ('risk_level', 'equipment_type', 'dataset')
    search_fields = ('name', 'equipment_type')


@admin.register(TrendComparison)
class TrendComparisonAdmin(admin.ModelAdmin):
    """Admin interface for TrendComparison model."""
    list_display = ('current_dataset', 'previous_dataset', 'pressure_change', 'temperature_change', 'created_at')
    list_filter = ('created_at',)
    readonly_fields = ('created_at',)
