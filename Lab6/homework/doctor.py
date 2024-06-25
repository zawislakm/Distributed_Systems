import json

import pika

DOCTOR_ID = None
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
channel.basic_qos(prefetch_count=1)


def process_admin_message(ch, method, properties, body):
    global DOCTOR_ID
    print(f"Doctor {DOCTOR_ID} got message from ADMIN: {str(body, 'utf-8')}")
    ch.basic_ack(delivery_tag=method.delivery_tag)


def process_results_from_technician(ch, method, properties, body):
    global DOCTOR_ID

    patient_results = json.loads(body)
    print(
        f"Doctor {DOCTOR_ID}: patient {patient_results['patient_name']} with injury {patient_results['injury']} has "
        f"results: {patient_results['results']}")
    ch.basic_ack(delivery_tag=method.delivery_tag)


def process_patients_from_admission_room(ch, method, properties, body):
    global DOCTOR_ID
    patient_data = json.loads(body)
    print(
        f"Doctor {DOCTOR_ID}: patient {patient_data['patient_name']} with injury {patient_data['injury']} sent to "
        f"technician")
    ch.basic_ack(delivery_tag=method.delivery_tag)

    patient_data = {
        "doctor_id": DOCTOR_ID,
        "patient_name": patient_data['patient_name'],
        "injury": patient_data['injury']
    }
    message = json.dumps(patient_data)
    channel.basic_publish(exchange='doctor_exchange', routing_key=patient_data['injury'], body=message)


DOCTOR_ID = input("Enter doctor id: ")

# doctor exchange and queues
channel.exchange_declare(exchange='doctor_exchange', exchange_type='topic')
channel.queue_declare(queue='doctor_queue')

# technician exchange and queues

channel.exchange_declare(exchange='technician_exchange', exchange_type='topic')
channel.queue_declare(queue='technician_queue')

# doctor gets results of its patients from technician
injury_type1 = "doctor_" + str(DOCTOR_ID)

channel.queue_declare(queue=injury_type1 + "_queue")
channel.queue_bind(exchange='technician_exchange', queue=injury_type1 + "_queue", routing_key=injury_type1)
channel.basic_consume(queue=injury_type1 + "_queue", on_message_callback=process_results_from_technician,
                      auto_ack=False)

# doctor gets patients from admission room
channel.exchange_declare(exchange='controller_exchange', exchange_type='direct')

channel.queue_declare(queue='admission_room_queue')
channel.queue_bind(exchange='controller_exchange', queue='admission_room_queue', routing_key='admission_room')
channel.basic_consume(queue='admission_room_queue', on_message_callback=process_patients_from_admission_room,
                      auto_ack=False)

# messages exchange and queues
channel.exchange_declare(exchange='admin_exchange', exchange_type='topic')
queue_name = "doctor_message" + str(DOCTOR_ID) + "_queue"

channel.queue_declare(queue=queue_name)
channel.queue_bind(exchange='admin_exchange', queue=queue_name, routing_key='doctor.' + str(DOCTOR_ID))
channel.queue_bind(exchange='admin_exchange', queue=queue_name, routing_key='doctor.all')
channel.queue_bind(exchange='admin_exchange', queue=queue_name, routing_key='all')
channel.basic_consume(queue=queue_name, on_message_callback=process_admin_message, auto_ack=False)

print(f"Doctor {DOCTOR_ID} is ready")
channel.start_consuming()
# connection.close()
