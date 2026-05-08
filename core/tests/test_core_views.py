from django.urls import reverse


def test_welcome_page_renders(client):
    """Landing page should render successfully."""
    response = client.get(reverse("core:welcome"))
    assert response.status_code == 200


def test_ptsd_info_page_renders(client):
    """PTSD info page should render successfully."""
    response = client.get(reverse("core:ptsdinfo"))
    assert response.status_code == 200


def test_books_page_renders(client):
    """Books page should render successfully."""
    response = client.get(reverse("core:books"))
    assert response.status_code == 200


def test_selfhelp_page_renders(client):
    """Self-help page should render successfully."""
    response = client.get(reverse("core:self-help"))
    assert response.status_code == 200
