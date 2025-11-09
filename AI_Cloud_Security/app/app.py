from flask import Flask, render_template, request, jsonify
import pandas as pd
import pickle
import json
import plotly
import plotly.graph_objs as go
import plotly.express as px
import os
import sys

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from main import scan_cloud_resources

app = Flask(__name__)

def load_data():
    """Load dataset and model predictions"""
    try:
        df = pd.read_csv('../dataset/cloud_security_data.csv')
        return df
    except:
        return None

def create_visualizations(df):
    """Create interactive visualizations"""
    if df is None:
        return {}, {}, {}
    
    # Risk distribution by resource type
    risk_by_type = df.groupby(['Resource_Type', 'Breach_Risk']).size().unstack(fill_value=0)
    fig1 = px.bar(risk_by_type, title="Risk Distribution by Resource Type")
    graph1JSON = json.dumps(fig1, cls=plotly.utils.PlotlyJSONEncoder)
    
    # Anomaly score distribution
    fig2 = px.histogram(df, x='Anomaly_Score', color='Breach_Risk', 
                       title="Anomaly Score Distribution")
    graph2JSON = json.dumps(fig2, cls=plotly.utils.PlotlyJSONEncoder)
    
    # Risk pie chart
    risk_counts = df['Breach_Risk'].value_counts()
    fig3 = px.pie(values=risk_counts.values, names=['Secure', 'Risky'], 
                  title="Overall Risk Distribution")
    graph3JSON = json.dumps(fig3, cls=plotly.utils.PlotlyJSONEncoder)
    
    return graph1JSON, graph2JSON, graph3JSON

@app.route('/')
def index():
    """Home page"""
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    """Dashboard with visualizations"""
    df = load_data()
    if df is not None:
        graph1, graph2, graph3 = create_visualizations(df)
        stats = {
            'total_resources': len(df),
            'risky_resources': len(df[df['Breach_Risk'] == 1]),
            'secure_resources': len(df[df['Breach_Risk'] == 0]),
            'risk_percentage': round((len(df[df['Breach_Risk'] == 1]) / len(df)) * 100, 1)
        }
        return render_template('dashboard.html', graph1=graph1, graph2=graph2, 
                             graph3=graph3, stats=stats)
    else:
        return render_template('dashboard.html', error="Dataset not found")

@app.route('/results')
def results():
    """Scan results page"""
    df = load_data()
    if df is not None:
        # Show sample of results
        sample_data = df.head(20).to_dict('records')
        return render_template('results.html', data=sample_data)
    else:
        return render_template('results.html', error="Dataset not found")

@app.route('/remediation')
def remediation():
    """Remediation recommendations page"""
    df = load_data()
    if df is not None:
        risky_resources = df[df['Breach_Risk'] == 1].head(10)
        recommendations = []
        
        for _, row in risky_resources.iterrows():
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