import pytest

from accounts.forms import CustomUserCreationForm, CustomUserLoginForm


@pytest.mark.django_db
def test_creation_form_rejects_duplicate_email(user):
    """Registration form should not allow duplicate email."""
    form = CustomUserCreationForm(
        data={
            "first_name": "New",
            "last_name": "User",
            "email": user.email,
            "password1": "StrongPass123!",
            "password2": "StrongPass123!",
        }
    )

    assert not form.is_valid()
    assert "email" in form.errors


@pytest.mark.django_db
def test_login_form_accepts_email_credentials(client, user):
    """Login form should authenticate via email field."""
    form = CustomUserLoginForm(
        request=None,
        data={
            "username": user.email,
            "password": "StrongPass123!",
        },
    )

    assert form.is_valid()
