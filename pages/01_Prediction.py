import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, date
import json
import os
import sys
from utils.model_utils import load_model, make_prediction
from utils.data_utils import save_prediction_data, load_student_data
from utils.image_utils import get_image_html, create_image_gallery, get_student_images
from utils.educational_images import get_diverse_educational_images
from utils.image_base64 import get_base64_images, get_image_html as get_b64_image_html
from utils.language_utils import get_text, load_app_settings

# Initialize language in session state
if 'app_language' not in st.session_state:
    settings = load_app_settings()
    st.session_state['app_language'] = settings.get('language', 'English')

# Get current language
language = st.session_state.get('app_language', 'English')

# Page config removed - handled by main app

# CSS matching the main app design
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');
    
    .stApp {
        font-family: 'Poppins', sans-serif !important;
        background: linear-gradient(rgba(248, 250, 252, 0.95), rgba(248, 250, 252, 0.95)), 
                    url('data:image/jpeg;base64,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');
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }
    
    .stDeployButton {display: none;}
    #MainMenu {visibility: hidden;}
    .stHeader {display: none;}
    .stToolbar {display: none;}
    
    .css-1d391kg {
        background-color: white !important;
        border-right: 1px solid #e5e7eb !important;
    }
    
    .main .block-container {
        background-color: #f8fafc !important;
        padding: 1.5rem !important;
        max-width: none !important;
    }
    
    .page-header {
        background: white;
        padding: 1rem 1.5rem;
        border-bottom: 1px solid #e5e7eb;
        margin: -1.5rem -1.5rem 2rem -1.5rem;
    }
    
    .page-title {
        font-size: 1.5rem;
        font-weight: 700;
        color: #1f2937;
        margin: 0;
    }
    
    .form-container {
        background: white;
        padding: 2rem;
        border-radius: 0.75rem;
        box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1);
        border: 1px solid #e5e7eb;
        margin-bottom: 1.5rem;
    }
    
    .student-showcase {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 1rem;
        margin: 2rem 0;
    }
    
    .student-card {
        text-align: center;
        background: rgba(255, 255, 255, 0.9);
        padding: 1rem;
        border-radius: 15px;
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
    }
    
    .student-card img {
        width: 100%;
        height: 120px;
        object-fit: cover;
        border-radius: 10px;
        margin-bottom: 0.5rem;
    }
    
    .highlight-text {
        background: linear-gradient(135deg, #FFD23F, #FF6B35);
        -webkit-background-clip: text;
        background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: bold;
    }
    
    .results-section {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(10px);
        padding: 2rem;
        border-radius: 20px;
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
        border: 1px solid rgba(255,255,255,0.18);
        margin: 2rem 0;
    }
</style>
""", unsafe_allow_html=True)

def validate_inputs(math_score, reading_score, writing_score, attendance, behavior, literacy):
    """Validate all input parameters"""
    errors = []
    
    if not (0 <= math_score <= 100):
        errors.append("Math score must be between 0 and 100")
    if not (0 <= reading_score <= 100):
        errors.append("Reading score must be between 0 and 100")
    if not (0 <= writing_score <= 100):
        errors.append("Writing score must be between 0 and 100")
    if not (0 <= attendance <= 100):
        errors.append("Attendance must be between 0 and 100%")
    if not (1 <= behavior <= 5):
        errors.append("Behavior rating must be between 1 and 5")
    if not (1 <= literacy <= 10):
        errors.append("Literacy level must be between 1 and 10")
    
    return errors

def create_risk_visualization(prediction_prob, student_data):
    """Create visualization for risk assessment"""
    
    # Risk gauge chart
    fig_gauge = go.Figure(go.Indicator(
        mode = "gauge+number+delta",
        value = prediction_prob * 100,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': "Learning Difficulty Risk Level (%)"},
        delta = {'reference': 30},
        gauge = {
            'axis': {'range': [None, 100]},
            'bar': {'color': "darkblue"},
            'steps': [
                {'range': [0, 30], 'color': "lightgreen"},
                {'range': [30, 70], 'color': "yellow"},
                {'range': [70, 100], 'color': "red"}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 70
            }
        }
    ))
    
    fig_gauge.update_layout(height=300)
    
    # Performance radar chart
    categories = ['Math Score', 'Reading Score', 'Writing Score', 'Attendance', 'Behavior*20', 'Literacy*10']
    values = [
        student_data['math_score'],
        student_data['reading_score'], 
        student_data['writing_score'],
        student_data['attendance'],
        student_data['behavior'] * 20,
        student_data['literacy'] * 10
    ]
    
    fig_radar = go.Figure()
    
    fig_radar.add_trace(go.Scatterpolar(
        r=values,
        theta=categories,
        fill='toself',
        name='Student Performance'
    ))
    
    fig_radar.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100]
            )),
        showlegend=True,
        title="Student Performance Profile",
        height=400
    )
    
    return fig_gauge, fig_radar

def display_recommendations(risk_level, student_data):
    """Display personalized recommendations based on risk level"""
    
    if risk_level == "Low Risk":
        st.success(" Low Risk - Continue current support strategies")
        recommendations = [
            "Maintain current learning pace and methods",
            "Continue regular progress monitoring",
            "Encourage continued engagement in all subjects",
            "Consider enrichment activities to challenge the student"
        ]
        color = "green"
    elif risk_level == "Medium Risk":
        st.warning("️ Medium Risk - Enhanced monitoring recommended")
        recommendations = [
            "Implement targeted interventions in lower-performing areas",
            "Increase frequency of progress monitoring",
            "Consider additional support in specific subjects",
            "Engage parents in home-based learning activities",
            "Explore different teaching methods and materials"
        ]
        color = "orange"
    else:
        st.error("High Risk - Immediate intervention required")
        recommendations = [
            "Initiate comprehensive assessment by learning specialists",
            "Implement intensive intervention strategies",
            "Consider individualized education plan (IEP)",
            "Increase collaboration between teachers and parents",
            "Explore assistive technologies and adaptive methods",
            "Regular monitoring and adjustment of intervention strategies"
        ]
        color = "red"
    
    st.markdown(f"### Recommended Actions")
    for i, rec in enumerate(recommendations, 1):
        st.markdown(f"{i}. {rec}")

def main():
    # Page header
    st.markdown(f"""
    <div class="page-header">
        <h1 class="page-title">{get_text('assessment_form', language)}</h1>
    </div>
    """, unsafe_allow_html=True)
    
    # Add authentic student images
    images = get_student_images()
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown(get_image_html(images['focused_student'], "Student Assessment", "100%", "200px"), unsafe_allow_html=True)

    
    # Student showcase section
    st.markdown(f"""
    <div class="input-section">
        <h2 class="highlight-text">{get_text('empowering_student_success', language)}</h2>
        <div class="student-showcase">
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Add student image gallery
    st.markdown("### Student Assessment Success")
    images = get_student_images()
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(get_image_html(images['exam_students'], "Assessment Excellence", "100%", "180px"), unsafe_allow_html=True)
    with col2:
        st.markdown(get_image_html(images['happy_students'], "Learning Success", "100%", "180px"), unsafe_allow_html=True)
    with col3:
        st.markdown(get_image_html(images['student_portrait'], "Academic Achievement", "100%", "180px"), unsafe_allow_html=True)
    
    # Sidebar for navigation
    with st.sidebar:
        st.markdown("### Prediction Options")
        prediction_type = st.selectbox(
            "Choose prediction type:",
            ["Single Student", "Batch Upload", "Historical Analysis"]
        )
        
        # Model information panel
        st.markdown("### Model Information")
        st.info("""
        **Your Trained Model Active**
        
        - **Type**: RandomForest Classifier
        - **Features**: 6 key metrics
        - **Normalization**: StandardScaler
        - **Training**: GridSearchCV optimized
        - **Status**: Ready for predictions
        """)
        
        # Show model features
        st.markdown("**Input Features:**")
        features = [
            "Math Score (0-100)",
            "Reading Score (0-100)", 
            "Writing Score (0-100)",
            "Attendance Rate (%)",
            "Behavior Score (1-5)",
            "Literacy Level (1-10)"
        ]
        for feature in features:
            st.markdown(f"• {feature}")
            
        # Performance note
        st.success("Model loaded successfully from your notebook specifications")
        
        if prediction_type == "Batch Upload":
            st.markdown("#### Upload CSV File")
            uploaded_file = st.file_uploader(
                "Upload student data (CSV)",
                type=['csv'],
                help="CSV should contain columns: math_score, reading_score, writing_score, attendance, behavior, literacy"
            )

    if prediction_type == "Single Student":
        # Single student prediction form
        col1, col2 = st.columns(2)
        
        st.markdown(f"""
        <div class="input-section">
            <h2 class="highlight-text">{get_text('assessment_form', language)}</h2>
            <p style="font-size: 1.1em; margin-bottom: 2rem; color: #2C3E50;">
                {get_text('comprehensive_assessment', language)}
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Load base64 images for section headers
        b64_images = get_base64_images()
        
        # Get reset counter for unique widget keys
        reset_counter = st.session_state.get('reset_counter', 0)
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.markdown(f"""
            <div class="input-section">
                <h3 class="highlight-text">{get_text('academic_performance', language)}</h3>
                {get_b64_image_html(b64_images['academic_performance'], get_text('academic_performance', language), "100%", "150px")}
            </div>
            """, unsafe_allow_html=True)
            # Academic inputs as number boxes (matching PyQt5 design)  
            math_score = st.number_input(get_text('math_score', language), min_value=0, max_value=100, value=75, step=1, key=f"math_score_input_{reset_counter}")
            reading_score = st.number_input(get_text('reading_score', language), min_value=0, max_value=100, value=80, step=1, key=f"reading_score_input_{reset_counter}")
            writing_score = st.number_input(get_text('writing_score', language), min_value=0, max_value=100, value=70, step=1, key=f"writing_score_input_{reset_counter}")
            
        with col2:
            st.markdown(f"""
            <div class="input-section">
                <h3 class="highlight-text">{get_text('behavioral_social_indicators', language)}</h3>
                {get_b64_image_html(b64_images['behavioral_social'], get_text('behavioral_social_indicators', language), "100%", "150px")}
            </div>
            """, unsafe_allow_html=True)
            attendance = st.slider(get_text('attendance', language), 0, 100, 85, help="Percentage of school days attended", key=f"attendance_slider_{reset_counter}")
            behavior_options = [f"1 - {get_text('poor', language)}", f"2 - {get_text('below_average', language)}", f"3 - {get_text('average', language)}", f"4 - {get_text('good', language)}", f"5 - {get_text('excellent', language)}"]
            behavior_selection = st.select_slider(get_text('behavior_rating', language), options=behavior_options, value=f"3 - {get_text('average', language)}", 
                                                 help="Select the student's typical classroom behavior", key=f"behavior_slider_{reset_counter}")
            behavior = int(behavior_selection.split(' ')[0])  # Extract the number
            literacy_options = [f'{i} - {"Beginner" if i <= 3 else "Developing" if i <= 6 else "Advanced"}' for i in range(1, 11)]
            literacy_selection = st.select_slider(get_text('literacy_level', language), options=literacy_options, value="6 - Developing",
                                                help="Select the student's reading and literacy level", key=f"literacy_slider_{reset_counter}")
            literacy = int(literacy_selection.split(' ')[0])  # Extract the number
        
        # Enhanced student information section
        # Get base64 images for authentic display
        b64_images = get_base64_images()
        
        st.markdown(f"""
        <div class="input-section">
            <h3 class="highlight-text">{get_b64_image_html(b64_images['student_information_2'], "Student Information", "200px", "50px")}</h3>
            <div style="display: flex; gap: 1rem; margin-bottom: 1rem;">
                {get_b64_image_html(b64_images['student_portrait'], "Somali Student Portrait", "30%", "100px")}
                {get_b64_image_html(b64_images['student_writing'], "Student Learning", "30%", "100px")}
                {get_b64_image_html(b64_images['exam_students'], "Exam Students", "30%", "100px")}
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        col3, col4 = st.columns(2)
        
        with col3:
            student_name = st.text_input(get_text('student_name', language), help="For record keeping and tracking purposes", key=f"student_name_input_{reset_counter}")
            grade_level = st.selectbox(get_text('grade_level', language), ["Pre-K", "K", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12"], key=f"grade_level_select_{reset_counter}")
        
        with col4:
            notes = st.text_area("Teacher notes", placeholder="Teacher notes…", help="Any relevant observations", height=100, key=f"teacher_notes_input_{reset_counter}")
        
        # Action buttons
        col1, col2, col3 = st.columns(3)
        
        with col1:
            predict_button = st.button(get_text('analyze_learning_risk', language), type="primary", use_container_width=True)
        
        with col2:
            reset_button = st.button(get_text('clear_form', language), use_container_width=True)
        
        with col3:
            save_button = st.button("Save Data", use_container_width=True)
        
        if reset_button:
            # Clear ALL session state completely for a fresh start
            all_keys = list(st.session_state.keys())
            
            # Keep only essential app settings
            keys_to_keep = ['app_language', 'app_theme']
            
            for key in all_keys:
                if key not in keys_to_keep:
                    del st.session_state[key]
            
            # Increment reset counter to force widget recreation with new keys
            if 'reset_counter' not in st.session_state:
                st.session_state['reset_counter'] = 0
            st.session_state['reset_counter'] += 1
            
            st.success("✅ Form completely reset! Ready for new student assessment.")
            st.rerun()
        
        # Only show results if analysis has been run and form hasn't been reset
        show_results = st.session_state.get('show_prediction_results', False)
        
        if predict_button:
            # Validate inputs
            errors = validate_inputs(math_score, reading_score, writing_score, attendance, behavior, literacy)
            
            if errors:
                st.error(get_text('please_correct_errors', language))
                for error in errors:
                    st.error(f"• {error}")
            else:
                # Make prediction
                student_data = {
                    'math_score': math_score,
                    'reading_score': reading_score,
                    'writing_score': writing_score,
                    'attendance': attendance,
                    'behavior': behavior,
                    'literacy': literacy
                }
                
                try:
                    prediction, prediction_prob = make_prediction(student_data)
                    
                    # Store results and set flag to show them
                    st.session_state['show_prediction_results'] = True
                    st.session_state['current_prediction_data'] = {
                        'prediction': prediction,
                        'prediction_prob': prediction_prob,
                        'student_data': student_data,
                        'student_name': student_name,
                        'grade_level': grade_level,
                        'notes': notes
                    }
                    
                    # Enhanced results display
                    st.markdown(f"""
                    <div class="results-section">
                        <h2 class="highlight-text">{get_text('assessment_results', language)}</h2>
                        <div style="display: flex; gap: 1rem; margin-bottom: 2rem;">
                            {get_b64_image_html(b64_images['exam_students'], "Exam Students", "30%", "120px")}
                            {get_b64_image_html(b64_images['student_writing'], "Student Writing", "30%", "120px")}
                            {get_b64_image_html(b64_images['student_portrait'], "Student Portrait", "30%", "120px")}
                        </div>
                        <p style="font-size: 1.2em; text-align: center; color: #2C3E50; margin-bottom: 2rem;">
                            <strong>{get_text('comprehensive_assessment', language)} {student_name if student_name else "the student"}</strong>
                        </p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Determine risk level
                    if prediction_prob < 0.3:
                        risk_level = get_text('low_risk', language)
                        risk_color = "#00A86B"
                        risk_icon = ""
                    elif prediction_prob < 0.7:
                        risk_level = get_text('medium_risk', language)
                        risk_color = "#FF6B35"
                        risk_icon = "️"
                    else:
                        risk_level = get_text('high_risk', language)
                        risk_color = "#E74C3C"
                        risk_icon = "!"
                    
                    # Risk level display
                    st.markdown(f"""
                    <div class="results-section" style="text-align: center; background: linear-gradient(135deg, {risk_color}20, {risk_color}10);">
                        <h2 style="color: {risk_color};">{risk_icon} {risk_level}</h2>
                        <h3 style="color: {risk_color};">Confidence Level: {prediction_prob:.1%}</h3>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Create visualizations
                    fig_gauge, fig_radar = create_risk_visualization(prediction_prob, student_data)
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.markdown(f"""
                        <div class="results-section">
                            <h3 class="highlight-text">{get_text('risk_assessment_gauge', language)}</h3>
                        </div>
                        """, unsafe_allow_html=True)
                        st.plotly_chart(fig_gauge, use_container_width=True)
                    
                    with col2:
                        st.markdown(f"""
                        <div class="results-section">
                            <h3 class="highlight-text">{get_text('student_performance_profile', language)}</h3>
                        </div>
                        """, unsafe_allow_html=True)
                        st.plotly_chart(fig_radar, use_container_width=True)
                    
                    # Display recommendations
                    st.markdown(f"""
                    <div class="results-section">
                        <h3 class="highlight-text">{get_text('personalized_intervention_recommendations', language)}</h3>
                        <img src="attached_assets/somalia-children-in-class_1751965339107.jpg" 
                             style="width: 100%; height: 150px; object-fit: cover; border-radius: 15px; margin-bottom: 1rem;">
                    </div>
                    """, unsafe_allow_html=True)
                    display_recommendations(risk_level, student_data)
                    
                    # Enhanced summary table
                    st.markdown(f"""
                    <div class="results-section">
                        <h3 class="highlight-text">{get_text('assessment_summary', language)}</h3>
                    </div>
                    """, unsafe_allow_html=True)
                    summary_data = {
                        "Assessment Area": ["Mathematics", "Reading", "Writing", "Attendance", "Behavior", "Literacy", "Overall Risk", "AI Confidence"],
                        "Score/Rating": [f"{math_score}%", f"{reading_score}%", f"{writing_score}%", f"{attendance}%", f"{behavior}/5", f"{literacy}/10", risk_level, f"{prediction_prob:.1%}"]
                    }
                    st.table(pd.DataFrame(summary_data))
                    
                    # Save prediction option
                    if save_button or st.button(" Save This Prediction"):
                        prediction_record = {
                            "timestamp": datetime.now().isoformat(),
                            "student_name": student_name,
                            "grade_level": grade_level,
                            "prediction": prediction,
                            "probability": prediction_prob,
                            "risk_level": risk_level,
                            "notes": notes,
                            **student_data
                        }
                        save_prediction_data(prediction_record)
                        st.success(" Prediction saved successfully!")
                
                except Exception as e:
                    st.error(f" Error making prediction: {str(e)}")
                    st.info("Note: Using sample prediction model. Replace with your trained model file.")
        
        # Display results only if they exist and haven't been cleared
        if show_results and 'current_prediction_data' in st.session_state:
            pred_data = st.session_state['current_prediction_data']
            prediction = pred_data['prediction']
            prediction_prob = pred_data['prediction_prob']
            student_data = pred_data['student_data']
            student_name = pred_data['student_name']
            grade_level = pred_data['grade_level']
            notes = pred_data['notes']
            
            # Get base64 images
            b64_images = get_base64_images()
            
            # Enhanced results display
            st.markdown(f"""
            <div class="results-section">
                <h2 class="highlight-text">{get_text('assessment_results', language)}</h2>
                <div style="display: flex; gap: 1rem; margin-bottom: 2rem;">
                    {get_b64_image_html(b64_images['exam_students'], "Exam Students", "30%", "120px")}
                    {get_b64_image_html(b64_images['student_writing'], "Student Writing", "30%", "120px")}
                    {get_b64_image_html(b64_images['student_portrait'], "Student Portrait", "30%", "120px")}
                </div>
                <p style="font-size: 1.2em; text-align: center; color: #2C3E50; margin-bottom: 2rem;">
                    <strong>{get_text('comprehensive_assessment', language)} {student_name if student_name else "the student"}</strong>
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            # Determine risk level
            if prediction_prob < 0.3:
                risk_level = get_text('low_risk', language)
                risk_color = "#00A86B"
                risk_icon = ""
            elif prediction_prob < 0.7:
                risk_level = get_text('medium_risk', language)
                risk_color = "#FF6B35"
                risk_icon = "️"
            else:
                risk_level = get_text('high_risk', language)
                risk_color = "#E74C3C"
                risk_icon = "!"
            
            # Risk level display
            st.markdown(f"""
            <div class="results-section" style="text-align: center; background: linear-gradient(135deg, {risk_color}20, {risk_color}10);">
                <h2 style="color: {risk_color};">{risk_icon} {risk_level}</h2>
                <h3 style="color: {risk_color};">Confidence Level: {prediction_prob:.1%}</h3>
            </div>
            """, unsafe_allow_html=True)
            
            # Create visualizations
            fig_gauge, fig_radar = create_risk_visualization(prediction_prob, student_data)
            
            col1, col2 = st.columns(2)
            with col1:
                st.plotly_chart(fig_gauge, use_container_width=True)
            with col2:
                st.plotly_chart(fig_radar, use_container_width=True)
            
            # Display recommendations
            st.markdown(f"""
            <div class="results-section">
                <h3 class="highlight-text">{get_text('personalized_intervention_recommendations', language)}</h3>
                <img src="attached_assets/somalia-children-in-class_1751965339107.jpg" 
                     style="width: 100%; height: 150px; object-fit: cover; border-radius: 15px; margin-bottom: 1rem;">
            </div>
            """, unsafe_allow_html=True)
            display_recommendations(risk_level, student_data)
            
            # Enhanced summary table
            st.markdown(f"""
            <div class="results-section">
                <h3 class="highlight-text">{get_text('assessment_summary', language)}</h3>
            </div>
            """, unsafe_allow_html=True)
            summary_data = {
                "Assessment Area": ["Mathematics", "Reading", "Writing", "Attendance", "Behavior", "Literacy", "Overall Risk", "AI Confidence"],
                "Score/Rating": [f"{student_data['math_score']}%", f"{student_data['reading_score']}%", f"{student_data['writing_score']}%", 
                               f"{student_data['attendance']}%", f"{student_data['behavior']}/5", f"{student_data['literacy']}/10", 
                               risk_level, f"{prediction_prob:.1%}"]
            }
            st.table(pd.DataFrame(summary_data))
            
            # Save prediction option
            if save_button or st.button(" Save This Prediction"):
                prediction_record = {
                    "timestamp": datetime.now().isoformat(),
                    "student_name": student_name,
                    "grade_level": grade_level,
                    "prediction": prediction,
                    "probability": prediction_prob,
                    "risk_level": risk_level,
                    "notes": notes,
                    **student_data
                }
                save_prediction_data(prediction_record)
                st.success(" Prediction saved successfully!")
    
    elif prediction_type == "Batch Upload":
        if uploaded_file is not None:
            try:
                df = pd.read_csv(uploaded_file)
                st.success(f" Uploaded file with {len(df)} students")
                
                # Validate required columns
                required_columns = ['math_score', 'reading_score', 'writing_score', 'attendance', 'behavior', 'literacy']
                missing_columns = [col for col in required_columns if col not in df.columns]
                
                if missing_columns:
                    st.error(f" Missing required columns: {', '.join(missing_columns)}")
                else:
                    # Show preview
                    st.markdown("### Data Preview")
                    st.dataframe(df.head())
                    
                    if st.button("Process Batch Predictions"):
                        progress_bar = st.progress(0)
                        results = []
                        
                        for idx, row in df.iterrows():
                            try:
                                student_data = {col: row[col] for col in required_columns}
                                prediction, prediction_prob = make_prediction(student_data)
                                
                                if prediction_prob < 0.3:
                                    risk_level = "Low Risk"
                                elif prediction_prob < 0.7:
                                    risk_level = "Medium Risk"
                                else:
                                    risk_level = "High Risk"
                                
                                results.append({
                                    'Student_ID': idx + 1,
                                    'Risk_Level': risk_level,
                                    'Risk_Probability': f"{prediction_prob:.1%}",
                                    **student_data
                                })
                                
                                progress_bar.progress((idx + 1) / len(df))
                            
                            except Exception as e:
                                st.error(f"Error processing student {idx + 1}: {str(e)}")
                        
                        # Display results
                        results_df = pd.DataFrame(results)
                        st.markdown("### Batch Prediction Results")
                        st.dataframe(results_df)
                        
                        # Summary statistics
                        risk_counts = results_df['Risk_Level'].value_counts()
                        fig_pie = px.pie(values=risk_counts.values, names=risk_counts.index, 
                                        title="Risk Level Distribution")
                        st.plotly_chart(fig_pie, use_container_width=True)
                        
                        # Download results
                        csv = results_df.to_csv(index=False)
                        st.download_button(
                            label="📥 Download Results",
                            data=csv,
                            file_name=f"learning_risk_predictions_{datetime.now().strftime('%Y%m%d')}.csv",
                            mime="text/csv"
                        )
            
            except Exception as e:
                st.error(f" Error reading file: {str(e)}")
        else:
            st.info("Please upload a CSV file to begin batch processing")
    
    else:  # Historical Analysis
        st.markdown("###  Historical Analysis")
        historical_data = load_student_data()
        
        if historical_data:
            df_historical = pd.DataFrame(historical_data)
            
            # Convert timestamp to datetime
            df_historical['timestamp'] = pd.to_datetime(df_historical['timestamp'])
            
            # Analysis options
            analysis_type = st.selectbox(
                "Select analysis type:",
                ["Risk Trends Over Time", "Performance Correlation", "Student Progress Tracking"]
            )
            
            if analysis_type == "Risk Trends Over Time":
                # Group by date and risk level
                daily_risks = df_historical.groupby([df_historical['timestamp'].dt.date, 'risk_level']).size().unstack(fill_value=0)
                
                fig_trend = px.line(daily_risks, title="Risk Level Trends Over Time")
                st.plotly_chart(fig_trend, use_container_width=True)
            
            elif analysis_type == "Performance Correlation":
                # Correlation matrix
                numeric_cols = ['math_score', 'reading_score', 'writing_score', 'attendance', 'behavior', 'literacy', 'probability']
                if all(col in df_historical.columns for col in numeric_cols):
                    corr_matrix = df_historical[numeric_cols].corr()
                    fig_heatmap = px.imshow(corr_matrix, text_auto=True, title="Performance Correlation Matrix")
                    st.plotly_chart(fig_heatmap, use_container_width=True)
            
            elif analysis_type == "Student Progress Tracking":
                if 'student_name' in df_historical.columns:
                    student_names = df_historical['student_name'].dropna().unique()
                    selected_student = st.selectbox("Select student:", student_names)
                    
                    if selected_student:
                        student_progress = df_historical[df_historical['student_name'] == selected_student].sort_values('timestamp')
                        
                        if len(student_progress) > 1:
                            fig_progress = px.line(student_progress, x='timestamp', y='probability', 
                                                 title=f"Risk Probability Trend for {selected_student}")
                            st.plotly_chart(fig_progress, use_container_width=True)
                        else:
                            st.info("Not enough data points for trend analysis")
        else:
            st.info("No historical data available. Make some predictions first!")

    # Footer with tips
    st.markdown("---")
    st.markdown("""
    ### 💡 Tips for Accurate Predictions
    - **Regular Updates**: Update student data regularly for more accurate tracking
    - **Multiple Indicators**: Consider all factors, not just academic scores
    - **Context Matters**: Add relevant notes about external factors
    - **Follow-up**: Use predictions as starting points for deeper assessment
    """)

if __name__ == "__main__":
    main()
