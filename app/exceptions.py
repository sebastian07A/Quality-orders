class OrderError(Exception):
    """Excepcion base del dominio."""
    pass

class InvalidCustomerNameError(DomainError):
    """Nombre de cliente invalido."""
    pass

class InvalidProductCodeError(DomainError):
    """Codigo de producto invalido."""
    pass

class InvalidPriceError(DomainError):
    """Precio unitario invalido."""
    pass

class InvalidQuantityError(DomainError):
    """Cantidad fuera del rango permitido."""
    pass

class InvalidShippingZoneError(DomainError):
    """Zona de envio no permitida."""
    pass

class DuplicateOrderError(DomainError):
    """Codigo de pedido repetido."""
    pass