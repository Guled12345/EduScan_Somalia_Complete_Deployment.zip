import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import os
import json
from utils.data_utils import load_student_data, load_parent_observations, save_prediction_data, save_parent_observation
from utils.model_utils import load_model, make_prediction
from utils.icon_utils import *

# Set page config for faster loading
st.set_page_config(
    page_title="EduScan Somalia",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

def get_text(key, language=None):
    """Get localized text based on language setting"""
    # Get language from session state or settings if not provided
    if language is None:
        language = st.session_state.get('app_language')
        if language is None:
            settings = load_app_settings()
            language = settings.get('language', 'English')
            st.session_state['app_language'] = language
    translations = {
        'English': {
            # Navigation
            'dashboard': 'Dashboard',
            'assessment': 'Assessment', 
            'resources': 'Resources',
            'tracker': 'Tracker',
            'analytics': 'Analytics',
            'settings': 'Settings',
            
            # Header
            'app_title': 'EduScan Somalia',
            'app_subtitle': 'Professional Learning Assessment Application',
            'online_mode': 'Online Mode',
            'offline_mode': 'Offline Mode',
            
            # Dashboard
            'system_overview': 'System Overview',
            'total_students': 'Total Students',
            'on_track': 'On Track',
            'at_risk': 'At Risk', 
            'intervention': 'Intervention',
            'class_performance': 'Class Performance Overview',
            'recent_assessments': 'Recent Assessments',
            'students_needing_attention': 'Students Needing Attention',
            'quick_actions': 'Quick Actions',
            'academic_performance_by_subject': 'Academic Performance by Subject',
            'student_risk_distribution': 'Student Risk Distribution',
            'average_subject_scores': 'Average Subject Scores',
            'subjects': 'Subjects',
            'average_score': 'Average Score (%)',
            'student_risk_overview': 'Student Risk Assessment Overview',
            'recent_assessment_results': 'Recent Assessment Results',
            'monthly_trends': 'Monthly Assessment Trends',
            'student_name': 'Student Name',
            'grade': 'Grade',
            'math_score': 'Math Score',
            'reading_score': 'Reading Score',
            'risk_level': 'Risk Level',
            'assessment_date': 'Assessment Date',
            'monthly_performance_trends': 'Average Subject Performance Trends',
            'month': 'Month',
            'mathematics': 'Mathematics',
            'reading': 'Reading',
            
            # Assessment
            'learning_risk_assessment': 'Learning Risk Assessment',
            'student_information': 'Student Information',
            'student_name': 'Student Name',
            'grade_level': 'Grade Level',
            'academic_performance': 'Academic Performance',
            'math_score': 'Mathematics Score (%)',
            'reading_score': 'Reading Score (%)',
            'writing_score': 'Writing Score (%)',
            'attendance': 'Attendance (%)',
            'behavioral_assessment': 'Behavioral Assessment',
            'behavior_rating': 'Behavior Rating',
            'literacy_level': 'Literacy Level',
            'analyze_learning_risk': 'Analyze Learning Risk',
            'assessment_results': 'Assessment Results',
            'performance_profile': 'Performance Profile',
            'recommendations': 'Recommendations',
            
            # Parent Tracker
            'daily_observation_log': 'Daily Observation Log',
            'child_name': "Child's Name",
            'observation_date': 'Observation Date',
            'academic_observations': 'Academic Observations',
            'homework_completion': 'Homework Completion (%)',
            'reading_time': 'Reading Time (minutes)',
            'focus_level': 'Focus Level',
            'subjects_struggled': 'Subjects Struggled With',
            'behavioral_observations': 'Behavioral Observations',
            'mood_rating': 'Mood Rating',
            'sleep_hours': 'Sleep Hours',
            'energy_level': 'Energy Level',
            'learning_wins': 'Learning Wins Today',
            'challenges_faced': 'Challenges Faced',
            'save_observation': 'Save Observation',
            'progress_insights': 'Progress Insights',
            
            # Risk Levels
            'low_risk': 'Low Risk',
            'medium_risk': 'Medium Risk', 
            'high_risk': 'High Risk',
            
            # Common
            'excellent': 'Excellent',
            'good': 'Good',
            'average': 'Average',
            'below_average': 'Below Average',
            'poor': 'Poor',
            'low': 'Low',
            'medium': 'Medium',
            'high': 'High',
            'reset_app': 'Reset Application',
            'language': 'Language',
            'theme': 'Theme',
            'save_settings': 'Save Settings'
        },
        'Somali': {
            # Navigation
            'dashboard': 'Xarunta Xogta',
            'assessment': 'Qiimayn',
            'resources': 'Agabka',
            'tracker': 'Dabagal',
            'analytics': 'Falanqayn',
            'settings': 'Dejinta',
            
            # Header
            'app_title': 'EduScan Somalia',
            'app_subtitle': 'Barnaamijka Qiimaynta Barashada Xirfadlayaasha',
            'online_mode': 'Hab Toos ah',
            'offline_mode': 'Hab Offline ah',
            
            # Dashboard
            'system_overview': 'Guud ahaan Nidaamka',
            'total_students': 'Wadarta Ardayda',
            'on_track': 'Ku Socdaan',
            'at_risk': 'Khatar ku jira',
            'intervention': 'Faragelin',
            'class_performance': 'Guud ahaan Fasalka',
            'recent_assessments': 'Qiimaynta Dhowaan',
            'students_needing_attention': 'Ardayda u baahan Feejignaan',
            'quick_actions': 'Tallaabooyin Degdeg ah',
            'academic_performance_by_subject': 'Waxqabadka Tacliinta Maadooyinka',
            'student_risk_distribution': 'Qaybinta Khatarta Ardayda',
            'average_subject_scores': 'Celceliska Dhibcaha Maadooyinka',
            'subjects': 'Maadooyinka',
            'average_score': 'Celceliska Dhibcaha (%)',
            'student_risk_overview': 'Guud ahaan Qiimaynta Khatarta Ardayda',
            'recent_assessment_results': 'Natiijada Qiimaynta Dhowaan',
            'monthly_trends': 'Isbeddelka Qiimaynta Bishii',
            'student_name': 'Magaca Ardayga',
            'grade': 'Fasalka',
            'math_score': 'Dhibcaha Xisaabta',
            'reading_score': 'Dhibcaha Akhriska',
            'risk_level': 'Heerka Khatarta',
            'assessment_date': 'Taariikhda Qiimaynta',
            'monthly_performance_trends': 'Celceliska Isbeddelka Waxqabadka Maadooyinka',
            'month': 'Bisha',
            'mathematics': 'Xisaabta',
            'reading': 'Akhris',
            
            # Assessment
            'learning_risk_assessment': 'Qiimaynta Khatarta Barashada',
            'student_information': 'Macluumaadka Ardayga',
            'student_name': 'Magaca Ardayga',
            'grade_level': 'Heerka Fasalka',
            'academic_performance': 'Waxqabadka Tacliinta',
            'math_score': 'Dhibcaha Xisaabta (%)',
            'reading_score': 'Dhibcaha Akhriska (%)',
            'writing_score': 'Dhibcaha Qorista (%)',
            'attendance': 'Soo Gaadhitaanka (%)',
            'behavioral_assessment': 'Qiimaynta Dhaqanka',
            'behavior_rating': 'Qiimaynta Dhaqanka',
            'literacy_level': 'Heerka Aqrinta',
            'analyze_learning_risk': 'Falanqee Khatarta Barashada',
            'assessment_results': 'Natiijada Qiimaynta',
            'performance_profile': 'Astaanta Waxqabadka',
            'recommendations': 'Talooyinka',
            
            # Parent Tracker
            'daily_observation_log': 'Diiwaanka Indho-indhaynta Maalinta',
            'child_name': 'Magaca Ilmaha',
            'observation_date': 'Taariikhda Indho-indhaynta',
            'academic_observations': 'Indho-indhaynta Tacliinta',
            'homework_completion': 'Dhammaystirka Hawsha Guriga (%)',
            'reading_time': 'Waqtiga Akhriska (daqiiqado)',
            'focus_level': 'Heerka Diiradda',
            'subjects_struggled': 'Maadooyinka la Tacban yahay',
            'behavioral_observations': 'Indho-indhaynta Dhaqanka',
            'mood_rating': 'Qiimaynta Dareenka',
            'sleep_hours': 'Saacadaha Hurdada',
            'energy_level': 'Heerka Tamarta',
            'learning_wins': 'Guusha Barashada Maanta',
            'challenges_faced': 'Caqabadaha la Kulmay',
            'save_observation': 'Kaydi Indho-indhaynta',
            'progress_insights': 'Aragtiyo Horumarka',
            
            # Risk Levels  
            'low_risk': 'Khatar Yar',
            'medium_risk': 'Khatar Dhexdhexaad ah',
            'high_risk': 'Khatar Weyn',
            
            # Common
            'excellent': 'Aad u Fiican',
            'good': 'Fiican', 
            'average': 'Celcelis ah',
            'below_average': 'Ka hooseeya Celceliska',
            'poor': 'Liita',
            'low': 'Hoose',
            'medium': 'Dhexdhexaad',
            'high': 'Sare',
            'reset_app': 'Dib u Bilow Barnaamijka',
            'language': 'Luqadda',
            'theme': 'Qaabka',
            'save_settings': 'Kaydi Dejinta'
        },
        'Arabic': {
            # Navigation
            'dashboard': 'لوحة التحكم',
            'assessment': 'التقييم',
            'resources': 'الموارد',
            'tracker': 'المتتبع',
            'analytics': 'التحليلات',
            'settings': 'الإعدادات',
            
            # Header
            'app_title': 'EduScan Somalia',
            'app_subtitle': 'تطبيق التقييم التعليمي المهني',
            'online_mode': 'الوضع المتصل',
            'offline_mode': 'الوضع غير المتصل',
            
            # Dashboard
            'system_overview': 'نظرة عامة على النظام',
            'total_students': 'إجمالي الطلاب',
            'on_track': 'في المسار الصحيح',
            'at_risk': 'في خطر',
            'intervention': 'تدخل',
            'class_performance': 'أداء الصف العام',
            'recent_assessments': 'التقييمات الأخيرة',
            'students_needing_attention': 'الطلاب بحاجة للانتباه',
            'quick_actions': 'إجراءات سريعة',
            'academic_performance_by_subject': 'الأداء الأكاديمي حسب المادة',
            'student_risk_distribution': 'توزيع مخاطر الطلاب',
            'average_subject_scores': 'متوسط درجات المواد',
            'subjects': 'المواد',
            'average_score': 'متوسط الدرجات (%)',
            'student_risk_overview': 'نظرة عامة على تقييم مخاطر الطلاب',
            'recent_assessment_results': 'نتائج التقييمات الأخيرة',
            'monthly_trends': 'اتجاهات التقييم الشهرية',
            'student_name': 'اسم الطالب',
            'grade': 'الصف',
            'math_score': 'درجة الرياضيات',
            'reading_score': 'درجة القراءة',
            'risk_level': 'مستوى المخاطر',
            'assessment_date': 'تاريخ التقييم',
            'monthly_performance_trends': 'متوسط اتجاهات الأداء الشهرية',
            'month': 'الشهر',
            'mathematics': 'الرياضيات',
            'reading': 'القراءة',
            
            # Assessment
            'learning_risk_assessment': 'تقييم مخاطر التعلم',
            'student_information': 'معلومات الطالب',
            'student_name': 'اسم الطالب',
            'grade_level': 'مستوى الصف',
            'academic_performance': 'الأداء الأكاديمي',
            'math_score': 'درجة الرياضيات (%)',
            'reading_score': 'درجة القراءة (%)',
            'writing_score': 'درجة الكتابة (%)',
            'attendance': 'الحضور (%)',
            'behavioral_assessment': 'التقييم السلوكي',
            'behavior_rating': 'تقييم السلوك',
            'literacy_level': 'مستوى محو الأمية',
            'analyze_learning_risk': 'تحليل مخاطر التعلم',
            'assessment_results': 'نتائج التقييم',
            'performance_profile': 'ملف الأداء',
            'recommendations': 'التوصيات',
            
            # Parent Tracker
            'daily_observation_log': 'سجل الملاحظات اليومية',
            'child_name': 'اسم الطفل',
            'observation_date': 'تاريخ الملاحظة',
            'academic_observations': 'الملاحظات الأكاديمية',
            'homework_completion': 'إنجاز الواجبات المنزلية (%)',
            'reading_time': 'وقت القراءة (دقائق)',
            'focus_level': 'مستوى التركيز',
            'subjects_struggled': 'المواد التي يواجه صعوبة فيها',
            'behavioral_observations': 'الملاحظات السلوكية',
            'mood_rating': 'تقييم المزاج',
            'sleep_hours': 'ساعات النوم',
            'energy_level': 'مستوى الطاقة',
            'learning_wins': 'إنجازات التعلم اليوم',
            'challenges_faced': 'التحديات التي واجهها',
            'save_observation': 'حفظ الملاحظة',
            'progress_insights': 'رؤى التقدم',
            
            # Risk Levels
            'low_risk': 'خطر منخفض',
            'medium_risk': 'خطر متوسط',
            'high_risk': 'خطر عالي',
            
            # Common
            'excellent': 'ممتاز',
            'good': 'جيد',
            'average': 'متوسط',
            'below_average': 'أقل من المتوسط',
            'poor': 'ضعيف',
            'low': 'منخفض',
            'medium': 'متوسط',
            'high': 'عالي',
            'reset_app': 'إعادة تعيين التطبيق',
            'language': 'اللغة',
            'theme': 'المظهر',
            'save_settings': 'حفظ الإعدادات'
        }
    }
    
    return translations.get(language, translations['English']).get(key, key)

def get_recommendations(risk_level):
    """Get recommendations based on risk level"""
    recommendations = {
        'Low': [
            "Continue with current learning approach",
            "Maintain regular study schedule",
            "Encourage reading for pleasure",
            "Consider enrichment activities"
        ],
        'Medium': [
            "Provide additional support in weak areas",
            "Implement structured study time",
            "Monitor progress more closely",
            "Consider peer tutoring",
            "Use visual learning aids"
        ],
        'High': [
            "Immediate intervention required",
            "One-on-one tutoring recommended", 
            "Consult with learning specialist",
            "Implement individualized learning plan",
            "Regular progress monitoring",
            "Family support engagement"
        ]
    }
    return recommendations.get(risk_level, [])

def load_app_settings():
    """Load application settings from file"""
    settings_file = 'data/app_settings.json'
    default_settings = {
        'language': 'English',
        'theme': 'Modern',
        'offline_mode': False
    }
    
    try:
        if os.path.exists(settings_file):
            with open(settings_file, 'r', encoding='utf-8') as f:
                settings = json.load(f)
                # Validate theme setting
                valid_themes = ['Modern', 'Classic', 'Dark']
                if settings.get('theme') not in valid_themes:
                    settings['theme'] = 'Modern'
                return settings
    except:
        pass
    
    return default_settings

def save_app_settings(settings):
    """Save application settings to file"""
    settings_file = 'data/app_settings.json'
    os.makedirs('data', exist_ok=True)
    
    try:
        with open(settings_file, 'w', encoding='utf-8') as f:
            json.dump(settings, f, ensure_ascii=False, indent=2)
        return True
    except:
        return False

def apply_theme(theme):
    """Apply the selected theme to the application"""
    if theme == 'Modern':
        st.markdown("""
        <style>
        .stApp {
            background: linear-gradient(135deg, #ff7b00 0%, #ff5722 25%, #ff9800 50%, #ffab00 75%, #ffc107 100%);
            background-attachment: fixed;
            background-size: cover;
            background-repeat: no-repeat;
            font-family: 'Poppins', sans-serif;
            min-height: 100vh;
        }
        
        .main-header {
            background: linear-gradient(135deg, rgba(255,255,255,0.1) 0%, rgba(255,255,255,0.05) 100%);
            backdrop-filter: blur(20px);
            border: 1px solid rgba(255,255,255,0.2);
            border-radius: 20px;
            padding: 2rem;
            margin-bottom: 2rem;
            color: white;
            text-align: center;
            box-shadow: 0 8px 32px rgba(0,0,0,0.1);
        }
        
        .main-header h1 {
            font-size: 3rem;
            font-weight: 700;
            margin-bottom: 0.5rem;
            color: #000000;
            text-shadow: 2px 2px 4px rgba(255,255,255,0.3);
        }
        
        .main-header p {
            font-size: 1.2rem;
            opacity: 0.9;
            margin-bottom: 0;
        }
        
        .nav-button {
            background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255,255,255,0.2);
            border-radius: 15px;
            padding: 1rem 2rem;
            margin: 0.5rem;
            color: white;
            text-decoration: none;
            font-weight: 600;
            font-size: 1.1rem;
            transition: all 0.3s ease;
            display: inline-block;
            min-width: 150px;
            text-align: center;
            cursor: pointer;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        }
        
        .nav-button:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 25px rgba(0,0,0,0.2);
            background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
        }
        
        .nav-button.active {
            background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
            color: white;
            transform: translateY(-2px);
        }
        
        /* Force all Streamlit buttons to be blue */
        div[data-testid="stButton"] > button {
            background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%) !important;
            color: white !important;
            border: none !important;
            border-radius: 8px !important;
            font-weight: 600 !important;
            transition: all 0.3s ease !important;
        }
        
        div[data-testid="stButton"] > button:hover {
            background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%) !important;
            transform: translateY(-2px) !important;
            box-shadow: 0 4px 15px rgba(59, 130, 246, 0.3) !important;
        }
        
        .metric-card {
            background: linear-gradient(135deg, rgba(255,255,255,0.1) 0%, rgba(255,255,255,0.05) 100%);
            backdrop-filter: blur(15px);
            border: 1px solid rgba(255,255,255,0.2);
            border-radius: 15px;
            padding: 1.5rem;
            margin: 1rem 0;
            color: white;
            box-shadow: 0 8px 32px rgba(0,0,0,0.1);
            transition: all 0.3s ease;
        }
        
        .metric-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 15px 40px rgba(0,0,0,0.2);
        }
        
        .metric-value {
            font-size: 2.5rem;
            font-weight: 700;
            color: #2c3e50;
        }
        
        .metric-title {
            font-size: 1.1rem;
            opacity: 0.9;
            margin-bottom: 0.5rem;
        }
        
        .metric-desc {
            font-size: 0.9rem;
            opacity: 0.7;
        }
        
        .content-card {
            background: linear-gradient(135deg, rgba(255,255,255,0.95) 0%, rgba(255,255,255,0.9) 100%);
            backdrop-filter: blur(20px);
            border: 1px solid rgba(255,255,255,0.3);
            border-radius: 20px;
            padding: 2rem;
            margin: 1rem 0;
            box-shadow: 0 8px 32px rgba(0,0,0,0.1);
            color: #2c3e50;
        }
        
        .stSelectbox > div > div {
            background: linear-gradient(135deg, rgba(255,255,255,0.1) 0%, rgba(255,255,255,0.05) 100%);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255,255,255,0.2);
            border-radius: 10px;
            color: white;
        }
        
        .stButton > button {
            background: linear-gradient(135deg, #ffd700 0%, #ffed4a 100%);
            color: #2c3e50;
            border: none;
            border-radius: 10px;
            padding: 0.5rem 2rem;
            font-weight: 600;
            transition: all 0.3s ease;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        }
        
        .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 25px rgba(0,0,0,0.2);
        }
        
        .status-indicator {
            display: inline-block;
            width: 10px;
            height: 10px;
            border-radius: 50%;
            margin-right: 8px;
            animation: pulse 2s infinite;
        }
        
        .status-online {
            background-color: #10b981;
        }
        
        .status-offline {
            background-color: #f59e0b;
        }
        
        @keyframes pulse {
            0% { opacity: 1; }
            50% { opacity: 0.5; }
            100% { opacity: 1; }
        }
        
        .sidebar .sidebar-content {
            background: linear-gradient(135deg, rgba(255,255,255,0.1) 0%, rgba(255,255,255,0.05) 100%);
            backdrop-filter: blur(20px);
        }
        
        .student-image {
            border-radius: 15px;
            box-shadow: 0 8px 25px rgba(0,0,0,0.2);
            margin: 1rem 0;
            width: 100%;
            height: auto;
        }
        
        .success-story {
            background: linear-gradient(135deg, rgba(16, 185, 129, 0.1) 0%, rgba(16, 185, 129, 0.05) 100%);
            border-left: 4px solid #10b981;
            padding: 1rem;
            margin: 1rem 0;
            border-radius: 0 10px 10px 0;
        }
        
        .progress-indicator {
            background: linear-gradient(90deg, #10b981 0%, #34d399 100%);
            height: 8px;
            border-radius: 4px;
            margin: 1rem 0;
        }
        </style>
        """, unsafe_allow_html=True)

def check_offline_mode():
    """Check if application can work offline"""
    settings = load_app_settings()
    return settings.get('offline_mode', False)

def render_app_header():
    """Render professional desktop application header"""
    # Get language from session state first, then settings
    language = st.session_state.get('app_language')
    if language is None:
        settings = load_app_settings()
        language = settings.get('language', 'English')
        st.session_state['app_language'] = language
    offline_mode = check_offline_mode()
    
    status_class = "status-online" if not offline_mode else "status-offline"
    status_text = get_text('online_mode', language) if not offline_mode else get_text('offline_mode', language)
    
    st.markdown(f"""
    <div class="main-header">
        <h1>{get_text('app_title', language)}</h1>
        <p style="color: #000000; font-weight: 500;">{get_text('app_subtitle', language)}</p>
        <div style="margin-top: 1rem;">
            <span class="status-indicator {status_class}"></span>
            <span style="color: #000000; font-weight: 500;">{status_text}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_navigation():
    """Render desktop-style navigation tabs"""
    # Get language from session state first, then settings
    language = st.session_state.get('app_language')
    if language is None:
        settings = load_app_settings()
        language = settings.get('language', 'English')
        st.session_state['app_language'] = language
    
    # Initialize session state for navigation
    if 'current_page' not in st.session_state:
        st.session_state.current_page = 'dashboard'
    
    # Simplified navigation - only Dashboard and Settings
    col1, col2, col3, col4, col5, col6 = st.columns([2, 2, 2, 2, 2, 2])
    
    nav_options = [
        ('dashboard', get_dashboard_icon(), get_text('dashboard', language)),
        ('settings', get_settings_icon(), get_text('settings', language))
    ]
    
    # Center the navigation buttons
    with col2:
        if st.button(get_text('dashboard', language), key="nav_dashboard", type="primary"):
            st.session_state.current_page = 'dashboard'
            st.rerun()
    
    with col5:
        if st.button(get_text('settings', language), key="nav_settings", type="primary"):
            st.session_state.current_page = 'settings'
            st.rerun()

def create_metric_card(title, value, description, color="#3b82f6"):
    """Create a professional metric card"""
    return f"""
    <div class="metric-card">
        <div class="metric-title">{title}</div>
        <div class="metric-value" style="color: {color};">{value}</div>
        <div class="metric-desc">{description}</div>
    </div>
    """

def render_dashboard():
    """Render the main dashboard"""
    # Get language from session state first, then settings
    language = st.session_state.get('app_language')
    if language is None:
        settings = load_app_settings()
        language = settings.get('language', 'English')
        st.session_state['app_language'] = language
    
    st.markdown(f"""
    <div class="content-card">
        <h2 style="margin-top: 0; color: #1e293b; text-align: center;">{get_text('system_overview', language)}</h2>
    </div>
    """, unsafe_allow_html=True)
    
    # Metrics row
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label=get_text('total_students', language),
            value="342",
            delta="12 new this month"
        )
    
    with col2:
        st.metric(
            label=get_text('on_track', language), 
            value="267",
            delta="78% performing well"
        )
    
    with col3:
        st.metric(
            label=get_text('at_risk', language),
            value="52", 
            delta="15% need support"
        )
    
    with col4:
        st.metric(
            label=get_text('intervention', language),
            value="23",
            delta="7% urgent attention"
        )
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Performance Charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader(f"📊 {get_text('academic_performance_by_subject', language)}")
        # Create subject performance chart
        subjects = ['Mathematics', 'Reading', 'Writing', 'Science', 'Social Studies']
        scores = [78, 82, 75, 80, 77]
        
        fig = px.bar(
            x=subjects, 
            y=scores,
            title=get_text('average_subject_scores', language),
            color=scores,
            color_continuous_scale='Blues'
        )
        fig.update_layout(
            xaxis_title=get_text('subjects', language),
            yaxis_title=get_text('average_score', language),
            showlegend=False,
            height=400
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader(f"📈 {get_text('student_risk_distribution', language)}")
        # Create risk level pie chart
        risk_labels = [get_text('on_track', language), get_text('at_risk', language), get_text('intervention', language)]
        risk_values = [267, 52, 23]
        risk_colors = ['#10b981', '#f8f9fa', '#ef4444']
        
        fig = go.Figure(data=[go.Pie(
            labels=risk_labels, 
            values=risk_values,
            hole=0.4,
            marker_colors=risk_colors,
            marker_line=dict(color='#000000', width=2)
        )])
        fig.update_layout(
            title=get_text('student_risk_overview', language),
            height=400
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Recent Assessment Data
    st.subheader(f"📋 {get_text('recent_assessment_results', language)}")
    
    # Create sample assessment data with translated headers
    assessment_data = pd.DataFrame({
        get_text('student_name', language): ['Ahmed Hassan', 'Fatima Ali', 'Omar Mohamed', 'Sahra Abdi', 'Yusuf Ibrahim'],
        get_text('grade', language): ['Grade 6', 'Grade 5', 'Grade 7', 'Grade 6', 'Grade 5'],
        get_text('math_score', language): [85, 92, 78, 88, 75],
        get_text('reading_score', language): [80, 89, 82, 85, 73],
        get_text('risk_level', language): ['Low', 'Low', 'Medium', 'Low', 'Medium'],
        get_text('assessment_date', language): ['2025-07-07', '2025-07-06', '2025-07-05', '2025-07-04', '2025-07-03']
    })
    
    st.dataframe(
        assessment_data,
        use_container_width=True,
        hide_index=True
    )
    
    # Monthly Progress Trend
    st.subheader(f"📈 {get_text('monthly_trends', language)}")
    
    # Create trend data
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul']
    math_avg = [72, 74, 76, 78, 77, 79, 78]
    reading_avg = [75, 76, 78, 80, 79, 81, 82]
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=months, y=math_avg, mode='lines+markers', name=get_text('mathematics', language), line=dict(color='#3b82f6')))
    fig.add_trace(go.Scatter(x=months, y=reading_avg, mode='lines+markers', name=get_text('reading', language), line=dict(color='#10b981')))
    
    fig.update_layout(
        title=get_text('monthly_performance_trends', language),
        xaxis_title=get_text('month', language),
        yaxis_title=get_text('average_score', language),
        height=400
    )
    st.plotly_chart(fig, use_container_width=True)

def render_assessment():
    """Render the assessment page"""
    settings = load_app_settings()
    language = settings.get('language', 'English')
    
    st.markdown(f"""
    <div class="content-card">
        <h2 style="margin-top: 0;">{get_text('learning_risk_assessment', language)}</h2>
    </div>
    """, unsafe_allow_html=True)
    
    with st.container():
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f"### {get_text('student_information', language)}")
            student_name = st.text_input(get_text('student_name', language))
            grade_level = st.selectbox(get_text('grade_level', language), 
                                     ["1", "2", "3", "4", "5", "6", "7", "8"])
            
            st.markdown(f"### {get_text('academic_performance', language)}")
            math_score = st.slider(get_text('math_score', language), 0, 100, 75)
            reading_score = st.slider(get_text('reading_score', language), 0, 100, 80)
            writing_score = st.slider(get_text('writing_score', language), 0, 100, 70)
            attendance = st.slider(get_text('attendance', language), 0, 100, 85)
        
        with col2:
            st.markdown(f"### {get_text('behavioral_assessment', language)}")
            
            behavior_options = [
                f"1 - {get_text('poor', language)}",
                f"2 - {get_text('below_average', language)}",
                f"3 - {get_text('average', language)}",
                f"4 - {get_text('good', language)}",
                f"5 - {get_text('excellent', language)}"
            ]
            
            behavior_rating = st.selectbox(
                get_text('behavior_rating', language),
                behavior_options,
                index=2
            )
            
            literacy_options = [
                f"1 - Beginner",
                f"2 - Basic",
                f"3 - Elementary",
                f"4 - Pre-Intermediate", 
                f"5 - Intermediate",
                f"6 - Developing",
                f"7 - Upper-Intermediate",
                f"8 - Advanced",
                f"9 - Proficient",
                f"10 - Expert"
            ]
            
            literacy_level = st.selectbox(
                get_text('literacy_level', language),
                literacy_options,
                index=5
            )
            
            # Clean assessment interface without heavy images
    
    if st.button(get_text('analyze_learning_risk', language), key="analyze_risk"):
        # Extract numeric values
        behavior_val = int(behavior_rating.split(' - ')[0])
        literacy_val = int(literacy_level.split(' - ')[0])
        
        # Calculate risk
        features = np.array([[math_score, reading_score, writing_score, attendance, behavior_val, literacy_val]])
        
        try:
            model = load_model()
            if model is not None:
                prediction = make_prediction(model, features)
                risk_level = prediction[0] if prediction is not None else "Medium"
                
                # Save prediction
                prediction_data = {
                    'student_name': student_name,
                    'grade_level': grade_level,
                    'math_score': math_score,
                    'reading_score': reading_score, 
                    'writing_score': writing_score,
                    'attendance': attendance,
                    'behavior_rating': behavior_val,
                    'literacy_level': literacy_val,
                    'risk_level': risk_level,
                    'date': datetime.now().isoformat()
                }
                
                save_prediction_data(prediction_data)
                
                # Display results
                st.markdown(f"""
                <div class="content-card">
                    <h3>{get_text('assessment_results', language)}</h3>
                    <p><strong>{get_text('risk_level', language)}:</strong> {risk_level}</p>
                </div>
                """, unsafe_allow_html=True)
                
                # Show recommendations
                recommendations = get_recommendations(risk_level)
                if recommendations:
                    st.markdown(f"### {get_text('recommendations', language)}")
                    for rec in recommendations:
                        st.markdown(f"• {rec}")
            else:
                st.error("Model could not be loaded. Please check your model files.")
                
        except Exception as e:
            st.error(f"Assessment error: {str(e)}")

def render_resources():
    """Render the resources page with comprehensive teacher tools"""
    settings = load_app_settings()
    language = settings.get('language', 'English')
    
    st.markdown(f"""
    <div class="content-card">
        <h2 style="margin-top: 0;">{get_text('resources', language)}</h2>
        <p>Comprehensive educational resources and teaching materials</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Resource categories
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(create_metric_card(
            "Teaching Guides",
            "50+",
            "Research-based strategies",
            "#8b5cf6"
        ), unsafe_allow_html=True)
    
    with col2:
        st.markdown(create_metric_card(
            "Lesson Plans", 
            "200+",
            "Ready-to-use templates",
            "#06b6d4"
        ), unsafe_allow_html=True)
    
    with col3:
        st.markdown(create_metric_card(
            "Activities",
            "100+", 
            "Interactive exercises",
            "#10b981"
        ), unsafe_allow_html=True)
    
    # Add resource images
    st.markdown("""
    <div class="content-card">
        <h3>Featured Resources</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Educational resource areas
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("**Teaching Excellence**")
        st.markdown("Professional development and classroom management")
    with col2:
        st.markdown("**Student Engagement**") 
        st.markdown("Interactive activities and learning strategies")
    with col3:
        st.markdown("**Academic Focus**")
        st.markdown("Assessment methods and learning interventions")

def render_tracker():
    """Render the parent tracker page"""
    settings = load_app_settings()
    language = settings.get('language', 'English')
    
    st.markdown(f"""
    <div class="content-card">
        <h2 style="margin-top: 0;">{get_text('daily_observation_log', language)}</h2>
    </div>
    """, unsafe_allow_html=True)
    
    with st.container():
        col1, col2 = st.columns(2)
        
        with col1:
            child_name = st.text_input(get_text('child_name', language))
            observation_date = st.date_input(get_text('observation_date', language))
            
            st.markdown(f"### {get_text('academic_observations', language)}")
            homework_completion = st.slider(get_text('homework_completion', language), 0, 100, 80)
            reading_time = st.number_input(get_text('reading_time', language), 0, 240, 30)
            
            focus_options = [
                f"1 - {get_text('poor', language)}",
                f"2 - {get_text('below_average', language)}", 
                f"3 - {get_text('average', language)}",
                f"4 - {get_text('good', language)}",
                f"5 - {get_text('excellent', language)}"
            ]
            focus_level = st.selectbox(get_text('focus_level', language), focus_options, index=2)
            
            subjects_struggled = st.text_area(get_text('subjects_struggled', language))
        
        with col2:
            st.markdown(f"### {get_text('behavioral_observations', language)}")
            
            mood_options = [
                "1 - Very Upset",
                "2 - Upset", 
                "3 - Neutral",
                "4 - Happy",
                "5 - Very Happy"
            ]
            mood_rating = st.selectbox(get_text('mood_rating', language), mood_options, index=2)
            
            sleep_hours = st.slider(get_text('sleep_hours', language), 0, 12, 8)
            
            energy_options = [
                f"1 - {get_text('low', language)}",
                f"2 - Below Average",
                f"3 - {get_text('average', language)}",
                f"4 - Above Average", 
                f"5 - {get_text('high', language)}"
            ]
            energy_level = st.selectbox(get_text('energy_level', language), energy_options, index=2)
            
            learning_wins = st.text_area(get_text('learning_wins', language))
            challenges_faced = st.text_area(get_text('challenges_faced', language))
            
            # Parent support information
            st.markdown("**Parent Support Resources**")
            st.markdown("Access guides and tips for supporting your child's learning journey at home.")
    
    if st.button(get_text('save_observation', language), key="save_observation"):
        # Extract numeric values
        focus_val = int(focus_level.split(' - ')[0])
        mood_val = int(mood_rating.split(' - ')[0])
        energy_val = int(energy_level.split(' - ')[0])
        
        observation_data = {
            'child_name': child_name,
            'observation_date': observation_date.isoformat(),
            'homework_completion': homework_completion,
            'reading_time': reading_time,
            'focus_level': focus_val,
            'subjects_struggled': subjects_struggled,
            'mood_rating': mood_val,
            'sleep_hours': sleep_hours,
            'energy_level': energy_val,
            'learning_wins': learning_wins,
            'challenges_faced': challenges_faced,
            'timestamp': datetime.now().isoformat()
        }
        
        if save_parent_observation(observation_data):
            st.success("Observation saved successfully!")
        else:
            st.error("Failed to save observation. Please try again.")

def render_analytics():
    """Render the analytics page"""
    settings = load_app_settings()
    language = settings.get('language', 'English')
    
    st.markdown(f"""
    <div class="content-card">
        <h2 style="margin-top: 0;">{get_text('analytics', language)}</h2>
        <p>Comprehensive data analysis and insights</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sample analytics data
    col1, col2 = st.columns(2)
    
    with col1:
        # Performance trends chart
        dates = pd.date_range(start='2024-01-01', end='2024-06-01', freq='M')
        performance_data = {
            'Date': dates,
            'Math': [75, 78, 82, 79, 85],
            'Reading': [70, 73, 76, 80, 82],
            'Writing': [68, 72, 75, 78, 81]
        }
        
        df = pd.DataFrame(performance_data)
        
        fig = px.line(df, x='Date', y=['Math', 'Reading', 'Writing'],
                     title='Academic Performance Trends',
                     color_discrete_map={'Math': '#3b82f6', 'Reading': '#10b981', 'Writing': '#f59e0b'})
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='#2c3e50'
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Risk distribution
        risk_data = {
            'Risk Level': ['Low Risk', 'Medium Risk', 'High Risk'],
            'Count': [267, 52, 23]
        }
        
        fig2 = px.pie(values=risk_data['Count'], names=risk_data['Risk Level'],
                     title='Student Risk Distribution',
                     color_discrete_map={'Low Risk': '#10b981', 'Medium Risk': '#f59e0b', 'High Risk': '#ef4444'})
        fig2.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='#2c3e50'
        )
        st.plotly_chart(fig2, use_container_width=True)

def render_settings():
    """Render the settings page"""
    # Get language from session state first, then settings
    language = st.session_state.get('app_language')
    if language is None:
        settings = load_app_settings()
        language = settings.get('language', 'English')
        st.session_state['app_language'] = language
    else:
        settings = load_app_settings()
    
    # Add CSS to fix text color for selectboxes
    st.markdown("""
    <style>
    /* Fix selectbox text color */
    .stSelectbox > div > div > div {
        color: #000000 !important;
        background-color: #ffffff !important;
    }
    
    /* Fix selectbox dropdown text */
    .stSelectbox > div > div > div > div {
        color: #000000 !important;
    }
    
    /* Fix selectbox options */
    [data-baseweb="select"] > div {
        color: #000000 !important;
        background-color: #ffffff !important;
    }
    
    /* Fix all text in settings to be black */
    .stMarkdown h3 {
        color: #000000 !important;
    }
    
    /* Fix checkbox text */
    .stCheckbox > label {
        color: #000000 !important;
    }
    
    /* Fix all text labels */
    .stSelectbox label {
        color: #000000 !important;
    }
    
    /* Make sure preview text is visible */
    .stMarkdown p {
        color: #000000 !important;
    }
    
    /* Style navigation buttons to be blue */
    div[data-testid="stButton"] > button {
        background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
    }
    
    div[data-testid="stButton"] > button:hover {
        background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%) !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 4px 15px rgba(59, 130, 246, 0.3) !important;
    }
    
    /* Style primary buttons specifically */
    button[kind="primary"] {
        background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%) !important;
        color: white !important;
    }
    
    button[kind="primary"]:hover {
        background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%) !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class="main-header">
        <h1 class="page-title">{get_text('settings', language)}</h1>
    </div>
    """, unsafe_allow_html=True)
    
    with st.container():
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f"### {get_text('language', language)}")
            language_options = ['English', 'Somali', 'Arabic']
            language_display = {
                'English': 'English 🇺🇸',
                'Somali': 'Af-Soomaali 🇸🇴',
                'Arabic': 'العربية 🇸🇦'
            }
            
            new_language = st.selectbox(
                get_text('language', language),
                language_options,
                index=language_options.index(language),
                format_func=lambda x: language_display[x],
                key="language_selector"
            )
            
            st.markdown(f"### {get_text('theme', language)}")
            theme_options = ['Modern', 'Classic', 'Dark']
            current_theme = settings.get('theme', 'Modern')
            # Handle case where saved theme is not in options
            if current_theme not in theme_options:
                current_theme = 'Modern'
            new_theme = st.selectbox(
                get_text('theme', language),
                theme_options,
                index=theme_options.index(current_theme)
            )
            
            offline_mode = st.checkbox(
                "Offline Mode",
                value=settings.get('offline_mode', False)
            )
        
        with col2:
            st.markdown("### Preview")
            st.markdown(f"**Current Language:** {language_display.get(language, language)}", unsafe_allow_html=True)
            st.markdown(f"**Current Theme:** {current_theme}", unsafe_allow_html=True)
            st.markdown(f"**Offline Mode:** {'Enabled' if settings.get('offline_mode', False) else 'Disabled'}", unsafe_allow_html=True)
            
            # Language preview text
            if new_language == 'Somali':
                st.info("Luqadda: Af-Soomaali - Barnaamijkan wuxuu u shaqeeyaa barashada ardayda")
            elif new_language == 'Arabic':
                st.info("اللغة: العربية - هذا التطبيق يعمل على تقييم تعلم الطلاب")
            else:
                st.info("Language: English - This application works for student learning assessment")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button(get_text('save_settings', language), type="primary"):
            new_settings = {
                'language': new_language,
                'theme': new_theme,
                'offline_mode': offline_mode
            }
            
            if save_app_settings(new_settings):
                # Update session state to immediately apply language change
                st.session_state['app_language'] = new_language
                st.success("Settings saved successfully!")
                st.rerun()
            else:
                st.error("Failed to save settings.")
    
    with col2:
        if st.button(get_text('reset_app', language), type="secondary"):
            # Reset session state
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            
            # Reset to default settings
            default_settings = {
                'language': 'English',
                'theme': 'Modern', 
                'offline_mode': False
            }
            save_app_settings(default_settings)
            
            st.success("Application reset successfully!")
            st.rerun()

def render_bottom_navigation():
    """Render bottom navigation with offline toggle and reset"""
    settings = load_app_settings()
    offline_mode = settings.get('offline_mode', False)
    
    st.markdown("---")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("**EduScan Somalia** | Professional Learning Assessment")
    
    with col2:
        status = "🟢 Online" if not offline_mode else "🟡 Offline"
        st.markdown(f"Status: {status}")
    
    with col3:
        if st.button("Toggle Offline Mode", type="primary"):
            new_settings = settings.copy()
            new_settings['offline_mode'] = not offline_mode
            save_app_settings(new_settings)
            st.rerun()

def main():
    """Main application function"""
    # Page configuration
    st.set_page_config(
        page_title="EduScan Somalia",
        page_icon="📚",
        layout="wide",
        initial_sidebar_state="collapsed"
    )
    
    # Initialize language in session state
    if 'app_language' not in st.session_state:
        settings = load_app_settings()
        st.session_state['app_language'] = settings.get('language', 'English')
    
    # Load settings and apply theme
    settings = load_app_settings()
    apply_theme(settings.get('theme', 'Modern'))
    
    # Clean background without image
    st.markdown("""
    <style>
    .stApp {
        background: #f8fafc !important;
        min-height: 100vh !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Render header
    render_app_header()
    
    # Render navigation
    render_navigation()
    
    # Render current page
    current_page = st.session_state.get('current_page', 'dashboard')
    
    if current_page == 'dashboard':
        render_dashboard()
    elif current_page == 'settings':
        render_settings()
    
    # Render bottom navigation
    render_bottom_navigation()

if __name__ == "__main__":
    main()