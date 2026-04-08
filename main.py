import requests
from time import sleep
from datetime import date
import os
import base64

from dotenv import load_dotenv

load_dotenv()

wakapi_url = os.environ['WAKAPI_URL']

github_api, wakapi_api = 'https://api.github.com/user', wakapi_url + '/api/summary'

wakapi_key = os.environ['WAKAPI_API_KEY']
github = os.environ['GITHUB_API_KEY']


def format_duration_compact(seconds: int) -> str:
    """Short duration for bio (GitHub bio max 160 chars)."""
    if seconds <= 0:
        return "0m"
    h, rem = divmod(seconds, 3600)
    m, s = divmod(rem, 60)
    if h:
        return f"{h}h {m}m" if m else f"{h}h" #hours and minutes
    if m:
        return f"{m}m {s}s" if s else f"{m}m" #minutes and seconds
    return f"{s}s" #seconds


def build_profile_bio(total_seconds: int) -> str:
    dur = format_duration_compact(total_seconds)
    year = date.today().strftime("%Y")
    return f"⚡{dur} coding in {year}"

while True:
    res = requests.get(wakapi_api,
    headers={
        "Authorization": f"Basic {base64.b64encode(wakapi_key.encode('ascii')).decode('ascii')}"
    },
    params={
        'interval': 'year'
    })

    if res.status_code == 200:

        res = res.json()

        time = sum(project['total'] for project in res['projects'])
        bio = build_profile_bio(time)

        post = requests.patch(github_api, headers={
            'Accept': "application/vnd.github.v3+json",
            'Authorization': f'token {github}'
        }, json={'bio': bio})

        if post.status_code == 200:
            print("<SUCCESS> Bio updated: " + bio)
        else:
            print("<FAIL> " + post.content)

    # Update bio every 15 minutes
    sleep(900)