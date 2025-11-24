import pytest
from httpx import AsyncClient

from src.main import app


@pytest.fixture(scope="module")
async def async_client() -> AsyncClient:
    async with AsyncClient(app=app, base_url="http://testserver") as client:
        yield client
