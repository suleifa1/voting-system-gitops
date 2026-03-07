"""
Integration tests for survey endpoints
"""
import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_get_surveys_list(client: AsyncClient):
    """Test getting list of surveys"""
    response = await client.get("/api/surveys/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

@pytest.mark.asyncio
async def test_get_surveys_with_filter(client: AsyncClient):
    """Test getting surveys with status filter"""
    response = await client.get("/api/surveys/?status_filter=active")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    # All returned surveys should be active
    for survey in data:
        assert survey["status"] == "active"

@pytest.mark.asyncio
async def test_unauthorized_start_survey(client: AsyncClient):
    """Test starting survey without authentication"""
    fake_survey_id = "11111111-1111-1111-1111-111111111111"
    response = await client.post(f"/api/surveys/{fake_survey_id}/start")
    assert response.status_code in [401, 403]  # Unauthorized or Forbidden
