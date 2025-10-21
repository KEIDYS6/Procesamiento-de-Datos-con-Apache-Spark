import time
import json
from kafka import KafkaProducer
from random import choice, randint

KAFKA_BROKER = 'localhost:9092'
KAFKA_TOPIC = 'beneficios_stream'

producer = KafkaProducer(
    bootstrap_servers=[KAFKA_BROKER],
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

departamentos = ["CUNDINAMARCA", "ANTIOQUIA", "VALLE DEL CAUCA", "ATLANTICO", "BOLIVAR"]
etnias = ["INDIGENA", "AFROCOLOMBIANO", "NINGUNA", "ROM"]
tipos_beneficio = ["SUBVENCION", "ASIGNACION DIRECTA", "CREDITO EDUCATIVO"]

def generate_message():
    return {
        "timestamp": int(time.time()),
        "departamento": choice(departamentos),
        "etnia": choice(etnias),
        "edad_min": randint(18, 90),
        "monto_beneficio": randint(100000, 500000)
    }

try:
    while True:
        message = generate_message()
        producer.send(KAFKA_TOPIC, value=message)
        print(f"Producido: {message}")
        time.sleep(1)
except KeyboardInterrupt:
    print("\nProductor detenido por el usuario.")
finally:
    producer.close()
