from mcp.server.fastmcp import FastMCP
import os
import requests
import json

# Create an MCP server
mcp = FastMCP("Aviationstack MCP")

def fetch_flight_data() -> dict:
    """Fetch raw flight data from the AviationStack API."""
    api_key = os.getenv('AVIATION_STACK_API_KEY')
    if not api_key:
        raise ValueError("AVIATION_STACK_API_KEY not set in environment.")

    url = 'http://api.aviationstack.com/v1/flights'
    params = {'access_key': api_key}

    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()

@mcp.tool()
def get_flights_with_airline(airline: str) -> str:
    """MCP tool to get flights for a specific airline."""
    try:
        data = fetch_flight_data()
        flights = []
        for flight in data.get('data', []):
            if flight.get('airline', {}).get('name') == airline:
                flights.append({
                    'flight_number': flight['flight']['iata'],
                    'departure_airport': flight['departure']['airport'],
                    'departure_timezone': flight['departure']['timezone'],
                    'departure_time': flight['departure']['scheduled'],
                    'arrival_airport': flight['arrival']['airport'],
                    'arrival_timezone': flight['arrival']['timezone'],
                    'flight_status': flight['flight_status'],
                })
        return json.dumps(flights) if flights else f"No flights found for airline '{airline}'."
    except requests.RequestException as e:
        return f"Request error: {str(e)}"
    except Exception as e:
        return f"Error fetching flights: {str(e)}"

@mcp.tool()
def get_flights_departure_airport(airport: str) -> str:
    """MCP tool to get flights for a specific airport."""
    try:
        data = fetch_flight_data()
        flights = []
        for flight in data.get('data', []):
            if flight.get('departure', {}).get('airport') == airport:
                flights.append({
                    'flight_number': flight['flight']['iata'],
                    'departure_timezone': flight['departure']['timezone'],
                    'departure_time': flight['departure']['scheduled'],
                    'arrival_airport': flight['arrival']['airport'],
                    'arrival_timezone': flight['arrival']['timezone'],
                    'flight_status': flight['flight_status'],
                })
        return json.dumps(flights) if flights else f"No flights found for airport '{airport}'."
    except requests.RequestException as e:
        return f"Request error: {str(e)}"
    except Exception as e:
        return f"Error fetching flights: {str(e)}"

def main():
    mcp.run()

if __name__ == "__main__":
    main()