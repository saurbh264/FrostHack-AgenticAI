import streamlit as st
import os
from dotenv import load_dotenv
import time
from route_planner import generate_route_options
from itinerary_generator import generate_itinerary
from utils import load_lottie, display_lottie

# Load environment variables
load_dotenv()

# Check for API key
if os.getenv("GOOGLE_API_KEY") is None:
    st.error("GOOGLE_API_KEY is not set in the .env file")
    st.stop()

# Page configuration
st.set_page_config(
    page_title="AI Travel Planner",
    page_icon="✈️",
    layout="wide"
)

# App title and description
st.title("✈️ Smart Travel Planner")
st.markdown("""
This AI-powered tool helps you plan your perfect trip by:
1. Generating multiple route options between your start and destination
2. Creating a detailed day-by-day itinerary based on your selected route
""")

# Sidebar for basic information
with st.sidebar:
    st.header("Trip Details")
    start_location = st.text_input("Starting Location", "New York")
    destination = st.text_input("Destination", "San Francisco")
    budget = st.text_input("Budget (USD)", "$2000")
    duration = st.text_input("Duration (days)", "7")
    places = st.text_input("Places to visit (comma-separated)", "Times Square, Central Park")

    # Show loading animation in sidebar
    lottie_travel = load_lottie("https://assets1.lottiefiles.com/packages/lf20_UgZWvP.json")
    st_lottie_container = st.empty()

# Main workflow
tab1, tab2 = st.tabs(["Route Planning", "Detailed Itinerary"])

with tab1:
    st.header("Step 1: Choose Your Route")
    st.markdown("First, let's explore different ways to reach your destination.")
    
    if st.button("Generate Route Options", key="generate_routes"):
        with st.spinner("Generating route options..."):
            with st_lottie_container:
                display_lottie(lottie_travel)
            
            # Call function to generate route options
            route_options = generate_route_options(
                start_location, 
                destination, 
                budget, 
                duration
            )
            
            # Store in session state for later use
            st.session_state.route_options = route_options
        
        # Display options
        st.success("Route options generated!")
        
    # Display route options if available
    if 'route_options' in st.session_state:
        route_options = st.session_state.route_options
        
        for option in route_options["route_options"]:
            with st.expander(f"Option {option['option_id']}: {option['name']}"):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown(f"**Cost:** {option['estimated_cost']}")
                    st.markdown(f"**Time:** {option['travel_time']}")
                    
                    st.markdown("**Pros:**")
                    for pro in option['pros']:
                        st.markdown(f"- {pro}")
                        
                with col2:
                    st.markdown("**Cons:**")
                    for con in option['cons']:
                        st.markdown(f"- {con}")
                
                st.markdown("**Transportation Details:**")
                st.info(option['transportation_details'])
                
                # Button to select this route
                if st.button(f"Select Option {option['option_id']}", key=f"select_{option['option_id']}"):
                    st.session_state.selected_route = option
                    st.success(f"Option {option['option_id']} selected! Go to the Detailed Itinerary tab.")

with tab2:
    st.header("Step 2: View Your Detailed Itinerary")
    
    # Check if a route has been selected
    if 'selected_route' not in st.session_state:
        st.info("Please select a route option in the Route Planning tab first.")
    else:
        if st.button("Generate Detailed Itinerary", key="generate_itinerary"):
            with st.spinner("Creating your personalized itinerary..."):
                with st_lottie_container:
                    display_lottie(lottie_travel)
                
                # Call function to generate itinerary
                itinerary = generate_itinerary(
                    st.session_state.selected_route,
                    start_location,
                    destination,
                    budget,
                    duration,
                    places
                )
                
                # Store in session state
                st.session_state.itinerary = itinerary
            
            st.success("Itinerary created!")
        
        # Display itinerary if available
        if 'itinerary' in st.session_state:
            itinerary = st.session_state.itinerary
            
            # Overview
            st.subheader("Trip Overview")
            st.write(itinerary["overview"])
            
            # Daily Plan
            st.subheader("Daily Plan")
            for day in itinerary["daily_plan"]:
                with st.expander(f"Day {day['day']} - {day['date']} - {day['location']}"):
                    st.markdown(f"**Accommodation:** {day['accommodation']}")
                    st.markdown(f"**Transportation:** {day['transportation_for_day']}")
                    
                    st.markdown("**Activities:**")
                    for activity in day['activities']:
                        st.markdown(f"- {activity}")
                    
                    st.markdown("**Meals:**")
                    for meal in day['meals']:
                        st.markdown(f"- {meal}")
            
            # Budget
            st.subheader("Budget Breakdown")
            budget_data = [[k.capitalize(), v] for k, v in itinerary["budget_breakdown"].items()]
            st.table(budget_data)
            
            # Packing
            st.subheader("Packing Suggestions")
            col1, col2, col3 = st.columns(3)
            cols = [col1, col2, col3]
            items_per_col = len(itinerary["packing_suggestions"]) // 3 + 1
            
            for i, item in enumerate(itinerary["packing_suggestions"]):
                col_idx = i // items_per_col
                cols[col_idx].markdown(f"- {item}")
            
            # Download as PDF option
            st.download_button(
                "Download Itinerary as PDF",
                "Itinerary PDF content would go here",  # In a real app, you'd generate a PDF
                file_name="travel_itinerary.pdf",
                mime="application/pdf",
            )

# Footer
st.markdown("---")
st.markdown("Developed with ❤️ using LangChain and Gemini 1.5 Pro")