import pytest

from app.pricing import (
    calculate_subtotal,
    calculate_discount,
    calculate_shipping_cost,
    calculate_order_total,
    COSTOS_ENVIO,
    ENVIO_GRATIS_DESDE,
)


# ---------- calculate_subtotal (RN-05) ----------

@pytest.mark.parametrize(
    "unit_price, quantity, subtotal_esperado",
    [
        (50000, 1, 50000.0),      # una sola unidad
        (50000, 3, 150000.0),     # varias unidades
        (12345, 7, 86415.0),      # precio "no redondo" x cantidad mayor
    ],
)
def test_calculate_subtotal_combinaciones_precio_cantidad(unit_price, quantity, subtotal_esperado):
    """Positiva: subtotal = precio_unitario * cantidad, en varias combinaciones."""
    assert calculate_subtotal(unit_price, quantity) == subtotal_esperado


def test_calculate_subtotal_unit_price_tipo_invalido():
    """Negativa: unit_price no numerico lanza error."""
    with pytest.raises(ValueError):
        calculate_subtotal("cien", 2)


# ---------- calculate_discount (RN-06) ----------

@pytest.mark.parametrize(
    "subtotal, tasa_esperada",
    [
        (99999, 0.0),      # justo debajo de 100000 -> sin descuento
        (100000, 0.10),    # exactamente 100000 -> entra al tramo 10%
        (499999, 0.10),    # justo debajo de 500000 -> aun en el tramo 10%
        (500000, 0.15),    # exactamente 500000 -> entra al tramo 15%
        (600000, 0.15),    # un valor superior -> se mantiene en 15%
    ],
)
def test_calculate_discount_por_tramo_y_fronteras(subtotal, tasa_esperada):
    """Positiva/frontera: cada tramo de descuento aplica la tasa correcta,
    incluyendo los limites exactos de cada tramo."""
    assert calculate_discount(subtotal) == pytest.approx(subtotal * tasa_esperada)


def test_calculate_discount_subtotal_negativo():
    """Negativa: un subtotal negativo no es valido."""
    with pytest.raises(ValueError):
        calculate_discount(-1000)


# ---------- calculate_shipping_cost (RN-07/RN-08/RN-09) ----------

@pytest.mark.parametrize(
    "zone, costo_esperado",
    [
        ("local", COSTOS_ENVIO["local"]),
        ("regional", COSTOS_ENVIO["regional"]),
        ("nacional", COSTOS_ENVIO["nacional"]),
    ],
)
def test_calculate_shipping_cost_por_zona(zone, costo_esperado):
    """Positiva: cada zona tiene su costo fijo cuando no aplica envio gratis."""
    assert calculate_shipping_cost(zone, 50000) == costo_esperado


@pytest.mark.parametrize(
    "total_after_discount, costo_esperado",
    [
        (699999, COSTOS_ENVIO["local"]),  # justo debajo del umbral: aun se cobra envio
        (700000, 0.0),                    # exactamente en el umbral: envio gratis (RN-09)
    ],
)
def test_calculate_shipping_cost_umbral_envio_gratis(total_after_discount, costo_esperado):
    """Frontera: el envio gratis aplica desde ENVIO_GRATIS_DESDE (700000) inclusive."""
    assert ENVIO_GRATIS_DESDE == 700000
    assert calculate_shipping_cost("local", total_after_discount) == costo_esperado


def test_calculate_shipping_cost_zona_invalida():
    """Negativa: una zona no reconocida lanza error."""
    with pytest.raises(ValueError):
        calculate_shipping_cost("internacional", 50000)


# ---------- calculate_order_total (RN-10): pedidos completos ----------

@pytest.mark.parametrize(
    "unit_price, quantity, zone, total_esperado",
    [
        # Pedido 1: subtotal 150000 -> descuento 10% (15000) -> 135000
        # + envio local (8000) = 143000
        (50000, 3, "local", 143000.0),
        # Pedido 2: subtotal 600000 -> descuento 15% (90000) -> 510000
        # + envio nacional (25000) = 535000
        (100000, 6, "nacional", 535000.0),
        # Pedido 3: subtotal 1000000 -> descuento 15% (150000) -> 850000
        # >= 700000 -> envio gratis -> total 850000
        (100000, 10, "regional", 850000.0),
    ],
)
def test_calculate_order_total_pedidos_completos(unit_price, quantity, zone, total_esperado):
    """Positiva: pedidos completos con distintos tramos de descuento y envio,
    incluyendo un caso con envio gratis."""
    assert calculate_order_total(unit_price, quantity, zone) == pytest.approx(total_esperado)