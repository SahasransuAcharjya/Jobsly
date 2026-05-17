from urllib.parse import quote

def build_naukri_url(role: str, location: str) -> str:
    # Naukri typically formats like: https://www.naukri.com/python-developer-jobs-in-bangalore
    role_formatted = role.lower().replace(" ", "-")
    location_formatted = location.lower().replace(" ", "-")
    return f"https://www.naukri.com/{role_formatted}-jobs-in-{location_formatted}"

def build_linkedin_url(role: str, location: str) -> str:
    return f"https://www.linkedin.com/jobs/search/?keywords={quote(role)}&location={quote(location)}"

def build_wellfound_url(role: str, location: str) -> str:
    role_formatted = role.lower().replace(" ", "-")
    location_formatted = location.lower().replace(" ", "-")
    return f"https://wellfound.com/role/l/{role_formatted}/{location_formatted}"

def parse_query(role: str, location: str, source: str) -> str:
    if source.lower() == "naukri":
        return build_naukri_url(role, location)
    elif source.lower() == "linkedin":
        return build_linkedin_url(role, location)
    elif source.lower() == "wellfound":
        return build_wellfound_url(role, location)
    # Add other sources here as needed
    raise ValueError(f"Unknown source: {source}")
