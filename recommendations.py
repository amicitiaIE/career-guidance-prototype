import streamlit as st

def get_career_paths(interests, education_level):
    """Generate career path suggestions based on interests and education"""
    career_suggestions = {
        "Technology & Computers": [
            "IT Support Specialist",
            "Web Developer",
            "Data Entry Specialist",
            "Computer Network Technician"
        ],
        "Healthcare & Medical": [
            "Medical Assistant",
            "Patient Care Technician",
            "Healthcare Support Worker",
            "Pharmacy Technician"
        ],
        "Construction & Trades": [
            "Apprentice Electrician",
            "Construction Worker",
            "HVAC Technician",
            "Carpenter's Assistant"
        ],
        "Business & Administration": [
            "Administrative Assistant",
            "Customer Service Representative",
            "Sales Associate",
            "Office Support Staff"
        ]
    }
    
    suggested_careers = []
    for interest in interests:
        if interest in career_suggestions:
            suggested_careers.extend(career_suggestions[interest])
    
    return suggested_careers[:5]  # Return top 5 suggestions

def get_skill_recommendations(caas_scores):
    """Generate skill development recommendations based on CAAS scores"""
    recommendations = {
        "Concern": {
            "low": [
                "Set short-term career goals (3-6 months)",
                "Create a weekly planning routine",
                "Research career paths in your interest areas",
                "Connect with a career counselor"
            ],
            "medium": [
                "Develop a 1-year career plan",
                "Start networking in your chosen field",
                "Identify potential mentors",
                "Join professional organizations"
            ],
            "high": [
                "Create 3-5 year career plans",
                "Mentor others in career planning",
                "Explore advancement opportunities",
                "Lead career development workshops"
            ]
        },
        "Control": {
            "low": [
                "Practice daily decision-making exercises",
                "Learn basic project management skills",
                "Set small, achievable weekly goals",
                "Take a personal development course"
            ],
            "medium": [
                "Take on leadership roles in small projects",
                "Improve time management skills",
                "Build problem-solving abilities",
                "Learn conflict resolution techniques"
            ],
            "high": [
                "Mentor others in decision-making",
                "Lead team projects",
                "Develop crisis management skills",
                "Train others in leadership skills"
            ]
        },
        "Curiosity": {
            "low": [
                "Try one new activity each week",
                "Read about different career paths",
                "Shadow someone in a job you're interested in",
                "Take personality and career assessments"
            ],
            "medium": [
                "Attend career fairs and workshops",
                "Interview professionals in different fields",
                "Take courses in new subject areas",
                "Join professional networking groups"
            ],
            "high": [
                "Organize career exploration events",
                "Start a career research project",
                "Cross-train in different roles",
                "Write career guidance content"
            ]
        },
        "Confidence": {
            "low": [
                "Complete online skill-building courses",
                "Practice public speaking",
                "Document your daily achievements",
                "Join a supportive study group"
            ],
            "medium": [
                "Take on challenging assignments",
                "Present at team meetings",
                "Mentor newcomers in your field",
                "Lead small group projects"
            ],
            "high": [
                "Teach others in your area of expertise",
                "Take on leadership positions",
                "Start your own initiatives",
                "Write expert guides or tutorials"
            ]
        }
    }
    
    skill_suggestions = []
    for dimension, score in caas_scores.items():
        if score < 3:
            level = "low"
        elif score < 4:
            level = "medium"
        else:
            level = "high"
            
        if dimension in recommendations:
            skill_suggestions.append({
                "dimension": dimension,
                "level": level,
                "score": score,
                "recommendations": recommendations[dimension][level]
            })
    
    return skill_suggestions

def get_resource_recommendations(location, barriers):
    """Generate local resource recommendations based on location and barriers"""
    general_resources = [
        {
            "name": "Local Workforce Development Center",
            "description": "Offers job training, resume writing, and career counseling services. Programs are often free or low-cost, and they can help connect you with local employers.",
            "contact": "Visit CareerOneStop.org to find your nearest American Job Center"
        },
        {
            "name": "Community College Career Services",
            "description": "Provides educational guidance, career development support, and often offers short-term certificate programs.",
            "contact": "Search for your nearest community college online",
            "links": ["Use the College Navigator tool at NCES.ed.gov"]
        },
        {
            "name": "Online Learning Resources",
            "description": "Free or low-cost online courses and certifications to build job-ready skills.",
            "links": [
                "Coursera.org - Offers financial aid",
                "edX.org - Free courses available",
                "FreeCodeCamp.org - Completely free",
                "DigitalLiteracy.gov - Basic computer skills"
            ]
        },
        {
            "name": "Employment Support Organizations",
            "description": "Organizations that provide job search assistance, interview preparation, and sometimes professional clothing for interviews.",
            "links": [
                "Goodwill Career Centers",
                "Salvation Army Employment Services",
                "United Way Employment Programs"
            ]
        }
    ]
    return general_resources

def show_career_paths():
    """Display career path recommendations"""
    st.subheader("Recommended Career Paths")
    
    careers = get_career_paths(
        st.session_state.background_info['interests'],
        st.session_state.background_info['education']
    )
    
    for career in careers:
        with st.expander(career):
            st.write(f"Based on your interests in {', '.join(st.session_state.background_info['interests'])}")
            st.write("Next steps to explore this career:")
            st.write("1. Research typical job responsibilities")
            st.write("2. Look for entry-level positions or apprenticeships")
            st.write("3. Identify required certifications or training")
            st.write("4. Connect with professionals in this field")

def show_skill_development():
    """Display skill development recommendations"""
    st.subheader("Skill Development Recommendations")
    
    # Calculate CAAS dimension scores
    caas_scores = {}
    
    # Get CAAS questions structure
    from caas_assessment import CAAS_QUESTIONS
    
    # Calculate scores for each dimension
    for dimension in ["Concern", "Control", "Curiosity", "Confidence"]:
        dimension_questions = CAAS_QUESTIONS.get(dimension, [])
        matching_responses = [
            st.session_state.responses[question]
            for question in dimension_questions
            if question in st.session_state.responses
        ]
        
        if matching_responses:
            score = sum(matching_responses) / len(matching_responses)
            caas_scores[dimension] = score
    
    if not caas_scores:
        st.warning("No scores could be calculated. Please ensure you've completed the full assessment.")
        return
    
    # Display dimension scores
    st.write("### Your CAAS Dimension Scores")
    cols = st.columns(4)
    for i, (dimension, score) in enumerate(caas_scores.items()):
        with cols[i]:
            st.metric(
                dimension,
                f"{score:.1f}/5.0",
                help=f"Score for {dimension} dimension"
            )
    
    st.write("---")
    
    # Get and display recommendations
    skill_recommendations = get_skill_recommendations(caas_scores)
    
    for skill_set in skill_recommendations:
        with st.expander(f"{skill_set['dimension']} Development Plan"):
            st.write(f"**Current Level:** {skill_set['level'].title()} ({skill_set['score']:.1f}/5.0)")
            st.write("**Recommended Activities:**")
            for rec in skill_set['recommendations']:
                st.write(f"• {rec}")
            
            st.write("\n**Development Timeline:**")
            if skill_set['level'] == "low":
                st.write("Focus on these activities over the next 1-3 months to build a strong foundation.")
            elif skill_set['level'] == "medium":
                st.write("Work on these activities over the next 3-6 months to enhance your capabilities.")
            else:
                st.write("Incorporate these activities into your ongoing development to maintain and share your expertise.")

def show_resources():
    """Display resource recommendations"""
    st.subheader("Resources & Support")
    
    resources = get_resource_recommendations(
        "local",
        st.session_state.background_info['barriers']
    )
    
    for resource in resources:
        with st.expander(resource["name"]):
            st.write(resource["description"])
            if "contact" in resource:
                st.write(f"**How to Access:** {resource['contact']}")
            if "links" in resource:
                st.write("**Useful Links:**")
                for link in resource["links"]:
                    st.write(f"• {link}")
    
    if st.session_state.background_info['barriers']:
        st.subheader("Support for Specific Barriers")
        for barrier in st.session_state.background_info['barriers']:
            with st.expander(f"Resources for: {barrier}"):
                st.write("**Available Support:**")
                st.write("• Contact local support services")
                st.write("• Explore available assistance programs")
                st.write("• Connect with community organizations")
                
                if barrier == "Transportation issues":
                    st.write("• Research public transportation options")
                    st.write("• Look into carpool programs")
                elif barrier == "Childcare needs":
                    st.write("• Explore subsidized childcare programs")
                    st.write("• Research flexible work arrangements")
                elif barrier == "Housing instability":
                    st.write("• Contact local housing assistance programs")
                    st.write("• Connect with housing support services")

def show_recommendations_page():
    """Main recommendations page showing all sections"""
    st.title("Your Personalized Career Guidance")
    
    # Ensure we have both CAAS results and background info
    if 'responses' not in st.session_state or 'background_info' not in st.session_state:
        st.error("Please complete the assessment and background information first.")
        if st.button("← Return to Assessment"):
            st.session_state.page = 'assessment'
            st.rerun()
        return
    
    # Create tabs for different types of recommendations
    tabs = st.tabs(["Career Paths", "Skill Development", "Resources & Support"])
    
    with tabs[0]:
        show_career_paths()
    
    with tabs[1]:
        show_skill_development()
    
    with tabs[2]:
        show_resources()