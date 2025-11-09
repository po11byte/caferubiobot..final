import os
import logging
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException

logger = logging.getLogger(__name__)

class TwilioService:
    def __init__(self):
        try:
            self.account_sid = os.getenv('TWILIO_ACCOUNT_SID')
            self.auth_token = os.getenv('TWILIO_AUTH_TOKEN')
            self.phone_number = os.getenv('TWILIO_PHONE_NUMBER')
            
            if not all([self.account_sid, self.auth_token, self.phone_number]):
                raise ValueError("Faltan credenciales de Twilio en las variables de entorno")
            
            self.client = Client(self.account_sid, self.auth_token)
            logger.info(" Twilio service inicializado correctamente")
            
        except Exception as e:
            logger.error(f" Error inicializando Twilio: {str(e)}")
            raise
    
    def send_whatsapp_message(self, to_number: str, message: str) -> bool:
        """Enviar mensaje por WhatsApp"""
        try:
            logger.info(f" Enviando WhatsApp a {to_number}")
            
            message_instance = self.client.messages.create(
                body=message,
                from_=f'whatsapp:{self.phone_number}',
                to=f'whatsapp:{to_number}'
            )
            
            logger.info(f" Mensaje enviado: SID {message_instance.sid}")
            return True
            
        except TwilioRestException as e:
            logger.error(f" Error de Twilio: {e.code} - {e.msg}")
            return False
        except Exception as e:
            logger.error(f" Error enviando mensaje: {str(e)}")
            return False
    
    def send_sms(self, to_number: str, message: str) -> bool:
        """Enviar SMS (opcional)"""
        try:
            message_instance = self.client.messages.create(
                body=message,
                from_=self.phone_number,
                to=to_number
            )
            logger.info(f"SMS enviado: SID {message_instance.sid}")
            return True
        except Exception as e:
            logger.error(f"Error enviando SMS: {str(e)}")
            return False