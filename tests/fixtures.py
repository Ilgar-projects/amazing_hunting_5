import pytest


@pytest.fixture
def hr_token(client, django_user_model, db):
    username = "igor"
    password = "igor"

    django_user_model.objects.create_user(
        username=username, password=password, role="hr"
    )

    response = client.post(
        "/user/login/",
        {"username": username, "password": password},
        format='json'
    )

    return response.data["token"]
