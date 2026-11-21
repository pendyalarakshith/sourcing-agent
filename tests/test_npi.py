from tools.npi import search_npi

def test_search_returns_clean_profiles():
    out = search_npi(specialty="Cardiovascular Disease", city="Austin", state="TX", limit=3)
    assert out["error"] is None
    assert len(out["results"]) > 0
    assert out["results"][0]["npi"].isdigit()