import os
import requests
from dotenv import load_dotenv

load_dotenv()


def scrape_linkedin_profile(linkedin_profile_url: str, mock: bool = False):
    """scrape information form Linkedin profiles"""

    if mock:
        linkedin_profile_url = "https://gist.githubusercontent.com/nabeykoon/e707d9c98d079ef0277b1fbd0f600850/raw/eea2d63d49e75b223d8cf2ab884dacaac0fb2544/nadeera-abeykoon-proxycurl.json"
        response = requests.get(linkedin_profile_url, timeout=10)

    else:
        api_endpoint = "https://nubela.co/proxycurl/api/v2/linkedin"
        header_dic = {"Authorization": f"Bearer {os.getenv('PROXYCURL_API_KEY')}"}
        response = requests.get(
            api_endpoint,
            params={"url": linkedin_profile_url},
            headers=header_dic,
            timeout=10,
        )

    data = response.json()

    data = {
        k: v
        for k, v in data.items()
        if v not in ([], "", "", None) and k not in ["people_also_viewed", "certifications"]
    }

    if data.get("groups"):
        for group_dict in data["groups"]:
            group_dict.pop("profile_pic_url")

    return data


if __name__ == "__main__":
    print(
        scrape_linkedin_profile(
            linkedin_profile_url="https://www.linkedin.com/in/nadeera-abeykoon-40a991b8/", mock=True
        )
    )
