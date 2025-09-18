from flask import Flask, render_template, request, jsonify
import json
from datetime import datetime
from llama_service import llama_service
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Sample medical knowledge base
MEDICAL_KB = {
    "fever": {
        "symptoms": [
            "high temperature",
            "chills",
            "sweating",
            "headache",
            "muscle aches",
        ],
        "prevention": [
            "Stay hydrated",
            "Get adequate rest",
            "Maintain good hygiene",
            "Avoid crowded places",
        ],
        "when_to_seek_help": "Seek immediate medical attention if fever exceeds 103°F (39.4°C) or persists for more than 3 days",
    },
    "cold": {
        "symptoms": ["runny nose", "sneezing", "cough", "sore throat", "mild fever"],
        "prevention": [
            "Wash hands frequently",
            "Avoid touching face",
            "Stay away from sick people",
            "Get enough sleep",
        ],
        "when_to_seek_help": "See a doctor if symptoms worsen after 7-10 days or if you develop high fever",
    },
    "diabetes": {
        "symptoms": [
            "excessive thirst",
            "frequent urination",
            "fatigue",
            "blurred vision",
            "slow healing wounds",
        ],
        "prevention": [
            "Maintain healthy weight",
            "Exercise regularly",
            "Eat balanced diet",
            "Limit sugar intake",
        ],
        "when_to_seek_help": "Consult doctor immediately if you experience severe symptoms or blood sugar irregularities",
    },
    "hypertension": {
        "symptoms": [
            "headache",
            "shortness of breath",
            "chest pain",
            "dizziness",
            "nosebleeds",
        ],
        "prevention": [
            "Reduce salt intake",
            "Exercise regularly",
            "Maintain healthy weight",
            "Limit alcohol",
            "Quit smoking",
        ],
        "when_to_seek_help": "Seek immediate help if blood pressure readings are consistently above 140/90 mmHg",
    },
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
        "15-18 months": ["DPT", "Polio", "Hib", "PCV"],
    },
    "adults": {
        "annual": ["Influenza"],
        "every_10_years": ["Tetanus", "Diphtheria"],
        "one_time": ["Hepatitis A", "Hepatitis B", "HPV (for young adults)"],
    },
}


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message", "").lower()

    # Simple keyword-based response system
    response = get_medical_response(user_message)

    return jsonify(
        {"response": response, "timestamp": datetime.now().strftime("%H:%M:%S")}
    )


@app.route("/vaccination-schedule")
def vaccination_schedule():
    return jsonify(VACCINATION_SCHEDULE)


@app.route("/health-alert")
def health_alert():
    # Simulate health alerts (in real implementation, this would connect to government health databases)
    alerts = [
        {
            "type": "outbreak",
            "disease": "Dengue",
            "location": "Urban areas",
            "severity": "medium",
            "prevention": "Use mosquito repellent, remove stagnant water",
        },
        {
            "type": "vaccination_drive",
            "vaccine": "COVID-19 Booster",
            "location": "Community health centers",
            "dates": "Available throughout the month",
        },
    ]
    return jsonify(alerts)


def get_medical_response(message):
    """Generate AI-powered medical response using Llama 3.2 with intelligent fallback"""

    original_message = message

    # Greetings - Keep simple responses for basic interactions
    if any(word in message for word in ["hello", "hi", "hey", "namaste"]):
        return "Hello! I'm your AI-powered health assistant using advanced AI to provide personalized medical information. I can help you with diseases, symptoms, prevention tips, and vaccination schedules. How can I assist you today?"

    # Emergency queries - Always handle these immediately without AI delay
    if any(
        word in message
        for word in ["emergency", "urgent", "severe", "critical", "help me"]
    ):
        emergency_response = llama_service.get_emergency_guidance(message)
        if emergency_response:
            return emergency_response
        # Fallback for emergencies
        return "🚨 **EMERGENCY:** If you're experiencing a medical emergency, please:\n• Call emergency services immediately (108 in India)\n• Go to the nearest hospital\n• Contact your doctor\n\nThis chatbot is for informational purposes only and cannot handle medical emergencies."

    # Try AI-powered response first for medical queries
    try:
        # Detect query type and use appropriate AI method
        # if detect_disease_query(message):
        #     logger.info(f"Processing disease query: {message}")
        #     # Extract disease name
        #     disease_names = extract_disease_names(message)
        #     if disease_names:
        #         ai_response = llama_service.get_disease_info(disease_names[0])
        #         if ai_response:
        #             return f"🤖 **AI-Powered Response:**\n\n{ai_response}"

        if detect_symptom_query(message):
            logger.info(f"Processing symptom query: {message}")
            ai_response = llama_service.analyze_symptoms(message)
            if ai_response:
                return f"{ai_response}"

        elif detect_prevention_query(message):
            logger.info(f"Processing prevention query: {message}")
            ai_response = llama_service.get_prevention_tips(message)
            if ai_response:
                return f"{ai_response}"

        elif "vaccination" in message or "vaccine" in message:
            # Handle vaccination with AI enhancement
            ai_response = llama_service.get_medical_response(
                f"Provide information about vaccination: {message}"
            )
            if ai_response:
                return f"{ai_response}"

        # General medical query - let AI handle it
        else:
            logger.info(f"Processing general medical query: {message}")
            ai_response = llama_service.get_medical_response(message)
            if ai_response:
                return f"{ai_response}"

    except Exception as e:
        logger.error(f"Error in AI processing: {e}")

    # Fallback to static responses if AI is unavailable
    logger.info("Using fallback static responses")
    return get_fallback_response(message)


# def detect_disease_query(message):
#     """Detect if message is asking about a specific disease"""
#     disease_indicators = ['tell me about', 'what is', 'information about', 'about', 'disease', 'condition']
#     disease_names = list(MEDICAL_KB.keys()) + ['cancer', 'covid', 'malaria', 'tuberculosis', 'asthma', 'migraine']

#     has_disease_indicator = any(indicator in message for indicator in disease_indicators)
#     has_disease_name = any(disease in message for disease in disease_names)

#     return has_disease_indicator or has_disease_name


def detect_symptom_query(message):
    """Detect if message is describing symptoms"""
    symptom_indicators = [
        "i have",
        "experiencing",
        "symptoms",
        "feeling",
        "pain",
        "ache",
        "hurt",
        "sick",
    ]
    common_symptoms = [
        "headache",
        "fever",
        "cough",
        "cold",
        "nausea",
        "vomiting",
        "diarrhea",
        "fatigue",
        "tired",
    ]

    has_symptom_indicator = any(
        indicator in message for indicator in symptom_indicators
    )
    has_symptom = any(symptom in message for symptom in common_symptoms)

    return has_symptom_indicator or has_symptom


def detect_prevention_query(message):
    """Detect if message is asking about prevention"""
    prevention_indicators = [
        "prevent",
        "prevention",
        "avoid",
        "protect",
        "stay healthy",
        "tips",
        "how to",
    ]
    return any(indicator in message for indicator in prevention_indicators)


def extract_disease_names(message):
    """Extract disease names from message"""
    all_diseases = list(MEDICAL_KB.keys()) + [
        "cancer",
        "covid",
        "malaria",
        "tuberculosis",
        "asthma",
        "migraine",
        "pneumonia",
        "bronchitis",
    ]
    found_diseases = [disease for disease in all_diseases if disease in message]
    return found_diseases if found_diseases else ["general health condition"]


def get_fallback_response(message):
    """Provide fallback static responses when AI is unavailable"""

    # Vaccination queries
    if "vaccination" in message or "vaccine" in message:
        if "child" in message or "baby" in message:
            return "📋 **Vaccination Information (Static):**\n\nFor children's vaccination schedule:\n• BCG, DPT, Polio at early months\n• Measles, MMR as they grow\n• Consult pediatrician for complete schedule\n\n⚠️ **Note:** AI assistant temporarily unavailable. Consult healthcare provider for detailed information."
        else:
            return "📋 **Adult Vaccination (Static):**\n\n• Annual flu shots\n• Tetanus boosters every 10 years\n• Hepatitis vaccines as recommended\n\n⚠️ **Note:** AI assistant temporarily unavailable. Consult healthcare provider for personalized recommendations."

    # Disease-specific queries
    for disease, info in MEDICAL_KB.items():
        if disease in message:
            response = f"📋 **{disease.title()} Information (Static):**\n\n"
            response += f"**Common Symptoms:** {', '.join(info['symptoms'])}\n\n"
            response += f"**Prevention Tips:** {', '.join(info['prevention'])}\n\n"
            response += f"**When to Seek Help:** {info['when_to_seek_help']}\n\n"
            response += "⚠️ **Note:** AI assistant temporarily unavailable. This is basic information only. Please consult a healthcare professional for proper diagnosis and treatment."
            return response

    # Symptom queries
    symptoms_mentioned = []
    all_symptoms = []
    for disease, info in MEDICAL_KB.items():
        all_symptoms.extend([(symptom, disease) for symptom in info["symptoms"]])

    for symptom, disease in all_symptoms:
        if symptom in message:
            symptoms_mentioned.append((symptom, disease))

    if symptoms_mentioned:
        diseases = list(set([disease for _, disease in symptoms_mentioned]))
        response = f"📋 **Symptom Analysis (Static):**\n\nBased on the symptoms you mentioned, you might be experiencing: {', '.join(diseases)}.\n\n"
        response += "**General Recommendations:**\n"
        response += "• Stay hydrated and get adequate rest\n"
        response += "• Monitor your symptoms\n"
        response += (
            "• Consult a healthcare professional if symptoms persist or worsen\n\n"
        )
        response += "⚠️ **Important:** This is not a medical diagnosis. AI assistant temporarily unavailable. Please consult a doctor for proper evaluation."
        return response

    # Prevention queries
    if "prevent" in message or "prevention" in message:
        return "📋 **General Prevention Tips (Static):**\n\n• Wash hands frequently\n• Eat a balanced diet\n• Exercise regularly\n• Get adequate sleep\n• Stay hydrated\n• Avoid smoking and limit alcohol\n• Get regular health checkups\n• Follow vaccination schedules\n\n⚠️ **Note:** AI assistant temporarily unavailable. Consult healthcare provider for personalized prevention strategies."

    # Default response
    return "**Medical Assistant:**\n\nI can help you with information about diseases, symptoms, prevention tips, and vaccination schedules.\n\n**Try asking me about:**\n• Specific diseases (fever, cold, diabetes, hypertension)\n• Symptoms you're experiencing\n• Prevention tips\n• Vaccination schedules\n• Health alerts\n\n⚠️ **Note:** AI-powered responses may be temporarily unavailable. For immediate concerns, consult a healthcare professional.\n\nWhat would you like to know?"


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
