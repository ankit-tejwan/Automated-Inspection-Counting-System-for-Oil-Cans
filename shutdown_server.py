import httpx
import asyncio

# Define the server URL with host and port
server_url = "http://127.0.0.1:5000"  # Change this to your server's URL if needed

# Create an asynchronous context for making the request
async def main():
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{server_url}/shutdown")
        if response.status_code == 200:
            print("Shutdown request sent successfully.")
            print(response.json())
        else:
            print("Failed to send shutdown request.")

# Run the main coroutine
if __name__ == "__main__":
    asyncio.run(main())