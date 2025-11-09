"""
Utility functions for model operations
"""

class SimpleMLModel:
    """Simple rule-based model for cloud security prediction"""
    
    def __init__(self):
        self.resource_mapping = {'S3': 0, 'EC2': 1, 'IAM': 2}
        self.privilege_mapping = {'Low': 0, 'Medium': 1, 'High': 2}
        self.accuracy = 0.87  # Simulated accuracy
    
    def fit(self, X, y):
        """Simulate model training"""
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

def scan_cloud_resources(resource_config):
    """Scan and predict risk for cloud resources"""
    try:
        import pickle
        with open('model/cloud_model.pkl', 'rb') as f:
            saved_data = pickle.load(f)
            model = saved_data['model']
            resource_mapping = saved_data['resource_mapping']
            privilege_mapping = saved_data['privilege_mapping']
    except:
        # Fallback to creating new model
        model = SimpleMLModel()
        resource_mapping = model.resource_mapping
        privilege_mapping = model.privilege_mapping
    
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