import requests
import json
import os

API_KEY = "YgcWbJQUCe4PC6zhd9z34ilc9VyB1pfGvk3dwETy"
URL = "https://api.data.gov/ed/collegescorecard/v1/schools"
PER_PAGE = 100

colleges = []
page = 0

while True:
    params = {
        "api_key": API_KEY,
        "school.state": "CA",
        "fields": "id,school.name,school.degrees_awarded.predominant,school.ownership,school.school_url",
        "per_page": PER_PAGE,
        "page": page
    }

    response = requests.get(URL, params=params)
    if response.status_code != 200:
        print("ERROR:", response.text)
        break

    data = response.json()
    results = data.get("results", [])

    if not results:
        break

    for school in results:
        name = school.get("school.name", "")
        degrees = school.get("school.degrees_awarded.predominant")
        ownership = school.get("school.ownership")
        url = school.get("school.school_url", "")

        # Filter for public 2-year colleges with "college" in name
        if degrees in [1, 2] and ownership == 1 and "college" in name.lower():
            colleges.append({
                "id": school["id"],
                "name": name,
                "url": url
            })

    page += 1

# Deduplicate and sort
colleges = sorted({c["id"]: c for c in colleges}.values(), key=lambda x: x["name"])

# Print all CCCs with URL
for i, c in enumerate(colleges, start=1):
    print(f"{i}. {c['name']} ({c['url']})")

print(f"\nTotal CCCs: {len(colleges)}")

# Save JSON – use absolute path to avoid confusion
output_file = os.path.expanduser("~/cruzHacks/cruzHacks/frontend/src/ca_community_colleges.json")
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(colleges, f, indent=2, ensure_ascii=False)

print(f"Saved to {output_file}")