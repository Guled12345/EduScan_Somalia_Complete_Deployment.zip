"""
Exact UI components matching the provided EduScan design mockup
"""
import streamlit as st

def add_exact_ui_styles():
    """Add CSS styles that exactly match the provided UI design"""
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
        
        /* Reset and base styles */
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        .main {
            font-family: 'Poppins', -apple-system, BlinkMacSystemFont, sans-serif !important;
            background: 
                linear-gradient(rgba(0, 0, 0, 0.4), rgba(0, 0, 0, 0.4)),
                url('/attached_assets/thumbnail_1750847532419.jpg') center center/cover no-repeat fixed !important;
            color: #ffffff !important;
            min-height: 100vh !important;
            position: relative;
        }
        
        .stApp {
            background: 
                linear-gradient(rgba(0, 0, 0, 0.4), rgba(0, 0, 0, 0.4)),
                url('/attached_assets/thumbnail_1750847532419.jpg') center center/cover no-repeat fixed !important;
            min-height: 100vh !important;
            width: 100% !important;
            position: relative;
        }
        
        /* Ensure content is readable over background */
        .main .block-container {
            background: rgba(255, 255, 255, 0.95) !important;
            backdrop-filter: blur(10px) !important;
            border-radius: 15px !important;
            padding: 2rem !important;
            margin: 1rem !important;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2) !important;
        }
        
        /* Hide Streamlit elements */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        .stDeployButton {visibility: hidden;}
        .stDecoration {display: none;}
        
        /* Ensure full viewport coverage */
        html, body, #root {
            height: 100% !important;
            width: 100% !important;
            margin: 0 !important;
            padding: 0 !important;
            overflow-x: hidden !important;
        }
        
        /* Global Styles - Somali Flag Inspired */
        .main {
            font-family: 'Poppins', -apple-system, BlinkMacSystemFont, sans-serif;
            background: linear-gradient(135deg, #87CEEB 0%, #E6F3FF 50%, #FFF8DC 100%);
            min-height: 100vh;
            color: #2C3E50;
        }
        
        .stApp {
            background: linear-gradient(135deg, #87CEEB 0%, #E6F3FF 50%, #FFF8DC 100%);
            min-height: 100vh;
        }
        
        /* Sidebar styling to match exact design */
        .css-1d391kg, .css-1cypcdb {
            background: linear-gradient(145deg, #ffffff 0%, #f8fafc 100%);
            border-right: 1px solid rgba(255, 255, 255, 0.2);
            width: 240px !important;
            min-width: 240px !important;
            max-width: 240px !important;
            box-shadow: 4px 0 20px rgba(0, 0, 0, 0.1);
        }
        
        /* Sidebar logo section */
        .sidebar-brand {
            display: flex;
            align-items: center;
            padding: 20px 16px;
            border-bottom: 1px solid #e1e5e9;
        }
        
        .sidebar-logo {
            width: 32px;
            height: 32px;
            background: linear-gradient(135deg, #4A90E2 0%, #87CEEB 100%);
            border-radius: 8px;
            display: flex;
            align-items: center;
            justify-content: center;
            margin-right: 12px;
            color: white;
            font-weight: 600;
            font-size: 14px;
            box-shadow: 0 2px 8px rgba(74, 144, 226, 0.3);
        }
        
        .sidebar-title {
            font-size: 16px;
            font-weight: 600;
            color: #1a1a1a;
            line-height: 1;
        }
        
        .sidebar-subtitle {
            font-size: 12px;
            color: #6b7280;
            line-height: 1.2;
            margin-top: 2px;
        }
        
        /* Navigation menu */
        .nav-menu {
            padding: 16px 0;
        }
        
        .nav-item {
            display: flex;
            align-items: center;
            padding: 10px 16px;
            margin: 2px 8px;
            border-radius: 8px;
            color: #6b7280;
            text-decoration: none;
            font-size: 14px;
            font-weight: 500;
            transition: all 0.15s ease;
            cursor: pointer;
        }
        
        .nav-item:hover {
            background-color: #f3f4f6;
            color: #374151;
        }
        
        .nav-item.active {
            background-color: #dbeafe;
            color: #2563eb;
        }
        
        .nav-icon {
            width: 20px;
            height: 20px;
            margin-right: 12px;
            font-size: 16px;
        }
        
        /* Teacher profile section */
        .teacher-profile {
            position: absolute;
            bottom: 16px;
            left: 16px;
            right: 16px;
            display: flex;
            align-items: center;
            padding: 12px;
            background-color: #f9fafb;
            border-radius: 8px;
        }
        
        .teacher-avatar {
            width: 32px;
            height: 32px;
            background: #6b7280;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-weight: 600;
            font-size: 12px;
            margin-right: 12px;
        }
        
        .teacher-info {
            flex: 1;
        }
        
        .teacher-name {
            font-size: 14px;
            font-weight: 600;
            color: #1a1a1a;
            line-height: 1.2;
        }
        
        .teacher-role {
            font-size: 12px;
            color: #6b7280;
        }
        
        /* Main content area */
        .main-content {
            padding: 32px 40px;
            background: transparent;
        }
        
        /* Dashboard header */
        .dashboard-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 32px;
        }
        
        .page-title {
            font-size: 28px;
            font-weight: 600;
            color: #2C3E50;
            margin: 0;
            letter-spacing: -0.3px;
        }
        
        .header-actions {
            display: flex;
            align-items: center;
            gap: 12px;
        }
        
        .header-icon {
            width: 40px;
            height: 40px;
            background: #ffffff;
            border: 1px solid #e1e5e9;
            border-radius: 8px;
            display: flex;
            align-items: center;
            justify-content: center;
            color: #6b7280;
            cursor: pointer;
            transition: all 0.15s ease;
        }
        
        .header-icon:hover {
            background: #f3f4f6;
        }
        
        /* Stats cards */
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 20px;
            margin-bottom: 32px;
        }
        
        .stat-card {
            background: rgba(255, 255, 255, 0.95) !important;
            border: 1px solid rgba(255, 255, 255, 0.3) !important;
            border-radius: 12px;
            padding: 20px;
            position: relative;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.15) !important;
            backdrop-filter: blur(10px) !important;
            transition: transform 0.2s ease, box-shadow 0.2s ease;
        }
        
        .stat-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 24px rgba(0, 0, 0, 0.12);
        }
        
        .stat-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 12px;
        }
        
        .stat-label {
            font-size: 14px;
            font-weight: 500;
            color: #6b7280;
        }
        
        .stat-icon {
            width: 32px;
            height: 32px;
            border-radius: 8px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 16px;
        }
        
        .stat-icon.total {
            background: linear-gradient(135deg, #4A90E2 0%, #87CEEB 100%);
            color: white;
            box-shadow: 0 2px 8px rgba(74, 144, 226, 0.3);
        }
        
        .stat-icon.on-track {
            background: linear-gradient(135deg, #2ECC71 0%, #27AE60 100%);
            color: white;
            box-shadow: 0 2px 8px rgba(46, 204, 113, 0.3);
        }
        
        .stat-icon.at-risk {
            background: linear-gradient(135deg, #F39C12 0%, #E67E22 100%);
            color: white;
            box-shadow: 0 2px 8px rgba(243, 156, 18, 0.3);
        }
        
        .stat-icon.intervention {
            background: linear-gradient(135deg, #E74C3C 0%, #C0392B 100%);
            color: white;
            box-shadow: 0 2px 8px rgba(231, 76, 60, 0.3);
        }
        
        .stat-number {
            font-size: 32px;
            font-weight: 700;
            color: #2C3E50;
            line-height: 1;
            margin-bottom: 4px;
        }
        
        .stat-subtitle {
            font-size: 14px;
            color: #6b7280;
        }
        
        /* Chart container */
        .chart-section {
            background: rgba(255, 255, 255, 0.95) !important;
            border: 1px solid rgba(255, 255, 255, 0.3) !important;
            border-radius: 12px;
            padding: 24px;
            margin-bottom: 24px;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.15) !important;
            backdrop-filter: blur(10px) !important;
        }
        
        .chart-title {
            font-size: 18px;
            font-weight: 600;
            color: #1a1a1a;
            margin-bottom: 20px;
        }
        
        /* Bottom sections */
        .bottom-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 24px;
        }
        
        .section-card {
            background: rgba(255, 255, 255, 0.95) !important;
            border: 1px solid rgba(255, 255, 255, 0.3) !important;
            border-radius: 12px;
            padding: 20px;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.15) !important;
            backdrop-filter: blur(10px) !important;
            transition: transform 0.2s ease, box-shadow 0.2s ease;
        }
        
        .section-card:hover {
            transform: translateY(-1px);
            box-shadow: 0 6px 20px rgba(0, 0, 0, 0.12);
        }
        
        .section-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 20px;
        }
        
        .section-title {
            font-size: 16px;
            font-weight: 600;
            color: #1a1a1a;
        }
        
        .view-all-link {
            color: #2563eb;
            text-decoration: none;
            font-size: 14px;
            font-weight: 500;
        }
        
        .view-all-link:hover {
            text-decoration: underline;
        }
        
        /* List items */
        .list-item {
            display: flex;
            align-items: center;
            padding: 12px 0;
            border-bottom: 1px solid #f3f4f6;
        }
        
        .list-item:last-child {
            border-bottom: none;
        }
        
        .item-icon {
            width: 32px;
            height: 32px;
            border-radius: 6px;
            display: flex;
            align-items: center;
            justify-content: center;
            margin-right: 12px;
            font-size: 14px;
        }
        
        .item-content {
            flex: 1;
        }
        
        .item-title {
            font-size: 14px;
            font-weight: 500;
            color: #1a1a1a;
            line-height: 1.3;
        }
        
        .item-subtitle {
            font-size: 12px;
            color: #6b7280;
            margin-top: 2px;
        }
        
        .item-meta {
            display: flex;
            align-items: center;
            gap: 8px;
        }
        
        .item-time {
            font-size: 12px;
            color: #6b7280;
        }
        
        .risk-badge {
            padding: 4px 8px;
            border-radius: 12px;
            font-size: 11px;
            font-weight: 500;
        }
        
        .risk-badge.high {
            background: #fee2e2;
            color: #dc2626;
        }
        
        .risk-badge.medium {
            background: #fef3c7;
            color: #d97706;
        }
        
        .risk-badge.low {
            background: #dcfce7;
            color: #16a34a;
        }
        
        /* User avatar in student list */
        .student-avatar {
            width: 32px;
            height: 32px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-weight: 600;
            font-size: 12px;
            margin-right: 12px;
        }
        
        .student-avatar.risk-high {
            background: #dc2626;
        }
        
        .student-avatar.risk-medium {
            background: #d97706;
        }
        
        .student-avatar.risk-low {
            background: #16a34a;
        }
        
        /* Responsive design */
        @media (max-width: 1200px) {
            .stats-grid {
                grid-template-columns: repeat(2, 1fr);
            }
        }
        
        @media (max-width: 768px) {
            .stats-grid {
                grid-template-columns: 1fr;
            }
            
            .bottom-grid {
                grid-template-columns: 1fr;
            }
        }
    </style>
    """, unsafe_allow_html=True)

def render_top_navigation():
    """Render clean top navigation bar with glass morphism effect"""
    nav_html = """
    <div style="background: rgba(255, 255, 255, 0.9); 
                padding: 16px 24px; 
                border-bottom: 1px solid rgba(255, 255, 255, 0.3); 
                margin-bottom: 24px;
                box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
                backdrop-filter: blur(10px);
                border-radius: 15px;
                margin: 1rem;">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <div style="display: flex; align-items: center;">
                <div style="background: linear-gradient(135deg, #4A90E2 0%, #87CEEB 100%); 
                           color: white; 
                           padding: 10px 16px; 
                           border-radius: 8px; 
                           font-weight: 600; 
                           font-size: 16px;
                           margin-right: 24px;
                           box-shadow: 0 4px 16px rgba(74, 144, 226, 0.3);
                           font-family: 'Poppins', sans-serif;">
                    EduScan Somalia
                </div>
            </div>
            <div style="display: flex; gap: 12px; align-items: center;">
                <div style="background: rgba(248, 220, 117, 0.9);
                           color: #2C3E50;
                           padding: 6px 12px;
                           border-radius: 16px;
                           font-size: 11px;
                           font-weight: 600;
                           box-shadow: 0 4px 12px rgba(248, 220, 117, 0.4);
                           backdrop-filter: blur(5px);">
                    ONLINE
                </div>
            </div>
        </div>
    </div>
    """
    st.markdown(nav_html, unsafe_allow_html=True)
    
    # Top navigation buttons
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        if st.button("Dashboard", key="nav_dashboard", use_container_width=True, type="primary"):
            st.switch_page("app.py")
    
    with col2:
        if st.button("Prediction", key="nav_pred", use_container_width=True):
            st.switch_page("pages/01_Prediction.py")
            
    with col3:
        if st.button("Resources", key="nav_res", use_container_width=True):
            st.switch_page("pages/02_Teacher_Resources.py")
            
    with col4:
        if st.button("Tracker", key="nav_track", use_container_width=True):
            st.switch_page("pages/03_Parent_Tracker.py")
            
    with col5:
        if st.button("Content", key="nav_content", use_container_width=True):
            st.switch_page("pages/04_Educational_Content.py")

def render_exact_sidebar():
    """Render minimal sidebar with just branding - no navigation buttons"""
    st.sidebar.markdown("""
    <div class="sidebar-brand">
        <div class="sidebar-logo">ES</div>
        <div>
            <div class="sidebar-title">EduScan</div>
            <div class="sidebar-subtitle">Learning Difficulties Detection Tool</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Simple info section (no buttons)
    st.sidebar.markdown("<br><br>", unsafe_allow_html=True)
    st.sidebar.markdown("""
    <div style="padding: 12px; background-color: #f8f9fa; border-radius: 8px; text-align: center;">
        <div style="font-weight: 600; color: #202124; font-size: 0.9rem;">System Status</div>
        <div style="color: #16a34a; font-size: 0.8rem;">Online</div>
    </div>
    """, unsafe_allow_html=True)

def create_exact_dashboard_header():
    """Create dashboard header exactly as in design"""
    return """
    <div class="dashboard-header">
        <h1 class="page-title">Dashboard</h1>
    </div>
    """

def create_exact_stats_cards():
    """Create stats cards exactly matching the design"""
    return """
    <div class="stats-grid">
        <div class="stat-card">
            <div class="stat-header">
                <span class="stat-label">Total</span>
                <div class="stat-icon total"></div>
            </div>
            <div class="stat-number">42</div>
            <div class="stat-subtitle">Students</div>
        </div>
        
        <div class="stat-card">
            <div class="stat-header">
                <span class="stat-label">On Track</span>
                <div class="stat-icon on-track"></div>
            </div>
            <div class="stat-number">28</div>
            <div class="stat-subtitle">Students</div>
        </div>
        
        <div class="stat-card">
            <div class="stat-header">
                <span class="stat-label">At Risk</span>
                <div class="stat-icon at-risk"></div>
            </div>
            <div class="stat-number">10</div>
            <div class="stat-subtitle">Students</div>
        </div>
        
        <div class="stat-card">
            <div class="stat-header">
                <span class="stat-label">Intervention</span>
                <div class="stat-icon intervention"></div>
            </div>
            <div class="stat-number">4</div>
            <div class="stat-subtitle">Students</div>
        </div>
    </div>
    """

def create_exact_recent_assessments():
    """Create recent assessments section exactly as in design"""
    return """
    <div class="section-card">
        <div class="section-header">
            <h3 class="section-title">Recent Assessments</h3>
            <a href="#" class="view-all-link">View All</a>
        </div>
        
        <div class="list-item">
            <div class="item-icon" style="background: #dbeafe; color: #2563eb;">R</div>
            <div class="item-content">
                <div class="item-title">Reading Comprehension</div>
                <div class="item-subtitle">Grade 3 • 24 Students</div>
            </div>
        </div>
        
        <div class="list-item">
            <div class="item-icon" style="background: #dcfce7; color: #16a34a;">M</div>
            <div class="item-content">
                <div class="item-title">Mathematics Assessment</div>
                <div class="item-subtitle">Grade 2 • 18 Students</div>
            </div>
        </div>
        
        <div class="list-item">
            <div class="item-icon" style="background: #fee2e2; color: #dc2626;">W</div>
            <div class="item-content">
                <div class="item-title">Writing Skills</div>
                <div class="item-subtitle">Grade 4 • 22 Students</div>
            </div>
        </div>
    </div>
    """

def create_exact_students_attention():
    """Create students needing attention section exactly as in design"""
    return """
    <div class="section-card">
        <div class="section-header">
            <h3 class="section-title">Students Needing Attention</h3>
            <a href="#" class="view-all-link">View All</a>
        </div>
        
        <div class="list-item">
            <div class="student-avatar risk-high">AH</div>
            <div class="item-content">
                <div class="item-title">Amina Hassan</div>
                <div class="item-subtitle">Grade 3 • Reading Difficulties</div>
            </div>
            <div class="item-meta">
                <span class="item-time">Today</span>
                <span class="risk-badge high">High Risk</span>
            </div>
        </div>
        
        <div class="list-item">
            <div class="student-avatar risk-medium">MA</div>
            <div class="item-content">
                <div class="item-title">Mohamed Ali</div>
                <div class="item-subtitle">Grade 2 • Math Difficulties</div>
            </div>
            <div class="item-meta">
                <span class="item-time">Yesterday</span>
                <span class="risk-badge medium">Medium Risk</span>
            </div>
        </div>
        
        <div class="list-item">
            <div class="student-avatar risk-low">SF</div>
            <div class="item-content">
                <div class="item-title">Sahra Farah</div>
                <div class="item-subtitle">Grade 4 • Attention Issues</div>
            </div>
            <div class="item-meta">
                <span class="item-time">2 days ago</span>
                <span class="risk-badge low">Low Risk</span>
            </div>
        </div>
    </div>
    """