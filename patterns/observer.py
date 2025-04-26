from abc import ABC, abstractmethod
from typing import List
import streamlit as st

class ChatObserver(ABC):
    @abstractmethod
    def update(self, message):
        pass

class ChatSubject:
    _observers: List[ChatObserver] = []
    
    def attach(self, observer):
        if observer not in self._observers:
            self._observers.append(observer)
    
    def detach(self, observer):
        self._observers.remove(observer)
    
    def notify(self, message):
        for observer in self._observers:
            observer.update(message)

class StreamlitChatObserver(ChatObserver):
    def update(self, message):
        # This method will update the Streamlit UI with new messages
        if 'chat_history' not in st.session_state:
            st.session_state.chat_history = []
        
        st.session_state.chat_history.append(message)
        
        # Force a rerun to update the UI
        st.rerun()

class DatabaseChatObserver(ChatObserver):
    def __init__(self, db_connector):
        self.db = db_connector
    
    def update(self, message):
        # Save the message to the database
        self.db.save_conversation(message)