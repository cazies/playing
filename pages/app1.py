import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import random
import json
import openai

# Initialize OpenAI API
if 'openai_api_key' not in st.session_state:
    st.session_state.openai_api_key = ''

def initialize_openai():
    if st.session_state.openai_api_key:
        openai.api_key = st.session_state.openai_api_key
        return True
    return False

# Page Configuration
st.set_page_config(layout="wide", page_title="Content Creator Suite")

def generate_script(topic, style, duration, audience):
    prompt = f"""Create a video script for a {duration}-minute {style} video about {topic}. 
                Target audience: {audience}.
                Include sections for:
                - Hook
                - Introduction
                - Main Points (3-5 key points)
                - Call to Action
                - Outro
                Format each section clearly."""
    
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a professional content creator and scriptwriter."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=1000
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error generating script: {str(e)}"

def script_generator():
    st.header("AI Script Generator")

    col1, col2 = st.columns([2, 1])

    with col1:
        video_topic = st.text_input("Video Topic")
        video_style = st.selectbox(
            "Content Style",
            ["Tutorial", "Vlog", "Review", "Educational", "Entertainment"]
        )
        duration = st.slider("Target Duration (minutes)", 3, 30, 10)
        target_audience = st.selectbox(
            "Target Audience",
            ["Beginners", "Intermediate", "Advanced", "General"]
        )

        if st.button("Generate Script"):
            with st.spinner("Generating script..."):
                generated_script = generate_script(
                    video_topic,
                    video_style,
                    duration,
                    target_audience
                )
                st.text_area("Generated Script", generated_script, height=400)

    with col2:
        st.subheader("Script Tips")
        st.info("""
        - Keep hooks under 15 seconds
        - Include timestamps for editing
        - Add b-roll suggestions
        - Mark emphasis points
        """)

def content_repurposing():
    st.header("Content Repurposing Tool")
    
    uploaded_file = st.file_uploader("Upload Video Script or Transcript", type=['txt', 'docx'])
    
    if uploaded_file:
        content = uploaded_file.read().decode()
        platforms = st.multiselect(
            "Select Platforms",
            ["Instagram", "TikTok", "Twitter", "LinkedIn", "YouTube Shorts"]
        )
        
        if platforms and st.button("Generate Content"):
            try:
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You are a social media content adaptation expert."},
                        {"role": "user", "content": f"Repurpose this content for {', '.join(platforms)}:\n\n{content}"}
                    ],
                    temperature=0.7
                )
                st.text_area("Repurposed Content", response.choices[0].message.content, height=300)
            except Exception as e:
                st.error(f"Error generating content: {str(e)}")


def channel_analytics():
    st.header("Channel Analytics Dashboard")

    # Mock data
    dates = pd.date_range(start='2024-01-01', end='2024-12-31', freq='D')
    analytics_data = pd.DataFrame({
        'Date': dates,
        'Views': np.random.randint(1000, 5000, size=len(dates)),
        'Subscribers': np.cumsum(np.random.randint(10, 50, size=len(dates))),
        'Watch Time (hours)': np.random.randint(100, 500, size=len(dates)),
        'Revenue ($)': np.random.uniform(50, 200, size=len(dates))
    })

    # Overview metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Views", f"{analytics_data['Views'].sum():,}")
    with col2:
        st.metric("Total Subscribers", f"{analytics_data['Subscribers'].iloc[-1]:,}")
    with col3:
        st.metric("Watch Time", f"{analytics_data['Watch Time (hours)'].sum():,}h")
    with col4:
        st.metric("Revenue", f"${analytics_data['Revenue ($)'].sum():,.2f}")

    # Graphs
    fig = px.line(analytics_data, x='Date', y=['Views', 'Subscribers'])
    st.plotly_chart(fig, use_container_width=True)


def marketing_planner():
    st.header("Marketing Campaign Planner")

    col1, col2 = st.columns([2, 1])

    with col1:
        campaign_name = st.text_input("Campaign Name")
        start_date = st.date_input("Start Date")
        duration = st.number_input("Duration (days)", min_value=1, value=30)

        platforms = st.multiselect(
            "Marketing Channels",
            ["YouTube", "Instagram", "TikTok", "Twitter", "Facebook", "Email"]
        )

        if st.button("Generate Marketing Plan"):
            st.subheader("Marketing Timeline")

            timeline_data = []
            current_date = start_date

            for _ in range(duration):
                for platform in platforms:
                    if random.random() > 0.7:  # 30% chance of having a task
                        timeline_data.append({
                            'Date': current_date,
                            'Platform': platform,
                            'Task': f"Post content on {platform}",
                            'Type': random.choice(['Post', 'Story', 'Live', 'Community'])
                        })
                current_date += timedelta(days=1)

            timeline_df = pd.DataFrame(timeline_data)
            st.dataframe(timeline_df)

    with col2:
        st.subheader("Campaign Budget")
        st.slider("Daily Budget ($)", 0, 1000, 50)
        st.slider("Total Budget ($)", 0, 10000, 1000)


def idea_generator():
    st.header("Content Idea Generator")

    niche = st.text_input("Your Content Niche")
    content_type = st.multiselect(
        "Content Types",
        ["Tutorial", "Review", "Behind the Scenes", "Interview", "Challenge"]
    )

    if niche and content_type and st.button("Generate Ideas"):
        st.subheader("Content Ideas")

        # Mock idea generation
        for _ in range(10):
            idea_type = random.choice(content_type)
            st.write(f"- {idea_type}: {niche}-related content idea here")


def trend_analysis():
    st.header("Trend Analysis")

    col1, col2 = st.columns(2)

    with col1:
        keyword = st.text_input("Track Keyword")
        timeframe = st.selectbox("Timeframe", ["Last 7 days", "Last 30 days", "Last 90 days"])

        if keyword and st.button("Analyze Trends"):
            # Mock trend data
            trend_data = pd.DataFrame({
                'Date': pd.date_range(start='2024-01-01', periods=30),
                'Search Volume': np.random.randint(1000, 5000, 30),
                'Social Mentions': np.random.randint(500, 2000, 30)
            })

            fig = px.line(trend_data, x='Date', y=['Search Volume', 'Social Mentions'])
            st.plotly_chart(fig)

    with col2:
        st.subheader("Related Topics")
        st.write("1. Topic One")
        st.write("2. Topic Two")
        st.write("3. Topic Three")


def thumbnail_designer():
    st.header("Thumbnail Designer")

    col1, col2 = st.columns(2)

    with col1:
        title = st.text_input("Video Title")
        style = st.selectbox("Thumbnail Style", ["Minimal", "Bold", "Professional", "Dramatic"])
        color_scheme = st.color_picker("Primary Color", "#FF0000")

        if st.button("Generate Thumbnail"):
            st.image("https://via.placeholder.com/1280x720", caption="Generated Thumbnail")

    with col2:
        st.subheader("Thumbnail Tips")
        st.info("""
        - Use contrasting colors
        - Include clear text
        - Show emotion
        - Use rule of thirds
        """)


def engagement_analytics():
    st.header("Engagement Analytics")

    # Mock engagement data
    engagement_data = pd.DataFrame({
        'Metric': ['Comments', 'Likes', 'Shares', 'Saves'],
        'Count': [1200, 5000, 800, 300],
        'Growth': ['+15%', '+22%', '+10%', '+5%']
    })

    st.dataframe(engagement_data)

    # Engagement graph
    fig = go.Figure(data=[
        go.Bar(name='Count', x=engagement_data['Metric'], y=engagement_data['Count'])
    ])
    st.plotly_chart(fig)


def seo_optimizer():
    st.header("SEO Optimizer")

    video_title = st.text_input("Video Title")
    description = st.text_area("Video Description")

    if video_title and description and st.button("Optimize SEO"):
        st.subheader("SEO Recommendations")

        recommendations = {
            "Title Score": "8/10",
            "Description Score": "7/10",
            "Suggested Tags": ["tag1", "tag2", "tag3"],
            "Keyword Density": "2.3%"
        }

        for key, value in recommendations.items():
            st.write(f"**{key}:** {value}")



def sidebar_menu():
    st.sidebar.title("Creator Suite")
    return st.sidebar.radio(
        "Navigate",
        ["Script Generator", "Content Repurposing", "Channel Analytics",
         "Marketing Planner", "Idea Generator", "Trend Analysis",
         "Thumbnail Designer", "Engagement Analytics", "SEO Optimizer"]
    )
def settings():
    st.header("Settings")
    st.session_state.openai_api_key = st.text_input("Enter OpenAI API Key", 
                                                   value=st.session_state.openai_api_key, 
                                                   type="password")
    if st.session_state.openai_api_key:
        st.success("API key set successfully!")

def sidebar_menu():
    st.sidebar.title("Creator Suite")
    return st.sidebar.radio(
        "Navigate",
        ["Script Generator", "Content Repurposing", "Channel Analytics",
         "Marketing Planner", "Idea Generator", "Trend Analysis",
         "Thumbnail Designer", "Engagement Analytics", "SEO Optimizer", "Settings"]
    )

def main():
    page = sidebar_menu()
    
    if not initialize_openai() and page not in ["Settings"]:
        st.warning("Please set your OpenAI API key in Settings first!")
        settings()
        return
        
    if page == "Script Generator":
        script_generator()
    elif page == "Content Repurposing":
        content_repurposing()
    elif page == "Channel Analytics":
        channel_analytics()
    elif page == "Marketing Planner":
        marketing_planner()
    elif page == "Idea Generator":
        idea_generator()
    elif page == "Trend Analysis":
        trend_analysis()
    elif page == "Thumbnail Designer":
        thumbnail_designer()
    elif page == "Engagement Analytics":
        engagement_analytics()
    elif page == "SEO Optimizer":
        seo_optimizer()

if __name__ == "__main__":
    main()