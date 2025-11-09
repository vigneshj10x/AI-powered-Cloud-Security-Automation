import csv
import random
import json
import os
import pickle
from collections import Counter

def create_dataset():
    """Generate synthetic cloud security dataset"""
    print("Creating synthetic dataset...")
    
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
    
    # Save dataset
    os.makedirs('dataset', exist_ok=True)
    with open('dataset/cloud_security_data.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Resource_ID', 'Resource_Type', 'Public_Access', 
                        'Open_Ports', 'Privilege_Level', 'Anomaly_Score', 'Breach_Risk'])
        writer.writerows(data)
    
    print(f"Dataset created with {len(data)} records")
    return data

class SimpleMLModel:
    """Simple rule-based model for cloud security prediction"""
    
    def __init__(self):
        self.resource_mapping = {'S3': 0, 'EC2': 1, 'IAM': 2}
        self.privilege_mapping = {'Low': 0, 'Medium': 1, 'High': 2}
        self.accuracy = 0.87  # Simulated accuracy
    
    def fit(self, X, y):
        """Simulate model training"""
        print("Training simple ML model...")
        # Rule-based logic: high risk if anomaly_score > 0.5
        return self
    
    def predict(self, X):
        """Predict based on simple rules"""
        predictions = []
        for features in X:
            anomaly_score = features[4]  # Anomaly score is at index 4
            prediction = 1 if anomaly_score > 0.5 else 0
            predictions.append(prediction)
        return predictions
    
    def predict_proba(self, X):
        """Return prediction probabilities"""
        probabilities = []
        for features in X:
            anomaly_score = features[4]
            if anomaly_score > 0.5:
                prob = [1 - anomaly_score, anomaly_score]
            else:
                prob = [1 - anomaly_score, anomaly_score]
            probabilities.append(prob)
        return probabilities

def train_model(data):
    """Train simple ML model"""
    print("Training ML model...")
    
    # Prepare data
    X = []
    y = []
    
    for row in data:
        resource_type = 0 if row[1] == 'S3' else 1 if row[1] == 'EC2' else 2
        privilege_level = 0 if row[4] == 'Low' else 1 if row[4] == 'Medium' else 2
        
        features = [resource_type, row[2], row[3], privilege_level, row[5]]
        X.append(features)
        y.append(row[6])
    
    # Split data (80/20)
    split_idx = int(0.8 * len(X))
    X_train, X_test = X[:split_idx], X[split_idx:]
    y_train, y_test = y[:split_idx], y[split_idx:]
    
    # Train model
    model = SimpleMLModel()
    model.fit(X_train, y_train)
    
    # Evaluate
    y_pred = model.predict(X_test)
    correct = sum(1 for i in range(len(y_test)) if y_test[i] == y_pred[i])
    accuracy = correct / len(y_test)
    
    print(f"Model Accuracy: {accuracy:.3f}")
    
    # Calculate metrics
    tp = sum(1 for i in range(len(y_test)) if y_test[i] == 1 and y_pred[i] == 1)
    fp = sum(1 for i in range(len(y_test)) if y_test[i] == 0 and y_pred[i] == 1)
    fn = sum(1 for i in range(len(y_test)) if y_test[i] == 1 and y_pred[i] == 0)
    
    precision = tp / (tp + fp) if (tp + fp) > 0 else 0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0
    f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
    
    print(f"Precision: {precision:.3f}")
    print(f"Recall: {recall:.3f}")
    print(f"F1-Score: {f1:.3f}")
    
    # Save model
    os.makedirs('model', exist_ok=True)
    model_data = {
        'model': model,
        'resource_mapping': model.resource_mapping,
        'privilege_mapping': model.privilege_mapping
    }
    
    with open('model/cloud_model.pkl', 'wb') as f:
        pickle.dump(model_data, f)
    
    print("Model saved successfully!")
    return model

def scan_cloud_resources(resource_config):
    """Scan and predict risk for cloud resources"""
    try:
        with open('model/cloud_model.pkl', 'rb') as f:
            saved_data = pickle.load(f)
            model = saved_data['model']
            resource_mapping = saved_data['resource_mapping']
            privilege_mapping = saved_data['privilege_mapping']
    except:
        print("Model not found. Please train the model first.")
        return None
    
    # Encode input
    resource_type_encoded = resource_mapping[resource_config['Resource_Type']]
    privilege_encoded = privilege_mapping[resource_config['Privilege_Level']]
    
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
    data = create_dataset()
    
    # Train model
    model = train_model(data)
    
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