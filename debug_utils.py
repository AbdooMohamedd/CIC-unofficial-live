import streamlit as st
import google.generativeai as genai
from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError
import os
from datetime import datetime
from config import GEMINI_API_KEY, MONGODB_CONNECTION_STRING

def check_gemini_api():
    """Test the Gemini API connection and return status"""
    try:
        genai.configure(api_key=GEMINI_API_KEY)
        model = genai.GenerativeModel('gemini-2.0-flash')
        response = model.generate_content("Reply with 'Connection successful' if you can read this message.")
        
        if "Connection successful" in response.text:
            return True, "Gemini API connection successful"
        else:
            return True, f"Connected but unexpected response: {response.text[:100]}"
    
    except Exception as e:
        return False, f"Gemini API error: {str(e)}"

def check_mongodb():
    """Test the MongoDB connection and return status"""
    try:
        client = MongoClient(MONGODB_CONNECTION_STRING, serverSelectionTimeoutMS=5000)
        server_info = client.server_info()
        
        return True, f"MongoDB connection successful (version: {server_info.get('version')})"
    
    except ServerSelectionTimeoutError:
        return False, "MongoDB connection timeout - is the server running?"
    except Exception as e:
        return False, f"MongoDB error: {str(e)}"

def run_diagnostics():
    """Run diagnostics on all connections and dependencies"""
    st.header("System Diagnostics")
    
    # Check Gemini API
    with st.spinner("Testing Gemini API connection..."):
        gemini_success, gemini_message = check_gemini_api()
        
        if gemini_success:
            st.success(f"✅ {gemini_message}")
        else:
            st.error(f"❌ {gemini_message}")
    
    # Check MongoDB
    with st.spinner("Testing MongoDB connection..."):
        mongo_success, mongo_message = check_mongodb()
        
        if mongo_success:
            st.success(f"✅ {mongo_message}")
        else:
            st.error(f"❌ {mongo_message}")
    
    # Environment info
    st.subheader("Environment Information")
    st.code(f"""
Python: {os.sys.version}
Streamlit: {st.__version__}
API Key: {'Configured' if GEMINI_API_KEY else 'Missing'}
MongoDB URI: {'Configured' if MONGODB_CONNECTION_STRING else 'Missing'}
Timestamp: {datetime.now()}
    """)
    
    # Recommendations
    if not gemini_success or not mongo_success:
        st.warning("⚠️ Some connections failed. Here are some troubleshooting steps:")
        
        if not gemini_success:
            st.markdown("""
            ### Gemini API Issues
            1. Check your API key in the `.env` file
            2. Make sure you have access to the Gemini API
            3. Ensure your API key has the necessary permissions
            4. Check your internet connection
            """)
        
        if not mongo_success:
            st.markdown("""
            ### MongoDB Issues
            1. Ensure MongoDB is installed and running
            2. Check the connection string in your `.env` file
            3. For local MongoDB: Start MongoDB service or run `mongod`
            4. For MongoDB Atlas: Check your network connection and whitelist your IP
            """)