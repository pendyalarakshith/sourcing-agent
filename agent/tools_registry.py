from tools.npi import search_npi

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "search_npi",
            "description": "Search the US NPI registry for healthcare providers.",
            "parameters": {
                "type": "object",
                "properties": {
                    "first_name": {"type": "string"},
                    "last_name": {"type": "string"},
                    "specialty": {"type": "string", "description": "Official NPPES taxonomy, e.g. 'Cardiovascular Disease'"},
                    "city": {"type": "string"},
                    "state": {"type": "string", "description": "Two-letter code, e.g. 'TX'"},
                    "limit": {"type": "integer", "default": 10},
                },
            },
        },
    }
]

TOOL_FUNCTIONS = {"search_npi": search_npi}