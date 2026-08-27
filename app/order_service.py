from app.validators import (
    validate_customer_name,
    validate_product_code,
    validate_unit_price,
    validate_quantity,
    validate_shipping_zone,
)
from app.pricing import (
    calculate_subtotal,
    calculate_discount,
    calculate_shipping_cost,
)
 
 
class OrderService:
    def __init__(self, repository) -> None:
        self.repository = repository
 
    def create(self, data: dict) -> dict:
        """
        1. Validar y normalizar datos.
        2. Verificar que order_code no exista (RN-11).
        3. Calcular subtotal (RN-05).
        4. Calcular descuento (RN-06).
        5. Calcular envio (RN-07/RN-08/RN-09).
        6. Calcular total (RN-10).
        7. Construir el pedido con estado pending (RN-12).
        8. Guardar y retornar el pedido.
        """
        # 1. Validar y normalizar datos
        order_code = data.get("order_code")
        if not isinstance(order_code, str) or not order_code.strip():
            raise ValueError("order_code es obligatorio y debe ser texto no vacio")
        order_code = order_code.strip()
 
        customer_name = validate_customer_name(data.get("customer_name"))
        product_code = validate_product_code(data.get("product_code"))
        unit_price = validate_unit_price(data.get("unit_price"))
        quantity = validate_quantity(data.get("quantity"))
        shipping_zone = validate_shipping_zone(data.get("shipping_zone"))
 
        # 2. Verificar que order_code no exista (RN-11)
        if self.repository.exists_by_code(order_code):
            raise ValueError(
                f"Ya existe un pedido con order_code '{order_code}'"
            )
 
        # 3. Calcular subtotal
        subtotal = calculate_subtotal(unit_price, quantity)
 
        # 4. Calcular descuento
        discount = calculate_discount(subtotal)
        total_after_discount = subtotal - discount
 
        # 5. Calcular envio
        shipping_cost = calculate_shipping_cost(shipping_zone, total_after_discount)
 
        # 6. Calcular total (RN-10)
        total = total_after_discount + shipping_cost
 
        # 7. Construir el pedido con estado pending (RN-12)
        order = {
            "order_code": order_code,
            "customer_name": customer_name,
            "product_code": product_code,
            "unit_price": unit_price,
            "quantity": quantity,
            "shipping_zone": shipping_zone,
            "subtotal": subtotal,
            "discount": discount,
            "shipping_cost": shipping_cost,
            "total": total,
            "status": "pending",
        }
 
        # 8. Guardar y retornar el pedido
        return self.repository.save(order)


