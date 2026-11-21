import requests

NPPES_URL = "https://npiregistry.cms.hhs.gov/api/"


def search_npi(first_name=None, last_name=None, specialty=None,
               city=None, state=None, postal_code=None,
               provider_type="individual", limit=20):
    params = {
        "version": "2.1",
        "first_name": first_name,
        "last_name": last_name,
        "taxonomy_description": specialty,
        "city": city,
        "state": state,
        "postal_code": postal_code,
        "enumeration_type": "NPI-1" if provider_type == "individual" else "NPI-2",
        "limit": min(limit, 200),
    }
    params = {k: v for k, v in params.items() if v}

    resp = requests.get(NPPES_URL, params=params, timeout=15)
    resp.raise_for_status()
    data = resp.json()

    if "Errors" in data:
        return {"error": [e.get("description") for e in data["Errors"]], "results": []}

    return {"error": None, "results": [_clean(r) for r in data.get("results", [])]}


def _clean(raw):
    basic = raw.get("basic", {})
    location = next((a for a in raw.get("addresses", [])
                     if a.get("address_purpose") == "LOCATION"), {})
    taxonomies = raw.get("taxonomies", [])
    primary = next((t for t in taxonomies if t.get("primary")), taxonomies[0] if taxonomies else {})

    return {
        "npi": raw.get("number"),
        "first_name": basic.get("first_name"),
        "last_name": basic.get("last_name"),
        "credential": basic.get("credential"),
        "status": basic.get("status"),
        "specialty": primary.get("desc"),
        "licenses": [{"state": t.get("state"), "number": t.get("license")}
                     for t in taxonomies if t.get("license")],
        "practice_address": {
            "line1": location.get("address_1"),
            "city": location.get("city"),
            "state": location.get("state"),
            "postal_code": location.get("postal_code"),
            "phone": location.get("telephone_number"),
        },
        "source": "nppes",
    }


if __name__ == "__main__":
    out = search_npi(specialty="Cardiovascular Disease", city="Austin", state="TX", limit=5)
    if out["error"]:
        print("Error:", out["error"])
    for p in out["results"]:
        print(p["npi"], p["first_name"], p["last_name"], p["credential"], "|", p["specialty"])