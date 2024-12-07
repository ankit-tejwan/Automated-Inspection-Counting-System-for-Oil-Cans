import requests

url = 'http://127.0.0.1:5000/ServerCheck'

try:
    # Sending a GET request to the server
    response = requests.get(url)

    # Checking if the response status code is 200 (OK)
    if response.status_code == 200:
        print("Response from server:")
        try:
            # Attempting to parse the JSON response
            print(response.json())
        except ValueError:
            print("Response is not in JSON format.")
    else:
        print(f"Server error: Received status code {response.status_code}")
        print("Please check the server logs for errors.")
    
except requests.exceptions.RequestException as e:
    # Catching any network or connection errors
    print(f"Network error occurred: {e}")
    print("Please ensure the server is running and reachable.")
