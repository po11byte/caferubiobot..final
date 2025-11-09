from flask import Flask, request, jsonify
from dotenv import load_dotenv
import os
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Cargar variables de entorno
load_dotenv()

app = Flask(__name__)

# Importar servicios después de cargar las variables de entorno
try:
    from services.twilio_service import TwilioService
    from services.gemini_service import GeminiService
    
    # Inicializar servicios
    twilio_service = TwilioService()
    gemini_service = GeminiService()
    logger.info(" Servicios inicializados correctamente")
    
except Exception as e:
    logger.error(f" Error inicializando servicios: {str(e)}")
    twilio_service = None
    gemini_service = None

@app.route('/')
def home():
    return """
    <h1> Café Rubio Bot está funcionando!</h1>
    <p>Servicio activo y listo para recibir mensajes.</p>
    <p>Verificar <a href="/health">health check</a></p>
    """

@app.route('/webhook', methods=['POST'])
def webhook():
    """Webhook para recibir mensajes de WhatsApp"""
    try:
        # Log de depuración
        logger.info(" Webhook recibido")
        logger.info(f"Datos recibidos: {request.form}")
        
        # Obtener datos del mensaje
        incoming_msg = request.form.get('Body', '').strip()
        from_number = request.form.get('From', '')
        
        logger.info(f" Mensaje de {from_number}: {incoming_msg}")
        
        # Verificar que los servicios estén inicializados
        if not gemini_service or not twilio_service:
            logger.error("Servicios no inicializados")
            return jsonify({"status": "error", "message": "Servicios no disponibles"}), 500
        
        # Procesar mensaje con Gemini
        if incoming_msg:
            response_text = gemini_service.generate_response(incoming_msg)
            logger.info(f" Respuesta generada: {response_text}")
            
            # Enviar respuesta por Twilio
            success = twilio_service.send_whatsapp_message(
                to_number=from_number,
                message=response_text
            )
            
            if success:
                logger.info(" Mensaje enviado exitosamente")
                return jsonify({"status": "success"})
            else:
                logger.error(" Error enviando mensaje")
                return jsonify({"status": "error", "message": "Error enviando respuesta"}), 500
        else:
            logger.warning(" Mensaje vacío recibido")
            return jsonify({"status": "no message"})
            
    except Exception as e:
        logger.error(f" Error en webhook: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/health', methods=['GET'])
def health_check():
    """Endpoint para verificar el estado del servicio"""
    status = {
        "status": "healthy",
        "service": "Café Rubio Bot",
        "twilio_configured": bool(os.getenv('TWILIO_ACCOUNT_SID')),
        "gemini_configured": bool(os.getenv('GEMINI_API_KEY')),
        "services_ready": bool(gemini_service and twilio_service)
    }
    return jsonify(status)

@app.route('/test', methods=['GET'])
def test():
    """Endpoint de prueba para verificar funcionamiento básico"""
    try:
        test_message = "Hola, ¿están abiertos hoy?"
        if gemini_service:
            response = gemini_service.generate_response(test_message)
            return jsonify({
                "test_message": test_message,
                "response": response,
                "status": "success"
            })
        else:
            return jsonify({"status": "error", "message": "Gemini service not available"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    logger.info(f" Iniciando servidor en puerto {port}")
    app.run(host='0.0.0.0', port=port, debug=False)