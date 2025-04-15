import pytest
from unittest.mock import AsyncMock, patch
from fastapi.testclient import TestClient

from src.domain.dtos.calculation_request import CalculationRequest
from src.domain.dtos.order_request import OrderRequest
from src.domain.dtos.product_creation_request import ProductUpsertRequest
from src.domain.dtos.product_request import ProductRequest
from src.main import app

client = TestClient(app)

@pytest.fixture
def test_client():
    return client

# Test for listing products with mock
@patch("src.application.dic.DIC.product_service", new_callable=AsyncMock)
def test_list_products(mock_product_service, test_client):
    # Mock the list method to return a predefined list of products
    mock_product_service.list.return_value = [
        {"id": 1, "name": "Product A", "price": 10.0, "vat": 2.0},
        {"id": 2, "name": "Product B", "price": 20.0, "vat": 4.0},
    ]

    # Perform the GET request
    response = test_client.get("/product/")

    # Ensure the mock method was called
    mock_product_service.list.assert_called_once()

    # Validate the response
    assert response.status_code == 200
    assert len(response.json()) == 2

# Test for creating a product with mock
@patch("src.application.dic.DIC.product_service", new_callable=AsyncMock)
def test_create_product(mock_product_service, test_client):
    # Mock the create method to return a predefined product
    mock_product_service.create.return_value = {"id": 1, "name": "Test Product", "price": 10.0, "vat": 2.0}
    request: ProductUpsertRequest = ProductUpsertRequest(name="Test Product", price=10.0, vat=2.0)

    # Convert the Pydantic model to a dictionary
    payload = request.model_dump()

    # Perform the POST request
    response = test_client.post("/product/1", json=payload)

    # Ensure the mock method was called with the correct arguments
    mock_product_service.create.assert_called_once()

    # Validate the response
    assert response.status_code == 200
    assert response.json()["name"] == "Test Product"

# Test for updating a product with mock
@patch("src.application.dic.DIC.product_service", new_callable=AsyncMock)
def test_update_product(mock_product_service, test_client):
    # Mock the update method to return an updated product
    mock_product_service.update.return_value = {"id": 1, "name": "Updated Product", "price": 15.0, "vat": 3.0}

    request: ProductUpsertRequest = ProductUpsertRequest(name="Updated Product", price=15.0, vat=3.0)

    # Convert the Pydantic model to a dictionary
    payload = request.model_dump()

    # Perform the PUT request
    response = test_client.put("/product/1", json=payload)

    # Ensure the mock method was called
    mock_product_service.update.assert_called_once_with(1, "Updated Product", 15.0, 3.0)

    # Validate the response
    assert response.status_code == 200
    assert response.json()["name"] == "Updated Product"

# Test for deleting a product with mock
@patch("src.application.dic.DIC.product_service", new_callable=AsyncMock)
def test_delete_product(mock_product_service, test_client):
    # Mock the delete method to return None
    mock_product_service.delete.return_value = None

    # Perform the DELETE request
    response = test_client.delete("/product/1")

    # Ensure the mock method was called
    mock_product_service.delete.assert_called_once_with(1)

    # Validate the response
    assert response.status_code == 200


@patch("src.application.dic.DIC.order_service", new_callable=AsyncMock)
def test_calculate_order_with_rate_limiter(mock_order_service, test_client):
    mock_order_service.calculate_order.return_value = {
        "order_id": "123e4567-e89b-12d3-a456-426614174000",
        "items": [
            {"id": 1, "name": "Product A", "quantity": 2, "price": 10.0, "vat": 2.0},
            {"id": 2, "name": "Product B", "quantity": 1, "price": 20.0, "vat": 4.0},
        ],
        "order_price": 40.0,
        "order_vat": 8.0,
    }

    products = [
        ProductRequest(product_id=1, quantity=2).model_dump(),
        ProductRequest(product_id=2, quantity=1).model_dump(),
    ]

    order = OrderRequest(items=products).model_dump()

    request = CalculationRequest(order=order)

    payload = request.model_dump()

    response = test_client.post("/order/calculate", json=payload)
    mock_order_service.calculate_order.assert_called_once()

    if response.status_code == 429:
        assert response.json()["detail"] == "Too Many Requests"
    else:
        assert response.status_code == 200
        assert response.json()["order_price"] == 40.0
        assert response.json()["order_vat"] == 8.0


@patch("src.application.dic.DIC.order_service", new_callable=AsyncMock)
def test_rate_limiter_exceeded(mock_order_service, test_client):
    # Mock the calculate_order method to return a predefined response
    mock_order_service.calculate_order.return_value = {
        "order_id": "123e4567-e89b-12d3-a456-426614174000",
        "items": [
            {"id": 1, "name": "Product A", "quantity": 2, "price": 10.0, "vat": 2.0},
            {"id": 2, "name": "Product B", "quantity": 1, "price": 20.0, "vat": 4.0},
        ],
        "order_price": 40.0,
        "order_vat": 8.0,
    }

    # Create input data using Pydantic models and convert them to dictionaries
    products = [
        ProductRequest(product_id=1, quantity=2).model_dump(),
        ProductRequest(product_id=2, quantity=1).model_dump(),
    ]
    order = OrderRequest(items=products).model_dump()
    request = CalculationRequest(order=order)
    payload = request.model_dump()

    # Perform consecutive requests to exceed the rate limit
    for _ in range(6):  # Assuming a limit of 5 requests per minute
        response = test_client.post("/order/calculate", json=payload)

    # Verify that the last request returns 429 Too Many Requests
    assert response.status_code == 429
    assert response.reason_phrase == "Too Many Requests"