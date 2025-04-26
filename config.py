import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API Configuration
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL = "gemini-2.0-flash"

# MongoDB Configuration
MONGODB_CONNECTION_STRING = os.getenv("MONGODB_CONNECTION_STRING", "mongodb://localhost:27017")
MONGODB_DB_NAME = os.getenv("MONGODB_DB_NAME", "customer_service")
MONGODB_COLLECTION = os.getenv("MONGODB_COLLECTION", "conversations")

# App Configuration
COMPANY_NAME = "Canadian International College (CIC)"
SUPPORT_EMAIL = "info@cic-cairo.com"  # General Info Email
SUPPORT_PHONE = "(+202) 19242"  # Hotline
COMPANY_ADDRESS = "South of Police Academy, New Cairo, Cairo Governorate, Egypt" # New Cairo Campus