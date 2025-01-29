import streamlit as st

# Predefined options for form selections
EDUCATION_LEVELS = [
    "Less than high school",
    "Some high school",
    "High school diploma/GED",
    "Some college/vocational training",
    "College degree",
    "Other"
]

INTEREST_AREAS = [
    "Technology & Computers",
    "Healthcare & Medical",
    "Construction & Trades",
    "Business & Administration",
    "Creative Arts & Design",
    "Education & Teaching",
    "Food Service & Hospitality",
    "Manufacturing & Production",
    "Transportation & Logistics",
    "Other"
]

POTENTIAL_BARRIERS = [
    "Transportation issues",
    "Childcare needs",
    "Housing instability",
    "Legal concerns",
    "Health/medical issues",
    "Lack of work experience",
    "Education gaps",
    "Technology access",
    "Other"
]

# UK Counties for location selection
UK_COUNTIES = [
    "Greater London",
    "Greater Manchester",
    "West Midlands",
    "West Yorkshire",
    "Kent",
    "Essex",
    "Merseyside",
    "South Yorkshire",
    "Hampshire",
    "Surrey",
    # Add more counties as needed
]

def initialize_background_state():
    """Initialize session state variables for background information"""
    if 'background_info' not in st.session_state:
        st.session_state.background_info = {
            'county': '',
            'postcode_area': '',
            'education': '',
            'current_situation': '',
            'interests': [],
            'barriers': [],
            'support_systems': '',
            'goals': '',
            'additional_info': ''
        }

def show_background_page():
    initialize_background_state()
    
    st.title("Background Information")
    st.write("Please share some information to help us provide more personalized career guidance.")

    # Create tabs for different sections
    tabs = st.tabs(["Education & Location", "Interests & Goals", "Barriers & Support"])

    with tabs[0]:
        show_education_location_section()
    
    with tabs[1]:
        show_interests_section()
    
    with tabs[2]:
        show_barriers_section()

    # Save and Continue button
    if all_required_fields_filled():
        if st.button("Save and Continue to Recommendations →", type="primary"):
            save_background_info()
            st.session_state.page = 'recommendations'
            st.rerun()
    else:
        st.warning("Please fill in all required fields to continue.")

def show_education_location_section():
    st.subheader("Education & Location")
    
    # Location information
    col1, col2 = st.columns(2)
    
    with col1:
        selected_county = st.selectbox(
            "Select your county/region: *",
            options=[""] + UK_COUNTIES,
            index=UK_COUNTIES.index(st.session_state.background_info['county']) + 1 if st.session_state.background_info['county'] in UK_COUNTIES else 0,
            help="This helps us find local resources in your area"
        )
        st.session_state.background_info['county'] = selected_county
    
    with col2:
        postcode_area = st.text_input(
            "Enter your postcode area (e.g., SW1, M1): *",
            value=st.session_state.background_info['postcode_area'],
            help="Just the first part of your postcode for finding nearby services",
            max_chars=4
        ).upper()
        st.session_state.background_info['postcode_area'] = postcode_area
    
    st.markdown("---")
    
    # Education level
    selected_education = st.selectbox(
        "What is your highest level of education? *",
        options=EDUCATION_LEVELS,
        index=EDUCATION_LEVELS.index(st.session_state.background_info['education']) if st.session_state.background_info['education'] in EDUCATION_LEVELS else 0
    )
    st.session_state.background_info['education'] = selected_education

    # Current situation
    st.session_state.background_info['current_situation'] = st.text_area(
        "Please describe your current work/education situation: *",
        value=st.session_state.background_info['current_situation'],
        help="For example: 'Currently working part-time and studying' or 'Looking for work opportunities'",
        height=100
    )

def show_interests_section():
    st.subheader("Interests & Career Goals")
    
    # Career interests
    interests = st.multiselect(
        "Select your areas of career interest (choose all that apply): *",
        options=INTEREST_AREAS,
        default=st.session_state.background_info['interests']
    )
    st.session_state.background_info['interests'] = interests

    # Career goals
    st.session_state.background_info['goals'] = st.text_area(
        "What are your main career goals? *",
        value=st.session_state.background_info['goals'],
        help="What kind of work would you like to do? What are you hoping to achieve?",
        height=100
    )

def show_barriers_section():
    st.subheader("Barriers & Support Systems")
    
    # Barriers
    barriers = st.multiselect(
        "Select any barriers you're currently facing (choose all that apply):",
        options=POTENTIAL_BARRIERS,
        default=st.session_state.background_info['barriers']
    )
    st.session_state.background_info['barriers'] = barriers

    # Support systems
    st.session_state.background_info['support_systems'] = st.text_area(
        "What support systems do you currently have? *",
        value=st.session_state.background_info['support_systems'],
        help="This could include family, friends, mentors, community organizations, etc.",
        height=100
    )

    # Additional information
    st.session_state.background_info['additional_info'] = st.text_area(
        "Is there anything else you'd like to share?",
        value=st.session_state.background_info['additional_info'],
        help="Any additional information that might be helpful for career guidance",
        height=100
    )

def all_required_fields_filled():
    """Check if all required fields are filled"""
    required_fields = [
        st.session_state.background_info['county'],
        st.session_state.background_info['postcode_area'],
        st.session_state.background_info['education'],
        st.session_state.background_info['current_situation'],
        st.session_state.background_info['interests'],
        st.session_state.background_info['goals'],
        st.session_state.background_info['support_systems']
    ]
    return all(field for field in required_fields)

def save_background_info():
    """Save background information to session state"""
    # Additional processing or validation could be added here
    pass