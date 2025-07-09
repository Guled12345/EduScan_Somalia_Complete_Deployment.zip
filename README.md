# EduScan Somalia - Learning Risk Assessment Application

## Overview
EduScan Somalia is a comprehensive learning risk assessment application designed to help educators identify and support students who may be at risk of learning difficulties. The application provides multilingual support (English, Somali, Arabic) and includes machine learning-based risk prediction.

## Features
- **Student Assessment**: Comprehensive risk evaluation using academic and behavioral metrics
- **Teacher Resources**: Educational materials and teaching strategies
- **Parent Tracker**: Daily observation logging for parents
- **Analytics**: Data visualization and progress tracking
- **Multilingual Support**: English, Somali, and Arabic languages

## Deployment Instructions

### Render Deployment
1. Upload all files to GitHub repository
2. Connect GitHub to Render
3. Deploy using the render.yaml configuration
4. Application will be available at your Render URL

### Local Development
```bash
pip install -r requirements.txt
streamlit run app.py
```

## File Structure
```
├── app.py                 # Main application
├── pages/                 # Additional pages
├── utils/                 # Utility functions
├── data/                  # ML models and data
├── .streamlit/           # Streamlit configuration
├── requirements.txt      # Python dependencies
├── runtime.txt          # Python version
├── render.yaml          # Render deployment config
└── README.md            # This file
```

## Technical Requirements
- Python 3.11.9
- Streamlit 1.28.1
- pandas 2.0.3
- numpy 1.24.3
- scikit-learn 1.3.0
- plotly 5.15.0

## Support
For technical support or questions, please contact the development team.