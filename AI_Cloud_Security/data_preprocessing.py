
def preprocess_data(raw_data):
    
    X = []
    y = []
    
    # Label encoding mappings
    resource_mapping = {'S3': 0, 'EC2': 1, 'IAM': 2}
    privilege_mapping = {'Low': 0, 'Medium': 1, 'High': 2}
    
    for row in raw_data:
        # Encode categorical features
        resource_type_encoded = resource_mapping[row[1]]  # Resource_Type
        privilege_encoded = privilege_mapping[row[4]]     # Privilege_Level
        
        # Create feature vector
        features = [
            resource_type_encoded,  # Encoded resource type
            row[2],                # Public_Access (0/1)
            row[3],                # Open_Ports (numeric)
            privilege_encoded,     # Encoded privilege level
            row[5]                 # Anomaly_Score (float)
        ]
        
        X.append(features)
        y.append(row[6])  # Breach_Risk (target)
    
    return X, y

def split_data(X, y, test_size=0.2):
    
    split_idx = int((1 - test_size) * len(X))
    
    X_train = X[:split_idx]
    X_test = X[split_idx:]
    y_train = y[:split_idx]
    y_test = y[split_idx:]
    
    return X_train, X_test, y_train, y_test

def calculate_anomaly_score(public_access, open_ports, privilege_level):
    
    score = 0.0
    
    # Public access increases risk
    if public_access == 1:
        score += 0.4
    
    # Many open ports increase risk
    if open_ports > 50:
        score += 0.3
    
    # High privileges increase risk
    if privilege_level == 'High':
        score += 0.3
    elif privilege_level == 'Medium':
        score += 0.15
    
    # Add random noise and normalize
    import random
    score = min(score + random.uniform(-0.1, 0.1), 1.0)
    score = max(score, 0.0)
    
    return round(score, 3)

def encode_features(resource_config):
    
    resource_mapping = {'S3': 0, 'EC2': 1, 'IAM': 2}
    privilege_mapping = {'Low': 0, 'Medium': 1, 'High': 2}
    
    encoded_features = [
        resource_mapping[resource_config['Resource_Type']],
        resource_config['Public_Access'],
        resource_config['Open_Ports'],
        privilege_mapping[resource_config['Privilege_Level']],
        resource_config['Anomaly_Score']
    ]
    
    return encoded_features