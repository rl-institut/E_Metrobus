
import pytest
from django.test import Client
from django.urls import reverse


def test_landing_page():
    client = Client()
    url = reverse('navigation:landing_page')
    response = client.get(url)
    assert response.status_code == 200


def test_welcome_page():
    client = Client()
    url = reverse('navigation:welcome')
    response = client.get(url)
    assert response.status_code == 200


def test_route_redirect():
    client = Client()
    url = reverse('navigation:dashboard')
    response = client.get(url)
    assert response.status_code == 302


def test_route_page():
    client = Client()
    url = reverse('navigation:route')
    response = client.get(url)
    assert response.status_code == 200


def test_display_route_page():
    client = Client()
    session = client.session
    session["stations"] = (0, 3)
    session.save()
    url = reverse('navigation:display_route')
    response = client.get(url)
    assert response.status_code == 200


def test_comparison_page():
    client = Client()
    session = client.session
    session["stations"] = (0, 3)
    session.save()
    url = reverse('navigation:comparison')
    response = client.get(url)
    assert response.status_code == 200


def test_tour_page():
    client = Client()
    session = client.session
    session["stations"] = (0, 3)
    session.save()
    url = reverse('navigation:tour')
    response = client.get(url)
    assert response.status_code == 200


def test_dashboard_page():
    client = Client()
    session = client.session
    session["stations"] = (0, 3)
    session.save()
    url = reverse('navigation:dashboard')
    response = client.get(url)
    assert response.status_code == 200


def test_environment_page():
    client = Client()
    session = client.session
    session["stations"] = (0, 3)
    session.save()
    url = reverse('navigation:environment')
    response = client.get(url)
    assert response.status_code == 200


def test_summary_page():
    client = Client()
    session = client.session
    session["stations"] = (0, 3)
    session.save()
    url = reverse('navigation:questions_as_text')
    response = client.get(url)
    assert response.status_code == 200


def test_legal_page():
    client = Client()
    session = client.session
    session["stations"] = (0, 3)
    session.save()
    url = reverse('navigation:legal')
    response = client.get(url)
    assert response.status_code == 200


# TEST QUESTIONS
def test_category_e_metrobus():
    client = Client()
    session = client.session
    session["stations"] = (0, 3)
    session["questions"] = []
    session.save()
    url = reverse('navigation:question', kwargs={"category": "e_metrobus"})
    response = client.post(url, {"question": "energy", "answer": "2"})
    assert response.status_code == 200
