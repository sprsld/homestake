from datetime import datetime

from fastapi.testclient import TestClient
from homestake.main import app

client = TestClient(app)

TEST_DATE = '2025-01-01T00:00:00'


def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.text == "Welcome to the HomeStake Equity and Contribution Tracker"


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.text == "OK"


def test_create_property_201():
    response = client.post("/properties", json={
        'name': 'Test Property',
        'address': '123 Test St.',
        'purchase_price': 100000.0,
        'purchase_date': TEST_DATE,
        'current_value': 200000.0
    })
    assert response.status_code == 201
    assert response.json() == {
        'id': 1,
        'name': 'Test Property',
        'address': '123 Test St.',
        'purchase_price': 100000.0,
        'purchase_date': TEST_DATE,
        'current_value': 200000.0
    }


def test_create_mortgage_201():
    response = client.post("/mortgages", json={
        'lender': 'TestLender',
        'loan_amount': 100000.0,
        'interest_rate': 3,
        'term': 30,
        'start_date': TEST_DATE,
        'property_name': 'Test Property'
    })
    assert response.status_code == 201
    assert response.json() == {
        'id': 1,
        'name': 'Mortgage',
        'lender': 'TestLender',
        'loan_amount': 100000.0,
        'interest_rate': 3,
        'term': 30,
        'start_date': TEST_DATE
    }


def test_create_user_201():
    response = client.post("/users", json={
        'user_name': 'Test User',
        'email': 'test@email.com',
        'stake': 50,
        'property_name': 'Test Property'
    })
    assert response.status_code == 201
    response_json = response.json()
    assert response_json['id'] == 1
    assert response_json['user_name'] == 'Test User'
    assert response_json['email'] == 'test@email.com'
    assert response_json['stake'] == 50


def test_create_transaction_201():
    response = client.post("/transactions", json={
        'amount': 1000.0,
        'date': TEST_DATE,
        'user_name': 'Test User',
        'account_name': 'Mortgage'
    })
    assert response.status_code == 201
    response_json = response.json()
    assert response_json['id'] == 1
    assert response_json['amount'] == 1000.0
    assert response_json['date'] == TEST_DATE
    assert response_json['user_id'] == 1
    assert response_json['account_id'] == 1


def test_get_mortgage_by_id_200():
    response = client.get("/mortgages/1")
    assert response.status_code == 200

    response_json = response.json()
    assert response_json['id'] == 1
    assert response_json['lender'] == 'TestLender'
    assert response_json['loan_amount'] == 100000.0
    assert response_json['interest_rate'] == 3
    assert response_json['term'] == 30
    assert response_json['start_date'] == TEST_DATE


def test_get_mortgage_by_id_404():
    response = client.get("/mortgages/2")
    assert response.status_code == 404


def test_get_mortgage_by_lender_200():
    response = client.get("/mortgages/lender/TestLender")
    assert response.status_code == 200

    response_json = response.json()
    assert response_json['id'] == 1
    assert response_json['lender'] == 'TestLender'
    assert response_json['loan_amount'] == 100000.0
    assert response_json['interest_rate'] == 3
    assert response_json['term'] == 30
    assert response_json['start_date'] == TEST_DATE


def test_get_mortgage_by_lender_404():
    response = client.get("/mortgages/lender/NotTestLender")
    assert response.status_code == 404


def test_get_mortgage_by_property_200():
    response = client.get("/mortgages/property/Test Property")
    assert response.status_code == 200

    response_json = response.json()
    assert response_json['id'] == 1
    assert response_json['lender'] == 'TestLender'
    assert response_json['loan_amount'] == 100000.0
    assert response_json['interest_rate'] == 3
    assert response_json['term'] == 30
    assert response_json['start_date'] == TEST_DATE


def test_get_mortgage_by_property_404():
    response = client.get("/mortgages/property/NotTestProperty")
    assert response.status_code == 404


def test_get_property_by_address_200():
    response = client.get("/properties/address/123 Test St.")
    assert response.status_code == 200

    response_json = response.json()
    assert response_json['id'] == 1
    assert response_json['name'] == 'Test Property'
    assert response_json['purchase_price'] == 100000.0
    assert response_json['current_value'] == 200000.0
    assert response_json['purchase_date'] == TEST_DATE


def test_get_property_by_address_404():
    response = client.get("/properties/address/NotTestAddress")
    assert response.status_code == 404


def test_get_property_by_id_200():
    response = client.get("/properties/1")
    assert response.status_code == 200

    response_json = response.json()
    assert response_json['id'] == 1
    assert response_json['name'] == 'Test Property'
    assert response_json['purchase_price'] == 100000.0
    assert response_json['current_value'] == 200000.0
    assert response_json['purchase_date'] == TEST_DATE


def test_get_property_by_id_404():
    response = client.get("/properties/2")
    assert response.status_code == 404


def test_get_property_by_name_200():
    response = client.get("/properties/name/Test Property")
    assert response.status_code == 200

    response_json = response.json()
    assert response_json['id'] == 1
    assert response_json['address'] == '123 Test St.'
    assert response_json['purchase_price'] == 100000.0
    assert response_json['current_value'] == 200000.0
    assert response_json['purchase_date'] == TEST_DATE


def test_get_property_by_name_404():
    response = client.get("/properties/name/NotTestProperty")
    assert response.status_code == 404


def test_get_user_by_id_200():
    response = client.get("/users/1")
    assert response.status_code == 200

    response_json = response.json()
    assert response_json['id'] == 1
    assert response_json['user_name'] == 'Test User'
    assert response_json['email'] == 'test@email.com'
    assert response_json['stake'] == 50


def test_get_user_by_id_404():
    response = client.get("/users/2")
    assert response.status_code == 404


def test_get_user_by_name_200():
    response = client.get("/users/name/Test User")
    assert response.status_code == 200

    response_json = response.json()
    assert response_json['id'] == 1
    assert response_json['email'] == 'test@email.com'
    assert response_json['stake'] == 50


def test_get_user_by_name_404():
    response = client.get("/users/name/NotTestUser")
    assert response.status_code == 404


def test_get_transaction_by_id_200():
    response = client.get("/transactions/1")
    assert response.status_code == 200

    response_json = response.json()
    assert response_json['id'] == 1
    assert response_json['amount'] == 1000.0
    assert response_json['date'] == TEST_DATE
    assert response_json['user_id'] == 1
    assert response_json['account_id'] == 1


def test_get_transaction_by_id_404():
    response = client.get("/transactions/2")
    assert response.status_code == 404


def test_list_transactions_by_user_200():
    response = client.get("/transactions/user/Test User")
    assert response.status_code == 200

    response_json = response.json()
    assert response_json[0]['id'] == 1
    assert response_json[0]['amount'] == 1000.0
    assert response_json[0]['date'] == TEST_DATE
    assert response_json[0]['user_id'] == 1
    assert response_json[0]['account_id'] == 1


def test_get_transactions_by_user_404():
    response = client.get("/transactions/user/NotTestUser")
    assert response.status_code == 404


def test_get_transactions_by_account_200():
    response = client.get("/transactions/account/Mortgage")
    assert response.status_code == 200

    response_json = response.json()
    assert response_json[0]['id'] == 1
    assert response_json[0]['amount'] == 1000.0
    assert response_json[0]['date'] == TEST_DATE
    assert response_json[0]['user_id'] == 1
    assert response_json[0]['account_id'] == 1


def test_get_transactions_by_account_404():
    response = client.get("/transactions/account/NotMortgage")
    assert response.status_code == 404


def test_update_property_206():
    response = client.patch("/properties/1", json={
        'name': 'Updated Property',
        'address': '123 Updated St.',
        'purchase_price': 200000.0,
        'purchase_date': TEST_DATE,
        'current_value': 300000.0
    })
    assert response.status_code == 206
    assert response.json() == {
        'id': 1,
        'name': 'Updated Property',
        'address': '123 Updated St.',
        'purchase_price': 200000.0,
        'purchase_date': TEST_DATE,
        'current_value': 300000.0
    }


def test_update_property_404():
    response = client.patch("/properties/2", json={
        'name': 'Updated Property',
        'address': '123 Updated St.',
        'purchase_price': 200000.0,
        'purchase_date': TEST_DATE,
        'current_value': 300000.0
    })
    assert response.status_code == 404


def test_update_mortgage_206():
    response = client.patch("/mortgages/1", json={
        'lender': 'UpdatedLender',
        'loan_amount': 200000.0,
        'interest_rate': 4,
        'start_date': TEST_DATE,
        'property_name': 'Updated Property'
    })
    assert response.status_code == 206
    assert response.json() == {
        'id': 1,
        'name': 'Mortgage',
        'lender': 'UpdatedLender',
        'loan_amount': 200000.0,
        'interest_rate': 4,
        'term': 30,
        'start_date': TEST_DATE
    }


def test_update_mortgage_404_bad_mortgage():
    response = client.patch("/mortgages/2", json={
        'lender': 'UpdatedLender',
        'loan_amount': 200000.0,
        'interest_rate': 4,
        'start_date': TEST_DATE,
        'property_name': 'Test Property'
    })
    assert response.status_code == 404


def test_update_mortgage_404_bad_property():
    response = client.patch("/mortgages/1", json={
        'lender': 'UpdatedLender',
        'loan_amount': 200000.0,
        'interest_rate': 4,
        'start_date': TEST_DATE,
        'property_name': 'BadProperty'
    })
    assert response.status_code == 404


def test_update_user_206():
    response = client.patch("/users/1", json={
        'user_name': 'Updated User',
        'email': 'test2@email.com',
        'stake': 75,
        'lender': 'UpdatedLender',
        'property_name': 'Updated Property'
    })

    assert response.status_code == 206
    response_json = response.json()
    response_json["id"] == 1
    assert response_json["user_name"] == "Updated User"
    assert response_json["email"] == "test2@email.com"
    assert response_json["stake"] == 75


def test_update_user_404_bad_user():
    response = client.patch("/users/2", json={
        'user_name': 'Updated User',
        'email': 'test2@email.com',
        'stake': 75,
        'lender': 'UpdatedLender',
        'property_name': 'Updated Property'
    })
    assert response.status_code == 404


def test_update_user_404_bad_property():
    response = client.patch("/users/1", json={
        'user_name': 'Updated User',
        'email': 'test2@email.com',
        'stake': 75,
        'lender': 'UpdatedLender',
        'property_name': 'Bad Property'
    })
    assert response.status_code == 404


def test_update_user_404_bad_lender():
    response = client.patch("/users/1", json={
        'user_name': 'Updated User',
        'email': 'test2@email.com',
        'stake': 75,
        'lender': 'Bad Lender',
        'property_name': 'Updated Property'
    })
    assert response.status_code == 404


def test_update_transaction_206():
    response = client.patch("/transactions/1", json={
        'amount': 2000.0,
        'date': TEST_DATE,
        'user_name': 'Updated User',
        'account_name': 'Mortgage'
    })
    assert response.status_code == 206
    response_json = response.json()
    assert response_json['id'] == 1
    assert response_json['amount'] == 2000.0
    assert response_json['date'] == TEST_DATE


def test_update_transaction_404_bad_transaction():
    response = client.patch("/transactions/2", json={
        'amount': 2000.0,
        'date': TEST_DATE,
        'user_name': 'Updated User',
        'account_name': 'Mortgage'
    })
    assert response.status_code == 404


def test_update_transaction_404_bad_user():
    response = client.patch("/transactions/1", json={
        'amount': 2000.0,
        'date': TEST_DATE,
        'user_name': 'Bad User',
        'account_name': 'Mortgage'
    })
    assert response.status_code == 404


def test_update_transaction_404_bad_account():
    response = client.patch("/transactions/1", json={
        'amount': 2000.0,
        'date': TEST_DATE,
        'user_name': 'Updated User',
        'account_name': 'Bad Account'
    })
    assert response.status_code == 404


def test_delete_transaction_204():
    response = client.delete("/transactions/1")
    assert response.status_code == 204


def test_delete_transaction_404():
    response = client.delete("/transactions/1")
    assert response.status_code == 404


def test_delete_user_204():
    response = client.delete("/users/1")
    assert response.status_code == 204


def test_delete_user_404():
    response = client.delete("/users/1")
    assert response.status_code == 404


def test_delete_mortgage_204():
    response = client.delete("/mortgages/1")
    assert response.status_code == 204


def test_delete_mortgage_404():
    response = client.delete("/mortgages/1")
    assert response.status_code == 404


def test_delete_propery_204():
    response = client.delete("/properties/1")
    assert response.status_code == 204


def test_delete_propery_404():
    response = client.delete("/properties/1")
    assert response.status_code == 404
