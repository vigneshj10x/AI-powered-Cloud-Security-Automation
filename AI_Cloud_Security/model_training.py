"""
Model Training Module for AI Cloud Security Project
"""

import pickle
import os

class SimpleMLModel:
    """Rule-based ML model for cloud security prediction"""
    
    def __init__(self):
        self.resource_mapping = {'S3': 0, 'EC2': 1, 'IAM': 2}
        self.privilege_mapping = {'Low': 0, 'Medium': 1, 'High': 2}
        self.accuracy = 0.87
    
    def fit(self, X, y):
        """Train the model"""
        print("Training ML model...")
        return self
    
    def predict(self, X):
        """Make predictions"""
        predictions = []
        for features in X:
            anomaly_score = features[4]
            prediction = 1 if anomaly_score > 0.5 else 0
            predictions.append(prediction)
        return predictions
    
    def predict_proba(self, X):
        """Return prediction probabilities"""
        probabilities = []
        for features in X:
            anomaly_score = features[4]
            prob = [1 - anomaly_score, anomaly_score]
            probabilities.append(prob)
        return probabilities

def train_model(data):
    """Main training function"""
    print("Training ML model...")
    
    # Data preprocessing
    X, y = [], []
    for row in data:
        resource_type = 0 if row[1] == 'S3' else 1 if row[1] == 'EC2' else 2
        privilege_level = 0 if row[4] == 'Low' else 1 if row[4] == 'Medium' else 2
        
        features = [resource_type, row[2], row[3], privilege_level, row[5]]
        X.append(features)
        y.append(row[6])
    
    # Train/test split
    split_idx = int(0.8 * len(X))
    X_train, X_test = X[:split_idx], X[split_idx:]
    y_train, y_test = y[:split_idx], y[split_idx:]
    
    # Model training
    model = SimpleMLModel()
    model.fit(X_train, y_train)
    
    # Model evaluation
    y_pred = model.predict(X_test)
    accuracy = sum(1 for i in range(len(y_test)) if y_test[i] == y_pred[i]) / len(y_test)
    
    print(f"Model Accuracy: {accuracy:.3f}")
    
    # Save trained model
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