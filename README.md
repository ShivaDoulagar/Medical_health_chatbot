# AI-Driven Public Health Chatbot for Disease Awareness

A multilingual AI chatbot MVP designed to educate rural and semi-urban populations about preventive healthcare, disease symptoms, and vaccination schedules.

## Features

- **Disease Information**: Provides symptoms, prevention tips, and when to seek medical help for common diseases
- **Vaccination Schedules**: Complete vaccination schedules for children and adults
- **Health Alerts**: Real-time health alerts and outbreak information (simulated)
- **Symptom Analysis**: Basic symptom checker with general recommendations
- **Emergency Guidance**: Clear instructions for medical emergencies
- **Web Interface**: User-friendly chat interface

## Supported Diseases

- Fever
- Cold/Flu
- Diabetes
- Hypertension

## Technology Stack

- **Backend**: Python Flask
- **Frontend**: HTML, CSS, JavaScript
- **Database**: In-memory (for MVP)

## Installation & Setup

### Prerequisites

- Python 3.7 or higher
- pip (Python package installer)

### Step 1: Clone or Download the Project

If you already have the project files, ensure you're in the project directory:

```powershell
cd D:\Code\medical_chatbot
```

### Step 2: Create Virtual Environment

Create a Python virtual environment to isolate project dependencies:

```powershell
python -m venv venv
```

### Step 3: Activate Virtual Environment

**For Windows PowerShell:**
```powershell
venv\Scripts\Activate.ps1
```

**For Windows Command Prompt:**
```cmd
venv\Scripts\activate.bat
```

**For Linux/Mac:**
```bash
source venv/bin/activate
```

You should see `(venv)` prefix in your terminal when the virtual environment is activated.

### Step 4: Install Dependencies

Install all required Python packages:

```powershell
pip install -r requirements.txt
```

### Step 5: Run the Application

Start the Flask development server:

```powershell
python app.py
```

The application will start running on:
- **Local Access**: http://127.0.0.1:5000
- **Network Access**: http://localhost:5000

## Usage

### Web Interface

1. Open your web browser
2. Navigate to `http://127.0.0.1:5000`
3. Start chatting with the medical assistant

### Example Queries

Try asking the chatbot:

- `"Hello"` - Get a greeting and overview
- `"Tell me about fever"` - Get detailed information about fever
- `"I have headache and chills"` - Symptom analysis
- `"Vaccination schedule for children"` - Get vaccination information
- `"Prevention tips"` - General health prevention advice
- `"Emergency help"` - Emergency guidance

### API Endpoints

The application also provides REST API endpoints:

- `GET /` - Main chat interface
- `POST /chat` - Send message to chatbot
- `GET /vaccination-schedule` - Get vaccination schedule data
- `GET /health-alert` - Get current health alerts

### Example API Usage

**Send a message to the chatbot:**
```bash
curl -X POST http://127.0.0.1:5000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "tell me about diabetes"}'
```

**Get vaccination schedule:**
```bash
curl http://127.0.0.1:5000/vaccination-schedule
```

## Project Structure

```
medical_chatbot/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── README.md             # Project documentation
├── venv/                 # Virtual environment (created after setup)
└── templates/            # HTML templates
    └── index.html        # Main chat interface
```

## Configuration

The application runs with the following default settings:
- **Host**: 0.0.0.0 (accessible from any IP)
- **Port**: 5000
- **Debug Mode**: Enabled (for development)

To modify these settings, edit the last line in `app.py`:

```python
app.run(debug=True, host='0.0.0.0', port=5000)
```

## Development

### Adding New Diseases

To add new diseases to the knowledge base, edit the `MEDICAL_KB` dictionary in `app.py`:

```python
MEDICAL_KB = {
    "new_disease": {
        "symptoms": ["symptom1", "symptom2"],
        "prevention": ["prevention1", "prevention2"],
        "when_to_seek_help": "When to see a doctor"
    }
}
```

### Extending Functionality

Future enhancements can include:
- Integration with government health databases
- WhatsApp/SMS integration
- Multi-language support
- Machine learning for better responses
- User authentication and history
- Database integration

## Troubleshooting

### Common Issues

1. **Virtual environment activation issues on Windows:**
   - If you get execution policy errors, run:
     ```powershell
     Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
     ```

2. **Port already in use:**
   - Change the port number in `app.py` or kill the process using the port

3. **Module not found errors:**
   - Ensure virtual environment is activated
   - Reinstall dependencies: `pip install -r requirements.txt`

### Getting Help

If you encounter any issues:
1. Check that Python 3.7+ is installed: `python --version`
2. Verify virtual environment is activated (look for `(venv)` prefix)
3. Ensure all dependencies are installed: `pip list`

## Deployment

For production deployment:

1. Use a production WSGI server like Gunicorn
2. Set `debug=False` in `app.py`
3. Configure proper logging
4. Set up environment variables for sensitive data
5. Use a proper database instead of in-memory storage

## Contributing

To contribute to this project:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is developed as an MVP for educational purposes.

## Disclaimer

This chatbot is for educational and informational purposes only. It is not a substitute for professional medical advice, diagnosis, or treatment. Always seek the advice of your physician or other qualified health provider with any questions you may have regarding a medical condition.
