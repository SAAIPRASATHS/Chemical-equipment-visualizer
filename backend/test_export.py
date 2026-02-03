import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from api.models import Dataset
from api.exporters import DataExporter

# Get the first dataset
datasets = Dataset.objects.all()
print(f"Found {datasets.count()} datasets")

if datasets.exists():
    dataset = datasets.first()
    print(f"Testing export for dataset: {dataset.id} - {dataset.filename}")
    
    try:
        print("\n=== Testing Excel Export ===")
        response = DataExporter.export_to_excel(dataset.id)
        print(f"Excel export result: {response is not None}")
        if response:
            print(f"Content-Type: {response.get('Content-Type')}")
            print(f"Content-Disposition: {response.get('Content-Disposition')}")
    except Exception as e:
        print(f"Excel export error: {e}")
        import traceback
        traceback.print_exc()
    
    try:
        print("\n=== Testing CSV Export ===")
        response = DataExporter.export_to_csv(dataset.id)
        print(f"CSV export result: {response is not None}")
    except Exception as e:
        print(f"CSV export error: {e}")
        import traceback
        traceback.print_exc()
    
    try:
        print("\n=== Testing JSON Export ===")
        response = DataExporter.export_to_json(dataset.id)
        print(f"JSON export result: {response is not None}")
    except Exception as e:
        print(f"JSON export error: {e}")
        import traceback
        traceback.print_exc()
else:
    print("No datasets found!")
