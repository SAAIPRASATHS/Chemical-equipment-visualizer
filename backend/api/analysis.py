"""
Core analysis engine for chemical equipment health monitoring.
Uses Pandas for data analysis and implements health scoring algorithms.
"""
import pandas as pd
import numpy as np
from django.conf import settings
from typing import Dict, List, Tuple


class EquipmentAnalyzer:
    """Analyzes equipment data and calculates health scores."""
    
    def __init__(self):
        self.max_safe_pressure = settings.MAX_SAFE_PRESSURE
        self.max_safe_temperature = settings.MAX_SAFE_TEMPERATURE
    
    def validate_csv(self, df: pd.DataFrame) -> Tuple[bool, str]:
        """
        Validate CSV structure.
        
        Args:
            df: Pandas DataFrame from uploaded CSV
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        required_columns = ['Equipment Name', 'Type', 'Flowrate', 'Pressure', 'Temperature']
        
        # Check if all required columns exist
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            return False, f"Missing required columns: {', '.join(missing_columns)}"
        
        # Check for empty dataframe
        if df.empty:
            return False, "CSV file is empty"
        
        # Check for numeric columns
        numeric_columns = ['Flowrate', 'Pressure', 'Temperature']
        for col in numeric_columns:
            if not pd.api.types.is_numeric_dtype(df[col]):
                try:
                    df[col] = pd.to_numeric(df[col], errors='coerce')
                except:
                    return False, f"Column '{col}' must contain numeric values"
        
        # Check for null values in critical columns
        if df[required_columns].isnull().any().any():
            return False, "CSV contains missing values in required columns"
        
        return True, "Valid"
    
    def calculate_health_score(self, pressure: float, temperature: float, flowrate: float) -> float:
        """
        Calculate health score based on equipment parameters.
        
        Formula: Health Score = 100 - (Pressure/MaxSafePressure * 30) 
                                     - (Temperature/MaxSafeTemperature * 40) 
                                     + Flowrate Stability Bonus
        
        Args:
            pressure: Equipment pressure
            temperature: Equipment temperature
            flowrate: Equipment flowrate
            
        Returns:
            Health score (0-100)
        """
        # Pressure penalty (max 30 points)
        pressure_penalty = (pressure / self.max_safe_pressure) * 30
        
        # Temperature penalty (max 40 points)
        temperature_penalty = (temperature / self.max_safe_temperature) * 40
        
        # Flowrate stability bonus (0-10 points)
        # Higher flowrate is generally better (assuming positive correlation with stability)
        flowrate_bonus = min(flowrate / 10, 10) if flowrate > 0 else 0
        
        # Calculate final score
        health_score = 100 - pressure_penalty - temperature_penalty + flowrate_bonus
        
        # Ensure score is within 0-100 range
        return max(0, min(100, health_score))
    
    def classify_risk(self, health_score: float) -> str:
        """
        Classify equipment risk level based on health score.
        
        Args:
            health_score: Calculated health score
            
        Returns:
            Risk level: 'Healthy', 'Warning', or 'Critical'
        """
        if health_score >= 80:
            return 'Healthy'
        elif health_score >= 50:
            return 'Warning'
        else:
            return 'Critical'
    
    def generate_recommendations(self, pressure: float, temperature: float, 
                                 flowrate: float, equipment_type: str) -> str:
        """
        Generate smart recommendations based on equipment parameters.
        
        Args:
            pressure: Equipment pressure
            temperature: Equipment temperature
            flowrate: Equipment flowrate
            equipment_type: Type of equipment
            
        Returns:
            Recommendation string
        """
        recommendations = []
        
        # Pressure-based recommendations
        if pressure > self.max_safe_pressure * 0.8:
            recommendations.append("⚠️ High pressure detected - Recommend valve inspection and pressure relief system check")
        elif pressure > self.max_safe_pressure * 0.6:
            recommendations.append("⚡ Elevated pressure - Monitor closely and schedule preventive maintenance")
        
        # Temperature-based recommendations
        if temperature > self.max_safe_temperature * 0.8:
            recommendations.append("🔥 High temperature detected - Recommend cooling system check and thermal insulation inspection")
        elif temperature > self.max_safe_temperature * 0.6:
            recommendations.append("🌡️ Elevated temperature - Verify cooling system efficiency")
        
        # Flowrate-based recommendations
        if flowrate < 5:
            recommendations.append("🔧 Low flowrate detected - Recommend pump calibration and line obstruction check")
        elif flowrate < 10:
            recommendations.append("📊 Below optimal flowrate - Consider pump performance evaluation")
        
        # Equipment type specific recommendations
        if equipment_type.lower() in ['valve', 'control valve']:
            recommendations.append("🔍 Valve-specific: Check for wear, leakage, and actuator performance")
        elif equipment_type.lower() in ['pump', 'centrifugal pump']:
            recommendations.append("🔍 Pump-specific: Inspect impeller, bearings, and seal condition")
        elif equipment_type.lower() in ['heat exchanger', 'exchanger']:
            recommendations.append("🔍 Heat Exchanger-specific: Check for fouling and tube integrity")
        
        if not recommendations:
            recommendations.append("✅ Equipment operating within normal parameters - Continue routine monitoring")
        
        return " | ".join(recommendations)
    
    def analyze_dataset(self, df: pd.DataFrame) -> Dict:
        """
        Perform comprehensive analysis on the dataset.
        
        Args:
            df: Pandas DataFrame with equipment data
            
        Returns:
            Dictionary containing analysis results
        """
        # Calculate health scores and risk levels for each equipment
        df['health_score'] = df.apply(
            lambda row: self.calculate_health_score(
                row['Pressure'], row['Temperature'], row['Flowrate']
            ), axis=1
        )
        
        df['risk_level'] = df['health_score'].apply(self.classify_risk)
        
        df['recommendations'] = df.apply(
            lambda row: self.generate_recommendations(
                row['Pressure'], row['Temperature'], row['Flowrate'], row['Type']
            ), axis=1
        )
        
        # Calculate summary statistics
        summary = {
            'total_equipment': len(df),
            'avg_flowrate': float(df['Flowrate'].mean()),
            'avg_pressure': float(df['Pressure'].mean()),
            'avg_temperature': float(df['Temperature'].mean()),
            'healthy_count': int((df['risk_level'] == 'Healthy').sum()),
            'warning_count': int((df['risk_level'] == 'Warning').sum()),
            'critical_count': int((df['risk_level'] == 'Critical').sum()),
            'type_distribution': df['Type'].value_counts().to_dict(),
            'critical_equipment': df[df['risk_level'] == 'Critical'][['Equipment Name', 'Type', 'health_score']].to_dict('records'),
        }
        
        # Generate executive summary
        summary['executive_summary'] = self.generate_executive_summary(summary)
        
        return summary, df
    
    def generate_executive_summary(self, summary: Dict) -> str:
        """
        Generate natural language executive summary.
        
        Args:
            summary: Analysis summary dictionary
            
        Returns:
            Executive summary string
        """
        total = summary['total_equipment']
        critical_pct = (summary['critical_count'] / total * 100) if total > 0 else 0
        warning_pct = (summary['warning_count'] / total * 100) if total > 0 else 0
        healthy_pct = (summary['healthy_count'] / total * 100) if total > 0 else 0
        
        # Find equipment type with highest risk
        type_dist = summary['type_distribution']
        most_common_type = max(type_dist, key=type_dist.get) if type_dist else "Unknown"
        
        # Build executive summary
        summary_parts = []
        
        summary_parts.append(
            f"Out of {total} equipment units analyzed, "
            f"{summary['critical_count']} ({critical_pct:.1f}%) are in critical condition, "
            f"{summary['warning_count']} ({warning_pct:.1f}%) require attention, "
            f"and {summary['healthy_count']} ({healthy_pct:.1f}%) are operating normally."
        )
        
        if summary['critical_count'] > 0:
            summary_parts.append(
                f"Immediate inspection is recommended for critical equipment. "
                f"The most common equipment type is {most_common_type}."
            )
        
        if summary['avg_pressure'] > self.max_safe_pressure * 0.7:
            summary_parts.append(
                f"Average pressure ({summary['avg_pressure']:.1f}) is approaching safety limits. "
                f"System-wide pressure management review recommended."
            )
        
        if summary['avg_temperature'] > self.max_safe_temperature * 0.7:
            summary_parts.append(
                f"Average temperature ({summary['avg_temperature']:.1f}°C) is elevated. "
                f"Cooling system efficiency should be evaluated."
            )
        
        return " ".join(summary_parts)
    
    def compare_trends(self, current_df: pd.DataFrame, previous_df: pd.DataFrame) -> Dict:
        """
        Compare current dataset with previous dataset to identify trends.
        
        Args:
            current_df: Current dataset DataFrame
            previous_df: Previous dataset DataFrame
            
        Returns:
            Dictionary containing trend comparison
        """
        # Calculate percentage changes
        pressure_change = ((current_df['Pressure'].mean() - previous_df['Pressure'].mean()) 
                          / previous_df['Pressure'].mean() * 100)
        temperature_change = ((current_df['Temperature'].mean() - previous_df['Temperature'].mean()) 
                             / previous_df['Temperature'].mean() * 100)
        flowrate_change = ((current_df['Flowrate'].mean() - previous_df['Flowrate'].mean()) 
                          / previous_df['Flowrate'].mean() * 100)
        
        # Find new critical equipment
        current_critical = set(current_df[current_df['risk_level'] == 'Critical']['Equipment Name'])
        previous_critical = set(previous_df[previous_df['risk_level'] == 'Critical']['Equipment Name'])
        new_critical = list(current_critical - previous_critical)
        
        return {
            'pressure_change': float(pressure_change),
            'temperature_change': float(temperature_change),
            'flowrate_change': float(flowrate_change),
            'new_critical_equipment': new_critical,
        }
