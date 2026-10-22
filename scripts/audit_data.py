"""
Script to execute complete data audit on raw datasets.
Generates:
- reports/data_inventory.csv
- reports/data_dictionary.csv
- reports/data_quality_report.md
- reports/relationship_analysis.md
- reports/id_quality.csv
"""

import sys
from pathlib import Path

# Add src to pythonpath
project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root / "src"))

from healthconnect.data.audit import audit_all

def main():
    print("Starting HealthConnect Rwanda Data Audit...")
    results = audit_all()
    print("Data audit completed successfully!")
    print(f"Total files inventoried: {len(results['inventory'])}")
    print(f"Total columns documented: {len(results['dictionary'])}")

if __name__ == "__main__":
    main()
