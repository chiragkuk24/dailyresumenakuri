from src.utils.resume_profile import build_job_search_queries, extract_experience_years, extract_resume_keywords


def test_extract_resume_keywords_from_resume_text():
    text = (
        "Chirag Sharma | Project Manager | Payments Domain Expert with 12 years in fintech, "
        "stakeholder management, delivery management, digital transformation, program management, merchant services."
    )

    keywords = extract_resume_keywords(text)

    assert "payments" in keywords
    assert "project management" in keywords
    assert "fintech" in keywords


def test_build_job_search_queries_uses_resume_keywords():
    queries = build_job_search_queries(["payments", "project management", "fintech"], location="Bangalore")

    assert any(q.startswith("Payments Project Manager") for q in queries)
    assert any(q.startswith("Payments Domain Expert") for q in queries)
    assert any(q.startswith("Fintech Project Manager") for q in queries)


def test_extract_experience_years_from_resume_text():
    text = "12+ years of experience in project management and payments"

    assert extract_experience_years(text) == 12
