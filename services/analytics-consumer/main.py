import json
import logging
import pika
import threading
from fastapi import FastAPI
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST
from starlette.responses import Response

app = FastAPI()
logging.basicConfig(level=logging.INFO)

# Metrics
processed_orders = Counter('orders_processed_total', 'Total processed orders')

class OrderConsumer:
    def __init__(self):
        self.connection = None
        self.channel = None
        
    def connect(self):
        connection_params = pika.ConnectionParameters(
            host='localhost',
            port=5672,
            credentials=pika.PlainCredentials('guest', 'guest')
        )
        self.connection = pika.BlockingConnection(connection_params)
        self.channel = self.connection.channel()
        
    def process_message(self, ch, method, properties, body):
        try:
            order_data = json.loads(body)
            logging.info(f"Processing order: {order_data.get('orderId')}")
            processed_orders.inc()
            ch.basic_ack(delivery_tag=method.delivery_tag)
        except Exception as e:
            logging.error(f"Error processing message: {e}")
            ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)
    
    def start_consuming(self):
        self.connect()
        self.channel.queue_declare(queue='orders.q', durable=True)
        self.channel.basic_qos(prefetch_count=10)
        self.channel.basic_consume(queue='orders.q', on_message_callback=self.process_message)
        self.channel.start_consuming()

consumer = OrderConsumer()

@app.on_event("startup")
def startup_event():
    threading.Thread(target=consumer.start_consuming, daemon=True).start()

@app.get("/health")
def health():
    return {"status": "UP"}

@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8082)