from flask import Flask, render_template, request, jsonify
import csv
import json
import os
import sys

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from main_simple import scan_cloud_resources

app = Flask(__name__)

def load_data():
    """Load dataset"""
    try:
        data = []
        with open('../dataset/cloud_security_data.csv', 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                row['Public_Access'] = int(row['Public_Access'])
                row['Open_Ports'] = int(row['Open_Ports'])
                row['Anomaly_Score'] = float(row['Anomaly_Score'])
                row['Breach_Risk'] = int(row['Breach_Risk'])
                data.append(row)
        return data
    except:
        return None

def create_simple_charts(data):
    """Create simple chart data"""
    if not data:
        return {}, {}, {}
    
    # Risk by resource type
    risk_by_type = {}
    for row in data:
        resource_type = row['Resource_Type']
        risk = row['Breach_Risk']
        if resource_type not in risk_by_type:
            risk_by_type[resource_type] = {'secure': 0, 'risky': 0}
        if risk == 1:
            risk_by_type[resource_type]['risky'] += 1
        else:
            risk_by_type[resource_type]['secure'] += 1
    
    # Overall risk distribution
    total_risky = sum(1 for row in data if row['Breach_Risk'] == 1)
    total_secure = len(data) - total_risky
    
    # Anomaly score ranges
    score_ranges = {'0.0-0.2': 0, '0.2-0.4': 0, '0.4-0.6': 0, '0.6-0.8': 0, '0.8-1.0': 0}
    for row in data:
        score = row['Anomaly_Score']
        if score <= 0.2:
            score_ranges['0.0-0.2'] += 1
        elif score <= 0.4:
            score_ranges['0.2-0.4'] += 1
        elif score <= 0.6:
            score_ranges['0.4-0.6'] += 1
        elif score <= 0.8:
            score_ranges['0.6-0.8'] += 1
        else:
            score_ranges['0.8-1.0'] += 1
    
    return risk_by_type, {'secure': total_secure, 'risky': total_risky}, score_ranges

@app.route('/')
def index():
    """Home page"""
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    """Dashboard with visualizations"""
    data = load_data()
    if data:
        risk_by_type, overall_risk, score_ranges = create_simple_charts(data)
        stats = {
            'total_resources': len(data),
            'risky_resources': overall_risk['risky'],
            'secure_resources': overall_risk['secure'],
            'risk_percentage': round((overall_risk['risky'] / len(data)) * 100, 1)
        }
        return render_template('dashboard_simple.html', 
                             risk_by_type=risk_by_type,
                             overall_risk=overall_risk,
                             score_ranges=score_ranges,
                             stats=stats)
    else:
        return render_template('dashboard_simple.html', error="Dataset not found")

@app.route('/results')
def results():
    """Scan results page"""
    data = load_data()
    if data:
        # Show sample of results
        sample_data = data[:20]
        return render_template('results.html', data=sample_data)
    else:
        return render_template('results.html', error="Dataset not found")

@app.route('/remediation')
def remediation():
    """Remediation recommendations page"""
    data = load_data()
    if data:
        risky_resources = [row for row in data if row['Breach_Risk'] == 1][:10]
        recommendations = []
        
        for row in risky_resources:
            config = {
                'Resource_Type': row['Resource_Type'],
                'Public_Access': row['Public_Access'],
                'Open_Ports': row['Open_Ports'],
                'Privilege_Level': row['Privilege_Level'],
                'Anomaly_Score': row['Anomaly_Score']
            }
            
            result = scan_cloud_resources(config)
            if result:
                recommendations.append({
                    'resource_id': row['Resource_ID'],
                    'resource_type': row['Resource_Type'],
                    'risk_level': result['prediction'],
                    'confidence': round(result['confidence'], 3),
                    'recommendations': result['recommendations']
                })
        
        return render_template('remediation.html', recommendations=recommendations)
    else:
        return render_template('remediation.html', error="Dataset not found")

@app.route('/scan', methods=['POST'])
def scan_resource():
    """API endpoint for scanning individual resources"""
    try:
        data = request.json
        result = scan_cloud_resources(data)
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)