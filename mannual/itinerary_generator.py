import os
from langchain_core.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import JsonOutputParser

def generate_itinerary(selected_route, start_location, destination, budget, duration, places):
    """Generate a detailed itinerary based on the selected route"""
    
    # Initialize the model using Google Gemini API
    model = ChatGoogleGenerativeAI(model='gemini-1.5-pro', api_key=os.getenv("GOOGLE_API_KEY"))
    
    # Define the prompt template
    itinerary_template = """
    You are an expert AI travel planner. The traveler has selected the following route:
    {selected_route}

    Additional details:
    - Starting Location: {start_location}
    - Destination: {destination}
    - Budget: {budget}
    - Duration (in days): {duration}
    - Preferred Places to Visit: {places}

    Based on the selected transportation route and duration, create a day-by-day itinerary that includes:
    1. Where to stay each night (specific accommodation recommendations along the route)
    2. Activities and points of interest for each day ALONG THE ROUTE (not just at the destination)
    3. Dining recommendations for each day

    Generate the itinerary as JSON:
    ```json
    {{
      "overview": "Overall summary of the trip",
      "daily_plan": [
        {{
          "day": 1,
          "date": "Sample date",
          "location": "Current location for this day",
          "accommodation": "Where to stay tonight",
          "activities": [
            "Morning activity with specific details",
            "Afternoon activity with specific details",
            "Evening activity with specific details"
          ],
          "meals": [
            "Breakfast recommendation",
            "Lunch recommendation",
            "Dinner recommendation"
          ],
          "transportation_for_day": "Any transportation needed for this day"
        }},
        // Additional days follow the same structure
      ],
      "budget_breakdown": {{
        "accommodation": "$X",
        "food": "$X",
        "activities": "$X",
        "transportation": "$X",
        "total": "$X"
      }},
      "packing_suggestions": ["item1", "item2", "item3"]
    }}
    ```
    """

    itinerary_prompt = PromptTemplate(
        template=itinerary_template,
        input_variables=['selected_route', 'start_location', 'destination', 'budget', 'duration', 'places']
    )
    
    # Create output parser
    parser = JsonOutputParser()

    # Create chain
    chain = itinerary_prompt | model | parser

    # Invoke the chain with inputs
    itinerary = chain.invoke({
        "selected_route": selected_route["transportation_details"],
        "start_location": start_location,
        "destination": destination,
        "budget": budget,
        "duration": duration,
        "places": places
    })
    
    return itinerary