import pytest

from db_migrator import run_migration
from fakes.ShopApiTestRepository import ShopAPITestPostgresRepository


@pytest.fixture(scope='class')
def test_repo():
    repo = ShopAPITestPostgresRepository()
    repo.create_test_db()
    try:
        run_migration(repo=repo)
        yield repo
    finally:
        repo.drop_test_db()


@pytest.fixture(scope='class')
def test_date():
    return '2024-09-01'
