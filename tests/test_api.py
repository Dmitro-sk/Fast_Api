import pytest


@pytest.mark.asyncio
async def test_auth_register_login_logout_and_protected_routes(client):
    register_response = await client.post(
        "/auth/register",
        json={"username": "authuser", "email": "auth@example.com", "password": "secret123"},
    )
    assert register_response.status_code == 201
    assert register_response.cookies.get("access_token") is not None
    assert register_response.json()["user"]["username"] == "authuser"

    me_response = await client.get("/users/me")
    assert me_response.status_code == 200
    assert me_response.json()["email"] == "auth@example.com"

    motorcycles_response = await client.get("/users/me/motorcycles")
    assert motorcycles_response.status_code == 200
    assert motorcycles_response.json() == []

    logout_response = await client.post("/auth/logout")
    assert logout_response.status_code == 200

    protected_response = await client.get("/users/me")
    assert protected_response.status_code == 401

    login_response = await client.post(
        "/auth/login",
        json={"username": "authuser", "password": "secret123"},
    )
    assert login_response.status_code == 200
    assert login_response.cookies.get("access_token") is not None


@pytest.mark.asyncio
async def test_auth_rejects_bad_login(client):
    response = await client.post(
        "/auth/login",
        json={"username": "missing", "password": "secret123"},
    )
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_users_api_crud(client):
    create_response = await client.post(
        "/users/",
        json={"username": "apiuser", "email": "api@example.com", "password": "secret123"},
    )
    assert create_response.status_code == 201
    user_id = create_response.json()["id"]
    assert "password" not in create_response.json()

    list_response = await client.get("/users/")
    assert list_response.status_code == 200
    assert [item["id"] for item in list_response.json()] == [user_id]

    read_response = await client.get(f"/users/{user_id}")
    assert read_response.status_code == 200

    update_response = await client.put(f"/users/{user_id}", json={"username": "apiuser2"})
    assert update_response.status_code == 200
    assert update_response.json()["username"] == "apiuser2"

    delete_response = await client.delete(f"/users/{user_id}")
    assert delete_response.status_code == 204

    missing_response = await client.get(f"/users/{user_id}")
    assert missing_response.status_code == 404


@pytest.mark.asyncio
async def test_teams_api_crud_and_duplicate_conflict(client):
    create_response = await client.post("/teams/", json={"name": "KTM", "country": "Austria"})
    assert create_response.status_code == 201
    team_id = create_response.json()["id"]

    duplicate_response = await client.post("/teams/", json={"name": "KTM", "country": "Austria"})
    assert duplicate_response.status_code == 409

    list_response = await client.get("/teams/")
    assert list_response.status_code == 200
    assert len(list_response.json()) == 1

    read_response = await client.get(f"/teams/{team_id}")
    assert read_response.status_code == 200

    update_response = await client.put(f"/teams/{team_id}", json={"country": "AT"})
    assert update_response.status_code == 200
    assert update_response.json()["country"] == "AT"

    delete_response = await client.delete(f"/teams/{team_id}")
    assert delete_response.status_code == 204


@pytest.mark.asyncio
async def test_categories_api_crud(client):
    create_response = await client.post("/categories/", json={"name": "Sport"})
    assert create_response.status_code == 201
    category_id = create_response.json()["id"]

    assert (await client.get("/categories/")).status_code == 200
    assert (await client.get(f"/categories/{category_id}")).status_code == 200

    update_response = await client.put(f"/categories/{category_id}", json={"name": "Touring"})
    assert update_response.status_code == 200
    assert update_response.json()["name"] == "Touring"

    delete_response = await client.delete(f"/categories/{category_id}")
    assert delete_response.status_code == 204


@pytest.mark.asyncio
async def test_profiles_api_crud(client):
    user_response = await client.post(
        "/users/",
        json={"username": "profileuser", "email": "profile-api@example.com", "password": "secret123"},
    )
    user_id = user_response.json()["id"]
    create_response = await client.post(
        "/profiles/",
        json={"bio": "Fast rider", "experience_years": 5, "user_id": user_id},
    )
    assert create_response.status_code == 201
    profile_id = create_response.json()["id"]

    assert (await client.get("/profiles/")).status_code == 200
    assert (await client.get(f"/profiles/{profile_id}")).status_code == 200

    update_response = await client.put(f"/profiles/{profile_id}", json={"experience_years": 6})
    assert update_response.status_code == 200
    assert update_response.json()["experience_years"] == 6

    delete_response = await client.delete(f"/profiles/{profile_id}")
    assert delete_response.status_code == 204


@pytest.mark.asyncio
async def test_motorcycles_api_crud(client):
    user_id = (
        await client.post(
            "/users/",
            json={"username": "bikeowner", "email": "bike@example.com", "password": "secret123"},
        )
    ).json()["id"]
    category_id = (await client.post("/categories/", json={"name": "Sport"})).json()["id"]
    team_id = (await client.post("/teams/", json={"name": "Yamaha", "country": "Japan"})).json()["id"]

    create_response = await client.post(
        "/motorcycles/",
        json={
            "model_name": "R7",
            "year": 2024,
            "owner_id": user_id,
            "category_id": category_id,
            "team_id": team_id,
        },
    )
    assert create_response.status_code == 201
    motorcycle_id = create_response.json()["id"]

    assert (await client.get("/motorcycles/")).status_code == 200
    assert (await client.get(f"/motorcycles/{motorcycle_id}")).status_code == 200

    update_response = await client.put(f"/motorcycles/{motorcycle_id}", json={"model_name": "R9"})
    assert update_response.status_code == 200
    assert update_response.json()["model_name"] == "R9"

    delete_response = await client.delete(f"/motorcycles/{motorcycle_id}")
    assert delete_response.status_code == 204
