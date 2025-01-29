import streamlit as st

# CAAS Assessment Questions
CAAS_QUESTIONS = {
    "Concern": [
        "Thinking about what my future will be like",
        "Realizing that today's choices shape my future",
        "Preparing for the future",
        "Becoming aware of the educational and career choices I must make",
        "Planning how to achieve my goals",
        "Concerned about my career"
    ],
    "Control": [
        "Keeping upbeat",
        "Making decisions by myself",
        "Taking responsibility for my actions",
        "Sticking up for my beliefs",
        "Counting on myself",
        "Doing what's right for me"
    ],
    "Curiosity": [
        "Exploring my surroundings",
        "Looking for opportunities to grow as a person",
        "Investigating options before making a choice",
        "Observing different ways of doing things",
        "Probing deeply into questions I have",
        "Becoming curious about new opportunities"
    ],
    "Confidence": [
        "Performing tasks efficiently",
        "Taking care to do things well",
        "Learning new skills",
        "Working up to my ability",
        "Overcoming obstacles",
        "Solving problems"
    ]
}

def initialize_assessment_state():
    """Initialize session state variables for the assessment"""
    if 'responses' not in st.session_state:
        st.session_state.responses = {}
    if 'current_dimension' not in st.session_state:
        st.session_state.current_dimension = list(CAAS_QUESTIONS.keys())[0]
    if 'show_results' not in st.session_state:
        st.session_state.show_results = False

def calculate_dimension_score(dimension):
    """Calculate the score for a specific dimension"""
    questions = CAAS_QUESTIONS[dimension]
    total = 0
    count = 0
    for q in questions:
        if q in st.session_state.responses:
            total += st.session_state.responses[q]
            count += 1
    return round(total / count, 2) if count > 0 else 0

def show_assessment_page():
    initialize_assessment_state()
    
    st.title("Career Adapt-Abilities Scale (CAAS) Assessment")
    
    # Progress indication
    total_questions = sum(len(questions) for questions in CAAS_QUESTIONS.values())
    answered_questions = len(st.session_state.responses)
    progress = answered_questions / total_questions
    
    st.progress(progress)
    st.write(f"Progress: {answered_questions}/{total_questions} questions answered")

    if not st.session_state.show_results:
        # Show the assessment form
        dimension = st.session_state.current_dimension
        
        st.subheader(f"Section: {dimension}")
        st.write("Please rate how strongly you have developed each ability using the scale below:")
        st.write("1 = Not Strong, 2 = Somewhat Strong, 3 = Strong, 4 = Very Strong, 5 = Strongest")
        
        for question in CAAS_QUESTIONS[dimension]:
            col1, col2 = st.columns([3, 2])
            with col1:
                st.write(question)
            with col2:
                key = f"rating_{question}"
                response = st.select_slider(
                    "Rate your ability",
                    options=[1, 2, 3, 4, 5],
                    value=st.session_state.responses.get(question, 3),
                    key=key,
                    label_visibility="collapsed"
                )
                st.session_state.responses[question] = response

        # Navigation buttons
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if list(CAAS_QUESTIONS.keys()).index(dimension) > 0:
                if st.button("← Previous Section"):
                    current_index = list(CAAS_QUESTIONS.keys()).index(dimension)
                    st.session_state.current_dimension = list(CAAS_QUESTIONS.keys())[current_index - 1]
                    st.rerun()
        
        with col3:
            if dimension != list(CAAS_QUESTIONS.keys())[-1]:
                if st.button("Next Section →"):
                    current_index = list(CAAS_QUESTIONS.keys()).index(dimension)
                    st.session_state.current_dimension = list(CAAS_QUESTIONS.keys())[current_index + 1]
                    st.rerun()
            else:
                if answered_questions == total_questions:
                    if st.button("View Results", type="primary"):
                        st.session_state.show_results = True
                        st.rerun()
                else:
                    st.warning("Please answer all questions before viewing results.")

    else:
        # Show results
        st.subheader("Your CAAS Assessment Results")
        
        # Calculate and display scores
        scores = {}
        for dimension in CAAS_QUESTIONS.keys():
            scores[dimension] = calculate_dimension_score(dimension)
            
        # Display scores with interpretations
        for dimension, score in scores.items():
            col1, col2 = st.columns([1, 3])
            with col1:
                st.metric(dimension, f"{score}/5.0")
            with col2:
                interpretation = get_score_interpretation(dimension, score)
                st.write(interpretation)
        
        # Overall summary
        st.subheader("Next Steps")
        st.write("""
        Based on your responses, we'll now gather some additional information about your:
        - Educational background
        - Career interests
        - Potential barriers
        - Support systems
        
        This will help us provide more personalized recommendations.
        """)
        
        if st.button("Continue to Background Information →", type="primary"):
            st.session_state.page = 'background'
            st.rerun()

def get_score_interpretation(dimension, score):
    """Provide interpretation of the score for each dimension"""
    if dimension == "Concern":
        if score >= 4:
            return "You show strong future orientation and career planning abilities."
        elif score >= 3:
            return "You have a moderate level of career concern. Consider developing more specific future plans."
        else:
            return "You might benefit from activities that help you think more about your career future."
    
    elif dimension == "Control":
        if score >= 4:
            return "You demonstrate excellent decision-making and responsibility-taking abilities."
        elif score >= 3:
            return "You have a good sense of control over your career decisions. Consider building more confidence in your choices."
        else:
            return "You might benefit from activities that help you take more control of your career decisions."
    
    elif dimension == "Curiosity":
        if score >= 4:
            return "You show strong exploratory tendencies and openness to new experiences."
        elif score >= 3:
            return "You have a good level of curiosity. Consider exploring even more career options."
        else:
            return "You might benefit from activities that encourage more career exploration."
    
    elif dimension == "Confidence":
        if score >= 4:
            return "You demonstrate high self-efficacy and problem-solving abilities."
        elif score >= 3:
            return "You have good confidence levels. Consider taking on more challenging tasks to build it further."
        else:
            return "You might benefit from activities that help build your career confidence."
    
    return "Score interpretation not available."