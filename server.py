from mcp.server.fastmcp import FastMCP
import os
import requests
import json
import random

# Create an MCP server
mcp = FastMCP("Aviationstack MCP")

def fetch_flight_data(url: str) -> dict:
    """Fetch raw flight data from the AviationStack API."""
    api_key = os.getenv('AVIATION_STACK_API_KEY')
    if not api_key:
        raise ValueError("AVIATION_STACK_API_KEY not set in environment.")
    params = {'access_key': api_key}

    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()

@mcp.tool()
def get_flights_with_airline(airline: str) -> str:
    """MCP tool to get flights with a specific airline."""
    try:
        data = fetch_flight_data('http://api.aviationstack.com/v1/flights')
        filtered_flights = []
        for flight_data in data.get('data', []):
            if flight_data.get('airline', {}).get('name') == airline:
                filtered_flights.append({
                    'flight_number': flight_data['flight']['iata'],
                    'airline': flight_data['airline']['name'],
                    'departure_airport': flight_data['departure']['airport'],
                    'departure_timezone': flight_data['departure']['timezone'],
                    'departure_time': flight_data['departure']['scheduled'],
                    'arrival_airport': flight_data['arrival']['airport'],
                    'arrival_timezone': flight_data['arrival']['timezone'],
                    'flight_status': flight_data['flight_status'],
                })
        return json.dumps(filtered_flights) if filtered_flights else f"No flights found for airline '{airline}'."
    except requests.RequestException as e:
        return f"Request error: {str(e)}"
    except Exception as e:
        return f"Error fetching flights: {str(e)}"

@mcp.tool()
def get_flights_departure_airport(airport: str) -> str:
    """MCP tool to get flights departing from a specific airport."""
    try:
        data = fetch_flight_data('http://api.aviationstack.com/v1/flights')
        filtered_flights = []
        for flight_data in data.get('data', []):
            if flight_data.get('departure', {}).get('airport') == airport:
                filtered_flights.append({
                    'flight_number': flight_data['flight']['iata'],
                    'airline': flight_data['airline']['name'],
                    'departure_timezone': flight_data['departure']['timezone'],
                    'departure_time': flight_data['departure']['scheduled'],
                    'arrival_airport': flight_data['arrival']['airport'],
                    'arrival_timezone': flight_data['arrival']['timezone'],
                    'arrival_time': flight_data['arrival']['scheduled'],
                    'flight_status': flight_data['flight_status'],
                })
        return json.dumps(filtered_flights) if filtered_flights else f"No flights found for airport '{airport}'."
    except requests.RequestException as e:
        return f"Request error: {str(e)}"
    except Exception as e:
        return f"Error fetching flights: {str(e)}"
    

@mcp.tool()
def get_flights_arrival_airport(airport: str) -> str:
    """MCP tool to get flights arriving at a specific airport."""
    try:
        data = fetch_flight_data('http://api.aviationstack.com/v1/flights')
        filtered_flights = []
        for flight_data in data.get('data', []):
            if flight_data.get('arrival', {}).get('airport') == airport:
                filtered_flights.append({
                    'flight_number': flight_data['flight']['iata'],
                    'airline': flight_data['airline']['name'],
                    'arrival_timezone': flight_data['arrival']['timezone'],
                    'arrival_time': flight_data['arrival']['scheduled'],
                    'departure_airport': flight_data['departure']['airport'],
                    'departure_timezone': flight_data['departure']['timezone'],
                    'departure_time': flight_data['departure']['scheduled'],
                    'flight_status': flight_data['flight_status'],
                })
        return json.dumps(filtered_flights) if filtered_flights else f"No flights found for arrival airport '{airport}'."
    except requests.RequestException as e:
        return f"Request error: {str(e)}"
    except Exception as e:
        return f"Error fetching flights: {str(e)}"
    

@mcp.tool()
def get_random_aircraft_type(number_of_aircraft: int) -> str:
    """MCP tool to get random aircraft type."""
    try:
        data = fetch_flight_data('http://api.aviationstack.com/v1/aircraft_types')
        aircraft_types = []
        for _ in range(number_of_aircraft):
            random_index = random.randint(0, len(data.get('data')) - 1)
            random_aircraft_type = data.get('data')[random_index]
            aircraft_types.append({
                'aircraft_name': random_aircraft_type.get('aircraft_name'),
                'icao_code': random_aircraft_type.get('iata_code'),
            })
        return json.dumps(aircraft_types)
    except requests.RequestException as e:
        return f"Request error: {str(e)}"
    except Exception as e:
        return f"Error fetching aircraft type: {str(e)}"

def main():
    mcp.run()

if __name__ == "__main__":
    main()