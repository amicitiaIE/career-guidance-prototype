import streamlit as st
from caas_assessment import show_assessment_page, initialize_assessment_state
from background_form import show_background_page, initialize_background_state
from recommendations import (
    show_recommendations_page,
    show_career_paths,
    show_skill_development,
    show_resources
)

def main():
    # Set page config
    st.set_page_config(
        page_title="Career Guidance Assistant",
        page_icon="🎯",
        layout="wide"
    )

    # Initialize session state if not already done
    if 'page' not in st.session_state:
        st.session_state.page = 'welcome'

    # Create sidebar navigation
    with st.sidebar:
        st.title("Navigation")
        if st.button("Home", use_container_width=True):
            st.session_state.page = 'welcome'
        if st.button("Start Assessment", use_container_width=True):
            st.session_state.page = 'assessment'
            initialize_assessment_state()
        if st.button("Background Information", use_container_width=True):
            st.session_state.page = 'background'
            initialize_background_state()
        if st.button("View Recommendations", use_container_width=True):
            st.session_state.page = 'recommendations'

    # Page routing
    if st.session_state.page == 'welcome':
        show_welcome_page()
    elif st.session_state.page == 'assessment':
        show_assessment_page()
    elif st.session_state.page == 'background':
        show_background_page()
    elif st.session_state.page == 'recommendations':
        show_recommendations_page()

def show_welcome_page():
    st.title("Welcome to Your Career Journey")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        ## Your Path to Career Success Starts Here
        
        Welcome to our AI-powered career guidance platform, designed specifically to help you:
        
        - Discover your career strengths and abilities
        - Understand your career adaptability
        - Get personalized career recommendations
        - Connect with local resources and opportunities
        
        This tool uses the Career Adapt-Abilities Scale (CAAS) to help understand your:
        - **Concern**: How you think about your career future
        - **Control**: Your approach to making career decisions
        - **Curiosity**: Your exploration of possible opportunities
        - **Confidence**: Your belief in achieving career goals
        """)
        
        if st.button("Begin Assessment →", type="primary"):
            st.session_state.page = 'assessment'
            initialize_assessment_state()

    with col2:
        st.markdown("""
        ### What to Expect
        
        1. Complete a brief assessment
        2. Share your background and interests
        3. Receive personalized guidance
        4. Connect with local resources
        
        *Your responses will be kept confidential and used only to provide personalized recommendations.*
        """)

if __name__ == "__main__":
    main()