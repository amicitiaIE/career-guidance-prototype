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

    Focus on practical, achievable recommendations that consider their specific circumstances.
    
    Format your response with clear section headers using markdown formatting (e.g., ### Strengths and Development Areas).
    """

    try:
        anthropic = Anthropic(api_key=st.secrets["anthropic"]["api_key"])
        
        response = anthropic.messages.create(
            model="claude-3-sonnet-20240229",
            max_tokens=1500,
            temperature=0.7,
            system="You are a career guidance expert specializing in supporting people at risk of offending. Provide practical, empathetic guidance with clear section headers using markdown.",
            messages=[{
                "role": "user",
                "content": prompt
            }]
        )
        
        # Extract the content from the response
        if hasattr(response, 'content') and len(response.content) > 0:
            return response.content[0].text
        else:
            return "Error: Unable to generate analysis"
    
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

def generate_fallback_analysis(caas_scores, background_info):
    """Generate basic analysis if AI service is unavailable"""
    return """### Analysis Currently Unavailable

We apologize, but we're unable to generate a personalized analysis at the moment. 
Please refer to the Career Paths, Skill Development, and Resources tabs for guidance.
"""

def display_ai_analysis(analysis):
    """Display the AI analysis in the Streamlit UI"""
    if isinstance(analysis, str) and len(analysis.strip()) > 0:
        # Convert the string response into formatted markdown
        st.markdown(analysis)
    else:
        st.error("Unable to generate career analysis. Please try again later.")