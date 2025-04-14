class ProductNotFoundError(Exception):
    """Exception for product not found."""
    pass

class ProductAlreadyExistsError(Exception):
    """Exception for product already exists."""
    pass

class OrderValidationError(Exception):
    """Exception for order validation error."""
    pass