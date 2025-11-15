"""
Real Estate Market Insights Agent using Azure AI Foundry

This agent provides market insights, property analysis, and real estate information.
"""

import asyncio
import os
from typing import Annotated, Literal
from datetime import datetime

from agent_framework.azure import AzureAIAgentClient
from azure.identity.aio import AzureCliCredential
from pydantic import Field
from dotenv import load_dotenv
from agent_framework.observability import setup_observability

# Load environment variables
load_dotenv()

# Setup observability/telemetry
setup_observability()


# Create the agent instance for DevUI discovery
# The variable MUST be named 'agent' to be discovered by DevUI
agent = AzureAIAgentClient(
    async_credential=AzureCliCredential()
).create_agent(
    name="RealEstateInsightsAgent",
    instructions="""You are an expert real estate market analyst with deep knowledge of property 
markets, pricing trends, and neighborhood analysis. You help users with:

- Searching for properties based on their criteria
- Analyzing market trends and providing insights
- Calculating mortgage payments and affordability
- Providing detailed neighborhood information
- Comparing properties to help make informed decisions

Always provide detailed, data-driven insights and practical recommendations. When users ask about 
specific locations or properties, use the available tools to gather accurate information. Be friendly, 
professional, and focus on helping users make informed real estate decisions.""",
    tools=[]  # Tools will be added after they are defined below
)


def search_properties(
    location: Annotated[str, Field(description="The city or neighborhood to search in")],
    property_type: Annotated[
        Literal["house", "apartment", "condo", "townhouse"],
        Field(description="Type of property to search for")
    ] = "house",
    min_price: Annotated[int, Field(description="Minimum price in USD")] = 0,
    max_price: Annotated[int, Field(description="Maximum price in USD")] = 1000000,
    bedrooms: Annotated[int, Field(description="Minimum number of bedrooms")] = 1,
) -> str:
    """Search for properties based on location, type, price range, and bedrooms."""
    # Simulated property search results
    properties = [
        {
            "address": f"123 Main St, {location}",
            "type": property_type,
            "price": min_price + 50000,
            "bedrooms": bedrooms,
            "bathrooms": 2,
            "sqft": 1800,
            "year_built": 2018,
        },
        {
            "address": f"456 Oak Ave, {location}",
            "type": property_type,
            "price": min_price + 75000,
            "bedrooms": bedrooms + 1,
            "bathrooms": 2.5,
            "sqft": 2200,
            "year_built": 2020,
        },
        {
            "address": f"789 Elm Dr, {location}",
            "type": property_type,
            "price": min_price + 100000,
            "bedrooms": bedrooms + 2,
            "bathrooms": 3,
            "sqft": 2800,
            "year_built": 2022,
        },
    ]
    
    # Filter by max price
    filtered = [p for p in properties if p["price"] <= max_price]
    
    if not filtered:
        return f"No {property_type}s found in {location} within price range ${min_price:,} - ${max_price:,}"
    
    result = f"Found {len(filtered)} {property_type}(s) in {location}:\n\n"
    for i, prop in enumerate(filtered, 1):
        result += f"{i}. {prop['address']}\n"
        result += f"   Price: ${prop['price']:,} | {prop['bedrooms']} bed, {prop['bathrooms']} bath\n"
        result += f"   Size: {prop['sqft']:,} sqft | Built: {prop['year_built']}\n\n"
    
    return result


def get_market_trends(
    location: Annotated[str, Field(description="The city or region to analyze")],
    timeframe: Annotated[
        Literal["1_month", "3_months", "6_months", "1_year"],
        Field(description="Time period for trend analysis")
    ] = "3_months",
) -> str:
    """Analyze real estate market trends for a specific location and timeframe."""
    # Simulated market data
    trends = {
        "1_month": {"price_change": "+2.3%", "sales_volume": "+5%", "days_on_market": 28},
        "3_months": {"price_change": "+5.8%", "sales_volume": "+12%", "days_on_market": 32},
        "6_months": {"price_change": "+8.2%", "sales_volume": "+18%", "days_on_market": 35},
        "1_year": {"price_change": "+12.5%", "sales_volume": "+25%", "days_on_market": 38},
    }
    
    data = trends[timeframe]
    timeframe_display = timeframe.replace("_", " ")
    
    return f"""Market Trends for {location} (Last {timeframe_display}):

📈 Average Price Change: {data['price_change']}
📊 Sales Volume Change: {data['sales_volume']}
⏱️  Average Days on Market: {data['days_on_market']} days

Market Analysis:
- The {location} market shows {"strong growth" if "+" in data['price_change'] else "decline"} over the past {timeframe_display}
- Inventory levels are {"decreasing" if data['days_on_market'] < 40 else "stable"}, indicating a {"seller's" if data['days_on_market'] < 40 else "balanced"} market
- Sales activity has {"increased" if "+" in data['sales_volume'] else "decreased"} significantly
"""


def calculate_mortgage(
    property_price: Annotated[int, Field(description="Property price in USD")],
    down_payment_percent: Annotated[float, Field(description="Down payment as percentage (e.g., 20 for 20%)")] = 20.0,
    interest_rate: Annotated[float, Field(description="Annual interest rate as percentage (e.g., 6.5 for 6.5%)")] = 6.5,
    loan_term_years: Annotated[int, Field(description="Loan term in years")] = 30,
) -> str:
    """Calculate monthly mortgage payment and total cost breakdown."""
    down_payment = property_price * (down_payment_percent / 100)
    loan_amount = property_price - down_payment
    monthly_rate = (interest_rate / 100) / 12
    num_payments = loan_term_years * 12
    
    # Monthly payment formula
    if monthly_rate > 0:
        monthly_payment = loan_amount * (
            monthly_rate * (1 + monthly_rate) ** num_payments
        ) / ((1 + monthly_rate) ** num_payments - 1)
    else:
        monthly_payment = loan_amount / num_payments
    
    total_paid = monthly_payment * num_payments
    total_interest = total_paid - loan_amount
    
    return f"""Mortgage Calculator Results:

Property Price: ${property_price:,.2f}
Down Payment ({down_payment_percent}%): ${down_payment:,.2f}
Loan Amount: ${loan_amount:,.2f}

Monthly Payment: ${monthly_payment:,.2f}
Loan Term: {loan_term_years} years
Interest Rate: {interest_rate}%

Total Amount Paid: ${total_paid:,.2f}
Total Interest: ${total_interest:,.2f}

Additional Monthly Costs (Estimated):
- Property Tax: ~${property_price * 0.012 / 12:,.2f}
- Home Insurance: ~${property_price * 0.005 / 12:,.2f}
- HOA Fees: Varies by property

Estimated Total Monthly Cost: ${monthly_payment + (property_price * 0.012 / 12) + (property_price * 0.005 / 12):,.2f}
"""


def get_neighborhood_info(
    neighborhood: Annotated[str, Field(description="The neighborhood name and city")],
) -> str:
    """Get detailed information about a neighborhood including schools, amenities, and demographics."""
    # Simulated neighborhood data
    return f"""Neighborhood Profile: {neighborhood}

📚 Schools:
- Elementary: Lincoln Elementary (Rating: 8/10)
- Middle School: Jefferson Middle (Rating: 7/10)
- High School: Washington High (Rating: 9/10)

🏪 Amenities & Services:
- Shopping: 3 grocery stores, 1 shopping center within 2 miles
- Dining: 25+ restaurants, cafes, and bars
- Healthcare: 2 hospitals, 5 medical clinics nearby
- Parks: 4 parks, 2 recreation centers

🚗 Transportation:
- Walkability Score: 75/100
- Transit Score: 68/100
- Bike Score: 72/100
- Average Commute: 28 minutes

👥 Demographics:
- Median Age: 38 years
- Median Household Income: $85,000
- Owner-Occupied: 65%
- Crime Rate: Below average (Safe neighborhood)

📊 Market Stats:
- Median Home Price: $425,000
- Price per sqft: $245
- Market Trend: Appreciating (+6.2% YoY)
"""


def compare_properties(
    property_addresses: Annotated[
        str,
        Field(description="Comma-separated list of property addresses to compare")
    ],
) -> str:
    """Compare multiple properties side by side with key metrics and analysis."""
    addresses = [addr.strip() for addr in property_addresses.split(",")]
    
    if len(addresses) < 2:
        return "Please provide at least 2 property addresses to compare, separated by commas."
    
    result = f"Property Comparison Analysis\n{'=' * 60}\n\n"
    
    # Simulated comparison data
    for i, addr in enumerate(addresses[:3], 1):  # Compare up to 3 properties
        result += f"Property {i}: {addr}\n"
        result += f"  Price: ${300000 + (i * 50000):,}\n"
        result += f"  Price/sqft: ${150 + (i * 10)}\n"
        result += f"  Size: {1800 + (i * 200):,} sqft\n"
        result += f"  Bedrooms: {3 + (i - 1)} | Bathrooms: {2 + (i - 1) * 0.5}\n"
        result += f"  Year Built: {2015 + i}\n"
        result += f"  Days on Market: {30 - (i * 5)}\n"
        result += f"  School Rating: {7 + i}/10\n\n"
    
    result += "\nRecommendation:\n"
    result += f"Based on the comparison, Property 1 ({addresses[0]}) offers the best value per square foot "
    result += "and is in a highly-rated school district. However, consider your specific needs regarding "
    result += "size, location, and budget."
    
    return result


# Configure the agent with tools (now that they're defined)
# This updates the agent created at module level
agent._tools = [
    search_properties,
    get_market_trends,
    calculate_mortgage,
    get_neighborhood_info,
    compare_properties,
]


async def main():
    """Main function to run the real estate market insights agent."""
    print("🏡 Real Estate Market Insights Agent")
    print("=" * 60)
    print()
    
    # Verify environment variables
    endpoint = os.getenv("AZURE_AI_PROJECT_ENDPOINT")
    model = os.getenv("AZURE_AI_MODEL_DEPLOYMENT_NAME")
    
    if not endpoint or not model:
        print("❌ Error: Missing required environment variables")
        print("Please set AZURE_AI_PROJECT_ENDPOINT and AZURE_AI_MODEL_DEPLOYMENT_NAME in your .env file")
        return
    
    print(f"📍 Endpoint: {endpoint}")
    print(f"🤖 Model: {model}")
    print()
    
    # Use the module-level agent (already configured with tools)
    async with agent:
        print("✅ Agent created successfully!")
        print()
        print("Available capabilities:")
        print("  • Property search")
        print("  • Market trend analysis")
        print("  • Mortgage calculations")
        print("  • Neighborhood insights")
        print("  • Property comparisons")
        print()
        print("-" * 60)
        print()
        
        # Example queries to demonstrate the agent's capabilities
        queries = [
            "What are the current market trends in Seattle for the last 6 months?",
            "Search for houses in Seattle with 3 bedrooms under $500,000",
            "Calculate the monthly mortgage for a $450,000 home with 20% down at 6.5% interest",
        ]
        
        for query in queries:
            print(f"💬 User: {query}")
            print()
            print("🤖 Agent: ", end="", flush=True)
            
            # Stream the response
            async for chunk in agent.run_stream(query):
                if chunk.text:
                    print(chunk.text, end="", flush=True)
            
            print()
            print()
            print("-" * 60)
            print()
        
        # Interactive mode
        print("\n🎯 Interactive Mode - Ask your real estate questions!")
        print("(Type 'exit' to quit)\n")
        
        while True:
            try:
                user_input = input("💬 You: ").strip()
                
                if not user_input:
                    continue
                
                if user_input.lower() in ["exit", "quit", "bye"]:
                    print("\n👋 Thank you for using Real Estate Market Insights Agent!")
                    break
                
                print("\n🤖 Agent: ", end="", flush=True)
                
                # Stream the response
                async for chunk in agent.run_stream(user_input):
                    if chunk.text:
                        print(chunk.text, end="", flush=True)
                
                print("\n")
                
            except KeyboardInterrupt:
                print("\n\n👋 Thank you for using Real Estate Market Insights Agent!")
                break
            except Exception as e:
                print(f"\n❌ Error: {e}\n")


if __name__ == "__main__":
    asyncio.run(main())
