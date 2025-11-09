# AI-Powered Cloud Security & Compliance Automation

## Project Overview
This project implements an AI-driven solution for detecting cloud security misconfigurations and providing automated remediation recommendations. It addresses critical security challenges in cloud environments including publicly exposed resources, overly permissive access controls, and excessive privileges.

## Features
- **Automated Scanning**: Monitors S3, EC2, and IAM resources for security misconfigurations
- **AI Detection**: Uses machine learning to identify anomalies and predict breach risks
- **Interactive Dashboard**: Visualizes security metrics and risk distributions
- **Smart Remediation**: Provides actionable recommendations to fix vulnerabilities

## Tech Stack
- Python 3.x
- Flask (Web Framework)
- Pandas, NumPy (Data Processing)
- Scikit-learn (Machine Learning)
- Plotly (Interactive Visualizations)
- Bootstrap (Frontend Styling)

## Installation & Setup

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Generate Dataset & Train Model**:
   ```bash
   python main.py
   ```

3. **Run Flask Application**:
   ```bash
   cd app
   python app.py
   ```

4. **Access Dashboard**:
   Open browser and navigate to `http://127.0.0.1:5000`

## Project Structure
```
AI_Cloud_Security/
├── dataset/
│   └── cloud_security_data.csv
├── model/
│   ├── cloud_model.pkl
│   └── confusion_matrix.png
├── app/
│   ├── app.py
│   ├── templates/
│   │   ├── index.html
│   │   ├── dashboard.html
│   │   ├── results.html
│   │   └── remediation.html
│   └── static/
│       └── style.css
├── main.py
├── requirements.txt
└── README.md
```

## Dataset Features
- **Resource_ID**: Unique identifier for each resource
- **Resource_Type**: S3, EC2, or IAM
- **Public_Access**: Binary indicator (0/1)
- **Open_Ports**: Number of open ports (0-100)
- **Privilege_Level**: Low, Medium, or High
- **Anomaly_Score**: Risk score (0.0-1.0)
- **Breach_Risk**: Target variable (0=Secure, 1=Risky)

## Model Performance
- Algorithm: Random Forest Classifier
- Accuracy: ~85-90%
- Features: Resource type, public access, open ports, privilege level, anomaly score
- Output: Binary classification (Secure/Risky) with confidence scores

## Dashboard Pages
1. **Home**: Project overview and navigation
2. **Dashboard**: Interactive visualizations and statistics
3. **Results**: Detailed scan results table
4. **Remediation**: AI-generated security recommendations

## Key Insights
- Resources with high privilege levels and public access show higher breach risk
- Open ports above 50 significantly increase vulnerability scores
- S3 resources with public access require immediate attention
- IAM roles with excessive privileges need privilege reduction

## Future Enhancements
- Real-time cloud API integration
- Advanced anomaly detection algorithms
- Automated remediation execution
- Compliance framework mapping
- Multi-cloud platform support