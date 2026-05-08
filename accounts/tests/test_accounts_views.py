import pytest
from django.urls import reverse

from tools.models import JournalEntry, TriggerLog
from assessments.models import Assessment, TestResult


@pytest.mark.django_db
def test_register_creates_user_and_redirects(client):
    """Registration should create user and redirect to profile."""
    response = client.post(
        reverse("accounts:register"),
        data={
            "first_name": "Іван",
            "last_name": "Петренко",
            "email": "ivan@example.com",
            "password1": "StrongPass123!",
            "password2": "StrongPass123!",
        },
    )

    assert response.status_code == 302
    assert response.url == reverse("accounts:profile")


@pytest.mark.django_db
def test_profile_requires_authentication(client):
    """Anonymous user should be redirected to login."""
    response = client.get(reverse("accounts:profile"))
    assert response.status_code == 302
    assert reverse("accounts:login") in response.url


@pytest.mark.django_db
def test_profile_journal_sorting(client, user):
    """Journal tab should support oldest/newest sorting."""
    client.force_login(user)
    first = JournalEntry.objects.create(user=user, text="first")
    second = JournalEntry.objects.create(user=user, text="second")

    newest_response = client.get(reverse("accounts:profile_journal"))
    oldest_response = client.get(reverse("accounts:profile_journal"), data={"sort": "oldest"})

    newest_entries = list(newest_response.context["entries"])
    oldest_entries = list(oldest_response.context["entries"])
    assert newest_entries[0].id == second.id
    assert oldest_entries[0].id == first.id


@pytest.mark.django_db
def test_profile_triggers_sorting_by_distress(client, user):
    """Trigger tab should sort by distress with highest option."""
    client.force_login(user)
    low = TriggerLog.objects.create(user=user, distress_level=2)
    high = TriggerLog.objects.create(user=user, distress_level=9)

    response = client.get(reverse("accounts:profile_triggers"), data={"sort": "highest"})
    logs = list(response.context["trigger_logs"])
    assert logs[0].id == high.id
    assert logs[-1].id == low.id


@pytest.mark.django_db
def test_profile_tests_sorting_by_score(client, user):
    """Tests tab should sort test results by total score."""
    client.force_login(user)
    assessment = Assessment.objects.create(title="Demo", short_name="demo")
    low = TestResult.objects.create(user=user, assessment=assessment, total_score=5)
    high = TestResult.objects.create(user=user, assessment=assessment, total_score=20)

    response = client.get(reverse("accounts:profile_tests"), data={"sort": "highest"})
    results = list(response.context["test_results"])
    assert results[0].id == high.id
    assert results[-1].id == low.id
