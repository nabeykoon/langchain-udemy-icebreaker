import os
import requests
from dotenv import load_dotenv

load_dotenv()


def scrape_linkedin_profile(linkedin_profile_url: str, mock: bool = False):
    """scrape information form Linkedin profiles"""

    if mock:
        linkedin_profile_url = "https://gist.githubusercontent.com/nabeykoon/75947b0d40894a64420894eed0b897b2/raw/081d51ddd16b531aa02461f4a37fd5b053f48b12/nadeera-abeykoon-scrapin.json"
        response = requests.get(linkedin_profile_url, timeout=10)

    else:
        api_endpoint = "https://api.scrapin.io/enrichment/profile"
        params = {
            "linkedInUrl": linkedin_profile_url,
            "apikey": os.getenv("SCRAPIN_API_KEY"),
        }
        response = requests.get(
            api_endpoint,
            params=params,
            timeout=10,
        )

    data = response.json().get("person")

    data = {
        k: v
        for k, v in data.items()
        if v not in ([], "", "", None) and k not in ["certifications"]
    }

    return data


if __name__ == "__main__":
    print(
        scrape_linkedin_profile(
            linkedin_profile_url="https://www.linkedin.com/in/nadeera-abeykoon-40a991b8/", mock=True
        )
    )
