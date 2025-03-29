import os
from langchain_core.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import JsonOutputParser

def generate_route_options(start_location, destination, budget, duration):
    """Generate different route options between start and destination"""
    
    # Initialize the model using Google Gemini API
    model = ChatGoogleGenerativeAI(model='gemini-1.5-pro', api_key=os.getenv("GOOGLE_API_KEY"))
    
    # Define the prompt template
    route_template = """
    You are an expert AI travel route planner. A traveler has provided the following details:
    - Starting Location: {start_location}
    - Destination: {destination}
    - Budget: {budget}
    - Duration (in days): {duration}

    Generate 3 different travel route options with detailed transportation instructions (including specific bus/train numbers, 
    walking directions, flight suggestions, car rental options, etc.) in JSON format:

    ```json
    {{
      "route_options": [
        {{
          "option_id": 1,
          "name": "Budget-friendly bus and train route",
          "transportation_details": "Detailed step-by-step instructions for this route option",
          "estimated_cost": "$X",
          "travel_time": "X hours/days",
          "pros": ["pro1", "pro2"],
          "cons": ["con1", "con2"]
        }},
        {{
          "option_id": 2,
          "name": "Quick flight and public transport route",
          "transportation_details": "Detailed step-by-step instructions for this route option",
          "estimated_cost": "$X",
          "travel_time": "X hours/days",
          "pros": ["pro1", "pro2"],
          "cons": ["con1", "con2"]
        }},
        {{
          "option_id": 3,
          "name": "Scenic drive route",
          "transportation_details": "Detailed step-by-step instructions for this route option",
          "estimated_cost": "$X",
          "travel_time": "X hours/days",
          "pros": ["pro1", "pro2"],
          "cons": ["con1", "con2"]
        }}
      ]
    }}
    ```
    """

    route_prompt = PromptTemplate(
        template=route_template,
        input_variables=['start_location', 'destination', 'budget', 'duration']
    )
    
    # Create output parser
    parser = JsonOutputParser()

    # Create chain
    chain = route_prompt | model | parser

    # Invoke the chain with inputs
    route_options = chain.invoke({
        "start_location": start_location,
        "destination": destination,
        "budget": budget,
        "duration": duration
    })
    
    return route_options