import streamlit as st
from patterns.singleton import GeminiConnector
from patterns.factory import ResponseFactory
from patterns.decorator import BaseResponse, TimestampDecorator, FormattingDecorator
from patterns.observer import ChatSubject, StreamlitChatObserver, DatabaseChatObserver
from database.mongodb import MongoDBConnector
import time

# Initialize the chat subject and observers
chat_subject = ChatSubject()
streamlit_observer = StreamlitChatObserver()
db_connector = MongoDBConnector()
db_observer = DatabaseChatObserver(db_connector)

# Attach observers
chat_subject.attach(streamlit_observer)
chat_subject.attach(db_observer)

def show():
    st.markdown('<h1 class="main-header">CIC AI Assistant</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Ask me anything about CIC programs, admissions, campus life, and more!</p>', unsafe_allow_html=True)

    # Initialize the Gemini API connection using Singleton
    gemini_connector = GeminiConnector()

    # --- Chat Display Area ---
    # Use a dedicated container with a specific height and scrollbar
    chat_container = st.container(height=400) # Adjust height as needed
    with chat_container:
        # Check for prefilled question from home page
        prefill_question = st.session_state.pop('prefill_chat', None)
        if prefill_question and 'chat_history' in st.session_state and not any(msg['content'] == prefill_question for msg in st.session_state.chat_history if msg['role'] == 'user'):
             # Add prefilled question as user message and get response immediately
             user_message = {"role": "user", "content": prefill_question, "timestamp": time.time()}
             if 'chat_history' not in st.session_state:
                 st.session_state.chat_history = []
             st.session_state.chat_history.append(user_message)
             try:
                 response_text = gemini_connector.get_response(prefill_question)
                 bot_message = {"role": "assistant", "content": response_text, "timestamp": time.time()}
                 st.session_state.chat_history.append(bot_message)
                 # Optionally save to DB here if needed
                 # db_connector.save_conversation({...})
             except Exception as e:
                 error_message = {"role": "assistant", "content": f"Sorry, I encountered an error processing your request: {str(e)}", "timestamp": time.time()}
                 st.session_state.chat_history.append(error_message)
             # No rerun here, let the normal display flow handle it

        # Display chat history
        for message in st.session_state.get('chat_history', []):
            role = message.get("role", "unknown")
            content = message.get("content", "")
            # Escape content safely
            safe_content = content.replace('<', '&lt;').replace('>', '&gt;') \
                                  .replace('{', '&#123;').replace('}', '&#125;')
            
            if role == "user":
                chat_container.markdown(f'<div class="chat-message user-message"><strong>You:</strong><br>{safe_content}</div>', unsafe_allow_html=True)
            elif role == "assistant":
                chat_container.markdown(f'<div class="chat-message bot-message"><strong>CIC Assistant:</strong><br>{safe_content}</div>', unsafe_allow_html=True)
            else:
                 chat_container.markdown(f'<div class="chat-message"><strong>System:</strong><br>{safe_content}</div>', unsafe_allow_html=True)

    st.markdown("--- ") # Separator

    # --- Chat Input Area ---
    # Use columns for better layout
    col_input, col_button = st.columns([4, 1])
    with col_input:
        user_input = st.text_input("Your message:", key="input_message", placeholder="Ask about programs, admissions, etc.", label_visibility="collapsed")
    with col_button:
        submit_button = st.button("Send", key="send_button", use_container_width=True)

    # --- Action Buttons ---
    col_a, col_b, col_c = st.columns(3)
    with col_a:
        if st.button("✨ Sample Questions", key="show_samples_btn", use_container_width=True):
            st.session_state.show_samples = not st.session_state.get('show_samples', False)
            st.rerun()
    with col_b:
        if st.button("🔄 Clear Chat", key="clear_chat_btn", use_container_width=True):
            st.session_state.chat_history = []
            gemini_connector.reset_chat()
            st.rerun()
    with col_c:
        # Add a button to go back home or to resources
        if st.button("🏠 Back to Home", key="back_home_btn", use_container_width=True):
            st.session_state.page = "Home"
            st.rerun()

    # Process user input
    if submit_button and user_input:
        # Add user message
        user_message = {"role": "user", "content": user_input, "timestamp": time.time()}
        if 'chat_history' not in st.session_state:
            st.session_state.chat_history = []
        st.session_state.chat_history.append(user_message)
        
        try:
            # Get response from Gemini API
            response_text = gemini_connector.get_response(user_input)
            
            # Process response using Factory pattern (if still applicable)
            # response_handler = ResponseFactory.create_handler(user_input)
            # processed_response = response_handler.process_response(user_input, response_text)
            
            # Apply decorators (if still applicable)
            # base_response = BaseResponse(processed_response)
            # formatted_response = FormattingDecorator(base_response)
            # timestamped_response = TimestampDecorator(formatted_response)
            # final_response = timestamped_response.get_content()
            # display_text = ... extract text ...
            
            # Simplified: Use direct response for now
            display_text = response_text
            
            # Add bot message
            bot_message = {"role": "assistant", "content": display_text, "timestamp": time.time()}
            st.session_state.chat_history.append(bot_message)
            
            # Store in MongoDB (Simplified)
            db_connector.save_conversation({
                "user_query": user_input,
                "bot_response": display_text,
                "timestamp": time.time()
            })
            
        except Exception as e:
            error_message = {"role": "assistant", "content": f"Sorry, I encountered an error: {str(e)}", "timestamp": time.time()}
            st.session_state.chat_history.append(error_message)
            
        # Rerun to display new messages
        st.rerun()

    # Show sample questions if requested
    if st.session_state.get('show_samples', False):
        st.markdown("--- ")
        st.subheader("Sample Questions")
        sample_questions = [
            "What programs are offered at CIC?",
            "What are the admission requirements for Engineering?",
            "Tell me about the New Cairo campus.",
            "How can I apply to CIC?",
            "What are the tuition fees?",
            "Can I study part of my degree in Canada?",
            "What majors are in Mass Communication?",
            "Is there a Computer Science program?"
        ]
        
        cols = st.columns(2) # Display samples in two columns
        col_idx = 0
        for question in sample_questions:
            with cols[col_idx % 2]:
                if st.button(question, key=f"sample_{question}", use_container_width=True):
                    # Set the question as input and submit immediately
                    user_message = {"role": "user", "content": question, "timestamp": time.time()}
                    if 'chat_history' not in st.session_state:
                        st.session_state.chat_history = []
                    st.session_state.chat_history.append(user_message)
                    
                    try:
                        response_text = gemini_connector.get_response(question)
                        bot_message = {"role": "assistant", "content": response_text, "timestamp": time.time()}
                        st.session_state.chat_history.append(bot_message)
                        
                        # Store in MongoDB
                        db_connector.save_conversation({
                            "user_query": question,
                            "bot_response": response_text,
                            "timestamp": time.time()
                        })
                    except Exception as e:
                        error_message = {"role": "assistant", "content": f"Sorry, I encountered an error: {str(e)}", "timestamp": time.time()}
                        st.session_state.chat_history.append(error_message)
                    
                    st.session_state.show_samples = False # Hide samples after selection
                    st.rerun()
            col_idx += 1