import asyncio
import time

import httpx
import requests

URL = "http://localhost:8000/delayed_ping"
URLS = [URL] * 5

def fetch_blocking() -> None:
    start = time.perf_counter()
    for url in URLS:
        response = requests.get(url)
        print(f"Response {response.json()} in {time.perf_counter() - start}")
    print(f"Total time: {time.perf_counter() - start}")

async def fetch_async() -> None:
    start = time.perf_counter()
    async with httpx.AsyncClient() as client:
        # tasks = [client.get(url) for url in URLS] <- List Comprehensions way
        
        tasks = []
        for url in URLS:
            
            tasks.append(client.get(url))

        responses = await asyncio.gather(*tasks)

        for response in responses:
            print(f"Response {response.json()} in {time.perf_counter() - start}")
    print(f"Total time: {time.perf_counter() - start}")

if __name__ == "__main__":
    print("Benchmarking blocking requests...")
    fetch_blocking()
    print("\nBenchmarking async requests...")
    asyncio.run(fetch_async())