import pytest
 
from app.validators import (
    validate_customer_name,
    validate_product_code,
    validate_unit_price,
    validate_quantity,
    validate_shipping_zone,
)
 
 
# ---------- validate_customer_name (RN-01) ----------
 
def test_validate_customer_name_normaliza_espacios():
    """Positiva: se recortan espacios al inicio y al final."""
    assert validate_customer_name("  Ana Torres  ") == "Ana Torres"
 
 
def test_validate_customer_name_valido_minimo_3_caracteres():
    """Frontera positiva: exactamente 3 caracteres es valido."""
    assert validate_customer_name("Ana") == "Ana"
 
 
def test_validate_customer_name_invalido_menor_a_3_caracteres():
    """Negativa/frontera: menos de 3 caracteres despues de normalizar falla."""
    with pytest.raises(ValueError):
        validate_customer_name(" An ")
 
 
# ---------- validate_product_code (RN-02) ----------
 
def test_validate_product_code_normaliza_a_mayusculas():
    """Positiva: el codigo se normaliza a mayusculas."""
    assert validate_product_code("abc123") == "ABC123"
 
 
def test_validate_product_code_demasiado_corto():
    """Negativa/frontera: menos de 3 caracteres falla."""
    with pytest.raises(ValueError):
        validate_product_code("ab")
 
 
# ---------- validate_unit_price (RN-03) ----------
 
def test_validate_unit_price_valor_positivo():
    """Positiva: un precio mayor a 0 es valido."""
    assert validate_unit_price(15000) == 15000.0
 
 
def test_validate_unit_price_igual_a_cero():
    """Negativa/frontera: precio igual a 0 no es valido."""
    with pytest.raises(ValueError):
        validate_unit_price(0)
 
 
def test_validate_unit_price_negativo():
    """Negativa: precio negativo no es valido."""
    with pytest.raises(ValueError):
        validate_unit_price(-500)
 
 
# ---------- validate_quantity (RN-04) ----------
 
@pytest.mark.parametrize("quantity", [1, 20])
def test_validate_quantity_valores_validos_en_frontera(quantity):
    """Positiva/frontera: 1 y 20 son los limites validos (inclusive)."""
    assert validate_quantity(quantity) == quantity
 
 
@pytest.mark.parametrize("quantity", [0, 21])
def test_validate_quantity_valores_invalidos_en_frontera(quantity):
    """Negativa/frontera: 0 y 21 quedan fuera del rango permitido."""
    with pytest.raises(ValueError):
        validate_quantity(quantity)
 
 
# ---------- validate_shipping_zone (RN-07) ----------
 
def test_validate_shipping_zone_normaliza_mayusculas_y_espacios():
    """Positiva: la zona se normaliza a minusculas, sin espacios."""
    assert validate_shipping_zone("  Local  ") == "local"
 
 
def test_validate_shipping_zone_desconocida():
    """Negativa: una zona no listada en ZONAS_PERMITIDAS falla."""
    with pytest.raises(ValueError):
        validate_shipping_zone("internacional")
