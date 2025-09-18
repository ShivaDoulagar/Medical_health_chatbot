import ollama
import json
import logging
from typing import Optional, Dict, Any

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LlamaService:
    def __init__(self, model_name: str = "llama3.2:latest"):
        self.model_name = model_name
        self.client = ollama
        self.is_available = self._check_availability()
        
    def _check_availability(self) -> bool:
        """Check if Ollama and the model are available"""
        try:
            # Test if ollama is running and model is available
            response = self.client.list()
            available_models = [model['name'] for model in response.get('models', [])]
            
            if self.model_name in available_models:
                logger.info(f"Llama model {self.model_name} is available")
                return True
            else:
                logger.warning(f"Model {self.model_name} not found. Available models: {available_models}")
                return False
                
        except Exception as e:
            logger.error(f"Ollama not available: {e}")
            return False
    
    def get_medical_response(self, user_query: str, context: Dict[str, Any] = None) -> Optional[str]:
        """
        Get AI-powered medical response from Llama 3.2
        
        Args:
            user_query: The user's medical question
            context: Additional context (symptoms, patient info, etc.)
            
        Returns:
            AI-generated medical response or None if unavailable
        """
        if not self.is_available:
            logger.warning("Llama service not available, falling back to static responses")
            return None
            
        try:
            # Create a comprehensive medical prompt
            prompt = self._create_medical_prompt(user_query, context)
            
            # Get response from Llama
            response = self.client.chat(
                model=self.model_name,
                messages=[
                    {
                        'role': 'user',
                        'content': prompt
                    }
                ],
                options={
                    'temperature': 0.3,  # Lower temperature for more consistent medical advice
                    'top_p': 0.9,
                    'max_tokens': 500,
                }
            )
            
            ai_response = response['message']['content'].strip()
            logger.info("Successfully generated AI medical response")
            return ai_response
            
        except Exception as e:
            logger.error(f"Error generating AI response: {e}")
            return None
    
    def _create_medical_prompt(self, user_query: str, context: Dict[str, Any] = None) -> str:
        """Create a specialized medical prompt for Llama"""
        
        base_prompt = """You are an AI medical education assistant designed to provide helpful health information for educational purposes. Your responses should be:

1. ACCURATE and based on established medical knowledge
2. EDUCATIONAL - focus on general health information and awareness
3. SAFE - always include disclaimers about consulting healthcare professionals
4. APPROPRIATE for rural and semi-urban populations
5. CONCISE but comprehensive
6. Include prevention tips when relevant

IMPORTANT DISCLAIMERS TO ALWAYS INCLUDE:
- This information is for educational purposes only
- Not a substitute for professional medical advice
- Consult a healthcare provider for proper diagnosis and treatment
- For emergencies, contact emergency services immediately

"""
        
        # Add context if provided
        if context:
            base_prompt += f"\nAdditional context: {json.dumps(context, indent=2)}\n"
        
        # Add the user query
        base_prompt += f"\nUser Question: {user_query}\n"
        
        # Add specific medical response guidelines
        base_prompt += """
Please provide a helpful response that includes:
1. Direct answer to the question (if appropriate)
2. Key symptoms or signs to watch for
3. Prevention or self-care tips
4. When to seek professional medical help
5. Appropriate medical disclaimers

Format your response in a clear, easy-to-read manner suitable for general public education.
"""
        
        return base_prompt
    
    def get_disease_info(self, disease_name: str) -> Optional[str]:
        """Get comprehensive disease information"""
        prompt = f"""Provide comprehensive educational information about {disease_name} including:

1. **Overview**: Brief description of the condition
2. **Common Symptoms**: List main symptoms people should watch for
3. **Causes**: What typically causes this condition
4. **Prevention**: Practical prevention tips
5. **When to Seek Help**: Clear guidance on when to see a doctor
6. **Self-Care**: Safe home management tips (if applicable)

Focus on information relevant to rural and semi-urban populations. Include appropriate medical disclaimers.
"""
        return self.get_medical_response(prompt)
    
    def analyze_symptoms(self, symptoms: str) -> Optional[str]:
        """Analyze symptoms and provide general guidance"""
        prompt = f"""A person is experiencing these symptoms: {symptoms}

Please provide:
1. **General Assessment**: What these symptoms might commonly indicate (be careful not to diagnose)
2. **Immediate Care**: Safe self-care measures they can take
3. **Warning Signs**: Symptoms that would require immediate medical attention
4. **Next Steps**: Recommended actions (rest, hydration, when to see doctor)
5. **Important Reminders**: That this is not a diagnosis and professional consultation is needed

Be very careful to avoid making specific diagnoses. Focus on general health education and when to seek professional help.
"""
        return self.get_medical_response(prompt, {"symptoms": symptoms})
    
    def get_prevention_tips(self, condition_or_general: str = "general health") -> Optional[str]:
        """Get prevention tips for specific conditions or general health"""
        prompt = f"""Provide practical prevention tips for {condition_or_general} that are:

1. **Actionable**: Things people can realistically do
2. **Accessible**: Suitable for rural/semi-urban populations  
3. **Evidence-based**: Based on established medical knowledge
4. **Culturally appropriate**: Suitable for diverse populations

Include tips about:
- Diet and nutrition
- Exercise and physical activity
- Hygiene practices
- Lifestyle modifications
- When to get check-ups or screenings

Focus on practical, everyday measures people can take to stay healthy.
"""
        return self.get_medical_response(prompt)
    
    def get_emergency_guidance(self, situation: str) -> Optional[str]:
        """Get emergency medical guidance"""
        prompt = f"""Provide emergency guidance for: {situation}

Include:
1. **Immediate Actions**: What to do right now
2. **Emergency Contacts**: Remind about calling emergency services
3. **Do NOT Do**: Important things to avoid
4. **While Waiting**: Safe actions while waiting for help

Keep responses focused on immediate safety and getting professional help quickly. Emphasize calling emergency services (108 in India) for true emergencies.
"""
        return self.get_medical_response(prompt, {"emergency": True})

# Global instance
llama_service = LlamaService()
