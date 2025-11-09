import pandas as pd
import numpy as np
import random
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns
import pickle
import os

def create_dataset():
    """Generate synthetic cloud security dataset"""
    print("Creating synthetic dataset...")
    
    np.random.seed(42)
    random.seed(42)
    
    data = []
    resource_types = ['S3', 'EC2', 'IAM']
    privilege_levels = ['Low', 'Medium', 'High']
    
    for i in range(1000):
        resource_id = f"R{i+1:03d}"
        resource_type = random.choice(resource_types)
        public_access = random.choice([0, 1])
        open_ports = random.randint(0, 100)
        privilege_level = random.choice(privilege_levels)
        
        # Calculate anomaly score based on risk factors
        anomaly_score = 0.0
        if public_access == 1:
            anomaly_score += 0.4
        if open_ports > 50:
            anomaly_score += 0.3
        if privilege_level == 'High':
            anomaly_score += 0.3
        elif privilege_level == 'Medium':
            anomaly_score += 0.15
            
        anomaly_score = min(anomaly_score + random.uniform(-0.1, 0.1), 1.0)
        anomaly_score = max(anomaly_score, 0.0)
        
        # Determine breach risk
        breach_risk = 1 if anomaly_score > 0.5 else 0
        
        data.append([resource_id, resource_type, public_access, open_ports, 
                    privilege_level, round(anomaly_score, 3), breach_risk])
    
    df = pd.DataFrame(data, columns=['Resource_ID', 'Resource_Type', 'Public_Access', 
                                   'Open_Ports', 'Privilege_Level', 'Anomaly_Score', 'Breach_Risk'])
    
    # Save dataset
    os.makedirs('dataset', exist_ok=True)
    df.to_csv('dataset/cloud_security_data.csv', index=False)
    print(f"Dataset created with {len(df)} records")
    return df

def train_model(df):
    """Train ML model for anomaly detection"""
    print("Training ML model...")
    
    # Preprocessing
    le_resource = LabelEncoder()
    le_privilege = LabelEncoder()
    
    df_encoded = df.copy()
    df_encoded['Resource_Type'] = le_resource.fit_transform(df['Resource_Type'])
    df_encoded['Privilege_Level'] = le_privilege.fit_transform(df['Privilege_Level'])
    
    # Features and target
    X = df_encoded[['Resource_Type', 'Public_Access', 'Open_Ports', 'Privilege_Level', 'Anomaly_Score']]
    y = df_encoded['Breach_Risk']
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Train model
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    # Evaluate
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    
    print(f"Model Accuracy: {accuracy:.3f}")
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred))
    
    # Confusion Matrix
    plt.figure(figsize=(8, 6))
    cm = confusion_matrix(y_test, y_pred)
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
    plt.title('Confusion Matrix')
    plt.ylabel('Actual')
    plt.xlabel('Predicted')
    plt.tight_layout()
    plt.savefig('model/confusion_matrix.png')
    plt.show()
    
    # Save model and encoders
    os.makedirs('model', exist_ok=True)
    with open('model/cloud_model.pkl', 'wb') as f:
        pickle.dump({
            'model': model,
            'resource_encoder': le_resource,
            'privilege_encoder': le_privilege
        }, f)
    
    print("Model saved successfully!")
    return model, le_resource, le_privilege

def scan_cloud_resources(resource_config):
    """Scan and predict risk for cloud resources"""
    try:
        with open('model/cloud_model.pkl', 'rb') as f:
            saved_data = pickle.load(f)
            model = saved_data['model']
            le_resource = saved_data['resource_encoder']
            le_privilege = saved_data['privilege_encoder']
    except:
        print("Model not found. Please train the model first.")
        return None
    
    # Encode input
    resource_type_encoded = le_resource.transform([resource_config['Resource_Type']])[0]
    privilege_encoded = le_privilege.transform([resource_config['Privilege_Level']])[0]
    
    # Prepare features
    features = [[
        resource_type_encoded,
        resource_config['Public_Access'],
        resource_config['Open_Ports'],
        privilege_encoded,
        resource_config['Anomaly_Score']
    ]]
    
    # Predict
    prediction = model.predict(features)[0]
    probability = model.predict_proba(features)[0]
    
    result = {
        'prediction': 'Risky' if prediction == 1 else 'Secure',
        'confidence': max(probability),
        'recommendations': get_recommendations(resource_config, prediction)
    }
    
    return result

def get_recommendations(config, prediction):
    """Generate remediation recommendations"""
    recommendations = []
    
    if prediction == 1:  # Risky
        if config['Public_Access'] == 1:
            recommendations.append("Restrict public access to resource")
        if config['Open_Ports'] > 50:
            recommendations.append("Close unused ports and implement port restrictions")
        if config['Privilege_Level'] == 'High':
            recommendations.append("Reduce IAM privilege level to minimum required")
        if config['Anomaly_Score'] > 0.7:
            recommendations.append("Immediate security review required")
    else:
        recommendations.append("Resource configuration appears secure")
    
    return recommendations

if __name__ == "__main__":
    # Create dataset
    df = create_dataset()
    
    # Train model
    model, le_resource, le_privilege = train_model(df)
    
    # Test prediction
    test_config = {
        'Resource_Type': 'S3',
        'Public_Access': 1,
        'Open_Ports': 80,
        'Privilege_Level': 'High',
        'Anomaly_Score': 0.8
    }
    
    result = scan_cloud_resources(test_config)
    print(f"\nTest Prediction: {result}")