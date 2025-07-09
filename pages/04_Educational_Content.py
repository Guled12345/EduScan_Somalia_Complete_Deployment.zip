import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
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
    page_title=f"{get_text('educational_content', language)} - EduScan",
    page_icon="⭕",
    layout="wide"
)

# CSS matching the main app design
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');
    

    
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
    
    .content-section {
        background: white;
        padding: 1.5rem;
        border-radius: 0.75rem;
        box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1);
        border: 1px solid #e5e7eb;
        margin-bottom: 1.5rem;
    }
    
    .education-header {
        background: linear-gradient(135deg, #8E44AD 0%, #3498DB 50%, #1ABC9C 100%);
        color: white;
        padding: 2rem;
        border-radius: 20px;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
        position: relative;
        overflow: hidden;
    }
    
    .education-header::before {
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
    
    .education-header > * {
        position: relative;
        z-index: 1;
    }
    
    .content-section {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(10px);
        padding: 2rem;
        border-radius: 20px;
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
        border: 1px solid rgba(255,255,255,0.18);
        margin: 1rem 0;
    }
    
    .research-showcase {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
        gap: 1.5rem;
        margin: 2rem 0;
    }
    
    .research-card {
        text-align: center;
        background: rgba(255, 255, 255, 0.9);
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 8px 25px rgba(0,0,0,0.1);
        transition: transform 0.3s ease;
        border-left: 4px solid #8E44AD;
    }
    
    .research-card:hover {
        transform: translateY(-5px);
    }
    
    .research-card img {
        width: 100%;
        height: 150px;
        object-fit: cover;
        border-radius: 10px;
        margin-bottom: 1rem;
    }
    
    .highlight-text {
        background: linear-gradient(135deg, #8E44AD, #3498DB);
        -webkit-background-clip: text;
        background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: bold;
    }
    
    .statistics-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 1rem;
        margin: 2rem 0;
    }
    
    .stat-highlight {
        background: linear-gradient(135deg, #8E44AD20, #3498DB20);
        padding: 1.5rem;
        border-radius: 15px;
        text-align: center;
        border: 2px solid #8E44AD30;
    }
</style>
""", unsafe_allow_html=True)

def main():
    # Page header
    st.markdown(f"""
    <div class="page-header">
        <h1 class="page-title">{get_text('educational_content', language)}</h1>
    </div>
    """, unsafe_allow_html=True)
    
    # Add authentic educational images
    st.markdown(f"### {get_text('educational_excellence_in_action', language)}")
    images = get_student_images()
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(get_image_html(images['happy_young_students'], "Research Excellence", "100%", "200px"), unsafe_allow_html=True)
    with col2:
        st.markdown(get_image_html(images['teacher_with_students'], "Academic Focus", "100%", "200px"), unsafe_allow_html=True)
    
    # Research showcase section with base64 images
    b64_images = get_base64_images()
    
    st.markdown(f"""
    <div class="content-section">
        <h2 class="highlight-text">{get_text('building_educational_excellence', language)}</h2>
        <div class="research-showcase">
            <div class="research-card">
                {get_b64_image_html(b64_images['global_practices'], "Educational research", "100%", "150px")}
                <h4>{get_text('global_best_practices', language)}</h4>
                <p>{get_text('international_standards', language)}</p>
            </div>
            <div class="research-card">
                {get_b64_image_html(b64_images['learning_science'], "Learning research", "100%", "150px")}
                <h4>{get_text('learning_science', language)}</h4>
                <p>{get_text('neuroscience_cognitive_research', language)}</p>
            </div>
            <div class="research-card">
                {get_b64_image_html(b64_images['intervention_studies'], "Intervention studies", "100%", "150px")}
                <h4>{get_text('intervention_studies', language)}</h4>
                <p>{get_text('evidence_based_strategies', language)}</p>
            </div>
            <div class="research-card">
                {get_b64_image_html(b64_images['cultural_adaptation'], "Cultural education", "100%", "150px")}
                <h4>{get_text('cultural_adaptation', language)}</h4>
                <p>{get_text('implementing_inclusive_education', language)}</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Add comprehensive student gallery
    st.markdown(f"### {get_text('educational_research_impact', language)}")
    images = get_student_images()
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(get_image_html(images['boys_in_classroom'], "Research Impact", "100%", "150px"), unsafe_allow_html=True)
    with col2:
        st.markdown(get_image_html(images['classroom_girls'], "Student Success", "100%", "150px"), unsafe_allow_html=True)
    with col3:
        st.markdown(get_image_html(images['happy_young_students'], "Learning Focus", "100%", "150px"), unsafe_allow_html=True)
    with col4:
        st.markdown(get_image_html(images['teacher_with_students'], "Educational Achievement", "100%", "150px"), unsafe_allow_html=True)
    
    # Sidebar navigation
    with st.sidebar:
        st.markdown(f"### {get_text('content_categories', language)}")
        content_type = st.selectbox(
            get_text('choose_content_type', language),
            [
                get_text('research_overview', language),
                get_text('types_learning_difficulties', language), 
                get_text('early_intervention', language),
                get_text('academic_resources', language),
                get_text('technology_tools', language),
                get_text('support_strategies', language)
            ]
        )
        
        st.markdown(f"### {get_text('target_audience', language)}")
        audience = st.selectbox(
            get_text('content_for', language),
            [get_text('teachers', language), get_text('parents', language), get_text('administrators', language), get_text('all', language)]
        )

    if content_type == get_text('research_overview', language):
        st.markdown(f"## {get_text('research_overview', language)}: {get_text('types_learning_difficulties', language)}")
        
        tab1, tab2, tab3 = st.tabs([get_text('statistics', language), get_text('neuroscience', language), get_text('impact_studies', language)])
        
        with tab1:
            st.markdown(f"### {get_text('learning_difficulties_statistics', language)}")
            
            # Create statistical visualizations
            prevalence_data = {
                "Type": ["Dyslexia", "ADHD", "Dyscalculia", "Dysgraphia", "Language Disorders", "Other"],
                "Prevalence (%)": [5.0, 11.0, 3.5, 4.0, 7.0, 2.5],
                "Description": [
                    "Reading and language processing difficulties",
                    "Attention deficit hyperactivity disorder", 
                    "Mathematical learning difficulties",
                    "Writing and fine motor difficulties",
                    "Spoken language comprehension issues",
                    "Other specific learning disabilities"
                ]
            }
            
            fig_prevalence = px.pie(
                prevalence_data, 
                values="Prevalence (%)", 
                names="Type",
                title="Prevalence of Learning Difficulties in School-Age Children"
            )
            st.plotly_chart(fig_prevalence, use_container_width=True)
            
            # Statistics table
            st.markdown("#### Detailed Statistics")
            stats_df = pd.DataFrame(prevalence_data)
            st.dataframe(stats_df, use_container_width=True)
            
            # Key statistics
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Students Affected", "15-20%", "of all students")
            
            with col2:
                st.metric("Early Identification", "< 30%", "before age 8")
            
            with col3:
                st.metric("Gender Ratio", "2:1", "Male to Female")
            
            with col4:
                st.metric("Improvement Rate", "80%", "with intervention")
        
        with tab2:
            st.markdown("### Brain Neuroscience of Learning Difficulties")
            
            st.markdown("""
            #### **Brain-Based Understanding**
            
            Learning difficulties are neurobiological in origin, involving differences in brain structure and function:
            
            **Key Brain Areas Affected:**
            
            **1. Left Hemisphere Language Areas**
            - Broca's Area: Speech production and grammar
            - Wernicke's Area: Language comprehension
            - Angular Gyrus: Word recognition and reading
            
            **2. Phonological Processing Networks**
            - Difficulty connecting sounds to letters
            - Reduced activation in reading circuits
            - Compensatory right hemisphere activation
            
            **3. Working Memory Systems**
            - Prefrontal cortex involvement
            - Information processing speed
            - Attention and executive function
            """)
            
            st.markdown("""
            #### **Neuroplasticity and Intervention**
            
            **🌟 The Brain's Ability to Change:**
            - Intensive intervention can create new neural pathways
            - Earlier intervention leads to greater plasticity
            - Multi-sensory approaches enhance brain connectivity
            - Practice strengthens neural networks
            
            **Research Evidence:**
            - fMRI studies show brain changes after intervention
            - Increased activation in reading networks
            - Improved connectivity between brain regions
            - Long-term structural brain changes possible
            """)
            
            # Intervention timeline
            st.markdown("#### ⏰ Critical Intervention Periods")
            
            timeline_data = {
                "Age Range": ["3-5 years", "6-8 years", "9-12 years", "13+ years"],
                "Brain Plasticity": ["Highest", "High", "Moderate", "Lower"],
                "Intervention Impact": ["Maximum", "High", "Moderate", "Requires intensity"],
                "Key Focus": [
                    "Language development, phonological awareness",
                    "Reading foundation, basic skills",
                    "Reading fluency, comprehension",
                    "Compensation strategies, technology"
                ]
            }
            
            timeline_df = pd.DataFrame(timeline_data)
            st.dataframe(timeline_df, use_container_width=True)
        
        with tab3:
            st.markdown("### Growth Impact and Intervention Studies")
            
            st.markdown("""
            #### **Major Research Findings**
            
            **National Reading Panel (2000)**
            - Systematic phonics instruction is essential
            - Phonemic awareness training improves reading
            - Guided oral reading builds fluency
            - Vocabulary instruction enhances comprehension
            
            **Meta-Analysis Studies**
            - Intensive intervention shows large effect sizes (0.8+)
            - Early intervention prevents reading failure
            - Multi-component approaches most effective
            - Technology tools can enhance traditional methods
            """)
            
            # Create intervention effectiveness chart
            intervention_data = {
                "Intervention Type": [
                    "Phonics Instruction",
                    "Reading Fluency",
                    "Comprehension Strategies", 
                    "Vocabulary Training",
                    "Multi-sensory Approaches",
                    "Technology-Assisted"
                ],
                "Effect Size": [0.86, 0.71, 0.68, 0.62, 0.75, 0.58],
                "Grade Levels": ["K-3", "2-5", "3-8", "K-8", "K-8", "K-12"]
            }
            
            fig_effectiveness = px.bar(
                intervention_data,
                x="Effect Size",
                y="Intervention Type",
                orientation='h',
                title="Intervention Effectiveness (Effect Sizes from Research)"
            )
            st.plotly_chart(fig_effectiveness, use_container_width=True)
            
            st.markdown("""
            #### **Longitudinal Study Results**
            
            **Connecticut Longitudinal Study (Shaywitz et al.)**
            - Followed 445 children from kindergarten to grade 12
            - Reading difficulties persist without intervention
            - Early identification and intervention crucial
            - Brain imaging shows intervention changes neural pathways
            
            **Chart Key Outcomes:**
            - 74% of poor readers in grade 3 remain poor readers in grade 9
            - Intensive intervention can normalize reading performance
            - Academic and social benefits extend beyond reading
            - Self-esteem and motivation significantly improve
            """)

    elif content_type == "Types of Learning Difficulties":
        st.markdown("## 🧩 Types of Learning Difficulties")
        
        difficulty_type = st.selectbox(
            "Select learning difficulty:",
            ["Dyslexia", "Dyscalculia", "Dysgraphia", "ADHD", "Language Processing", "Executive Function"]
        )
        
        if difficulty_type == "Dyslexia":
            st.markdown("""
            ### Dyslexia: Reading and Language Processing
            
            #### **Definition and Characteristics**
            Dyslexia is a neurobiological condition affecting reading and language processing despite adequate intelligence and instruction.
            
            **Core Characteristics:**
            - Difficulty with accurate and/or fluent word recognition
            - Poor spelling and decoding abilities
            - Challenges with phonological processing
            - Reading comprehension may be affected
            
            ** Observable Signs by Age:**
            """)
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown("""
                **Ages 3-5:**
                - Delayed speech development
                - Difficulty rhyming
                - Problems learning alphabet
                - Trouble following directions
                """)
            
            with col2:
                st.markdown("""
                **Ages 6-8:**
                - Slow reading progress
                - Difficulty sounding out words
                - Confusing similar words
                - Avoiding reading activities
                """)
            
            with col3:
                st.markdown("""
                **Ages 9+:**
                - Reading below grade level
                - Difficulty with comprehension
                - Poor spelling despite instruction
                - Avoiding written work
                """)
            
            st.markdown("""
            #### **Brain Neurological Basis**
            - Differences in left hemisphere language areas
            - Reduced connectivity in reading networks
            - Phonological processing deficits
            - Working memory challenges
            
            #### **Effective Interventions**
            - Systematic, explicit phonics instruction
            - Multi-sensory reading programs (Orton-Gillingham, Wilson)
            - Structured literacy approaches
            - Assistive technology support
            """)
        
        elif difficulty_type == "Dyscalculia":
            st.markdown("""
            ### Dyscalculia: Mathematical Learning Difficulties
            
            #### **Definition and Characteristics**
            Dyscalculia is a specific learning difficulty affecting mathematical understanding and computation.
            
            **Core Characteristics:**
            - Difficulty understanding number concepts
            - Problems with mathematical reasoning
            - Challenges with calculation and computation
            - Difficulty understanding mathematical symbols
            
            **Chart Common Manifestations:**
            """)
            
            manifestations = {
                "Area": [
                    "Number Sense",
                    "Calculation",
                    "Problem Solving",
                    "Mathematical Reasoning"
                ],
                "Difficulties": [
                    "Understanding quantity, comparing numbers, number line concepts",
                    "Basic arithmetic facts, multi-step calculations, algorithms",
                    "Word problems, mathematical language, applying concepts",
                    "Patterns, relationships, abstract mathematical thinking"
                ],
                "Support Strategies": [
                    "Visual number representations, manipulatives, number lines",
                    "Break down steps, provide algorithms, use calculators",
                    "Graphic organizers, key word strategies, real-world connections",
                    "Concrete examples, visual models, step-by-step instruction"
                ]
            }
            
            manifestations_df = pd.DataFrame(manifestations)
            st.dataframe(manifestations_df, use_container_width=True)
        
        elif difficulty_type == "Dysgraphia":
            st.markdown("""
            ### Dysgraphia: Writing Difficulties
            
            #### **Definition and Characteristics**
            Dysgraphia is a neurological condition affecting written expression and fine motor skills.
            
            **Types of Dysgraphia:**
            
            **1. Dyslexic Dysgraphia**
            - Legible copying but illegible spontaneous writing
            - Normal finger-tapping speed
            - Related to phonological processing
            
            **2. Motor Dysgraphia**
            - Illegible copying and spontaneous writing
            - Slow finger-tapping speed
            - Fine motor skill difficulties
            
            **3. Spatial Dysgraphia**
            - Illegible copying, normal spontaneous writing
            - Normal finger-tapping speed
            - Visual-spatial processing issues
            """)
            
            # Support strategies table
            st.markdown("#### Support Strategies by Type")
            
            support_data = {
                "Strategy Category": [
                    "Physical Accommodations",
                    "Technology Support", 
                    "Instruction Modifications",
                    "Assessment Alternatives"
                ],
                "Specific Strategies": [
                    "Pencil grips, slanted writing surface, alternative seating",
                    "Word processors, speech-to-text, digital note-taking",
                    "Break writing into steps, provide graphic organizers",
                    "Oral assessments, typed responses, extended time"
                ]
            }
            
            support_df = pd.DataFrame(support_data)
            st.dataframe(support_df, use_container_width=True)

    elif content_type == "Early Intervention":
        st.markdown("## 🚀 Early Intervention Strategies")
        
        intervention_focus = st.selectbox(
            "Intervention focus:",
            ["Pre-Reading Skills", "Early Math", "Language Development", "Social-Emotional"]
        )
        
        if intervention_focus == "Pre-Reading Skills":
            st.markdown("""
            ### Pre-Reading Skills Development
            
            #### **Essential Pre-Reading Components**
            
            **1. Phonological Awareness**
            - Recognizing and manipulating sounds in spoken language
            - Foundation for reading success
            - Can be developed before formal reading instruction
            """)
            
            # Phonological awareness progression
            progression_data = {
                "Skill Level": [
                    "Word Awareness",
                    "Syllable Awareness", 
                    "Onset-Rime",
                    "Phoneme Awareness"
                ],
                "Age Range": ["3-4 years", "4-5 years", "5-6 years", "6-7 years"],
                "Activities": [
                    "Counting words in sentences, recognizing word boundaries",
                    "Clapping syllables, syllable deletion and addition",
                    "Recognizing rhymes, identifying word families",
                    "Sound isolation, blending, segmentation, manipulation"
                ],
                "Assessment": [
                    "Can identify separate words in spoken sentences",
                    "Can clap and count syllables in words",
                    "Can identify rhyming words and word patterns",
                    "Can manipulate individual sounds in words"
                ]
            }
            
            progression_df = pd.DataFrame(progression_data)
            st.dataframe(progression_df, use_container_width=True)
            
            st.markdown("""
            #### **🎵 Effective Pre-Reading Activities**
            
            **Phonological Awareness Games:**
            - Sound matching and identification games
            - Rhyming songs and poems
            - Syllable clapping activities
            - Sound blending and segmentation
            
            **Print Awareness Activities:**
            - Environmental print exploration
            - Book handling and orientation
            - Letter recognition games
            - Name writing practice
            """)
        
        elif intervention_focus == "Early Math":
            st.markdown("""
            ### Early Mathematical Thinking
            
            #### **Number Sense Development**
            
            **Foundation Skills (Ages 3-5):**
            - Counting with one-to-one correspondence
            - Understanding "more" and "less"
            - Recognizing numerals
            - Simple pattern recognition
            
            **Advanced Skills (Ages 5-7):**
            - Understanding number relationships
            - Basic addition and subtraction concepts
            - Place value understanding
            - Mathematical problem-solving
            """)
            
            # Early math milestones
            milestone_data = {
                "Age": ["3-4 years", "4-5 years", "5-6 years", "6-7 years"],
                "Counting": [
                    "Counts to 5-10",
                    "Counts to 20, understands cardinality",
                    "Counts to 100, skip counting by 10s",
                    "Counts by 2s, 5s, 10s; understands odd/even"
                ],
                "Number Recognition": [
                    "Recognizes numerals 1-5",
                    "Recognizes numerals 1-10",
                    "Recognizes numerals 1-20",
                    "Recognizes numerals to 100"
                ],
                "Operations": [
                    "Understands 'more' and 'less'",
                    "Simple addition with objects",
                    "Addition/subtraction within 10",
                    "Addition/subtraction within 20"
                ]
            }
            
            milestone_df = pd.DataFrame(milestone_data)
            st.dataframe(milestone_df, use_container_width=True)

    elif content_type == "Academic Resources":
        st.markdown("## Academic Resource Library")
        
        resource_category = st.selectbox(
            "Resource category:",
            ["Research Articles", "Best Practice Guides", "Intervention Programs", "Assessment Tools"]
        )
        
        if resource_category == "Research Articles":
            st.markdown("### Key Research Articles")
            
            # Research articles database
            articles = [
                {
                    "Title": "The Science of Reading: A Handbook",
                    "Author": "Snowling, M. J. & Hulme, C.",
                    "Year": "2021",
                    "Key Findings": "Comprehensive review of reading research, emphasizing structured literacy approaches",
                    "Relevance": "Essential for understanding evidence-based reading instruction",
                    "Citation": "Snowling, M. J., & Hulme, C. (2021). The science of reading: A handbook. Wiley."
                },
                {
                    "Title": "Preventing Reading Difficulties in Young Children",
                    "Author": "Snow, C. E., Burns, M. S., & Griffin, P.",
                    "Year": "1998",
                    "Key Findings": "Identifies predictors of reading success and failure; emphasizes early intervention",
                    "Relevance": "Foundational text for early literacy intervention",
                    "Citation": "Snow, C. E., Burns, M. S., & Griffin, P. (1998). Preventing reading difficulties in young children. National Academy Press."
                },
                {
                    "Title": "Mathematical Learning Disabilities: Current Issues and Future Directions",
                    "Author": "Gersten, R. & Chard, D.",
                    "Year": "2019",
                    "Key Findings": "Reviews effective interventions for mathematical learning difficulties",
                    "Relevance": "Guidelines for math intervention and support",
                    "Citation": "Gersten, R., & Chard, D. (2019). Mathematical learning disabilities. Journal of Learning Disabilities, 52(3), 123-145."
                }
            ]
            
            for article in articles:
                with st.expander(f"{article['Title']} ({article['Year']})"):
                    st.write(f"**Author(s):** {article['Author']}")
                    st.write(f"**Key Findings:** {article['Key Findings']}")
                    st.write(f"**Relevance:** {article['Relevance']}")
                    st.write(f"**Citation:** {article['Citation']}")
        
        elif resource_category == "Best Practice Guides":
            st.markdown("### List Best Practice Implementation Guides")
            
            practice_areas = ["Structured Literacy", "Multi-Tiered Support", "Universal Design", "Family Engagement"]
            
            selected_practice = st.selectbox("Select practice area:", practice_areas)
            
            if selected_practice == "Structured Literacy":
                st.markdown("""
                #### 🏗️ Structured Literacy Implementation
                
                **Core Components:**
                
                **1. Systematic and Cumulative**
                - Skills taught in logical order
                - Each lesson builds on previous learning
                - Regular review and reinforcement
                
                **2. Explicit Instruction**
                - Direct teaching of concepts and skills
                - Clear explanations and modeling
                - Guided practice before independence
                
                **3. Diagnostic and Responsive**
                - Regular assessment of student progress
                - Instruction adjusted based on data
                - Individualized support as needed
                
                **Implementation Steps:**
                """)
                
                implementation_steps = [
                    "Assess current literacy curriculum and practices",
                    "Provide professional development for teachers",
                    "Select evidence-based curriculum materials",
                    "Establish assessment and progress monitoring systems",
                    "Create support structures for struggling students",
                    "Monitor implementation and student outcomes"
                ]
                
                for i, step in enumerate(implementation_steps, 1):
                    st.write(f"{i}. {step}")

    elif content_type == "Technology Tools":
        st.markdown("## Technology Tools for Learning Support")
        
        tool_category = st.selectbox(
            "Tool category:",
            ["Reading Support", "Writing Assistance", "Math Tools", "Organization Apps", "Communication Aids"]
        )
        
        if tool_category == "Reading Support":
            st.markdown("### 📱 Reading Support Technologies")
            
            reading_tools = [
                {
                    "Tool": "Text-to-Speech Software",
                    "Examples": "NaturalReader, Voice Dream Reader, Read&Write",
                    "Benefits": "Helps with decoding, comprehension, and accessing grade-level content",
                    "Best For": "Students with dyslexia, visual processing issues",
                    "Implementation": "Start with short texts, teach controls, practice daily"
                },
                {
                    "Tool": "Digital Highlighters",
                    "Examples": "Kami, Hypothesis, Adobe Reader",
                    "Benefits": "Helps with focus, note-taking, and text organization",
                    "Best For": "Students who struggle with attention and organization",
                    "Implementation": "Teach color-coding system, practice with short passages"
                },
                {
                    "Tool": "Reading Comprehension Apps",
                    "Examples": "Epic!, Reading A-Z, Lexia Core5",
                    "Benefits": "Adaptive practice, immediate feedback, engaging content",
                    "Best For": "Students needing additional reading practice",
                    "Implementation": "Set appropriate levels, monitor progress, supplement instruction"
                }
            ]
            
            for tool in reading_tools:
                with st.expander(f"🔧 {tool['Tool']}"):
                    st.write(f"**Examples:** {tool['Examples']}")
                    st.write(f"**Benefits:** {tool['Benefits']}")
                    st.write(f"**Best For:** {tool['Best For']}")
                    st.write(f"**Implementation:** {tool['Implementation']}")
        
        elif tool_category == "Writing Assistance":
            st.markdown("### Writing Assistance Technologies")
            
            writing_tools_data = {
                "Tool Type": [
                    "Word Prediction",
                    "Grammar Checkers", 
                    "Graphic Organizers",
                    "Speech-to-Text"
                ],
                "Examples": [
                    "Co:Writer, WordQ, Ginger",
                    "Grammarly, ProWritingAid, Ginger",
                    "Inspiration, Kidspiration, MindMeister",
                    "Dragon Naturally Speaking, Google Voice Typing"
                ],
                "Primary Benefits": [
                    "Reduces spelling errors, improves vocabulary",
                    "Identifies grammar and punctuation errors",
                    "Helps organize thoughts and ideas",
                    "Bypasses handwriting difficulties"
                ]
            }
            
            writing_tools_df = pd.DataFrame(writing_tools_data)
            st.dataframe(writing_tools_df, use_container_width=True)

    else:  # Support Strategies
        st.markdown("## 🤝 Support Strategies for Different Stakeholders")
        
        stakeholder = st.selectbox(
            "Select stakeholder group:",
            ["Teachers", "Parents", "Administrators", "Students"]
        )
        
        if stakeholder == "Teachers":
            st.markdown("""
            ### Teacher Teacher Support Strategies
            
            #### **Classroom Implementation**
            
            **Daily Practices:**
            - Use explicit instruction methods
            - Provide multiple means of representation
            - Offer choice in how students demonstrate learning
            - Implement regular progress monitoring
            
            **Lesson Planning:**
            - Include universal design principles
            - Plan for differentiated instruction
            - Prepare accommodations and modifications
            - Build in multiple practice opportunities
            """)
            
            # Teacher checklist
            st.markdown("####  Daily Teaching Checklist")
            
            checklist_items = [
                "Clear learning objectives posted and explained",
                "Multi-sensory instruction techniques used",
                "Students given choice in activities or materials",
                "Progress monitored and feedback provided",
                "Accommodations implemented as needed",
                "Positive reinforcement and encouragement given",
                "Instructions broken into manageable steps",
                "Visual supports and graphic organizers available"
            ]
            
            for item in checklist_items:
                st.checkbox(item, key=f"teacher_{item}")
        
        elif stakeholder == "Parents":
            st.markdown("""
            ### 👩👧👦 Parent Support Strategies
            
            #### **Home Home Support Techniques**
            
            **Creating a Supportive Environment:**
            - Establish consistent routines and expectations
            - Provide a quiet, organized homework space
            - Celebrate effort and progress, not just achievement
            - Maintain open communication with teachers
            
            **Academic Support:**
            - Break homework into manageable chunks
            - Use visual schedules and reminders
            - Practice skills in fun, game-like ways
            - Read together daily, regardless of child's reading level
            """)
            
            # Parent resources
            st.markdown("#### Recommended Parent Resources")
            
            parent_resources = [
                {
                    "Resource": "International Dyslexia Association",
                    "Type": "Website",
                    "Description": "Comprehensive information about dyslexia and reading difficulties",
                    "Link": "https://dyslexiaida.org"
                },
                {
                    "Resource": "Understood.org",
                    "Type": "Website", 
                    "Description": "Resources for learning and thinking differences",
                    "Link": "https://understood.org"
                },
                {
                    "Resource": "Learning Disabilities Association",
                    "Type": "Organization",
                    "Description": "Support and advocacy for individuals with learning disabilities",
                    "Link": "https://ldaamerica.org"
                }
            ]
            
            for resource in parent_resources:
                with st.expander(f"{resource['Resource']}"):
                    st.write(f"**Type:** {resource['Type']}")
                    st.write(f"**Description:** {resource['Description']}")
                    st.write(f"**Link:** {resource['Link']}")

    # Footer with additional resources
    st.markdown("---")
    st.markdown("### Additional Resources")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        **🏛️ Professional Organizations:**
        - International Dyslexia Association
        - Council for Exceptional Children
        - International Reading Association
        """)
    
    with col2:
        st.markdown("""
        **Research Centers:**
        - Haskins Laboratories
        - Florida Center for Reading Research
        - What Works Clearinghouse
        """)
    
    with col3:
        st.markdown("""
        **Practical Tools:**
        - Evidence-based practice guides
        - Assessment instruments
        - Intervention curricula
        """)

if __name__ == "__main__":
    main()
