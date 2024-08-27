import pytest
from app import create_app
from app.utils.db import db
from app.models.fund import Fund

@pytest.fixture
def app():
    app = create_app('testing')
    with app.app_context():
        yield app

@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def init_database(app):
    with app.app_context():
        db.create_all()
        
        sample_fund = Fund(name='Fund A', nav=100.0, fund_house='Fund House A', performance_percentage=0.1)
        
        db.session.add(sample_fund)
        db.session.commit()
        
        yield
        
        db.drop_all()

def test_get_funds(client, init_database):
    """It does fetch all funds"""

    response = client.get('/funds')
    assert response.status_code == 200
    assert len(response.json) == 1

def test_create_fund(client, init_database):
    """It does create a new fund"""

    response = client.post('/funds', json={
        "name": "Fund B",
        "nav": 200.0,
        "fund_house": "Fund House B",
        "performance_percentage": 0.2
    })
    
    assert response.status_code == 201
    assert response.json['name'] == 'Fund B'

def test_get_fund(client, init_database):
    """It does fetch a single fund"""

    uuid = Fund.query.first().uuid
    response = client.get('/funds/' + uuid)
    assert response.status_code == 200
    assert response.json['name'] == 'Fund A'

def test_get_fund_not_found(client, init_database):
    """It does return 404 if fund not found"""

    response = client.get('/funds/invalid-uuid')
    assert response.status_code == 404

def test_update_fund(client, init_database):
    """It does update a fund"""

    uuid = Fund.query.first().uuid
    response = client.put('/funds/' + uuid, json={
        "name": "Fund C",
        "nav": 300.0,
        "fund_house": "Fund House C",
        "performance_percentage": 0.3
    })
    
    assert response.status_code == 200
    assert response.json['name'] == 'Fund C'
    assert response.json['nav'] == 300.0
    assert response.json['fund_house'] == 'Fund House C'
    assert response.json['performance_percentage'] == 0.3

def test_delete_fund(client, init_database):
    """It does soft delete a fund"""

    uuid = Fund.query.first().uuid
    response = client.delete('/funds/' + uuid)
    assert response.status_code == 200
    assert Fund.query.filter_by(uuid=uuid, deleted_at=None).first() is None
