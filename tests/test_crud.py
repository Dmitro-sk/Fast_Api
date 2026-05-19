import pytest

from src.crud import categories, motorcycles, profiles, teams, users
from src.schemas.category import CategoryCreate, CategoryUpdate
from src.schemas.motorcycle import MotorcycleCreate, MotorcycleUpdate
from src.schemas.profile import ProfileCreate, ProfileUpdate
from src.schemas.team import TeamCreate, TeamUpdate
from src.schemas.user import UserCreate, UserUpdate
from src.security import verify_password


@pytest.mark.asyncio
async def test_user_crud_functions(db_session):
    user = await users.create_user(
        db_session,
        UserCreate(username="rider", email="rider@example.com", password="secret123"),
    )

    assert user.id is not None
    assert user.password != "secret123"
    assert verify_password("secret123", user.password)
    assert await users.get_user(db_session, user.id) == user
    assert await users.get_user_by_username_or_email(db_session, "rider") == user
    assert await users.get_user_by_username_or_email(db_session, "rider@example.com") == user
    assert [item.id for item in await users.get_users(db_session)] == [user.id]

    updated = await users.update_user(
        db_session,
        user,
        UserUpdate(username="updated-rider", password="newsecret"),
    )

    assert updated.username == "updated-rider"
    assert verify_password("newsecret", updated.password)

    await users.delete_user(db_session, updated)
    assert await users.get_user(db_session, updated.id) is None


@pytest.mark.asyncio
async def test_team_crud_functions(db_session):
    team = await teams.create_team(db_session, TeamCreate(name="KTM", country="Austria"))

    assert await teams.get_team(db_session, team.id) == team
    assert [item.id for item in await teams.get_teams(db_session)] == [team.id]

    updated = await teams.update_team(db_session, team, TeamUpdate(country="AT"))
    assert updated.country == "AT"

    await teams.delete_team(db_session, updated)
    assert await teams.get_team(db_session, updated.id) is None


@pytest.mark.asyncio
async def test_category_crud_functions(db_session):
    category = await categories.create_category(db_session, CategoryCreate(name="Sport"))

    assert await categories.get_category(db_session, category.id) == category
    assert [item.id for item in await categories.get_categories(db_session)] == [category.id]

    updated = await categories.update_category(db_session, category, CategoryUpdate(name="Touring"))
    assert updated.name == "Touring"

    await categories.delete_category(db_session, updated)
    assert await categories.get_category(db_session, updated.id) is None


@pytest.mark.asyncio
async def test_profile_crud_functions(db_session):
    user = await users.create_user(
        db_session,
        UserCreate(username="profile-user", email="profile@example.com", password="secret123"),
    )
    profile = await profiles.create_profile(
        db_session,
        ProfileCreate(bio="Track rider", experience_years=3, user_id=user.id),
    )

    assert await profiles.get_profile(db_session, profile.id) == profile
    assert [item.id for item in await profiles.get_profiles(db_session)] == [profile.id]

    updated = await profiles.update_profile(
        db_session,
        profile,
        ProfileUpdate(experience_years=4),
    )
    assert updated.experience_years == 4

    await profiles.delete_profile(db_session, updated)
    assert await profiles.get_profile(db_session, updated.id) is None


@pytest.mark.asyncio
async def test_motorcycle_crud_functions(db_session):
    user = await users.create_user(
        db_session,
        UserCreate(username="owner", email="owner@example.com", password="secret123"),
    )
    category = await categories.create_category(db_session, CategoryCreate(name="Sport"))
    team = await teams.create_team(db_session, TeamCreate(name="Honda", country="Japan"))
    motorcycle = await motorcycles.create_motorcycle(
        db_session,
        MotorcycleCreate(
            model_name="CBR600RR",
            year=2024,
            owner_id=user.id,
            category_id=category.id,
            team_id=team.id,
        ),
    )

    assert await motorcycles.get_motorcycle(db_session, motorcycle.id) == motorcycle
    assert [item.id for item in await motorcycles.get_motorcycles(db_session)] == [motorcycle.id]
    assert [item.id for item in await motorcycles.get_motorcycles_by_owner(db_session, user.id)] == [
        motorcycle.id,
    ]

    updated = await motorcycles.update_motorcycle(
        db_session,
        motorcycle,
        MotorcycleUpdate(model_name="CBR1000RR-R"),
    )
    assert updated.model_name == "CBR1000RR-R"

    await motorcycles.delete_motorcycle(db_session, updated)
    assert await motorcycles.get_motorcycle(db_session, updated.id) is None
