import pytest

from app.repositories import InMemoryOrderRepository
from app.order_service import OrderService


@pytest.fixture
def order_repository():
    """Repositorio en memoria limpio, aislado para cada prueba.

    Se crea una instancia NUEVA en cada prueba que la use, para que
    ninguna prueba herede estado dejado por otra (RN-11 depende de
    empezar siempre con un repositorio vacio).
    """
    return InMemoryOrderRepository()


@pytest.fixture
def order_service(order_repository):
    """OrderService listo para usar, conectado a un order_repository limpio.

    Depende de la fixture order_repository, asi que cada prueba recibe
    su propio par (repository, service) sin compartir estado con otras.
    """
    return OrderService(order_repository)


@pytest.fixture
def valid_order_data():
    """Payload valido base para crear un pedido (RN-01 a RN-12).

    Se devuelve un dict NUEVO en cada llamada (no una constante
    reutilizada), para que una prueba que lo modifique no afecte a
    las demas.
    """
    return {
        "order_code": "ORD-001",
        "customer_name": "  Ana Torres  ",
        "product_code": "abc123",
        "unit_price": 50000,
        "quantity": 2,
        "shipping_zone": "  Local  ",
    }