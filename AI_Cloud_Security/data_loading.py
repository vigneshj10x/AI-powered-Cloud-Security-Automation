import csv
import pickle

def load_dataset(file_path='dataset/cloud_security_data.csv'):
    """Load dataset from CSV file"""
    try:
        data = []
        with open(file_path, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                # Convert string values to appropriate types
                row['Public_Access'] = int(row['Public_Access'])
                row['Open_Ports'] = int(row['Open_Ports'])
                row['Anomaly_Score'] = float(row['Anomaly_Score'])
                row['Breach_Risk'] = int(row['Breach_Risk'])
                data.append(row)
        return data
    except FileNotFoundError:
        print("Dataset file not found!")
        return None

def load_trained_model(model_path='model/cloud_model.pkl'):
    try:
        with open(model_path, 'rb') as f:
            saved_data = pickle.load(f)
            model = saved_data['model']
            resource_mapping = saved_data['resource_mapping']
            privilege_mapping = saved_data['privilege_mapping']
        return model, resource_mapping, privilege_mapping
    except FileNotFoundError:
        print("Model file not found!")
        return None, None, None

def prepare_input_data(resource_config, resource_mapping, privilege_mapping):
    # Encode categorical features
    resource_type_encoded = resource_mapping[resource_config['Resource_Type']]
    privilege_encoded = privilege_mapping[resource_config['Privilege_Level']]
    
    # Create feature vector
    features = [[
        resource_type_encoded,
        resource_config['Public_Access'],
        resource_config['Open_Ports'],
        privilege_encoded,
        resource_config['Anomaly_Score']
    ]]
    
    return features