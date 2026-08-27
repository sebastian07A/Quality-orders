class InMemoryOrderRepository:
    def __init__(self) -> None:
        # Diccionario indexado por order_code para busqueda O(1)
        # y para poder verificar duplicidad (RN-11) de forma directa.
        self._orders: dict = {}
 
    def exists_by_code(self, order_code: str) -> bool:
        """
        RN-11: soporte para no permitir dos pedidos con el mismo
        codigo de pedido. Retorna True si el order_code ya existe.
        """
        return order_code in self._orders
 
    def save(self, order: dict) -> dict:
        """
        Guarda un pedido. Se espera que 'order' contenga la llave
        'order_code'. Si el codigo ya existe, se rechaza para no
        romper RN-11 desde este nivel tambien.
        """
        order_code = order.get("order_code")
 
        if not order_code:
            raise ValueError("order debe contener 'order_code'")
 
        if self.exists_by_code(order_code):
            raise ValueError(
                f"Ya existe un pedido con order_code '{order_code}'"
            )
 
        # Se guarda una copia para que mutaciones externas al dict
        # original no afecten el estado interno del repositorio.
        self._orders[order_code] = dict(order)
 
        return dict(self._orders[order_code])
 
    def list_all(self) -> list:
        """
        Lista todos los pedidos almacenados como copias, para
        proteger el estado interno del repositorio.
        """
        return [dict(order) for order in self._orders.values()]
