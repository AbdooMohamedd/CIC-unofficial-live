from pymongo import MongoClient
from config import MONGODB_CONNECTION_STRING, MONGODB_DB_NAME, MONGODB_COLLECTION
import streamlit as st

class MongoDBConnector:
    def __init__(self):
        try:
            print(f"Connecting to MongoDB at: {MONGODB_CONNECTION_STRING}")
            self.client = MongoClient(MONGODB_CONNECTION_STRING, serverSelectionTimeoutMS=5000)
            # Verify connection
            self.client.server_info()
            print("MongoDB connection successful")
            
            self.db = self.client[MONGODB_DB_NAME]
            self.collection = self.db[MONGODB_COLLECTION]
        except Exception as e:
            print(f"MongoDB connection error: {str(e)}")
            st.error(f"Failed to connect to MongoDB: {str(e)}")
    
    def save_conversation(self, message_data):
        """Save a conversation message to MongoDB"""
        try:
            print(f"Saving to MongoDB: {str(message_data)[:50]}...")
            # Ensure message_data is a dict
            if not isinstance(message_data, dict):
                message_data = {'content': str(message_data)}
            
            # Add timestamp if not present
            if 'timestamp' not in message_data:
                from datetime import datetime
                message_data['timestamp'] = datetime.now()
            
            result = self.collection.insert_one(message_data)
            print(f"Successfully saved to MongoDB with ID: {result.inserted_id}")
            return result.inserted_id
        except Exception as e:
            print(f"Error saving to MongoDB: {str(e)}")
            st.warning(f"Failed to save conversation to database: {str(e)}")
            return None
    
    def get_conversations(self, limit=100):
        """Retrieve conversations from MongoDB"""
        try:
            return list(self.collection.find().sort('timestamp', -1).limit(limit))
        except Exception as e:
            print(f"Error retrieving conversations: {str(e)}")
            return []
    
    def get_conversation_by_id(self, conversation_id):
        """Get a specific conversation by ID"""
        from bson.objectid import ObjectId
        return self.collection.find_one({'_id': ObjectId(conversation_id)})
    
    def close_connection(self):
        """Close the MongoDB connection"""
        self.client.close()