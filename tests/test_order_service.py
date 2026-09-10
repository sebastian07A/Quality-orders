import pytest


# ---------- creacion exitosa ----------

def test_create_order_exitoso_queda_pending(order_service, valid_order_data):
    """Positiva: un pedido valido se crea con estado pending (RN-12)."""
    order = order_service.create(valid_order_data)

    assert order["status"] == "pending"
    assert order["order_code"] == "ORD-001"


def test_create_order_normaliza_nombre_codigo_y_zona(order_service, valid_order_data):
    """Positiva: los datos se normalizan antes de guardarse."""
    order = order_service.create(valid_order_data)

    assert order["customer_name"] == "Ana Torres"
    assert order["product_code"] == "ABC123"
    assert order["shipping_zone"] == "local"


def test_create_order_calcula_totales_correctamente(order_service, valid_order_data):
    """Positiva: subtotal, descuento, envio y total quedan bien calculados."""
    order = order_service.create(valid_order_data)

    # subtotal 50000 * 2 = 100000 -> descuento 10% (10000) -> 90000 + envio local 8000
    assert order["subtotal"] == 100000.0
    assert order["discount"] == 10000.0
    assert order["shipping_cost"] == 8000.0
    assert order["total"] == 98000.0


# ---------- reglas de negocio criticas (RN-11) ----------

def test_create_order_duplicado_lanza_error(order_service, valid_order_data):
    """Negativa: no se permiten dos pedidos con el mismo order_code (RN-11)."""
    order_service.create(valid_order_data)

    with pytest.raises(ValueError):
        order_service.create(valid_order_data)


def test_create_order_sin_order_code_lanza_error(order_service, valid_order_data):
    """Negativa: order_code vacio (solo espacios) no es valido."""
    valid_order_data["order_code"] = "   "

    with pytest.raises(ValueError):
        order_service.create(valid_order_data)


def test_create_order_invalido_no_se_almacena(order_service, order_repository, valid_order_data):
    """Un pedido con datos invalidos no debe quedar guardado en el repositorio."""
    valid_order_data["quantity"] = 0  # fuera de rango permitido (RN-04)

    with pytest.raises(ValueError):
        order_service.create(valid_order_data)

    assert order_repository.list_all() == []


# ---------- independencia del repositorio ----------

def test_repository_devuelve_copias_independientes(order_repository):
    """El repositorio no debe exponer referencias mutables a su estado interno."""
    original = {
        "order_code": "ORD-XYZ",
        "customer_name": "Ana Torres",
        "status": "pending",
    }

    saved = order_repository.save(original)

    # Mutar el dict original despues de guardarlo no debe afectar lo almacenado.
    original["status"] = "mutado_desde_afuera"
    # Mutar la copia devuelta por save() tampoco debe afectar lo almacenado.
    saved["status"] = "mutado_desde_el_resultado"

    assert order_repository.list_all()[0]["status"] == "pending"