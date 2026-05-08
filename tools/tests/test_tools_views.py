import pytest
from django.urls import reverse

from tools.models import GettingOutOfHouseCard, InspirationalQuote, JournalEntry


def test_tools_home_renders(client):
    """Tools home page should render."""
    response = client.get(reverse("tools:home"))
    assert response.status_code == 200


@pytest.mark.django_db
def test_seeded_getting_out_of_house_has_minimum_30_cards():
    """Default data set should contain at least 30 cards."""
    assert GettingOutOfHouseCard.objects.count() >= 30


@pytest.mark.django_db
def test_getting_out_of_house_filters_only_active_cards(client):
    """Only active cards should be included in context."""
    active = GettingOutOfHouseCard.objects.create(
        title="Активна",
        description="Опис",
        image_url="https://example.com/a.jpg",
        is_active=True,
        sort_order=2,
    )
    GettingOutOfHouseCard.objects.create(
        title="Неактивна",
        description="Опис",
        image_url="https://example.com/b.jpg",
        is_active=False,
        sort_order=1,
    )

    response = client.get(reverse("tools:getting_out_of_house"))
    cards = response.context["cards"]

    assert response.status_code == 200
    titles = {card["title"] for card in cards}
    assert active.title in titles
    assert "Неактивна" not in titles


@pytest.mark.django_db
def test_getting_out_of_house_orders_cards(client):
    """Cards should be ordered by sort order then id."""
    first = GettingOutOfHouseCard.objects.create(
        title="Перша",
        description="Опис",
        image_url="https://example.com/1.jpg",
        sort_order=9991,
        is_active=True,
    )
    second = GettingOutOfHouseCard.objects.create(
        title="Друга",
        description="Опис",
        image_url="https://example.com/2.jpg",
        sort_order=9993,
        is_active=True,
    )

    response = client.get(reverse("tools:getting_out_of_house"))
    cards = response.context["cards"]
    ordered_ids = [c["title"] for c in cards if c["title"] in {"Перша", "Друга"}]
    assert ordered_ids == [first.title, second.title]


@pytest.mark.django_db
def test_inspirational_cards_fallback_when_empty(client):
    """Fallback quote should be shown when DB has no active quotes."""
    InspirationalQuote.objects.all().delete()
    response = client.get(reverse("tools:inspirational_cards_view"))

    assert response.status_code == 200
    assert response.context["quotes"][0]["author"] == "Елен Келлер"


@pytest.mark.django_db
def test_journal_post_creates_entry_for_logged_user(client, user):
    """Posting journal text should create entry and redirect."""
    client.force_login(user)
    response = client.post(reverse("tools:journal"), data={"text": "Тестовий запис"})

    assert response.status_code == 302
    assert response.url == reverse("accounts:profile")
    assert JournalEntry.objects.filter(user=user, text="Тестовий запис").exists()
