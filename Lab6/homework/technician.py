import json
import random
import time

import pika

TECHNICIAN_ID = None
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
channel.basic_qos(prefetch_count=1)


def process_admin_message(ch, method, properties, body):
    global TECHNICIAN_ID
    print(f"Technician {TECHNICIAN_ID} got message from ADMIN: {str(body, 'utf-8')}")
    ch.basic_ack(delivery_tag=method.delivery_tag)


def process_patient(ch, method, properties, body):
    global channel, TECHNICIAN_ID
    patient_data = json.loads(body)
    print(
        f"Technician with routing key {method.routing_key}: working on patient {patient_data['patient_name']} for doctor {patient_data['doctor_id']}")

    working_time = random.randint(1, 5)
    time.sleep(working_time)
    print("Technician DONE")
    ch.basic_ack(delivery_tag=method.delivery_tag)

    # send results
    patient_results = {
        "technician_id": TECHNICIAN_ID,
        "doctor_id": patient_data["doctor_id"],
        "patient_name": patient_data["patient_name"],
        "injury": patient_data["injury"],
        "results": "DONE"
    }
    message = json.dumps(patient_results)

    channel.basic_publish(exchange='technician_exchange', routing_key='doctor_' + str(patient_data['doctor_id']),
                          body=message)


TECHNICIAN_ID = int(input("Enter technician id:"))

channel.exchange_declare(exchange='doctor_exchange', exchange_type='topic')
channel.queue_declare(queue='doctor_queue')

print("Possible injuries: knee, elbow, hip")

injury_type1 = input("Enter injury type 1: ")

channel.queue_declare(queue=injury_type1 + "_queue")
channel.queue_bind(exchange='doctor_exchange', queue=injury_type1 + "_queue", routing_key=injury_type1)
channel.basic_consume(queue=injury_type1 + "_queue", on_message_callback=process_patient, auto_ack=False)

injury_type2 = input("Enter injury type 2: ")

channel.queue_declare(queue=injury_type2 + "_queue")
channel.queue_bind(exchange='doctor_exchange', queue=injury_type2 + "_queue", routing_key=injury_type2)
channel.basic_consume(queue=injury_type2 + "_queue", on_message_callback=process_patient, auto_ack=False)

# technician exchange and queues
channel.exchange_declare(exchange='technician_exchange', exchange_type='topic')
channel.queue_declare(queue='technician_queue')

# connection.close()

# messages exchange and queues

channel.exchange_declare(exchange='admin_exchange', exchange_type='topic')
queue_name = "technician_message" + str(TECHNICIAN_ID) + "_queue"

channel.queue_declare(queue=queue_name)
channel.queue_bind(exchange='admin_exchange', queue=queue_name, routing_key='technician.' + str(TECHNICIAN_ID))
channel.queue_bind(exchange='admin_exchange', queue=queue_name, routing_key='technician.all')
channel.queue_bind(exchange='admin_exchange', queue=queue_name, routing_key='all')
channel.basic_consume(queue=queue_name, on_message_callback=process_admin_message, auto_ack=False)

print(f"Technician {TECHNICIAN_ID} is ready")
channel.start_consuming()
