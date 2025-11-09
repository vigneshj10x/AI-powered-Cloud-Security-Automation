#!/usr/bin/env python3
"""
Test script to verify the AI Cloud Security system
"""

import os
import sys
import csv
import pickle

def test_dataset():
    """Test if dataset was created correctly"""
    print("🔍 Testing dataset...")
    
    if not os.path.exists('dataset/cloud_security_data.csv'):
        print("❌ Dataset file not found!")
        return False
    
    with open('dataset/cloud_security_data.csv', 'r') as f:
        reader = csv.reader(f)
        headers = next(reader)
        rows = list(reader)
    
    expected_headers = ['Resource_ID', 'Resource_Type', 'Public_Access', 
                       'Open_Ports', 'Privilege_Level', 'Anomaly_Score', 'Breach_Risk']
    
    if headers != expected_headers:
        print(f"❌ Headers mismatch! Expected: {expected_headers}, Got: {headers}")
        return False
    
    if len(rows) != 1000:
        print(f"❌ Expected 1000 rows, got {len(rows)}")
        return False
    
    print(f"✅ Dataset OK: {len(rows)} rows with correct headers")
    return True

def test_model():
    """Test if model was trained and saved correctly"""
    print("🔍 Testing model...")
    
    if not os.path.exists('model/cloud_model.pkl'):
        print("❌ Model file not found!")
        return False
    
    try:
        with open('model/cloud_model.pkl', 'rb') as f:
            model_data = pickle.load(f)
        
        required_keys = ['model', 'resource_mapping', 'privilege_mapping']
        for key in required_keys:
            if key not in model_data:
                print(f"❌ Missing key in model: {key}")
                return False
        
        print("✅ Model OK: All components present")
        return True
    except Exception as e:
        print(f"❌ Error loading model: {e}")
        return False

def test_prediction():
    """Test model prediction functionality"""
    print("🔍 Testing prediction...")
    
    try:
        sys.path.append('.')
        from main_simple import scan_cloud_resources
        
        test_config = {
            'Resource_Type': 'S3',
            'Public_Access': 1,
            'Open_Ports': 80,
            'Privilege_Level': 'High',
            'Anomaly_Score': 0.8
        }
        
        result = scan_cloud_resources(test_config)
        
        if result is None:
            print("❌ Prediction returned None")
            return False
        
        required_keys = ['prediction', 'confidence', 'recommendations']
        for key in required_keys:
            if key not in result:
                print(f"❌ Missing key in result: {key}")
                return False
        
        print(f"✅ Prediction OK: {result['prediction']} (confidence: {result['confidence']:.3f})")
        return True
    except Exception as e:
        print(f"❌ Error in prediction: {e}")
        return False

def main():
    print("=" * 60)
    print("🧪 AI Cloud Security System Test")
    print("=" * 60)
    
    tests = [
        ("Dataset", test_dataset),
        ("Model", test_model),
        ("Prediction", test_prediction)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n📋 Running {test_name} test...")
        if test_func():
            passed += 1
        print()
    
    print("=" * 60)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! System is ready to use.")
        print("🚀 Run 'python run_app.py' to start the web application")
    else:
        print("⚠️  Some tests failed. Please check the issues above.")
    
    print("=" * 60)

if __name__ == "__main__":
    main()