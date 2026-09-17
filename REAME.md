CODIGO PARA PRUEBAS
 
python -m pytest              # ejecución estándar
python -m pytest -v           # modo detallado, un caso por línea
python -m pytest tests/test_validators.py -v
python -m pytest tests/test_pricing.py -v
python -m pytest tests/test_order_service.py -v
python -m pytest -m positive  # solo casos positivos
python -m pytest -m negative  # solo casos negativos
python -m pytest -m frontera  # solo casos de frontera
python -m pytest -k discount -v
python -m pytest --lf         # solo repite las últimas pruebas que fallaron
python -m pytest tests/test_validators.py: nombre de la prueba #ejemplo prueba unitaria