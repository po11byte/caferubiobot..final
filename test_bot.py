import os
from dotenv import load_dotenv

load_dotenv()

print("🔧 Verificando variables de entorno:")
print(f"TWILIO_ACCOUNT_SID: {'✅' if os.getenv('TWILIO_ACCOUNT_SID') else '❌'}")
print(f"TWILIO_AUTH_TOKEN: {'✅' if os.getenv('TWILIO_AUTH_TOKEN') else '❌'}")  
print(f"TWILIO_PHONE_NUMBER: {'✅' if os.getenv('TWILIO_PHONE_NUMBER') else '❌'}")
print(f"GEMINI_API_KEY: {'✅' if os.getenv('GEMINI_API_KEY') else '❌'}")