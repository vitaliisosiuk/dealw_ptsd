import pytest
from django.urls import reverse

from assessments.models import Assessment, Choice, Question, ResultInterpretation, TestResult


@pytest.mark.django_db
def test_about_test_redirects_anonymous_user(client):
    """About page should redirect anonymous users to registration."""
    assessment = Assessment.objects.create(title="Demo", short_name="demo")
    response = client.get(reverse("assessments:about-test", kwargs={"test_slug": assessment.short_name}))
    assert response.status_code == 302
    assert response.url == reverse("accounts:register")


@pytest.mark.django_db
def test_take_test_creates_result_when_all_answers_present(client, user):
    """Submitting complete answers should create TestResult."""
    client.force_login(user)
    assessment = Assessment.objects.create(title="Demo", short_name="demo")
    q1 = Question.objects.create(assessment=assessment, text="Q1", order=1)
    q2 = Question.objects.create(assessment=assessment, text="Q2", order=2)
    Choice.objects.create(question=q1, value=1, text="A")
    Choice.objects.create(question=q2, value=2, text="B")

    response = client.post(
        reverse("assessments:take-test", kwargs={"test_slug": assessment.short_name}),
        data={f"question_{q1.id}": "1", f"question_{q2.id}": "2"},
    )

    assert response.status_code == 302
    assert response.url == reverse("assessments:test-result", kwargs={"test_slug": assessment.short_name})
    result = TestResult.objects.get(user=user, assessment=assessment)
    assert result.total_score == 3


@pytest.mark.django_db
def test_take_test_returns_error_when_answers_missing(client, user):
    """Missing answers should keep user on test page with message."""
    client.force_login(user)
    assessment = Assessment.objects.create(title="Demo", short_name="demo")
    q1 = Question.objects.create(assessment=assessment, text="Q1", order=1)
    q2 = Question.objects.create(assessment=assessment, text="Q2", order=2)
    Choice.objects.create(question=q1, value=1, text="A")
    Choice.objects.create(question=q2, value=2, text="B")

    response = client.post(
        reverse("assessments:take-test", kwargs={"test_slug": assessment.short_name}),
        data={f"question_{q1.id}": "1"},
    )

    assert response.status_code == 200
    assert response.context["error_message"] == "Ви пропустили деякі питання."
    assert not TestResult.objects.filter(user=user, assessment=assessment).exists()


@pytest.mark.django_db
def test_test_result_uses_total_score_interpretation(client, user):
    """Result page should use total-score interpretation for simple tests."""
    client.force_login(user)
    assessment = Assessment.objects.create(title="Demo", short_name="demo")
    question = Question.objects.create(assessment=assessment, text="Q1", order=1)
    Choice.objects.create(question=question, value=4, text="A")
    interpretation = ResultInterpretation.objects.create(
        assessment=assessment,
        min_score=0,
        max_score=10,
        result_title="Норма",
        result_text="Опис",
        recommendation="Рекомендація",
    )
    session = client.session
    session[f"test_score_{assessment.short_name}"] = 4
    session[f"test_scale_scores_{assessment.short_name}"] = {}
    session.save()

    response = client.get(reverse("assessments:test-result", kwargs={"test_slug": assessment.short_name}))
    assert response.status_code == 200
    assert response.context["interpretation"].id == interpretation.id


@pytest.mark.django_db
def test_test_result_detail_requires_owner(client, user):
    """Users should not access other users' saved result detail pages."""
    assessment = Assessment.objects.create(title="Demo", short_name="demo")
    result = TestResult.objects.create(user=user, assessment=assessment, total_score=5)

    response = client.get(reverse("assessments:test-result-detail", kwargs={"result_id": result.id}))
    assert response.status_code == 302
