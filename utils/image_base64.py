"""
Base64 encoded educational images for reliable display
"""
import base64
import os

def get_base64_images():
    """Get base64 encoded themed educational images"""
    
    # Convert images to base64
    def image_to_base64(image_path):
        try:
            with open(image_path, 'rb') as img_file:
                return base64.b64encode(img_file.read()).decode('utf-8')
        except:
            return None
    
    # Get base64 for themed section images (original set)
    assessment_innovation_b64 = image_to_base64('attached_assets/Assessment_Innovation_1751960419186.png')
    building_excellence_b64 = image_to_base64('attached_assets/Building_Educational_Excellence_Through_Research_1751960419192.png')
    cultural_adaptation_b64 = image_to_base64('attached_assets/Cultural_Adaptation_1751960419193.png')
    daily_tracking_b64 = image_to_base64('attached_assets/Daily_Tracking_1751960419193.png')
    educational_excellence_1_b64 = image_to_base64('attached_assets/Educational_Excellence_in_Action_1_1751960419194.png')
    educational_excellence_2_b64 = image_to_base64('attached_assets/Educational_Excellence_in_Action_2_1751960419195.png')
    educational_research_1_b64 = image_to_base64('attached_assets/Educational_Research_Impact_1_1751960419196.png')
    educational_research_2_b64 = image_to_base64('attached_assets/Educational_Research_Impact_2_1751960419196.png')
    educational_research_3_b64 = image_to_base64('attached_assets/Educational_Research_Impact_3_1751960419197.png')
    engaging_strategies_b64 = image_to_base64('attached_assets/Engaging_Learning_Strategies_1751960419198.png')
    global_practices_b64 = image_to_base64('attached_assets/Global_Best_Practices_1751960419199.png')
    inclusive_classroom_b64 = image_to_base64('attached_assets/Inclusive_Classroom_Excellence_1751960419200.png')
    
    # Get base64 for additional themed images (second set)
    inclusive_classroom_2_b64 = image_to_base64('attached_assets/Inclusive_Classroom_Excellence_1751960575285.png')
    intervention_studies_b64 = image_to_base64('attached_assets/Intervention_Studies_1751960575286.png')
    learning_science_b64 = image_to_base64('attached_assets/Learning_Science_1751960575288.png')
    parent_empowerment_b64 = image_to_base64('attached_assets/Parent_Empowerment_1751960575289.png')
    professional_collaboration_b64 = image_to_base64('attached_assets/Professional_Collaboration_1751960575290.png')
    reaching_every_student_b64 = image_to_base64('attached_assets/Reaching_Every_Student_1751960575291.png')
    school_partnership_b64 = image_to_base64('attached_assets/School_Partnership_1751960575293.png')
    strengthening_connections_b64 = image_to_base64('attached_assets/Strengthening_Home-School_Connections_1751960575294.png')
    student_information_2_b64 = image_to_base64('attached_assets/Student_Information_2_1751960575295.png')
    student_information_3_b64 = image_to_base64('attached_assets/Student_Information_3_1751960575296.png')
    student_progress_1_b64 = image_to_base64('attached_assets/Student_Progress_Stories_1_1751960575297.png')
    student_progress_2_b64 = image_to_base64('attached_assets/Student_Progress_Stories_2_1751960575298.png')
    
    # Assessment form section headers
    academic_performance_b64 = image_to_base64('attached_assets/ChatGPT Image Jul 8, 2025, 10_49_58 AM_1751961024971.png')
    behavioral_social_b64 = image_to_base64('attached_assets/ChatGPT Image Jul 8, 2025, 10_50_04 AM_1751961018098.png')
    
    # Also keep the original student photos for other sections
    exam_students_b64 = image_to_base64('attached_assets/Exam-Students_1750847086459.jpg')
    student_writing_b64 = image_to_base64('attached_assets/Ez0BdyeWUAQeFjt_1750847091267.jpg')
    student_portrait_b64 = image_to_base64('attached_assets/IMG_340E6A-360708-5A7F82-28A32F-B00A0B-5C1E93_1750847096365.jpg')
    
    return {
        # Themed section images (original set)
        'assessment_innovation': f'data:image/png;base64,{assessment_innovation_b64}' if assessment_innovation_b64 else '',
        'building_excellence': f'data:image/png;base64,{building_excellence_b64}' if building_excellence_b64 else '',
        'cultural_adaptation': f'data:image/png;base64,{cultural_adaptation_b64}' if cultural_adaptation_b64 else '',
        'daily_tracking': f'data:image/png;base64,{daily_tracking_b64}' if daily_tracking_b64 else '',
        'educational_excellence_1': f'data:image/png;base64,{educational_excellence_1_b64}' if educational_excellence_1_b64 else '',
        'educational_excellence_2': f'data:image/png;base64,{educational_excellence_2_b64}' if educational_excellence_2_b64 else '',
        'educational_research_1': f'data:image/png;base64,{educational_research_1_b64}' if educational_research_1_b64 else '',
        'educational_research_2': f'data:image/png;base64,{educational_research_2_b64}' if educational_research_2_b64 else '',
        'educational_research_3': f'data:image/png;base64,{educational_research_3_b64}' if educational_research_3_b64 else '',
        'engaging_strategies': f'data:image/png;base64,{engaging_strategies_b64}' if engaging_strategies_b64 else '',
        'global_practices': f'data:image/png;base64,{global_practices_b64}' if global_practices_b64 else '',
        'inclusive_classroom': f'data:image/png;base64,{inclusive_classroom_b64}' if inclusive_classroom_b64 else '',
        
        # Additional themed images (second set)
        'inclusive_classroom_2': f'data:image/png;base64,{inclusive_classroom_2_b64}' if inclusive_classroom_2_b64 else '',
        'intervention_studies': f'data:image/png;base64,{intervention_studies_b64}' if intervention_studies_b64 else '',
        'learning_science': f'data:image/png;base64,{learning_science_b64}' if learning_science_b64 else '',
        'parent_empowerment': f'data:image/png;base64,{parent_empowerment_b64}' if parent_empowerment_b64 else '',
        'professional_collaboration': f'data:image/png;base64,{professional_collaboration_b64}' if professional_collaboration_b64 else '',
        'reaching_every_student': f'data:image/png;base64,{reaching_every_student_b64}' if reaching_every_student_b64 else '',
        'school_partnership': f'data:image/png;base64,{school_partnership_b64}' if school_partnership_b64 else '',
        'strengthening_connections': f'data:image/png;base64,{strengthening_connections_b64}' if strengthening_connections_b64 else '',
        'student_information_2': f'data:image/png;base64,{student_information_2_b64}' if student_information_2_b64 else '',
        'student_information_3': f'data:image/png;base64,{student_information_3_b64}' if student_information_3_b64 else '',
        'student_progress_1': f'data:image/png;base64,{student_progress_1_b64}' if student_progress_1_b64 else '',
        'student_progress_2': f'data:image/png;base64,{student_progress_2_b64}' if student_progress_2_b64 else '',
        
        # Assessment form section headers
        'academic_performance': f'data:image/png;base64,{academic_performance_b64}' if academic_performance_b64 else '',
        'behavioral_social': f'data:image/png;base64,{behavioral_social_b64}' if behavioral_social_b64 else '',
        
        # Original student photos for prediction/assessment sections
        'exam_students': f'data:image/jpeg;base64,{exam_students_b64}' if exam_students_b64 else '',
        'student_writing': f'data:image/jpeg;base64,{student_writing_b64}' if student_writing_b64 else '',
        'student_portrait': f'data:image/jpeg;base64,{student_portrait_b64}' if student_portrait_b64 else '',
    }

def get_image_html(base64_data, alt_text, width="100%", height="200px"):
    """Generate HTML for base64 image"""
    if not base64_data:
        return f'<div style="width:{width}; height:{height}; background:#f0f0f0; display:flex; align-items:center; justify-content:center; border-radius:8px;"><span style="color:#666;">Image Loading...</span></div>'
    
    return f'<img src="{base64_data}" alt="{alt_text}" style="width:{width}; height:{height}; object-fit:cover; border-radius:8px;">'