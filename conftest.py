import pytest
from django.contrib.auth import get_user_model


@pytest.fixture
def user(db):
    """Create a default authenticated user for tests."""
    user_model = get_user_model()
    return user_model.objects.create_user(
        email="test@example.com",
        first_name="Test",
        last_name="User",
        password="StrongPass123!",
    )
