#!/usr/bin/env python3
"""
AI-Powered Cloud Security & Compliance Automation
Complete Demo Script
"""

import os
import sys
import csv
from model_utils import scan_cloud_resources

def display_header():
    print("=" * 70)
    print("AI-POWERED CLOUD SECURITY & COMPLIANCE AUTOMATION")
    print("=" * 70)
    print("Semester Project Demonstration")
    print("Developed by: [Your Name]")
    print("=" * 70)

def display_dataset_stats():
    print("\n[1] DATASET ANALYSIS")
    print("-" * 40)
    
    if not os.path.exists('dataset/cloud_security_data.csv'):
        print("[ERROR] Dataset not found!")
        return
    
    with open('dataset/cloud_security_data.csv', 'r') as f:
        reader = csv.DictReader(f)
        data = list(reader)
    
    total_resources = len(data)
    risky_resources = sum(1 for row in data if int(row['Breach_Risk']) == 1)
    secure_resources = total_resources - risky_resources
    
    # Resource type distribution
    resource_types = {}
    for row in data:
        rtype = row['Resource_Type']
        if rtype not in resource_types:
            resource_types[rtype] = 0
        resource_types[rtype] += 1
    
    print(f"Total Resources: {total_resources}")
    print(f"Secure Resources: {secure_resources} ({(secure_resources/total_resources)*100:.1f}%)")
    print(f"Risky Resources: {risky_resources} ({(risky_resources/total_resources)*100:.1f}%)")
    print("\nResource Type Distribution:")
    for rtype, count in resource_types.items():
        print(f"  {rtype}: {count} resources")

def demonstrate_ai_predictions():
    print("\n[2] AI MODEL PREDICTIONS")
    print("-" * 40)
    
    test_cases = [
        {
            'name': 'High Risk S3 Bucket',
            'config': {
                'Resource_Type': 'S3',
                'Public_Access': 1,
                'Open_Ports': 80,
                'Privilege_Level': 'High',
                'Anomaly_Score': 0.9
            }
        },
        {
            'name': 'Secure EC2 Instance',
            'config': {
                'Resource_Type': 'EC2',
                'Public_Access': 0,
                'Open_Ports': 22,
                'Privilege_Level': 'Low',
                'Anomaly_Score': 0.2
            }
        },
        {
            'name': 'Medium Risk IAM Role',
            'config': {
                'Resource_Type': 'IAM',
                'Public_Access': 0,
                'Open_Ports': 0,
                'Privilege_Level': 'Medium',
                'Anomaly_Score': 0.6
            }
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\nTest Case {i}: {test_case['name']}")
        print(f"Configuration: {test_case['config']}")
        
        result = scan_cloud_resources(test_case['config'])
        if result:
            print(f"Prediction: {result['prediction']}")
            print(f"Confidence: {result['confidence']:.3f}")
            print("Recommendations:")
            for rec in result['recommendations']:
                print(f"  - {rec}")
        else:
            print("  [ERROR] Prediction failed")

def show_sample_data():
    print("\n[3] SAMPLE DATASET RECORDS")
    print("-" * 40)
    
    if not os.path.exists('dataset/cloud_security_data.csv'):
        print("[ERROR] Dataset not found!")
        return
    
    with open('dataset/cloud_security_data.csv', 'r') as f:
        reader = csv.DictReader(f)
        data = list(reader)
    
    print("First 5 records:")
    print(f"{'ID':<8} {'Type':<5} {'Public':<7} {'Ports':<6} {'Privilege':<10} {'Score':<6} {'Risk':<5}")
    print("-" * 55)
    
    for i, row in enumerate(data[:5]):
        risk_status = "RISKY" if int(row['Breach_Risk']) == 1 else "SAFE"
        print(f"{row['Resource_ID']:<8} {row['Resource_Type']:<5} {row['Public_Access']:<7} "
              f"{row['Open_Ports']:<6} {row['Privilege_Level']:<10} {row['Anomaly_Score']:<6} {risk_status:<5}")

def display_project_features():
    print("\n[4] PROJECT FEATURES")
    print("-" * 40)
    features = [
        "Synthetic dataset generation (1000 cloud resources)",
        "AI-based anomaly detection using rule-based ML model",
        "Real-time risk assessment and scoring",
        "Interactive web dashboard with visualizations",
        "Automated remediation recommendations",
        "Support for S3, EC2, and IAM resource types",
        "RESTful API for resource scanning",
        "Comprehensive security metrics and reporting"
    ]
    
    for i, feature in enumerate(features, 1):
        print(f"{i:2d}. {feature}")

def display_tech_stack():
    print("\n[5] TECHNOLOGY STACK")
    print("-" * 40)
    tech_stack = {
        "Backend": "Python 3.x, Flask",
        "Data Processing": "CSV, JSON, Pickle",
        "Machine Learning": "Custom rule-based classifier",
        "Frontend": "HTML5, CSS3, Bootstrap 5, Chart.js",
        "Visualization": "Interactive charts and graphs",
        "Architecture": "MVC pattern, RESTful APIs"
    }
    
    for category, technologies in tech_stack.items():
        print(f"{category:15}: {technologies}")

def main():
    display_header()
    display_dataset_stats()
    demonstrate_ai_predictions()
    show_sample_data()
    display_project_features()
    display_tech_stack()
    
    print("\n[6] NEXT STEPS")
    print("-" * 40)
    print("1. Run 'python app/app_final.py' to start the web dashboard")
    print("2. Open browser and navigate to http://127.0.0.1:5000")
    print("3. Explore the interactive dashboard and visualizations")
    print("4. Review AI-generated remediation recommendations")
    
    print("\n" + "=" * 70)
    print("DEMONSTRATION COMPLETE")
    print("=" * 70)

if __name__ == "__main__":
    main()