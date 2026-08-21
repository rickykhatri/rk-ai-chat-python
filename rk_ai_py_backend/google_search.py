import requests
from dotenv import load_dotenv
import os   
from bs4 import BeautifulSoup

load_dotenv(dotenv_path=".env")  # Specify the path to your .env file
google_search_url = os.getenv("google_search_url")  # Get the Google search URL from environment variables      

# Method to perform a Google search and return the HTML response
def google_search(query:str): 
    url = google_search_url + query
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(f"Google search request failed with status code {response.status_code}")

    result = html_to_text(response.text)
    print(f"Google search result for query '{query}': {result}")
    return result


# Method to convert HTML content to plain text
def html_to_text(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")

    # Remove things that aren't useful for the AI
    for tag in soup([
        "script",
        "style",
        "noscript",
        "svg"
    ]):
        tag.decompose()

    return soup.get_text(
        separator="\n",
        strip=True
    )