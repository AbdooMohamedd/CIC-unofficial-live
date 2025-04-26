import streamlit as st
import os
import time
from patterns.singleton import GeminiConnector
from database.mongodb import MongoDBConnector
from patterns.observer import ChatSubject, StreamlitChatObserver, DatabaseChatObserver
from config import COMPANY_NAME, SUPPORT_EMAIL, SUPPORT_PHONE, COMPANY_ADDRESS

# --- Initialize services ---
# Chat services
chat_subject = ChatSubject()
streamlit_observer = StreamlitChatObserver()
db_connector = MongoDBConnector()
db_observer = DatabaseChatObserver(db_connector)
chat_subject.attach(streamlit_observer)
chat_subject.attach(db_observer)

# --- Page Configuration ---
st.set_page_config(
    page_title="CIC Assistant Portal",
    page_icon="https://www.cic-cairo.edu.eg/wp-content/uploads/2023/07/cropped-favicon-32x32.png",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Image paths ---
current_dir = os.path.dirname(os.path.abspath(__file__))
cairo_img_path = os.path.join(current_dir, "cairo.png")
zayed_img_path = os.path.join(current_dir, "Zayed.png")
CIC_LOGO_URL = os.path.join(current_dir, "CIC - 20 Years Logo-Final after el 90 amendments-02.png")

# --- Custom CSS ---
st.markdown("""
<style>
    /* General Styles */
    .stApp { 
        /* Add background or other global styles if desired */
    }

    /* Sidebar Styles */
    [data-testid="stSidebar"] > div:first-child {
        padding-top: 1rem;
        display: flex;
        flex-direction: column;
        align-items: center; /* Center logo */
    }
    [data-testid="stSidebar"] .sidebar-content {
        padding: 1rem;
    }
    [data-testid="stSidebar"] h2 {
        text-align: center; /* Center title */
        margin-top: 1rem;
        margin-bottom: 1rem;
    }
    
    /* Hide the development menu text items */
    section[data-testid="stSidebarNav"] {
        visibility: hidden;
        height: 0;
        position: absolute;
    }

    /* Logo */
    .sidebar-logo {
        width: 80%; /* Adjust size as needed */
        margin-bottom: 1rem;
        max-width: 200px; /* Max size */
    }

    /* Headers */
    .main-header {
        font-size: 2.2rem; /* Slightly smaller */
        color: #00447C; /* Dark Blue */
        margin-bottom: 0.5rem;
        border-bottom: 2px solid #00447C;
        padding-bottom: 0.3rem;
    }
    .sub-header {
        font-size: 1.4rem;
        color: #555;
        margin-bottom: 1.5rem;
    }

    /* Chat Messages */
    .chat-message {
        padding: 0.8rem 1rem;
        border-radius: 0.5rem;
        margin-bottom: 0.7rem;
        color: white;
        border-left: 5px solid transparent;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .user-message {
        background-color: #007bff; /* Standard blue for user */
        border-left-color: #0056b3;
        margin-left: auto; /* Align user messages to the right */
        max-width: 75%;
        text-align: left;
    }
    .bot-message {
        background-color: #f0f2f5; /* Light grey for bot */
        color: #333; /* Darker text for bot */
        border-left-color: #ccc;
        margin-right: auto; /* Align bot messages to the left */
        max-width: 75%;
        text-align: left;
    }
    .chat-message strong {
        display: block;
        margin-bottom: 0.3rem;
        font-size: 0.9rem;
    }
    .chat-message a {
        color: #0056b3; /* Link color for bot messages */
    }
    .user-message a {
        color: #ffffff; /* Link color for user messages */
        text-decoration: underline;
    }

    /* Expander styling */
    .st-expander { 
        border: 1px solid #ddd;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
    }
    .st-expander header {
        font-weight: bold;
        background-color: #f7f7f7;
        padding: 0.8rem 1rem;
        border-top-left-radius: 0.5rem;
        border-top-right-radius: 0.5rem;
    }

    /* Button styling */
    .stButton>button {
        border-radius: 0.3rem;
        /* Add more button styles if needed */
    }
</style>
""", unsafe_allow_html=True)

# --- Sidebar Navigation ---
# Logo at top of sidebar
if os.path.exists(CIC_LOGO_URL):
    st.sidebar.image(CIC_LOGO_URL, use_container_width=True)
else:
    st.sidebar.error("Logo not found")

# Remove Navigation header text and use space instead
st.sidebar.markdown("&nbsp;", unsafe_allow_html=True)
st.sidebar.markdown('<div class="sidebar-content">', unsafe_allow_html=True)

# Define page options
page_options = ["Home", "Chat Assistant", "Contact & Resources"]

# Use session state to manage the current page
if 'page' not in st.session_state:
    st.session_state.page = "Home"

def set_page(page_name):
    st.session_state.page = page_name

# Create buttons for navigation 
for option in page_options:
    if st.sidebar.button(option, key=f"nav_{option}", use_container_width=True, 
                        on_click=set_page, args=(option,), 
                        type="primary" if st.session_state.page == option else "secondary"):
        pass  # on_click handles the state change

st.sidebar.markdown('</div>', unsafe_allow_html=True)

# --- Session State Initialization ---
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

# --- PAGE DEFINITIONS ---

# --- HOME PAGE ---
def show_home():
    st.markdown(f'<h1 class="main-header">Welcome to {COMPANY_NAME}</h1>', unsafe_allow_html=True)
    
    # Add Cairo campus image below the title with proper path
    if os.path.exists(cairo_img_path):
        # Increase size by adjusting column proportions - wider middle column
        col1, col2, col3 = st.columns([1, 4, 1])  
        with col2:
            st.image(cairo_img_path, caption="CIC New Cairo Campus", use_container_width=True)
    else:
        st.error(f"Image not found: {cairo_img_path}")
        
    st.markdown('<h2 class="sub-header">Your Gateway to Canadian Education in Egypt</h2>', unsafe_allow_html=True)
    
    st.markdown("--- ") # Separator

    # --- Quick Access Sections --
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("🚀 For Prospective Students")
        st.markdown("Planning to join CIC? Find quick links below:")
        if st.button("Explore Programs", key="home_programs_btn", use_container_width=True):
            st.session_state.page = "Contact & Resources" 
            st.rerun()
        if st.button("Admission Process", key="home_admission_btn", use_container_width=True):
            st.session_state.page = "Chat Assistant"
            st.session_state.prefill_chat = "Tell me about the admission process"
            st.rerun()
        if st.button("Campus Tour Info", key="home_tour_btn", use_container_width=True):
            st.session_state.page = "Contact & Resources"
            st.rerun()
        if st.button("Ask the AI Assistant", key="home_ask_new_btn", use_container_width=True):
            st.session_state.page = "Chat Assistant"
            st.rerun()

    with col2:
        st.subheader("🎓 For Current Students")
        st.markdown("Access resources and information:")
        st.link_button("Student Portal (Example)", "https://example.com/student-portal", use_container_width=True)
        st.link_button("Library Access (Example)", "https://example.com/library", use_container_width=True)
        st.link_button("Academic Calendar (Example)", "https://example.com/calendar", use_container_width=True)
        if st.button("Get Support from AI", key="home_ask_current_btn", use_container_width=True):
            st.session_state.page = "Chat Assistant"
            st.rerun()

    st.markdown("--- ") # Separator

    # --- General Information ---
    st.markdown("### About CIC")
    st.markdown(f"""
    At {COMPANY_NAME}, we offer a unique educational experience combining Canadian curriculum with Egyptian culture. Since 2004, we have been providing top-tier post-secondary education, granting both Canadian and Egyptian degrees through our partnerships.
    
    **Our AI assistant can help with:**
    - **Admissions**: Requirements, deadlines, application process.
    - **Programs**: Details about our faculties (Business, Engineering, Mass Communication, IT, Computer Science).
    - **Campus Life**: Facilities, activities, student services.
    - **General Information**: Partnerships, study in Canada options.
    
    Navigate using the sidebar or use the quick links above.
    """)

    # --- Image and Testimonial ---
    st.markdown("--- ")
    col_img, col_quote = st.columns([1, 2])
    with col_img:
        # Add Zayed campus image with proper path
        if os.path.exists(zayed_img_path):
            st.image(zayed_img_path, caption="CIC Sheikh Zayed Campus", use_container_width=True)
        else:
            st.error(f"Image not found: {zayed_img_path}")
            
    with col_quote:
        st.markdown("### What Our Students Say")
        st.markdown("""        
        > "Studying at CIC opened doors for me. The Canadian curriculum and supportive environment were key to my success. The dual degree option was invaluable."
        > 
        > — *CIC Graduate*
        """)
        st.markdown("""        
        > "The practical experience and industry connections I gained at CIC prepared me well for my career in engineering."
        > 
        > — *CIC Alumnus*
        """)

    # --- FAQ Section ---
    st.markdown("--- ")
    st.markdown("### Frequently Asked Questions")
    with st.expander("What programs does CIC offer?"):
        st.write("CIC offers programs in Engineering, Mass Communication, Business Administration, Business Technology, and Computer Science. Some programs offer a Dual Degree option with Cape Breton University (CBU).")
    
    with st.expander("What are the admission requirements?"):
        st.write("Admissions are primarily handled through the governmental Tansik platform after high school results. You generally need to list CIC as your first preference and meet the minimum grade requirements set by the Ministry. An English placement test is also required.")
    
    with st.expander("Can I study in Canada?"):
        st.write("Yes, CIC offers pathways to study in Canada, particularly at our partner institution, Cape Breton University (CBU), through transfer or exchange programs.")
    
    with st.expander("Where is CIC located?"):
        st.write("CIC has two main campuses: one in New Cairo (Fifth Settlement) and one in Sheikh Zayed City (6th of October). You can find specific addresses on our Contact page.")

# --- CHAT PAGE ---
def show_chat():
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
             except Exception as e:
                 error_message = {"role": "assistant", "content": f"Sorry, I encountered an error processing your request: {str(e)}", "timestamp": time.time()}
                 st.session_state.chat_history.append(error_message)

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

# --- SUPPORT PAGE ---
def show_support():
    st.markdown('<h1 class="main-header">Contact & Resources</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Get in touch with CIC or find helpful resources.</p>', unsafe_allow_html=True)

    st.markdown("--- ")
    
    col1, col2 = st.columns([1, 1]) # Use equal columns for better balance
    
    with col1:
        st.subheader("📍 Contact Information")
        st.markdown(f"""
        **{COMPANY_NAME}**
        
        **New Cairo Campus:**
        *   South of Police Academy, Fifth Settlement
        *   Hotline: `{SUPPORT_PHONE}`
        *   Email: `{SUPPORT_EMAIL}`
        
        **Sheikh Zayed Campus:**
        *   District 12, Continental Gardens, El Sheikh Zayed City
        *   Phone: `(+202) 3854-3366/7/8`
        *   Email: `info.shz@cic-cairo.com` 
        
        **Business Hours:**
        *   Sunday - Thursday: 9:00 AM - 4:00 PM
        *   Friday - Saturday: Closed
        """)

        st.markdown("--- ")
        st.subheader("🗺️ Campus Maps Links")
        # Replace with actual map links or embedded maps if available
        st.link_button("New Cairo Campus Map", "https://www.google.com/maps/place/Canadian+International+college/@30.0351946,31.4300779,838m/data=!3m1!1e3!4m6!3m5!1s0x14583cd880d6ec4b:0xbaf0462037860f7c!8m2!3d30.0351946!4d31.4300779!16s%2Fm%2F04ycszl?authuser=0&hl=en&entry=ttu&g_ep=EgoyMDI1MDQyMy4wIKXMDSoASAFQAw%3D%3D", use_container_width=True)
        st.link_button("Sheikh Zayed Campus Map", "https://www.google.com/maps/place/Canadian+International+College/@30.0447339,30.9896529,838m/data=!3m1!1e3!4m6!3m5!1s0x14585a27d05b1289:0x4341717216197952!8m2!3d30.0447339!4d30.9896529!16s%2Fg%2F1v9gxmp_?authuser=0&hl=en&entry=ttu&g_ep=EgoyMDI1MDQyMy4wIKXMDSoASAFQAw%3D%3D", use_container_width=True)

    with col2:
        st.subheader("🔗 Quick Links & Resources")
        
        with st.expander("Admissions"):
            st.page_link("https://www.cic-cairo.edu.eg/admission-requirements/", label="Admission Requirements", icon="📄")
            st.page_link("https://www.cic-cairo.edu.eg/how-to-apply/", label="How to Apply", icon="📝")
            st.page_link("https://www.cic-cairo.edu.eg/tuition-fees/", label="Tuition Fees", icon="💰")
            st.page_link("https://www.cic-cairo.edu.eg/scholarships-financial-aid/", label="Scholarships & Financial Aid", icon="🎓")
        
        with st.expander("Academics"):
            st.page_link("https://www.cic-cairo.edu.eg/academic-life/", label="Faculties & Programs", icon="📚")
            st.page_link("https://www.cic-cairo.edu.eg/academic-calendar/", label="Academic Calendar", icon="🗓️")
            st.page_link("https://www.cic-cairo.edu.eg/library/", label="Library", icon="📖")
        
        with st.expander("Student Life"):
            st.page_link("https://www.cic-cairo.edu.eg/campus-facilities/", label="Campus Facilities", icon="🏢")
            st.page_link("https://www.cic-cairo.edu.eg/student-activities/", label="Student Activities", icon="🎉")
            st.page_link("https://www.cic-cairo.edu.eg/career-services/", label="Career Services", icon="💼")
            st.page_link("https://www.cic-cairo.edu.eg/alumni/", label="Alumni Network", icon="🤝")

        st.markdown("--- ")
        st.subheader("✉️ Send Us a Message")
        # Contact form remains largely the same, styling applied via CSS
        with st.form("contact_form"):
            name = st.text_input("Your Name")
            email = st.text_input("Your Email")
            subject = st.selectbox("Subject", [
                "Admission Inquiry", 
                "Program Information",
                "Campus Visit Request",
                "Current Student Issue",
                "Technical Support (Portal)",
                "General Question",
                "Feedback",
                "Other"
            ])
            message = st.text_area("Your Message", height=100)
            
            submit_button = st.form_submit_button("Send Message", use_container_width=True)
            
            if submit_button:
                if name and email and message:
                    st.success("Thank you! Your message has been sent. We'll get back to you soon.")
                    # Save to MongoDB
                    from database.mongodb import MongoDBConnector
                    db = MongoDBConnector()
                    db.save_conversation({
                        "type": "contact_form",
                        "name": name,
                        "email": email,
                        "subject": subject,
                        "message": message
                    })
                else:
                    st.error("Please fill out all required fields.")

# --- MAIN APP ROUTING ---
current_page = st.session_state.get('page', "Home")

if current_page == "Home":
    show_home()
elif current_page == "Chat Assistant":
    show_chat()
elif current_page == "Contact & Resources":
    show_support()
else:
    # Default to home if state is invalid
    st.session_state.page = "Home"
    show_home()