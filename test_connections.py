# save as test_connections.py
import google.generativeai as genai
from pymongo import MongoClient
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Test Gemini API
def test_gemini():
    print("Testing Gemini API connection...")
    try:
        gemini_key = os.getenv("GEMINI_API_KEY")
        print(f"Using API key starting with: {gemini_key[:5]}...")
        
        genai.configure(api_key=gemini_key)
        model = genai.GenerativeModel('gemini-2.0-flash')
        response = model.generate_content("Say hello world")
        
        print(f"Gemini response: {response.text}")
        print("Gemini API connection successful!")
        return True
    except Exception as e:
        print(f"Gemini API connection failed: {str(e)}")
        return False

# Test MongoDB connection
def test_mongodb():
    print("Testing MongoDB connection...")
    try:
        conn_string = os.getenv("MONGODB_CONNECTION_STRING")
        print(f"Using connection string: {conn_string}")
        
        client = MongoClient(conn_string, serverSelectionTimeoutMS=5000)
        server_info = client.server_info()
        
        print(f"MongoDB version: {server_info.get('version')}")
        print("MongoDB connection successful!")
        return True
    except Exception as e:
        print(f"MongoDB connection failed: {str(e)}")
        return False

if __name__ == "__main__":
    test_gemini()
    print("\n" + "-"*50 + "\n")
    test_mongodb()