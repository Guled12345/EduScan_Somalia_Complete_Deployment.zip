import json
import os
import sys
from datetime import datetime
import pandas as pd

# Import database functions
try:
    from utils.db_utils import (
        save_prediction_to_db, save_parent_observation_to_db,
        load_student_predictions, load_parent_observations, authenticate_user_db,
        get_database_stats
    )
    DATABASE_AVAILABLE = True
except ImportError:
    DATABASE_AVAILABLE = False

def get_data_directory():
    """Get the correct path for the data directory"""
    if getattr(sys, 'frozen', False):
        # Running as compiled executable
        base_path = sys._MEIPASS
    else:
        # Running as script
        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    data_dir = os.path.join(base_path, 'data')
    os.makedirs(data_dir, exist_ok=True)
    return data_dir

def save_prediction_data(prediction_record):
    """Save prediction data to database or JSON file as fallback"""
    # Try database first if available
    if DATABASE_AVAILABLE:
        try:
            return save_prediction_to_db(prediction_record)
        except Exception as e:
            print(f"Database error, falling back to JSON: {e}")
    
    # Fallback to JSON file storage
    try:
        data_dir = get_data_directory()
        file_path = os.path.join(data_dir, 'student_data.json')
        
        # Load existing data
        existing_data = []
        if os.path.exists(file_path):
            try:
                with open(file_path, 'r') as f:
                    existing_data = json.load(f)
            except (json.JSONDecodeError, FileNotFoundError):
                existing_data = []
        
        # Add new record
        existing_data.append(prediction_record)
        
        # Save updated data
        with open(file_path, 'w') as f:
            json.dump(existing_data, f, indent=2)
        
        return True
    
    except Exception as e:
        print(f"Error saving prediction data: {e}")
        return False

def load_student_data():
    """Load student prediction data from database or JSON file as fallback"""
    # Try database first if available
    if DATABASE_AVAILABLE:
        try:
            return load_student_predictions()
        except Exception as e:
            print(f"Database error, falling back to JSON: {e}")
    
    # Fallback to JSON file storage
    try:
        data_dir = get_data_directory()
        file_path = os.path.join(data_dir, 'student_data.json')
        
        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                data = json.load(f)
            return data
        else:
            return []
    
    except Exception as e:
        print(f"Error loading student data: {e}")
        return []

def save_parent_observation(observation_data):
    """Save parent observation data to database or JSON file as fallback"""
    # Try database first if available
    if DATABASE_AVAILABLE:
        try:
            return save_parent_observation_to_db(observation_data)
        except Exception as e:
            print(f"Database error, falling back to JSON: {e}")
    
    # Fallback to JSON file storage
    try:
        data_dir = get_data_directory()
        file_path = os.path.join(data_dir, 'parent_observations.json')
        
        # Load existing data
        existing_data = []
        if os.path.exists(file_path):
            try:
                with open(file_path, 'r') as f:
                    existing_data = json.load(f)
            except (json.JSONDecodeError, FileNotFoundError):
                existing_data = []
        
        # Add new observation
        existing_data.append(observation_data)
        
        # Save updated data
        with open(file_path, 'w') as f:
            json.dump(existing_data, f, indent=2)
        
        return True
    
    except Exception as e:
        print(f"Error saving parent observation: {e}")
        return False

def load_parent_observations():
    """Load parent observation data from database or JSON file as fallback"""
    # Try database first if available
    if DATABASE_AVAILABLE:
        try:
            from utils.db_utils import load_parent_observations as db_load_observations
            return db_load_observations()
        except Exception as e:
            print(f"Database error, falling back to JSON: {e}")
    
    # Fallback to JSON file storage
    try:
        data_dir = get_data_directory()
        file_path = os.path.join(data_dir, 'parent_observations.json')
        
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read().strip()
                if content:
                    data = json.loads(content)
                    # Ensure data is a list
                    if isinstance(data, list):
                        return data
                    else:
                        return []
                else:
                    return []
        else:
            # Create empty file if it doesn't exist
            with open(file_path, 'w') as f:
                json.dump([], f)
            return []
    
    except (json.JSONDecodeError, UnicodeDecodeError, TypeError) as e:
        print(f"JSON parsing error, creating new file: {e}")
        # Create fresh file if corrupted
        try:
            data_dir = get_data_directory()
            file_path = os.path.join(data_dir, 'parent_observations.json')
            with open(file_path, 'w') as f:
                json.dump([], f)
        except:
            pass
        return []
    except Exception as e:
        print(f"Error loading parent observations: {e}")
        return []

def save_user_data(user_data):
    """Save user authentication data"""
    try:
        data_dir = get_data_directory()
        file_path = os.path.join(data_dir, 'users.json')
        
        # Load existing users
        existing_users = []
        if os.path.exists(file_path):
            try:
                with open(file_path, 'r') as f:
                    existing_users = json.load(f)
            except (json.JSONDecodeError, FileNotFoundError):
                existing_users = []
        
        # Check if user already exists
        user_exists = False
        for i, user in enumerate(existing_users):
            if user['username'] == user_data['username']:
                existing_users[i] = user_data
                user_exists = True
                break
        
        if not user_exists:
            existing_users.append(user_data)
        
        # Save updated users
        with open(file_path, 'w') as f:
            json.dump(existing_users, f, indent=2)
        
        return True
    
    except Exception as e:
        print(f"Error saving user data: {e}")
        return False

def load_user_data():
    """Load user authentication data"""
    try:
        data_dir = get_data_directory()
        file_path = os.path.join(data_dir, 'users.json')
        
        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                data = json.load(f)
            return data
        else:
            # Create default admin user
            default_users = [
                {
                    "username": "admin",
                    "password": "admin123",
                    "user_type": "teacher",
                    "full_name": "Administrator",
                    "email": "admin@school.edu",
                    "created_date": datetime.now().isoformat()
                },
                {
                    "username": "teacher1",
                    "password": "teacher123",
                    "user_type": "teacher", 
                    "full_name": "Demo Teacher",
                    "email": "teacher@school.edu",
                    "created_date": datetime.now().isoformat()
                },
                {
                    "username": "parent1",
                    "password": "parent123",
                    "user_type": "parent",
                    "full_name": "Demo Parent",
                    "email": "parent@email.com",
                    "created_date": datetime.now().isoformat()
                }
            ]
            
            # Save default users
            with open(file_path, 'w') as f:
                json.dump(default_users, f, indent=2)
            
            return default_users
    
    except Exception as e:
        print(f"Error loading user data: {e}")
        return []

def authenticate_user(username, password):
    """Authenticate user credentials using database or JSON fallback"""
    # Try database first if available
    if DATABASE_AVAILABLE:
        try:
            return authenticate_user_db(username, password)
        except Exception as e:
            print(f"Database error, falling back to JSON: {e}")
    
    # Fallback to JSON file authentication
    users = load_user_data()
    
    for user in users:
        if user['username'] == username and user['password'] == password:
            return user
    
    return None

def export_data_to_csv(data_type='predictions'):
    """Export data to CSV format"""
    try:
        if data_type == 'predictions':
            data = load_student_data()
            df = pd.DataFrame(data)
            filename = f"predictions_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        
        elif data_type == 'observations':
            data = load_parent_observations()
            df = pd.DataFrame(data)
            filename = f"observations_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        
        else:
            return None, "Invalid data type"
        
        if df.empty:
            return None, "No data to export"
        
        csv_data = df.to_csv(index=False)
        return csv_data, filename
    
    except Exception as e:
        return None, f"Error exporting data: {e}"

def get_data_summary():
    """Get summary statistics of stored data"""
    try:
        predictions = load_student_data()
        observations = load_parent_observations()
        users = load_user_data()
        
        summary = {
            'total_predictions': len(predictions),
            'total_observations': len(observations),
            'total_users': len(users),
            'last_prediction_date': None,
            'last_observation_date': None
        }
        
        if predictions:
            latest_prediction = max(predictions, key=lambda x: x.get('timestamp', ''))
            summary['last_prediction_date'] = latest_prediction.get('timestamp')
        
        if observations:
            latest_observation = max(observations, key=lambda x: x.get('timestamp', ''))
            summary['last_observation_date'] = latest_observation.get('timestamp')
        
        return summary
    
    except Exception as e:
        print(f"Error getting data summary: {e}")
        return {
            'total_predictions': 0,
            'total_observations': 0,
            'total_users': 0,
            'last_prediction_date': None,
            'last_observation_date': None
        }

def clean_old_data(days_old=90):
    """Clean data older than specified days"""
    try:
        from datetime import datetime, timedelta
        cutoff_date = datetime.now() - timedelta(days=days_old)
        
        # Clean predictions
        predictions = load_student_data()
        filtered_predictions = []
        
        for pred in predictions:
            try:
                pred_date = datetime.fromisoformat(pred.get('timestamp', ''))
                if pred_date > cutoff_date:
                    filtered_predictions.append(pred)
            except ValueError:
                # Keep records without valid timestamps
                filtered_predictions.append(pred)
        
        # Clean observations
        observations = load_parent_observations()
        filtered_observations = []
        
        for obs in observations:
            try:
                obs_date = datetime.fromisoformat(obs.get('timestamp', ''))
                if obs_date > cutoff_date:
                    filtered_observations.append(obs)
            except ValueError:
                # Keep records without valid timestamps
                filtered_observations.append(obs)
        
        # Save cleaned data
        data_dir = get_data_directory()
        
        with open(os.path.join(data_dir, 'student_data.json'), 'w') as f:
            json.dump(filtered_predictions, f, indent=2)
        
        with open(os.path.join(data_dir, 'parent_observations.json'), 'w') as f:
            json.dump(filtered_observations, f, indent=2)
        
        removed_predictions = len(predictions) - len(filtered_predictions)
        removed_observations = len(observations) - len(filtered_observations)
        
        return {
            'removed_predictions': removed_predictions,
            'removed_observations': removed_observations,
            'remaining_predictions': len(filtered_predictions),
            'remaining_observations': len(filtered_observations)
        }
    
    except Exception as e:
        print(f"Error cleaning old data: {e}")
        return None
