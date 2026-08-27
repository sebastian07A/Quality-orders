import pytest
 
from app.repositories import InMemoryOrderRepository
from app.order_service import OrderService
 
 
@pytest.fixture
def repository():
    """Repositorio en memoria limpio, aislado para cada prueba."""
    return InMemoryOrderRepository()
 
 
@pytest.fixture
def service(repository):
    """OrderService listo para usar, conectado a un repositorio limpio."""
    return OrderService(repository)
 
 
@pytest.fixture
def valid_order_data():
    """Payload valido base para crear un pedido (RN-01 a RN-12)."""
    return {
        "order_code": "ORD-001",
        "customer_name": "  Ana Torres  ",
        "product_code": "abc123",
        "unit_price": 50000,
        "quantity": 2,
        "shipping_zone": "  Local  ",
    }
