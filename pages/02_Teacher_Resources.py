import streamlit as st
import pandas as pd
import json
from datetime import datetime
import random
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
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

st.set_page_config(
    page_title=f"{get_text('teacher_resources', language)} - EduScan", 
    page_icon="⭕",
    layout="wide"
)

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
    
    .resource-card {
        background: white;
        padding: 1.5rem;
        border-radius: 0.75rem;
        box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1);
        border: 1px solid #e5e7eb;
        margin-bottom: 1.5rem;
    }
    
    .resource-title {
        color: #1f2937;
        font-size: 1.125rem;
        font-weight: 600;
        margin-bottom: 1rem;
    }
    
    .teacher-header {
        background: linear-gradient(135deg, #00A86B 0%, #32CD32 100%);
        color: white;
        padding: 2rem;
        border-radius: 20px;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
        position: relative;
        overflow: hidden;
    }
    
    .teacher-header::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: url('attached_assets/Exam-Students_1750847086459.jpg
        opacity: 0.1;
        z-index: 0;
    }
    
    .teacher-header > * {
        position: relative;
        z-index: 1;
    }
    
    .resource-section {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(10px);
        padding: 2rem;
        border-radius: 20px;
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
        border: 1px solid rgba(255,255,255,0.18);
        margin: 1rem 0;
    }
    
    .strategy-card {
        background: rgba(255, 255, 255, 0.9);
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        border-left: 4px solid #00A86B;
    }
    
    .teacher-showcase {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
        gap: 1.5rem;
        margin: 2rem 0;
    }
    
    .teacher-card {
        text-align: center;
        background: rgba(255, 255, 255, 0.9);
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 8px 25px rgba(0,0,0,0.1);
        transition: transform 0.3s ease;
    }
    
    .teacher-card:hover {
        transform: translateY(-5px);
    }
    
    .teacher-card img {
        width: 100%;
        height: 150px;
        object-fit: cover;
        border-radius: 10px;
        margin-bottom: 1rem;
    }
    
    .highlight-text {
        background: linear-gradient(135deg, #00A86B, #32CD32);
        -webkit-background-clip: text;
        background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

def generate_activity(difficulty_type, grade_level):
    """Generate a random educational activity based on difficulty type and grade level"""
    
    activities = {
        "reading": {
            "K-2": [
                "Picture book discussion with visual cues",
                "Letter sound matching games",
                "Simple word building with letter tiles",
                "Reading comprehension with picture support",
                "Phonics songs and rhyming activities"
            ],
            "3-5": [
                "Graphic organizer for story elements",
                "Vocabulary word maps with illustrations",
                "Partner reading with guided questions",
                "Reading response journals with prompts",
                "Text-to-self connection activities"
            ],
            "6-8": [
                "Literature circles with differentiated roles",
                "Character analysis using graphic organizers",
                "Compare and contrast essays with templates",
                "Research projects with structured guidelines",
                "Reading strategy instruction (summarizing, questioning)"
            ]
        },
        "math": {
            "K-2": [
                "Hands-on counting with manipulatives",
                "Visual number line activities",
                "Shape recognition through real-world objects",
                "Simple addition/subtraction with pictures",
                "Math story problems with visual supports"
            ],
            "3-5": [
                "Fraction circles and visual representations",
                "Word problem solving with step-by-step guides",
                "Math journals for problem-solving strategies",
                "Multiplication games with visual arrays",
                "Real-world math applications (cooking, shopping)"
            ],
            "6-8": [
                "Algebra tiles for equation solving",
                "Geometric constructions with technology",
                "Data analysis projects with real data",
                "Mathematical modeling activities",
                "Peer tutoring for complex problem solving"
            ]
        },
        "writing": {
            "K-2": [
                "Picture prompts for creative writing",
                "Sentence frames for structured writing",
                "Interactive writing with teacher support",
                "Story sequencing activities",
                "Simple poetry with repetitive patterns"
            ],
            "3-5": [
                "Graphic organizers for essay planning",
                "Peer editing with specific checklists",
                "Multi-step writing process instruction",
                "Genre studies with mentor texts",
                "Writing conferences with guided feedback"
            ],
            "6-8": [
                "Research paper scaffolding with templates",
                "Argumentative writing with evidence support",
                "Creative writing workshops",
                "Digital storytelling projects",
                "Collaborative writing assignments"
            ]
        },
        "behavior": {
            "All": [
                "Positive behavior reinforcement system",
                "Clear classroom expectations with visual reminders",
                "Break cards for self-regulation",
                "Mindfulness and breathing exercises",
                "Social skills practice through role-play",
                "Sensory break activities",
                "Peer mentoring programs",
                "Goal-setting and progress tracking",
                "Conflict resolution strategies",
                "Emotional regulation techniques"
            ]
        }
    }
    
    if difficulty_type == "behavior":
        return random.choice(activities[difficulty_type]["All"])
    else:
        grade_group = "K-2" if grade_level in ["K", "1", "2"] else "3-5" if grade_level in ["3", "4", "5"] else "6-8"
        return random.choice(activities[difficulty_type].get(grade_group, activities[difficulty_type]["3-5"]))

def main():
    # Add CSS styling to match main app
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');
        
        .stApp {
            font-family: 'Poppins', sans-serif !important;
            background-color: #f8fafc !important;
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
        
        .resource-card {
            background: white;
            padding: 1.5rem;
            border-radius: 0.75rem;
            box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1);
            border: 1px solid #e5e7eb;
            margin-bottom: 1.5rem;
        }
        
        .resource-title {
            color: #1f2937;
            font-size: 1.125rem;
            font-weight: 600;
            margin-bottom: 1rem;
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Page header
    st.markdown(f"""
    <div class="page-header">
        <h1 class="page-title">{get_text('teacher_resources', language)}</h1>
    </div>
    """, unsafe_allow_html=True)
    
    # Dashboard header
    st.markdown(f"""
    <div class="dashboard-header">
        <h1 class="page-title">{get_text('teacher_resources', language)}</h1>
    </div>
    """, unsafe_allow_html=True)

    # Enhanced header for teacher resources
    st.markdown(f"""
    <div class="teacher-header">
        <h1>{get_text('excellence_in_education', language)}</h1>
        <h2>{get_text('empowering_teachers', language)}</h2>
        <p style="font-size: 1.2em; opacity: 0.9;">
            {get_text('professional_development', language)}
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Teacher showcase section with base64 images
    b64_images = get_base64_images()
    
    st.markdown(f"""
    <div class="resource-section">
        <h2 class="highlight-text">{get_text('supporting_every_teacher', language)}</h2>
        <div class="teacher-showcase">
            <div class="teacher-card">
                {get_b64_image_html(b64_images['inclusive_classroom_2'], "Inclusive classroom", "100%", "150px")}
                <h4>{get_text('inclusive_classroom_excellence', language)}</h4>
                <p>{get_text('create_learning_environments', language)}</p>
            </div>
            <div class="teacher-card">
                {get_b64_image_html(b64_images['professional_collaboration'], "Teacher collaboration", "100%", "150px")}
                <h4>{get_text('professional_collaboration', language)}</h4>
                <p>{get_text('build_strong_partnerships', language)}</p>
            </div>
            <div class="teacher-card">
                {get_b64_image_html(b64_images['engaging_strategies'], "Student engagement", "100%", "150px")}
                <h4>{get_text('engaging_learning_strategies', language)}</h4>
                <p>{get_text('implement_culturally_responsive', language)}</p>
            </div>
            <div class="teacher-card">
                {get_b64_image_html(b64_images['assessment_innovation'], "Assessment strategies", "100%", "150px")}
                <h4>{get_text('assessment_innovation', language)}</h4>
                <p>{get_text('use_multiple_assessment', language)}</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Add authentic teaching images
    st.markdown(f"### {get_text('teaching_excellence_showcase', language)}")
    images = get_student_images()
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(get_image_html(images['exam_students'], "Classroom Excellence", "100%", "150px"), unsafe_allow_html=True)
    with col2:
        st.markdown(get_image_html(images['happy_students'], "Student Engagement", "100%", "150px"), unsafe_allow_html=True)
    with col3:
        st.markdown(get_image_html(images['focused_student'], "Learning Focus", "100%", "150px"), unsafe_allow_html=True)
    with col4:
        st.markdown(get_image_html(images['student_portrait'], "Academic Growth", "100%", "150px"), unsafe_allow_html=True)
    
    # Sidebar navigation
    with st.sidebar:
        st.markdown(f"### {get_text('resource_categories', language)}")
        resource_type = st.selectbox(
            get_text('choose_resource_type', language),
            [
                get_text('differentiated_learning_strategies', language),
                get_text('inclusive_classroom_tips', language), 
                get_text('intervention_techniques', language),
                get_text('assessment_strategies', language),
                get_text('activity_generator', language),
                get_text('professional_development', language)
            ]
        )
    
    if resource_type == "Differentiated Learning Strategies":
        st.markdown("## Differentiated Learning Strategies")
        
        tab1, tab2, tab3, tab4 = st.tabs(["Reading", "Mathematics", "Writing", "General Strategies"])
        
        with tab1:
            st.markdown("""
            ### Reading Differentiation Strategies
            
            #### **For Students with Reading Difficulties:**
            
            **Phonics and Decoding Support**
            - Use multi-sensory phonics instruction (visual, auditory, kinesthetic)
            - Implement systematic phonics programs with explicit instruction
            - Provide word families and pattern recognition activities
            - Use color-coding for different sound patterns
            
            **Reading Comprehension Support**
            - Pre-teach vocabulary with visual supports
            - Use graphic organizers for story elements
            - Implement guided reading with leveled texts
            - Provide audio books and text-to-speech technology
            
            **🎧 Assistive Technology**
            - Text-to-speech software
            - Digital highlighters and annotation tools
            - Reading apps with built-in supports
            - Voice recording for reading practice
            """)
            
            with st.expander("List Reading Intervention Checklist"):
                st.markdown("""
                - [ ] Assess current reading level and specific difficulties
                - [ ] Set realistic, measurable reading goals
                - [ ] Provide daily phonics instruction (15-20 minutes)
                - [ ] Use high-interest, low-level reading materials
                - [ ] Implement peer reading partnerships
                - [ ] Monitor progress weekly with running records
                - [ ] Celebrate small victories and progress
                """)
        
        with tab2:
            st.markdown("""
            ### Mathematics Differentiation Strategies
            
            #### **For Students with Math Difficulties:**
            
            **Conceptual Understanding**
            - Use concrete manipulatives before abstract concepts
            - Implement visual math strategies (number lines, charts)
            - Break complex problems into smaller steps
            - Use real-world connections and applications
            
            **Chart Problem-Solving Support**
            - Provide step-by-step problem-solving templates
            - Use graphic organizers for word problems
            - Teach multiple solution strategies
            - Allow extra processing time
            
            **🔧 Tools and Accommodations**
            - Calculator use for appropriate tasks
            - Graph paper for organization
            - Visual fraction models
            - Math fact reference sheets
            """)
            
            with st.expander("Math Support Strategies"):
                st.markdown("""
                **Number Sense Building:**
                - Daily number talks (5-10 minutes)
                - Skip counting practice
                - Number pattern recognition
                - Estimation activities
                
                **Fact Fluency:**
                - Timed practice with progress tracking
                - Math fact games and apps
                - Visual multiplication charts
                - Strategic fact family instruction
                """)
        
        with tab3:
            st.markdown("""
            ### Writing Differentiation Strategies
            
            #### **For Students with Writing Difficulties:**
            
            **Note Writing Process Support**
            - Use graphic organizers for planning
            - Provide sentence and paragraph frames
            - Implement peer editing with specific guidelines
            - Allow voice-to-text technology
            
            **🎨 Creative Expression**
            - Offer choice in writing topics and formats
            - Use visual prompts and story starters
            - Implement interactive writing activities
            - Encourage multimedia presentations
            
            **✏️ Mechanics and Conventions**
            - Teach grammar in context
            - Use editing checklists and rubrics
            - Provide spelling support tools
            - Focus on one writing skill at a time
            """)
        
        with tab4:
            st.markdown("""
            ### Brain General Differentiation Strategies
            
            #### **Universal Design for Learning (UDL) Principles:**
            
            **Multiple Means of Representation**
            - Present information in various formats (visual, auditory, hands-on)
            - Use multimedia resources
            - Provide background knowledge activation
            - Offer multiple examples and non-examples
            
            **⚡ Multiple Means of Engagement**
            - Offer choices in topics, tools, and learning environment
            - Connect to student interests and cultural backgrounds
            - Provide appropriate challenges for all learners
            - Foster collaboration and community
            
            **🛠️ Multiple Means of Expression**
            - Allow various ways to demonstrate knowledge
            - Provide options for physical action and movement
            - Support planning and strategy development
            - Use assistive technologies as needed
            """)
    
    elif resource_type == "Inclusive Classroom Tips":
        st.markdown("##  Inclusive Classroom Environment")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            ### 🌈 Creating an Inclusive Environment
            
            **Physical Environment:**
            -  Flexible seating options (standing desks, stability balls, quiet corners)
            -  Clear visual schedules and expectations posted
            -  Sensory-friendly spaces for breaks
            -  Well-organized materials with visual labels
            -  Adequate lighting and minimal distractions
            
            **Social Environment:**
            -  Celebrate diverse learning styles and strengths
            -  Teach empathy and understanding of differences
            -  Implement peer support systems
            -  Use person-first language
            -  Foster a growth mindset culture
            """)
            
            st.markdown("""
            ### 🤝 Collaboration Strategies
            
            **With Special Education Teachers:**
            - Regular co-planning sessions
            - Shared responsibility for all students
            - Consistent communication about student progress
            - Joint problem-solving for challenges
            
            **With Parents/Families:**
            - Regular communication about strategies that work
            - Home-school consistency in approaches
            - Shared goal setting
            - Cultural responsiveness and sensitivity
            """)
        
        with col2:
            st.markdown("""
            ### List Daily Inclusive Practices
            
            **Morning Routines:**
            - Visual schedules for predictability
            - Greeting choices (handshake, high-five, wave)
            - Check-in systems for emotional regulation
            - Preview of the day's activities
            
            **During Instruction:**
            - Clear, concise directions with visual supports
            - Frequent check-ins and feedback
            - Movement breaks built into lessons
            - Multiple ways to participate
            
            **Behavior Support:**
            - Positive behavior intervention systems
            - Clear expectations with visual reminders
            - Teaching replacement behaviors
            - Restorative justice approaches
            """)
            
            with st.expander("Inclusive Teaching Checklist"):
                st.markdown("""
                **Daily Self-Check:**
                - [ ] Did I provide multiple ways to access content today?
                - [ ] Did I offer choices in how students demonstrated learning?
                - [ ] Did I check in with students who need extra support?
                - [ ] Did I celebrate diverse contributions and perspectives?
                - [ ] Did I use clear, consistent language and expectations?
                - [ ] Did I provide appropriate challenges for all learners?
                """)
    
    elif resource_type == "Intervention Techniques":
        st.markdown("## Evidence-Based Intervention Techniques")
        
        intervention_area = st.selectbox(
            "Select intervention focus:",
            ["Reading Interventions", "Math Interventions", "Behavioral Interventions", "Executive Function Support"]
        )
        
        if intervention_area == "Reading Interventions":
            st.markdown("""
            ### Tier 2 & 3 Reading Interventions
            
            #### **Systematic Phonics Interventions**
            - **Orton-Gillingham Approach**: Multi-sensory phonics instruction
            - **Wilson Reading System**: Structured literacy program
            - **REWARDS**: Reading strategies for older students
            - **Duration**: 30-45 minutes daily, 12-16 weeks minimum
            
            #### **Fluency Interventions**
            - **Repeated Reading**: Practice with the same text multiple times
            - **Paired Reading**: Student and tutor read together
            - **Reader's Theater**: Performance-based fluency practice
            - **Goal**: Increase words per minute and expression
            
            #### **Comprehension Interventions**
            - **Reciprocal Teaching**: Students take turns leading discussions
            - **Graphic Organizers**: Visual supports for understanding
            - **Question-Answer Relationships**: Teaching question types
            - **Think-Alouds**: Modeling comprehension strategies
            """)
            
            # Interactive intervention tracker
            st.markdown("#### Chart Intervention Progress Tracker")
            
            with st.form("reading_intervention_form"):
                student_name = st.text_input("Student Name")
                intervention_type = st.selectbox("Intervention Type", 
                    ["Phonics", "Fluency", "Comprehension", "Vocabulary"])
                baseline_score = st.number_input("Baseline Score", min_value=0, max_value=100)
                current_score = st.number_input("Current Score", min_value=0, max_value=100)
                weeks_elapsed = st.number_input("Weeks of Intervention", min_value=1, max_value=52)
                notes = st.text_area("Progress Notes")
                
                if st.form_submit_button("Track Progress"):
                    progress = current_score - baseline_score
                    rate = progress / weeks_elapsed if weeks_elapsed > 0 else 0
                    
                    st.success(f"Progress tracked for {student_name}")
                    st.metric("Score Improvement", f"{progress} points", f"{rate:.1f} pts/week")
        
        elif intervention_area == "Math Interventions":
            st.markdown("""
            ### Intensive Math Interventions
            
            #### **Number Sense Interventions**
            - **Number Worlds**: Comprehensive number sense program
            - **TouchMath**: Multi-sensory approach to basic facts
            - **Number Line Activities**: Visual representation of number relationships
            - **Subitizing Practice**: Quick recognition of small quantities
            
            #### **Fact Fluency Interventions**
            - **Math Facts in a Flash**: Systematic fact practice
            - **Rocket Math**: Timed practice with progression
            - **Computer-Based Programs**: Adaptive fact practice
            - **Goal**: Automatic recall of basic facts
            
            #### **Problem-Solving Interventions**
            - **Schema-Based Instruction**: Teaching problem types
            - **Concrete-Representational-Abstract**: Gradual release model
            - **Math Talk**: Verbalization of thinking processes
            - **Error Analysis**: Learning from mistakes
            """)
        
        elif intervention_area == "Behavioral Interventions":
            st.markdown("""
            ### Behavioral Support Interventions
            
            #### **Positive Behavior Interventions and Supports (PBIS)**
            - **Tier 1**: Universal classroom management
            - **Tier 2**: Targeted group interventions
            - **Tier 3**: Intensive individual supports
            - **Focus**: Prevention and positive reinforcement
            
            #### **Self-Regulation Strategies**
            - **Zones of Regulation**: Emotional awareness and control
            - **Mindfulness Practices**: Breathing and centering techniques
            - **Break Cards**: Self-advocacy for regulation needs
            - **Goal Setting**: Student-directed behavior goals
            
            #### **Social Skills Interventions**
            - **Social Stories**: Narrative-based skill instruction
            - **Role Playing**: Practice in safe environments
            - **Peer Mediation**: Student-led conflict resolution
            - **Circle Time**: Community building and problem-solving
            """)
        
        else:  # Executive Function Support
            st.markdown("""
            ### Brain Executive Function Support
            
            #### **Organization Strategies**
            - **Color-Coding Systems**: Different subjects, different colors
            - **Checklists and Templates**: Step-by-step guidance
            - **Digital Organization Tools**: Apps and platforms
            - **Clean Desk Policy**: Minimize distractions
            
            #### **Time Management Support**
            - **Visual Schedules**: Picture or text-based daily schedules
            - **Timer Use**: Breaking tasks into manageable chunks
            - **Transition Warnings**: 5-minute, 2-minute notices
            - **Priority Ranking**: Teaching importance vs. urgency
            
            #### **Working Memory Support**
            - **Chunking Information**: Breaking into smaller parts
            - **Rehearsal Strategies**: Repetition and practice
            - **External Memory Aids**: Notes, recordings, visuals
            - **Reduce Cognitive Load**: Simplify instructions
            """)
    
    elif resource_type == "Activity Generator":
        st.markdown("## 🎮 Interactive Activity Generator")
        st.markdown("Generate customized activities for students with learning difficulties")
        
        col1, col2 = st.columns(2)
        
        with col1:
            difficulty_type = st.selectbox(
                "Select area of difficulty:",
                ["reading", "math", "writing", "behavior"]
            )
            
            grade_level = st.selectbox(
                "Select grade level:",
                ["K", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12"]
            )
        
        with col2:
            group_size = st.selectbox(
                "Group size:",
                ["Individual", "Small Group (2-4)", "Large Group (5+)", "Whole Class"]
            )
            
            time_available = st.selectbox(
                "Time available:",
                ["5-10 minutes", "15-20 minutes", "30+ minutes", "Full lesson"]
            )
        
        if st.button("Generate Activity", type="primary"):
            activity = generate_activity(difficulty_type, grade_level)
            
            st.markdown("### Generated Activity")
            st.info(f"**Activity**: {activity}")
            
            # Additional details based on selections
            if difficulty_type == "reading":
                materials = ["Leveled books", "Graphic organizers", "Vocabulary cards", "Audio recordings"]
                objectives = ["Improve decoding skills", "Enhance comprehension", "Build vocabulary", "Increase fluency"]
            elif difficulty_type == "math":
                materials = ["Manipulatives", "Calculator", "Graph paper", "Visual aids"]
                objectives = ["Build number sense", "Improve problem-solving", "Practice facts", "Understand concepts"]
            elif difficulty_type == "writing":
                materials = ["Graphic organizers", "Word banks", "Sentence frames", "Editing checklists"]
                objectives = ["Improve organization", "Build vocabulary", "Practice mechanics", "Enhance creativity"]
            else:  # behavior
                materials = ["Visual cues", "Timer", "Reward system", "Calm down area"]
                objectives = ["Self-regulation", "Social skills", "Focus attention", "Follow directions"]
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**List Materials Needed:**")
                for material in materials[:3]:  # Show 3 relevant materials
                    st.write(f"• {material}")
            
            with col2:
                st.markdown("**Learning Objectives:**")
                for objective in objectives[:3]:  # Show 3 relevant objectives
                    st.write(f"• {objective}")
            
            # Adaptation suggestions
            st.markdown("### 🔧 Adaptation Suggestions")
            
            adaptations = {
                "Individual": "Provide one-on-one support and immediate feedback",
                "Small Group (2-4)": "Encourage peer collaboration and shared learning",
                "Large Group (5+)": "Use cooperative learning structures and clear roles",
                "Whole Class": "Implement universal supports and multiple ways to participate"
            }
            
            time_adaptations = {
                "5-10 minutes": "Focus on one specific skill with quick practice",
                "15-20 minutes": "Include instruction, practice, and brief reflection",
                "30+ minutes": "Full lesson with modeling, guided practice, and independent work",
                "Full lesson": "Complete learning cycle with assessment and extension"
            }
            
            st.write(f"**Group Size Adaptation**: {adaptations[group_size]}")
            st.write(f"**Time Adaptation**: {time_adaptations[time_available]}")
    
    elif resource_type == "Professional Development":
        st.markdown("## Professional Learning Modules")
        
        module_type = st.selectbox(
            "Choose learning module:",
            [
                "Understanding Learning Disabilities",
                "Evidence-Based Practices",
                "Assessment and Progress Monitoring",
                "Family Engagement",
                "Technology Integration"
            ]
        )
        
        if module_type == "Understanding Learning Disabilities":
            st.markdown("""
            ### Brain Understanding Learning Disabilities
            
            #### **Module Overview** (45 minutes)
            Learn about different types of learning disabilities and their characteristics.
            
            #### **Learning Objectives**
            By the end of this module, you will be able to:
            - Identify characteristics of common learning disabilities
            - Understand the neurological basis of learning differences
            - Recognize signs of learning difficulties in the classroom
            - Distinguish between learning disabilities and other factors
            
            #### **Content Sections**
            1. **Definition and Legal Framework** (10 minutes)
            2. **Types of Learning Disabilities** (15 minutes)
            3. **Identification and Assessment** (10 minutes)
            4. **Classroom Implications** (10 minutes)
            """)
            
            with st.expander("Section 1: Definition and Legal Framework"):
                st.markdown("""
                **What are Learning Disabilities?**
                
                Learning disabilities are neurologically-based processing problems that can interfere with learning basic skills such as reading, writing, or math. They can also interfere with higher level skills such as organization, time planning, abstract reasoning, long or short term memory, and attention.
                
                **Key Characteristics:**
                - Unexpected academic difficulty despite average or above-average intelligence
                - Significant discrepancy between potential and performance
                - Processing differences in specific areas
                - Lifelong condition that affects learning across settings
                
                **Legal Protections:**
                - Individuals with Disabilities Education Act (IDEA)
                - Section 504 of the Rehabilitation Act
                - Americans with Disabilities Act (ADA)
                """)
            
            with st.expander("Section 2: Types of Learning Disabilities"):
                st.markdown("""
                **Specific Learning Disability Categories:**
                
                **1. Dyslexia (Reading)**
                - Difficulty with accurate and/or fluent word recognition
                - Poor spelling and decoding abilities
                - Often results from deficit in phonological component of language
                
                **2. Dyscalculia (Mathematics)**
                - Difficulty with number sense, number facts, and calculation
                - Problems with mathematical reasoning
                - Challenges with math concepts and problem-solving
                
                **3. Dysgraphia (Writing)**
                - Difficulty with handwriting, spelling, and written expression
                - Problems with fine motor skills affecting writing
                - Challenges organizing thoughts on paper
                
                **4. Language Processing Disorders**
                - Difficulty understanding and using spoken language
                - Problems with listening comprehension
                - Challenges with verbal expression
                """)
        
        elif module_type == "Evidence-Based Practices":
            st.markdown("""
            ### Evidence-Based Practices for Learning Disabilities
            
            #### **High-Impact Instructional Strategies**
            
            **1. Explicit Instruction**
            - Clear learning objectives
            - Systematic skill progression
            - Immediate feedback
            - Multiple practice opportunities
            
            **2. Systematic Instruction**
            - Logical sequence of skills
            - Prerequisite skill development
            - Cumulative review
            - Mastery-based progression
            
            **3. Multi-sensory Instruction**
            - Visual, auditory, and kinesthetic input
            - Multiple pathways to learning
            - Enhanced memory and retention
            - Accommodates different learning styles
            """)
            
            research_studies = pd.DataFrame({
                "Practice": ["Explicit Instruction", "Peer Tutoring", "Graphic Organizers", "Self-Monitoring"],
                "Effect Size": [0.82, 0.74, 0.68, 0.61],
                "Grade Levels": ["K-12", "3-12", "3-12", "6-12"],
                "Subject Areas": ["All", "Reading/Math", "All", "All"]
            })
            
            st.markdown("#### Chart Research Evidence")
            st.dataframe(research_studies)
            st.caption("Effect sizes from meta-analyses of special education research")
    
    # Footer with quick links
    st.markdown("---")
    st.markdown("### 🔗 Quick Resources")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("Reading Strategies", use_container_width=True):
            st.info("Comprehensive reading support strategies loaded above!")
    
    with col2:
        if st.button("Math Support", use_container_width=True):
            st.info("Mathematics intervention techniques displayed above!")
    
    with col3:
        if st.button("Writing Help", use_container_width=True):
            st.info("Writing differentiation strategies shown above!")
    
    with col4:
        if st.button("Behavior Tips", use_container_width=True):
            st.info("Behavioral intervention strategies provided above!")

if __name__ == "__main__":
    main()
