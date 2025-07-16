import streamlit as st
import random

def get_task_recommendation(emotion):
    """
    Get task recommendations based on the detected emotion.
    
    Args:
        emotion (str): Detected emotion (Positive, Neutral, Negative)
        
    Returns:
        str: Recommended tasks
    """
    if emotion == "Positive":
        return """
        ### Creative & Strategic Tasks
        - 🧠 **Brainstorming**: Generate new ideas or solutions to challenges
        - 🎨 **Creative Work**: Design, writing, or artistic projects
        - 🗣️ **Leadership**: Lead team meetings or important presentations
        - 📝 **Strategic Planning**: Work on long-term goals and strategies
        - 🧩 **Complex Problems**: Tackle challenging issues requiring deep focus
        - 📢 **External Communication**: Client meetings or stakeholder engagement
        """
    elif emotion == "Neutral":
        return """
        ### Balanced & Productive Tasks
        - 📋 **Administrative Work**: Organize schedules, plan tasks
        - 📨 **Communications**: Respond to emails and messages
        - 📑 **Documentation**: Create or update reports and documentation
        - 👥 **Collaboration**: Join team projects and discussions
        - 📚 **Learning**: Develop new skills or study relevant materials
        - 📊 **Data Analysis**: Review metrics and extract insights
        """
    else:  # Negative
        return """
        ### Light & Structured Tasks
        - 🗄️ **Organizing**: Clean up your workspace or digital files
        - ✓ **Simple Tasks**: Complete routine activities with clear steps
        - 📝 **Review Work**: Edit or review existing documents
        - ⏱️ **Time-Boxed Activities**: Focus for 25 minutes on a single task
        - ☕ **Self-Care Break**: Consider a 10-minute walk or short break
        - 🤝 **Peer Connection**: Have a quick check-in with a trusted colleague
        """

def get_wellness_tip(emotion):
    """
    Get wellness tips based on the detected emotion.
    
    Args:
        emotion (str): Detected emotion (Positive, Neutral, Negative)
        
    Returns:
        str: Wellness tip
    """
    positive_tips = [
        "💫 Channel your positive energy into helping others who might need support",
        "📝 Document what's going well today to reference during challenging times",
        "🌟 Share your enthusiasm with team members who might need a boost",
        "🏆 Use this positive state to tackle something challenging you've been postponing",
        "🙏 Practice gratitude by noting three specific things you're thankful for"
    ]
    
    neutral_tips = [
        "🧘 Take a few minutes for mindful reflection on what would increase your satisfaction",
        "🔄 Try incorporating something new into your routine to create positive momentum",
        "🤝 Connect with colleagues for a brief social interaction to boost team morale",
        "✅ Set a small, achievable goal to accomplish by the end of the day",
        "⚖️ Appreciate the balance in your current state - it provides clarity and perspective"
    ]
    
    negative_tips = [
        "⏳ Remember that all emotions are temporary - this feeling will pass",
        "🧘 Try a 5-minute mindfulness or deep breathing exercise to reset",
        "💬 Consider talking to someone you trust about how you're feeling",
        "🚶 Physical movement can help shift your mood - try a short walk",
        "💙 Be kind to yourself - it's okay to not feel your best every day"
    ]
    
    if emotion == "Positive":
        return random.choice(positive_tips)
    elif emotion == "Neutral":
        return random.choice(neutral_tips)
    else:  # Negative
        return random.choice(negative_tips)

def display_alert_status(consecutive_negatives):
    """
    Display the alert status based on consecutive negative moods.
    
    Args:
        consecutive_negatives (int): Count of consecutive negative moods
    """
    if consecutive_negatives == 0:
        st.success("✅ No alerts active - Wellness status: Good")
    elif consecutive_negatives == 1:
        st.info("ℹ️ 1 negative mood recorded - Consider a short break")
    elif consecutive_negatives == 2:
        st.warning("⚠️ 2 consecutive negative moods - Suggested actions:\n- Take a longer break\n- Connect with a colleague\n- Consider wellness resources")
    else:
        st.error(f"🚨 Alert triggered: {consecutive_negatives} consecutive negative moods.\nWellbeing check recommended. HR has been notified.")
