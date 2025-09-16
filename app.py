from flask import Flask, render_template, request, jsonify
import json
from datetime import datetime

app = Flask(__name__)

# Sample medical knowledge base
MEDICAL_KB = {
    "fever": {
        "symptoms": ["high temperature", "chills", "sweating", "headache", "muscle aches"],
        "prevention": ["Stay hydrated", "Get adequate rest", "Maintain good hygiene", "Avoid crowded places"],
        "when_to_seek_help": "Seek immediate medical attention if fever exceeds 103°F (39.4°C) or persists for more than 3 days"
    },
    "cold": {
        "symptoms": ["runny nose", "sneezing", "cough", "sore throat", "mild fever"],
        "prevention": ["Wash hands frequently", "Avoid touching face", "Stay away from sick people", "Get enough sleep"],
        "when_to_seek_help": "See a doctor if symptoms worsen after 7-10 days or if you develop high fever"
    },
    "diabetes": {
        "symptoms": ["excessive thirst", "frequent urination", "fatigue", "blurred vision", "slow healing wounds"],
        "prevention": ["Maintain healthy weight", "Exercise regularly", "Eat balanced diet", "Limit sugar intake"],
        "when_to_seek_help": "Consult doctor immediately if you experience severe symptoms or blood sugar irregularities"
    },
    "hypertension": {
        "symptoms": ["headache", "shortness of breath", "chest pain", "dizziness", "nosebleeds"],
        "prevention": ["Reduce salt intake", "Exercise regularly", "Maintain healthy weight", "Limit alcohol", "Quit smoking"],
        "when_to_seek_help": "Seek immediate help if blood pressure readings are consistently above 140/90 mmHg"
    }
}

# Vaccination schedule data
VACCINATION_SCHEDULE = {
    "children": {
        "0-2 months": ["Hepatitis B", "BCG"],
        "2 months": ["DPT", "Polio", "Hib", "PCV"],
        "4 months": ["DPT", "Polio", "Hib", "PCV"],
        "6 months": ["DPT", "Polio", "Hib", "PCV", "Hepatitis B"],
        "9 months": ["Measles"],
        "12 months": ["MMR", "Varicella"],
        "15-18 months": ["DPT", "Polio", "Hib", "PCV"]
    },
    "adults": {
        "annual": ["Influenza"],
        "every_10_years": ["Tetanus", "Diphtheria"],
        "one_time": ["Hepatitis A", "Hepatitis B", "HPV (for young adults)"]
    }
}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message', '').lower()
    
    # Simple keyword-based response system
    response = get_medical_response(user_message)
    
    return jsonify({
        'response': response,
        'timestamp': datetime.now().strftime('%H:%M:%S')
    })

@app.route('/vaccination-schedule')
def vaccination_schedule():
    return jsonify(VACCINATION_SCHEDULE)

@app.route('/health-alert')
def health_alert():
    # Simulate health alerts (in real implementation, this would connect to government health databases)
    alerts = [
        {
            "type": "outbreak",
            "disease": "Dengue",
            "location": "Urban areas",
            "severity": "medium",
            "prevention": "Use mosquito repellent, remove stagnant water"
        },
        {
            "type": "vaccination_drive",
            "vaccine": "COVID-19 Booster",
            "location": "Community health centers",
            "dates": "Available throughout the month"
        }
    ]
    return jsonify(alerts)

def get_medical_response(message):
    """Generate response based on user message"""
    
    # Greetings
    if any(word in message for word in ['hello', 'hi', 'hey', 'namaste']):
        return "Hello! I'm your AI health assistant. I can help you with information about diseases, symptoms, prevention tips, and vaccination schedules. How can I assist you today?"
    
    # Vaccination queries
    if 'vaccination' in message or 'vaccine' in message:
        if 'child' in message or 'baby' in message:
            return "For children's vaccination schedule, please refer to our vaccination guide. Key vaccines include BCG, DPT, Polio, Measles, and MMR. Would you like specific information about any age group?"
        else:
            return "Adult vaccination recommendations include annual flu shots, tetanus boosters every 10 years, and hepatitis vaccines. Would you like more details about any specific vaccine?"
    
    # Disease-specific queries
    for disease, info in MEDICAL_KB.items():
        if disease in message:
            response = f"**{disease.title()} Information:**\n\n"
            response += f"**Common Symptoms:** {', '.join(info['symptoms'])}\n\n"
            response += f"**Prevention Tips:** {', '.join(info['prevention'])}\n\n"
            response += f"**When to Seek Help:** {info['when_to_seek_help']}\n\n"
            response += "⚠️ **Disclaimer:** This information is for educational purposes only. Please consult a healthcare professional for proper diagnosis and treatment."
            return response
    
    # Symptom queries
    symptoms_mentioned = []
    all_symptoms = []
    for disease, info in MEDICAL_KB.items():
        all_symptoms.extend([(symptom, disease) for symptom in info['symptoms']])
    
    for symptom, disease in all_symptoms:
        if symptom in message:
            symptoms_mentioned.append((symptom, disease))
    
    if symptoms_mentioned:
        diseases = list(set([disease for _, disease in symptoms_mentioned]))
        response = f"Based on the symptoms you mentioned, you might be experiencing: {', '.join(diseases)}.\n\n"
        response += "Here are some general recommendations:\n"
        response += "• Stay hydrated and get adequate rest\n"
        response += "• Monitor your symptoms\n"
        response += "• Consult a healthcare professional if symptoms persist or worsen\n\n"
        response += "⚠️ **Important:** This is not a medical diagnosis. Please consult a doctor for proper evaluation."
        return response
    
    # Prevention queries
    if 'prevent' in message or 'prevention' in message:
        return "General prevention tips for good health:\n• Wash hands frequently\n• Eat a balanced diet\n• Exercise regularly\n• Get adequate sleep\n• Stay hydrated\n• Avoid smoking and limit alcohol\n• Get regular health checkups\n• Follow vaccination schedules"
    
    # Emergency queries
    if any(word in message for word in ['emergency', 'urgent', 'severe', 'critical']):
        return "🚨 **EMERGENCY:** If you're experiencing a medical emergency, please:\n• Call emergency services immediately (108 in India)\n• Go to the nearest hospital\n• Contact your doctor\n\nThis chatbot is for informational purposes only and cannot handle medical emergencies."
    
    # Default response
    return "I can help you with information about diseases, symptoms, prevention tips, and vaccination schedules. Try asking me about:\n• Specific diseases (fever, cold, diabetes, hypertension)\n• Symptoms you're experiencing\n• Prevention tips\n• Vaccination schedules\n• Health alerts\n\nWhat would you like to know?"

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
