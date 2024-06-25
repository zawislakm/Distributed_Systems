import json
import time

import pika

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
channel.basic_qos(prefetch_count=1)


def process_doctor_examination_request(ch, method, properties, body):
    patient_data = json.loads(body)
    print(
        f"ADMIN log DOCTOR {patient_data['doctor_id']}, Routing key: {method.routing_key}, "
        f"patient {patient_data['patient_name']} sent to technician by "
        f"doctor {patient_data['doctor_id']}")
    ch.basic_ack(delivery_tag=method.delivery_tag)


def process_technician_examination_result(ch, method, properties, body):
    patient_results = json.loads(body)
    print(
        f"ADMIN log TECHNICIAN {patient_results['technician_id']}, Routing key: {method.routing_key}, "
        f"patient {patient_results['patient_name']} results sent to  doctor {patient_results['doctor_id']}")
    time.sleep(10)
    ch.basic_ack(delivery_tag=method.delivery_tag)


def process_controller_messages(ch, method, properties, body):
    admin_data = json.loads(body)

    print(f"ADMIN send message: {admin_data['message']} to routing key: {admin_data['routing_key']}")

    ch.basic_ack(delivery_tag=method.delivery_tag)

    channel.basic_publish(exchange='admin_exchange', routing_key=admin_data['routing_key'], body=admin_data['message'])


# doctor exchange and queues
channel.exchange_declare(exchange='doctor_exchange', exchange_type='topic')
channel.queue_declare(queue='doctor_queue')

injury_type1 = "*"
channel.queue_declare(queue="all_injuries" + "_queue")
channel.queue_bind(exchange='doctor_exchange', queue="all_injuries" + "_queue", routing_key=injury_type1)
channel.basic_consume(queue="all_injuries" + "_queue", on_message_callback=process_doctor_examination_request,
                      auto_ack=False)

# technician exchange and queues

channel.exchange_declare(exchange='technician_exchange', exchange_type='topic')
channel.queue_declare(queue='technician_queue')

channel.queue_declare(queue='all_results' + "_queue")
channel.queue_bind(exchange='technician_exchange', queue='technician_queue', routing_key='*')
channel.basic_consume(queue='technician_queue', on_message_callback=process_technician_examination_result,
                      auto_ack=False)

# messages exchange and queues

channel.exchange_declare(exchange='controller_exchange', exchange_type='direct')
channel.queue_declare(queue='controller_messages_queue')

channel.queue_bind(exchange='controller_exchange', queue='controller_messages_queue', routing_key='admin')
channel.basic_consume(queue='controller_messages_queue', on_message_callback=process_controller_messages,
                      auto_ack=False)

# admin exchange and queues

channel.exchange_declare(exchange='admin_exchange', exchange_type='topic')
channel.queue_declare(queue='admin_queue')

print("ADMIN is running")
channel.start_consuming()
