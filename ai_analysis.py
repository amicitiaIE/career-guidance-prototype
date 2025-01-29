import streamlit as st
from anthropic import Anthropic

def generate_career_analysis(caas_scores, background_info):
    """Generate comprehensive career analysis using Claude"""
    
    # Construct the prompt
    prompt = f"""You are a career guidance expert specializing in supporting people at risk of offending. 
    Please analyze the following assessment results and background information to provide personalized career guidance.

    CAAS Assessment Scores:
    {format_caas_scores(caas_scores)}

    Background Information:
    - Location: {background_info['county']}, {background_info['postcode_area']}
    - Education: {background_info['education']}
    - Current Situation: {background_info['current_situation']}
    - Career Interests: {', '.join(background_info['interests'])}
    - Barriers: {', '.join(background_info['barriers'])}
    - Support Systems: {background_info['support_systems']}
    - Goals: {background_info['goals']}

    Please provide:
    1. A summary of key strengths and areas for development
    2. Specific career recommendations considering local opportunities
    3. Tailored strategies for overcoming identified barriers
    4. Immediate next steps they can take
    5. Long-term development suggestions

    Focus on practical, achievable recommendations that consider their specific circumstances."""

    try:
        # Use Streamlit secrets for API key
        anthropic = Anthropic(api_key=st.secrets["anthropic"]["api_key"])
        
        response = anthropic.messages.create(
            model="claude-3-sonnet-20240229",
            max_tokens=1500,
            temperature=0.7,
            system="You are a career guidance expert specializing in supporting people at risk of offending. Provide practical, empathetic guidance.",
            messages=[{
                "role": "user",
                "content": prompt
            }]
        )
        
        return parse_ai_response(response.content)
    
    except Exception as e:
        st.error(f"Error generating AI analysis: {str(e)}")
        return generate_fallback_analysis(caas_scores, background_info)

def format_caas_scores(scores):
    """Format CAAS scores for the prompt"""
    formatted_scores = []
    for dimension, score in scores.items():
        level = "high" if score >= 4 else "medium" if score >= 3 else "low"
        formatted_scores.append(f"{dimension}: {score}/5.0 ({level})")
    return "\n".join(formatted_scores)

def parse_ai_response(response):
    """Parse and structure the AI response"""
    return {
        'summary': extract_section(response, 'strengths and areas'),
        'career_recommendations': extract_section(response, 'career recommendations'),
        'barrier_strategies': extract_section(response, 'strategies'),
        'next_steps': extract_section(response, 'next steps'),
        'long_term': extract_section(response, 'long-term')
    }

def extract_section(response, section_key):
    """Extract specific sections from the AI response"""
    # Add logic to parse and extract sections from the response
    # This would depend on the structure of Claude's response
    return response

def generate_fallback_analysis(caas_scores, background_info):
    """Generate basic analysis if AI service is unavailable"""
    # Implement basic rule-based analysis as fallback
    return {
        'summary': "Basic analysis based on your assessment scores...",
        'career_recommendations': "Career suggestions based on your interests...",
        'barrier_strategies': "General strategies for overcoming barriers...",
        'next_steps': "Standard next steps...",
        'long_term': "General long-term suggestions..."
    }

def display_ai_analysis(analysis):
    """Display the AI analysis in the Streamlit UI"""
    st.subheader("AI-Powered Career Analysis")
    
    with st.expander("Key Strengths & Development Areas", expanded=True):
        st.write(analysis['summary'])
    
    with st.expander("Personalized Career Recommendations"):
        st.write(analysis['career_recommendations'])
    
    with st.expander("Strategies for Success"):
        st.write(analysis['barrier_strategies'])
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### Immediate Next Steps")
        st.write(analysis['next_steps'])
    
    with col2:
        st.markdown("### Long-term Development")
        st.write(analysis['long_term'])