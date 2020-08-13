
import pytest
from django.core.exceptions import ImproperlyConfigured
from django.test import Client
from django.urls import reverse


def test_landing_page():
    client = Client()
    url = reverse("navigation:landing_page")
    response = client.get(url)
    assert response.status_code == 200


def test_welcome_page():
    client = Client()
    url = reverse("navigation:welcome")
    response = client.get(url)
    assert response.status_code == 200


def test_route_redirect():
    client = Client()
    url = reverse("navigation:dashboard")
    response = client.get(url)
    assert response.status_code == 302


def test_route_page():
    client = Client()
    url = reverse("navigation:route")
    response = client.get(url)
    assert response.status_code == 200


def test_display_route_page():
    client = Client()
    session = client.session
    session["stations"] = (0, 3)
    session.save()
    url = reverse("navigation:display_route")
    response = client.get(url)
    assert response.status_code == 200


def test_comparison_page():
    client = Client()
    session = client.session
    session["stations"] = (0, 3)
    session.save()
    url = reverse("navigation:comparison")
    response = client.get(url)
    assert response.status_code == 200


def test_tour_page():
    client = Client()
    session = client.session
    session["stations"] = (0, 3)
    session.save()
    url = reverse("navigation:tour")
    response = client.get(url)
    assert response.status_code == 200


def test_dashboard_page():
    client = Client()
    session = client.session
    session["stations"] = (0, 3)
    session.save()
    url = reverse("navigation:dashboard")
    response = client.get(url)
    assert response.status_code == 200


def test_environment_page():
    client = Client()
    session = client.session
    session["stations"] = (0, 3)
    session.save()
    url = reverse("navigation:environment")
    response = client.get(url)
    assert response.status_code == 200


def test_summary_page():
    client = Client()
    session = client.session
    session["stations"] = (0, 3)
    session.save()
    url = reverse("navigation:questions_as_text")
    response = client.get(url)
    assert response.status_code == 200


def test_legal_page():
    client = Client()
    session = client.session
    session["stations"] = (0, 3)
    session.save()
    url = reverse("navigation:legal")
    response = client.get(url)
    assert response.status_code == 200


# TEST QUESTIONS
def test_category_e_metrobus(client=None):
    client = Client() if client is None else client
    session = client.session
    session["stations"] = (0, 3)
    if "questions" not in session:
        session["questions"] = {}
    session.save()
    url = reverse("navigation:question", kwargs={"category": "e_metrobus"})
    response = client.post(url, {"question": "loading_time", "answer": "2"})
    assert response.status_code == 302
    assert response.url == reverse("navigation:answer")
    response = client.post(url, {"question": "loading", "answer": "2"})
    assert response.status_code == 302
    assert response.url == reverse("navigation:answer")
    response = client.post(url, {"question": "batteries", "answer": "2"})
    assert response.status_code == 302
    assert response.url == reverse("navigation:answer")
    response = client.post(url, {"question": "costs", "answer": "2"})
    assert response.status_code == 302
    assert response.url == reverse("navigation:answer")
    response = client.get(url)
    assert response.status_code == 302
    assert response.url == reverse(
        "navigation:category_finished", kwargs={"category": "e_metrobus"}
    )


def test_category_umwelt(client=None):
    client = Client() if client is None else client
    session = client.session
    session["stations"] = (0, 3)
    if "questions" not in session:
        session["questions"] = {}
    session.save()
    url = reverse("navigation:question", kwargs={"category": "umwelt"})
    response = client.post(url, {"question": "energy", "answer": "2"})
    assert response.status_code == 302
    assert response.url == reverse("navigation:answer")
    response = client.post(url, {"question": "weather", "answer": "2"})
    assert response.status_code == 302
    assert response.url == reverse("navigation:answer")
    response = client.post(url, {"question": "reach", "answer": "2"})
    assert response.status_code == 302
    assert response.url == reverse("navigation:answer")
    response = client.post(url, {"question": "windturbines", "answer": "2"})
    assert response.status_code == 302
    assert response.url == reverse("navigation:answer")
    response = client.get(url)
    assert response.status_code == 302
    assert response.url == reverse(
        "navigation:category_finished", kwargs={"category": "umwelt"}
    )


def test_category_politik(client=None):
    client = Client() if client is None else client
    session = client.session
    session["stations"] = (0, 3)
    if "questions" not in session:
        session["questions"] = {}
    session.save()
    url = reverse("navigation:question", kwargs={"category": "politik"})
    response = client.post(url, {"question": "ebus_time", "answer": "2"})
    assert response.status_code == 302
    assert response.url == reverse("navigation:answer")
    response = client.post(url, {"question": "full_electrification", "answer": "2"})
    assert response.status_code == 302
    assert response.url == reverse("navigation:answer")
    response = client.post(url, {"question": "schedule", "answer": "2"})
    assert response.status_code == 302
    assert response.url == reverse("navigation:answer")
    response = client.post(url, {"question": "neutral", "answer": "2"})
    assert response.status_code == 302
    assert response.url == reverse("navigation:answer")
    response = client.get(url)
    assert response.status_code == 302
    assert response.url == reverse(
        "navigation:category_finished", kwargs={"category": "politik"}
    )


def test_category_ich(client=None):
    client = Client() if client is None else client
    session = client.session
    session["stations"] = (0, 3)
    if "questions" not in session:
        session["questions"] = {}
    session.save()
    url = reverse("navigation:question", kwargs={"category": "ich"})
    response = client.post(url, {"question": "advantages", "answer": "2"})
    assert response.status_code == 302
    assert response.url == reverse("navigation:answer")
    response = client.post(url, {"question": "footprint", "answer": "2"})
    assert response.status_code == 302
    assert response.url == reverse("navigation:answer")
    response = client.post(url, {"question": "e_bus", "answer": "2"})
    assert response.status_code == 302
    assert response.url == reverse("navigation:answer")
    response = client.post(url, {"question": "lines", "answer": "2"})
    assert response.status_code == 302
    assert response.url == reverse("navigation:answer")
    response = client.get(url)
    assert response.status_code == 302
    assert response.url == reverse(
        "navigation:category_finished", kwargs={"category": "ich"}
    )


def test_quiz_finished():
    client = Client()
    url = reverse("navigation:finished_quiz")
    response = client.get(url)
    assert response.status_code == 404

    test_category_e_metrobus(client)
    test_category_umwelt(client)
    test_category_politik(client)
    test_category_ich(client)
    with pytest.raises(ImproperlyConfigured):
        client.get(url)


def test_comparison_charts():
    client = Client()
    session = client.session
    session["stations"] = (0, 3)
    session.save()
    url = "/get_comparison_chart/"
    for route in ("route", "fleet"):
        for emission in ("co2", "nitrogen", "fine_dust"):
            response = client.get(url, data={"route": route, "emission": emission})
            assert response.status_code == 200
