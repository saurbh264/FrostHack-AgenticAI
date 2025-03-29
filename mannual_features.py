from langchain_core.prompts import PromptTemplate
import os
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from langchain_core.output_parsers import JsonOutputParser
from langchain.chains import LLMChain

# Load environment variables from .env file
load_dotenv()

# Retrieve Google API key from environment variables
google_api_key = os.getenv("GOOGLE_API_KEY")
if not google_api_key:
    raise ValueError("GOOGLE_API_KEY is not set in the environment variables")

# Initialize the model using Google Gemini API
model = ChatGoogleGenerativeAI(model='gemini-1.5-pro', api_key=google_api_key)

# Define a prompt template that accepts travel parameters
template = """
You are an expert AI travel planner. A traveler has provided the following details:
- Starting Location: {start_location}
- Destination: {destination}
- Budget: {budget}
- Duration (in days): {duration}
- Preferred Places to Visit (comma separated) or type 'default' for AI recommendations: {places}

Based on these details, generate a structured travel itinerary with the following output format in JSON:
```json
{{
  "itinerary": "Overall summary of the trip",
  "daily_plan": [
      {{"day": 1, "activities": "Detailed plan for day 1"}},
      {{"day": 2, "activities": "Detailed plan for day 2"}},
      ... 
  ],
  "recommendations": "Additional suggestions such as dining, local transport, and hidden gems"
}}
```

Please provide clear and actionable recommendations.
"""

prompt = PromptTemplate(
    template=template,
    input_variables=['start_location', 'destination', 'budget', 'duration', 'places']
)

# Define sample input values
inputs = {
    "start_location": "New York",
    "destination": "Paris",
    "budget": "$2000",
    "duration": "7",
    "places": "default"
}

# Create output parser
parser = JsonOutputParser()

# Using the modern LCEL pattern (LangChain Expression Language)
chain = prompt | model | parser

# Invoke the chain with inputs
result = chain.invoke(inputs)
print(result)