import streamlit as st
import os
from config import COMPANY_NAME

def show():
    # Define image paths
    current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    cairo_img_path = os.path.join(current_dir, "cairo.png")
    zayed_img_path = os.path.join(current_dir, "Zayed.png")
    
    st.markdown(f'<h1 class="main-header">Welcome to {COMPANY_NAME}</h1>', unsafe_allow_html=True)
    
    # Add Cairo campus image below the title with proper path
    if os.path.exists(cairo_img_path):
        # Increase size by adjusting column proportions - wider middle column
        col1, col2, col3 = st.columns([1, 4, 1])  # Changed from [1, 2, 1] to [1, 4, 1] to make it larger
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
            # Link to a future dedicated programs page or scroll to relevant section
            # For now, maybe link to support/resources or trigger chat
            st.session_state.page = "Contact & Resources" # Go to resources for now
            st.rerun()
        if st.button("Admission Process", key="home_admission_btn", use_container_width=True):
            # Link to admission info or trigger chat
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
        # Add links to actual student portals/resources when available
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
    # Using session state for FAQ visibility is good, keep it if needed or simplify
    # if st.session_state.get('show_faq', False):
    with st.expander("What programs does CIC offer?"):
        st.write("CIC offers programs in Engineering, Mass Communication, Business Administration, Business Technology, and Computer Science. Some programs offer a Dual Degree option with Cape Breton University (CBU).")
    
    with st.expander("What are the admission requirements?"):
        st.write("Admissions are primarily handled through the governmental Tansik platform after high school results. You generally need to list CIC as your first preference and meet the minimum grade requirements set by the Ministry. An English placement test is also required.")
    
    with st.expander("Can I study in Canada?"):
        st.write("Yes, CIC offers pathways to study in Canada, particularly at our partner institution, Cape Breton University (CBU), through transfer or exchange programs.")
    
    with st.expander("Where is CIC located?"):
        st.write("CIC has two main campuses: one in New Cairo (Fifth Settlement) and one in Sheikh Zayed City (6th of October). You can find specific addresses on our Contact page.")
    
    # Reset FAQ visibility toggle if used
    # if 'show_faq' in st.session_state:
    #     del st.session_state['show_faq']