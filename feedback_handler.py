import json
import os
from datetime import datetime

FEEDBACK_DIR = "data/feedback"

def save_feedback(feedback_text):
    """Save user feedback for continuous improvement"""
    os.makedirs(FEEDBACK_DIR, exist_ok=True)
    
    # Create feedback entry
    feedback_data = {
        "text": feedback_text,
        "timestamp": datetime.now().isoformat(),
        "resolved": False
    }
    
    # Save to file
    filename = f"feedback_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(os.path.join(FEEDBACK_DIR, filename), 'w') as f:
        json.dump(feedback_data, f)
    
    # Simple learning - flag common issues
    analyze_feedback(feedback_text)

def analyze_feedback(feedback_text):
    """Basic analysis to identify common issues"""
    feedback_lower = feedback_text.lower()
    
    # Detect common problems
    if "slow" in feedback_lower:
        log_issue("performance", "User reported slow response")
    if "error" in feedback_lower:
        log_issue("stability", "User encountered an error")
    if "missing" in feedback_lower or "not found" in feedback_lower:
        log_issue("coverage", "User reported missing information")

def log_issue(issue_type, message):
    """Log systemic issues for improvement"""
    issue_file = os.path.join(FEEDBACK_DIR, "system_issues.json")
    
    # Load existing issues or create new
    if os.path.exists(issue_file):
        with open(issue_file, 'r') as f:
            issues = json.load(f)
    else:
        issues = []
    
    # Add new issue
    issues.append({
        "type": issue_type,
        "message": message,
        "timestamp": datetime.now().isoformat()
    })
    
    # Save back
    with open(issue_file, 'w') as f:
        json.dump(issues, f)
