import streamlit as st
from config import COMPANY_NAME, SUPPORT_EMAIL, SUPPORT_PHONE, COMPANY_ADDRESS

def show():
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