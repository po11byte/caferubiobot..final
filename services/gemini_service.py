import os
import logging
import google.generativeai as genai
from dotenv import load_dotenv

logger = logging.getLogger(__name__)
load_dotenv()

class GeminiService:
    def __init__(self):
        try:
            self.api_key = os.getenv('GEMINI_API_KEY')
            if not self.api_key:
                raise ValueError("GEMINI_API_KEY no encontrada en variables de entorno")
            
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel('gemini-pro')
            
            # Configuración del personaje del bot
            self.system_prompt = """
            Eres Café Rubio Bot, un asistente amable y servicial para una cafetería llamada "Café Rubio". 
            Responde de manera cálida y profesional en español.
            
            Información sobre Café Rubio:
            - Horario: Lunes a Viernes 7:00 AM - 8:00 PM, Sábados 8:00 AM - 6:00 PM
            - Especialidad: Café de especialidad, pasteles artesanales, sandwiches
            - Dirección: Calle Principal 123, Ciudad
            - Teléfono: +1234567890
            
            Responde preguntas sobre:
            * Menú y precios
            * Horarios de atención
            * Pedidos y reservas
            * Recomendaciones
            * Ubicación y contacto
            
            Sé breve pero útil en tus respuestas (máximo 2-3 líneas).
            Si no sabes algo, sugiere contactar al café directamente.
            """
            
            logger.info("✅ Gemini service inicializado correctamente")
            
        except Exception as e:
            logger.error(f"❌ Error inicializando Gemini: {str(e)}")
            raise
    
    def generate_response(self, user_message: str) -> str:
        """Generar respuesta usando Gemini"""
        try:
            logger.info(f"🧠 Procesando mensaje: {user_message}")
            
            prompt = f"{self.system_prompt}\n\nUsuario: {user_message}\nBot:"
            
            response = self.model.generate_content(prompt)
            
            if response.text:
                cleaned_response = response.text.strip()
                logger.info(f"✅ Respuesta generada: {cleaned_response}")
                return cleaned_response
            else:
                logger.warning("⚠️ Gemini devolvió respuesta vacía")
                return "Lo siento, no pude generar una respuesta en este momento. ¿Podrías intentarlo de nuevo?"
                
        except Exception as e:
            logger.error(f"💥 Error con Gemini: {str(e)}")
            return "⚠️ Estoy teniendo problemas técnicos momentáneos. Por favor, contacta al café directamente al teléfono +1234567890."