import streamlit as st
from views import home, chat, support  # Changed from "pages" to "views"
from debug_utils import run_diagnostics

# --- Page Configuration ---
st.set_page_config(
    page_title="CIC Assistant Portal",
    page_icon="https://www.cic-cairo.edu.eg/wp-content/uploads/2023/07/cropped-favicon-32x32.png", # Use CIC favicon
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CIC Logo URL ---
CIC_LOGO_URL = "CIC - 20 Years Logo-Final after el 90 amendments-02.png"

# --- Custom CSS ---
st.markdown(f"""
<style>
    /* General Styles */
    .stApp {{ 
        /* Add background or other global styles if desired */
    }}

    /* Sidebar Styles */
    [data-testid="stSidebar"] > div:first-child {{
        padding-top: 1rem;
        display: flex;
        flex-direction: column;
        align-items: center; /* Center logo */
    }}
    [data-testid="stSidebar"] .sidebar-content {{
        padding: 1rem;
    }}
    [data-testid="stSidebar"] h2 {{
        text-align: center; /* Center title */
        margin-top: 1rem;
        margin-bottom: 1rem;
    }}

    /* Logo */
    .sidebar-logo {{
        width: 80%; /* Adjust size as needed */
        margin-bottom: 1rem;
        max-width: 200px; /* Max size */
    }}

    /* Headers */
    .main-header {{
        font-size: 2.2rem; /* Slightly smaller */
        color: #00447C; /* Dark Blue - Adjust if CIC has specific brand colors */
        margin-bottom: 0.5rem;
        border-bottom: 2px solid #00447C;
        padding-bottom: 0.3rem;
    }}
    .sub-header {{
        font-size: 1.4rem;
        color: #555;
        margin-bottom: 1.5rem;
    }}

    /* Chat Messages */
    .chat-message {{
        padding: 0.8rem 1rem;
        border-radius: 0.5rem;
        margin-bottom: 0.7rem;
        color: white;
        border-left: 5px solid transparent;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }}
    .user-message {{
        background-color: #007bff; /* Standard blue for user */
        border-left-color: #0056b3;
        margin-left: auto; /* Align user messages to the right */
        max-width: 75%;
        text-align: left;
    }}
    .bot-message {{
        background-color: #f0f2f5; /* Light grey for bot */
        color: #333; /* Darker text for bot */
        border-left-color: #ccc;
        margin-right: auto; /* Align bot messages to the left */
        max-width: 75%;
        text-align: left;
    }}
    .chat-message strong {{
        display: block;
        margin-bottom: 0.3rem;
        font-size: 0.9rem;
    }}
    .chat-message a {{
        color: #0056b3; /* Link color for bot messages */
    }}
    .user-message a {{
        color: #ffffff; /* Link color for user messages */
        text-decoration: underline;
    }}

    /* Expander styling */
    .st-expander {{ 
        border: 1px solid #ddd;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
    }}
    .st-expander header {{
        font-weight: bold;
        background-color: #f7f7f7;
        padding: 0.8rem 1rem;
        border-top-left-radius: 0.5rem;
        border-top-right-radius: 0.5rem;
    }}

    /* Button styling */
    .stButton>button {{
        border-radius: 0.3rem;
        /* Add more button styles if needed */
    }}

</style>
""", unsafe_allow_html=True)

# --- Sidebar Navigation ---
# Add custom CSS to modify sidebar appearance
st.markdown("""
<style>
    /* Hide the development menu text items that show up in dev mode if possible */
    section[data-testid="stSidebarNav"] {
        visibility: hidden;
        height: 0;
        position: absolute;
    }
    
    /* Increase space above logo */
    [data-testid="stSidebar"] > div:first-child {
        padding-top: 2rem;
    }
    
    /* Make nav buttons more prominent */
    .sidebar-nav-button {
        margin-bottom: 0.8rem;
        border: none;
    }
</style>
""", unsafe_allow_html=True)

# Logo at top of sidebar
st.sidebar.image(CIC_LOGO_URL, use_container_width=True, output_format='PNG')

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

# Create buttons for navigation with better styling
for option in page_options:
    if st.sidebar.button(option, key=f"nav_{option}", use_container_width=True, 
                        on_click=set_page, args=(option,), 
                        type="primary" if st.session_state.page == option else "secondary"):
        pass  # on_click handles the state change

st.sidebar.markdown('</div>', unsafe_allow_html=True)

# --- Session State Initialization ---
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

# --- Page Routing ---
current_page = st.session_state.get('page', "Home")

if current_page == "Home":
    home.show()
elif current_page == "Chat Assistant":
    # Update page title for consistency
    st.session_state.page = "Chat Assistant" # Ensure state is correct if navigated directly
    chat.show()
elif current_page == "Contact & Resources":
    support.show()
else:
    # Default to home if state is invalid
    st.session_state.page = "Home"
    home.show()