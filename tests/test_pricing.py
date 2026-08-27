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
 
def test_calculate_subtotal_positivo():
    """Positiva: subtotal = precio_unitario * cantidad."""
    assert calculate_subtotal(50000, 3) == 150000.0
 
 
def test_calculate_subtotal_unit_price_tipo_invalido():
    """Negativa: unit_price no numerico lanza error."""
    with pytest.raises(ValueError):
        calculate_subtotal("cien", 2)
 
 
# ---------- calculate_discount (RN-06) ----------
 
@pytest.mark.parametrize(
    "subtotal, tasa_esperada",
    [
        (50000, 0.0),     # bajo el primer umbral -> sin descuento
        (100000, 0.10),   # frontera inferior del tramo 10%
        (499999, 0.10),   # justo antes del tramo 15%
        (500000, 0.15),   # frontera inferior del tramo 15%
    ],
)
def test_calculate_discount_por_tramo(subtotal, tasa_esperada):
    """Positiva/frontera: cada tramo de descuento aplica la tasa correcta."""
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
 
 
def test_calculate_shipping_cost_envio_gratis_en_el_umbral():
    """Frontera: justo en el umbral, el envio ya es gratis (RN-09)."""
    assert calculate_shipping_cost("local", ENVIO_GRATIS_DESDE) == 0.0
 
 
def test_calculate_shipping_cost_zona_invalida():
    """Negativa: una zona no reconocida lanza error."""
    with pytest.raises(ValueError):
        calculate_shipping_cost("internacional", 50000)
 
 
# ---------- calculate_order_total (RN-10) ----------
 
def test_calculate_order_total_orquesta_las_reglas():
    """Positiva: el total integra subtotal, descuento y costo de envio."""
    total = calculate_order_total(50000, 3, "local")
    # subtotal 150000 -> descuento 10% (15000) -> 135000 + envio local 8000
    assert total == pytest.approx(143000.0)
