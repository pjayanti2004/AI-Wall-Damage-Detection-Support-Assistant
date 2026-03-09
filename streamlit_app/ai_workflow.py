import random

# -------------------------
# KEYWORD DATABASE
# -------------------------

ISSUE_KEYWORDS = {
    "Water Leak": ["water", "leak", "drip", "flood", "ceiling", "pipe"],
    "Electrical Issue": ["electric", "spark", "shock", "wire", "socket"],
    "AC Problem": ["ac", "cooling", "air conditioner", "hvac"],
    "Gas Leak": ["gas", "smell", "cylinder"],
    "Broken Appliance": ["broken", "damage", "not working"]
}

# -------------------------
# INTENT DETECTION
# -------------------------

def detect_intent(user_input):

    text = user_input.lower()

    if any(word in text for word in ["leak", "water", "flood", "spark", "shock", "gas"]):
        return "Emergency"

    if any(word in text for word in ["repair", "fix", "service"]):
        return "Maintenance"

    if any(word in text for word in ["broken", "damage"]):
        return "Complaint"

    return "Inquiry"

# -------------------------
# ISSUE TYPE DETECTION
# -------------------------

def detect_issue_type(user_input):

    text = user_input.lower()

    for issue, keywords in ISSUE_KEYWORDS.items():
        if any(word in text for word in keywords):
            return issue

    return "General Issue"


# -------------------------
# SEVERITY
# -------------------------

def detect_severity(user_input):

    text = user_input.lower()

    if any(word in text for word in ["gas", "spark", "shock"]):
        return "Critical"

    if any(word in text for word in ["water", "leak", "flood"]):
        return "High"

    if any(word in text for word in ["ac", "cooling"]):
        return "Medium"

    return "Low"


# -------------------------
# RESPONSE GENERATION
# -------------------------

def generate_reply(user_input):

    issue = detect_issue_type(user_input)

    if issue == "Water Leak":

        responses = [

"""
### Issue Understanding
Water leakage may indicate plumbing failure or roof damage.

### Immediate Safety Steps
• Place a bucket to collect water  
• Move electronics away  
• Turn off electricity near water  

### Diagnostic Questions
• Did the leak start after rain?
• Is the leak near a bathroom or roof area?

### Recommended Action
Contact a plumber or roof inspector.
""",

"""
### Issue Understanding
Ceiling leaks usually occur due to damaged roofing or pipe leakage.

### Immediate Steps
• Contain the dripping water
• Protect furniture
• Inspect nearby plumbing

### Recommendation
Professional inspection is recommended.
"""
        ]

        return random.choice(responses)


    if issue == "Electrical Issue":

        return """
### Issue Understanding
Electrical sparks indicate wiring damage or overload.

### Immediate Safety Steps
• Turn off the main power supply
• Avoid touching exposed wires
• Keep water away from sockets

### Recommendation
Call a licensed electrician immediately.
"""


    if issue == "AC Problem":

        return """
### Issue Understanding
Poor cooling can be caused by dirty filters or low refrigerant.

### Immediate Steps
• Clean AC filters
• Check thermostat
• Ensure outdoor unit airflow

### Recommendation
Schedule an HVAC technician inspection.
"""


    if issue == "Gas Leak":

        return """
### Issue Understanding
Gas smell may indicate a dangerous gas leak.

### Immediate Safety Steps
• Do NOT switch electrical appliances
• Open windows immediately
• Turn off the gas supply

### Recommendation
Contact gas service emergency support immediately.
"""


    return """
### Support Response

Thank you for contacting support.

Please describe the issue in more detail so we can assist you better.
"""


# -------------------------
# VALIDATION
# -------------------------

def validate_response(text):

    risky_words = ["guarantee", "definitely", "100%", "always"]

    for word in risky_words:
        if word in text.lower():
            return False

    return True


# -------------------------
# TECHNICIAN
# -------------------------

def recommend_technician(issue):

    mapping = {
        "Water Leak": "Plumber / Roof Inspector",
        "Electrical Issue": "Licensed Electrician",
        "AC Problem": "HVAC Technician",
        "Gas Leak": "Gas Service Technician"
    }

    return mapping.get(issue, "General Maintenance Technician")


# -------------------------
# COST ESTIMATION
# -------------------------

def estimate_cost(issue):

    cost_map = {
        "Water Leak": "₹2000 – ₹8000",
        "Electrical Issue": "₹1500 – ₹5000",
        "AC Problem": "₹3000 – ₹10000",
        "Gas Leak": "₹2000 – ₹7000"
    }

    return cost_map.get(issue, "Inspection Required")

import cv2
import numpy as np

def analyze_image_damage(image):

    img = image.copy()

    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Blur to remove noise
    blur = cv2.GaussianBlur(gray,(5,5),0)

    # Edge detection
    edges = cv2.Canny(blur,50,150)

    # Dilate edges
    kernel = np.ones((3,3),np.uint8)
    edges = cv2.dilate(edges,kernel,iterations=1)

    # Find contours
    contours,_ = cv2.findContours(edges,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

    crack_count = 0

    for c in contours:

        area = cv2.contourArea(c)

        if area > 100:

            cv2.drawContours(img,[c],-1,(0,255,0),2)
            crack_count += 1


    # Damage percentage
    damage_pixels = np.sum(edges > 0)
    total_pixels = edges.size
    damage_percent = (damage_pixels / total_pixels) * 100


    # Heatmap
    heatmap = cv2.applyColorMap(edges, cv2.COLORMAP_JET)
    heatmap_overlay = cv2.addWeighted(img,0.7,heatmap,0.3,0)


    # Decision logic
    if damage_percent > 8:

        result = {
            "issue":"Severe Wall Damage",
            "severity":"High",
            "technician":"Structural Engineer",
            "cost":"₹7000 – ₹20000"
        }

    elif damage_percent > 3:

        result = {
            "issue":"Wall Damage / Paint Peeling",
            "severity":"Medium",
            "technician":"Contractor",
            "cost":"₹2000 – ₹7000"
        }

    else:

        result = {
            "issue":"Minor Surface Damage",
            "severity":"Low",
            "technician":"Inspection Recommended",
            "cost":"₹1000 – ₹3000"
        }

    return result, img, damage_percent, heatmap_overlay