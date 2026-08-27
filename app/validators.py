ZONAS_PERMITIDAS = {"local", "regional", "nacional"}
 
 
def validate_customer_name(customer_name: str) -> str:
    """
    RN-01: El nombre del cliente se normaliza eliminando espacios al
    inicio y al final. Debe tener minimo 3 caracteres.
    """
    if not isinstance(customer_name, str):
        raise ValueError("customer_name debe ser una cadena de texto")
 
    normalized = customer_name.strip()
 
    if len(normalized) < 3:
        raise ValueError(
            "customer_name debe tener minimo 3 caracteres despues de normalizar"
        )
 
    return normalized
 
 
def validate_product_code(product_code: str) -> str:
    """
    RN-02: El codigo de producto se normaliza a mayusculas.
    Debe tener minimo 3 caracteres.
    """
    if not isinstance(product_code, str):
        raise ValueError("product_code debe ser una cadena de texto")
 
    normalized = product_code.strip().upper()
 
    if len(normalized) < 3:
        raise ValueError(
            "product_code debe tener minimo 3 caracteres despues de normalizar"
        )
 
    return normalized
 
 
def validate_unit_price(unit_price: float) -> float:
    """
    RN-03: El precio unitario debe ser mayor que 0.
    """
    if isinstance(unit_price, bool) or not isinstance(unit_price, (int, float)):
        raise ValueError("unit_price debe ser un numero")
 
    if unit_price <= 0:
        raise ValueError("unit_price debe ser mayor que 0")
 
    return float(unit_price)
 
 
def validate_quantity(quantity: int) -> int:
    """
    RN-04: La cantidad permitida esta entre 1 y 20 unidades, inclusive.
    """
    if isinstance(quantity, bool) or not isinstance(quantity, int):
        raise ValueError("quantity debe ser un numero entero")
 
    if quantity < 1 or quantity > 20:
        raise ValueError("quantity debe estar entre 1 y 20 unidades, inclusive")
 
    return quantity
 
 
def validate_shipping_zone(zone: str) -> str:
    """
    RN-07: Las zonas permitidas son local, regional y nacional.
    Deben normalizarse a minusculas.
    """
    if not isinstance(zone, str):
        raise ValueError("zone debe ser una cadena de texto")
 
    normalized = zone.strip().lower()
 
    if normalized not in ZONAS_PERMITIDAS:
        raise ValueError(
            f"zone '{zone}' no es valida. Debe ser una de: {sorted(ZONAS_PERMITIDAS)}"
        )
 
    return normalized
