# Project Overview

This project is a FastAPI-based application for managing products. It provides a set of RESTful APIs to perform CRUD operations on products, including listing, retrieving, creating, updating, and deleting products.

## Project Structure

The project is organized as follows:

- **`src/domain`**: This module represents the core of the application, containing all the business logic and main entities. It is designed to be independent of the infrastructure and focuses exclusively on business rules and data models.

  - **`models`**: Contains the main domain entities, representing the fundamental objects and concepts of the application, such as `Product` and `Order`.
  - **`dtos`**: Includes Data Transfer Objects (DTOs), used for communication between application layers and for request/response validation in the APIs.
  - **`errors`**: Defines custom exceptions to handle domain-specific errors, such as `ProductNotFoundError` or `OrderValidationError`.
  - **`usecases`**: Contains the business logic use cases, encapsulating the core operations and workflows of the application, such as creating a product or calculating an order.
  - **`repositories`**: Defines repository interfaces to abstract data access, ensuring that the domain layer remains decoupled from the underlying data storage implementation.

- **`src/application`**: Contains the application services and dependency injection container (DIC).

- **`src/infrastructure`**: Contains infrastructure-related code, such as routers and external integrations.
  - `routers`: Defines the API endpoints using FastAPI.

- **`tests`**: Contains unit and integration tests for the application.

## Available Endpoints

### Product Endpoints

| Method | Endpoint         | Description                     |
|--------|------------------|---------------------------------|
| GET    | `/product/`      | List all products.             |
| GET    | `/product/{id}`  | Retrieve a product by ID.      |
| POST   | `/product/{id}`  | Create a new product.          |
| PUT    | `/product/{id}`  | Update an existing product.    |
| DELETE | `/product/{id}`  | Delete a product by ID.        |

### Order Endpoints
| Method | Endpoint              | Description                          |
|--------|-----------------------|--------------------------------------|
| POST   | `/order/calculate`    | Calculate the total price of an order. |


### Error Handling

- **404 Not Found**: Returned when a product is not found.
- **400 Bad Request**: Returned when trying to create a product that already exists.
- **500 Internal Server Error**: Returned for unexpected errors.

## How to Run via Docker

1. **Build the Docker image**:
   ```bash
   docker build -t purchase-cart-service . --progress=plain --no-cache
    ```

2. **Run the Docker container**:
   ```bash
   docker run -v ${PWD}:/mnt -p 9090:9090 -w /mnt purchase-cart-service ./scripts/run.sh
    ```

3. **Run the tests**:
The tests are included in the Docker image. You can run them using the following command:
   ```bash
   docker run -v ${PWD}:/mnt -p 9090:9090 -w /mnt purchase-cart-service ./scripts/tests.sh
    ```

4. **Access the API**:
Open your browser and navigate to `http://0.0.0.0:9090/docs` to access the Swagger UI for the API documentation.