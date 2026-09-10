from app.validators import validate_shipping_zone
 
# RN-08: costo de envio segun zona
COSTOS_ENVIO = {
    "local": 8000,
    "regional": 15000,
    "nacional": 25000,
}
 
# RN-09: umbral de total a partir del cual el envio es gratis
ENVIO_GRATIS_DESDE = 700000
 
 
def calculate_subtotal(unit_price: float, quantity: int) -> float:
    """
    RN-05: subtotal = precio_unitario * cantidad
    """
    if isinstance(unit_price, bool) or not isinstance(unit_price, (int, float)):
        raise ValueError("unit_price debe ser un numero")
    if isinstance(quantity, bool) or not isinstance(quantity, int):
        raise ValueError("quantity debe ser un numero entero")
 
    return float(unit_price) * quantity
 
 
def calculate_discount(subtotal: float) -> float:
    """
    RN-06: Subtotal menor a 100000: 0%.
           Desde 100000 y menor a 500000: 10%.
           Desde 500000: 15%.
 
    Retorna el VALOR del descuento (no el porcentaje ni el total).
    """
    if isinstance(subtotal, bool) or not isinstance(subtotal, (int, float)):
        raise ValueError("subtotal debe ser un numero")
    if subtotal < 0:
        raise ValueError("subtotal no puede ser negativo")
 
    if subtotal < 100000:
        rate = 0.0
    elif subtotal < 500000:
        rate = 0.10
    else:
        rate = 0.15
 
    return subtotal * rate
 
 
def calculate_shipping_cost(zone: str, total_after_discount: float) -> float:
    """
    RN-07/RN-08: costo de envio segun zona (local, regional, nacional).
    RN-09: si el total despues del descuento es >= 700000, el envio es 0.
    """
    if isinstance(total_after_discount, bool) or not isinstance(
        total_after_discount, (int, float)
    ):
        raise ValueError("total_after_discount debe ser un numero")
    if total_after_discount < 0:
        raise ValueError("total_after_discount no puede ser negativo")
 
    normalized_zone = validate_shipping_zone(zone)
 
    if total_after_discount >= ENVIO_GRATIS_DESDE:
        return 0.0
 
    return float(COSTOS_ENVIO[normalized_zone])
 
 
def calculate_order_total(
    unit_price: float,
    quantity: int,
    zone: str,
) -> float:
    """
    RN-10: total = subtotal - descuento + costo_envio
 
    Orquesta las funciones anteriores. No implementa reglas propias:
    delega en calculate_subtotal, calculate_discount y
    calculate_shipping_cost para que cada regla siga probandose
    de forma aislada.
    """
    subtotal = calculate_subtotal(unit_price, quantity)
    discount = calculate_discount(subtotal)
    total_after_discount = subtotal - discount
    shipping_cost = calculate_shipping_cost(zone, total_after_discount)
 
    return total_after_discount + shipping_cost