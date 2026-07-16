from src.client.jop_classifier import JobFilterPipeline2


def test_title_filter_allows_project_management_and_payments_roles():
    classifier = JobFilterPipeline2(openai_api_key="test")

    jobs = [{
        "title": "Project Manager - Payments",
        "company": "Fintech Co",
        "description": "Leading payments platform delivery and stakeholder management",
        "tags": ["payments", "project management", "stakeholder management"],
    }]

    result = classifier.title_filter(jobs)

    assert len(result) == 1
    assert result[0]["title"] == "Project Manager - Payments"


def test_experience_filter_accepts_senior_roles():
    classifier = JobFilterPipeline2(openai_api_key="test")

    jobs = [{
        "title": "Senior Program Manager, Payments",
        "company": "Payments Co",
        "experience": "10-15 Yrs",
        "tags": ["payments", "program management"],
    }]

    result = classifier.experience_filter(jobs)

    assert len(result) == 1
