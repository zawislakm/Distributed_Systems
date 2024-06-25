import json

import pika

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.exchange_declare(exchange='controller_exchange', exchange_type='direct')
channel.queue_declare(queue='admission_room_queue')
channel.queue_declare(queue='controller_messages_queue')

while True:

    mode = input("Enter mode (patient|admin|exit): ")

    match mode:

        case "patient":
            patient_name = input("Enter patient name: ")
            injury = input("Enter injury: ")

            patient_data = {
                "patient_name": patient_name,
                "injury": injury
            }

            message = json.dumps(patient_data)

            channel.basic_publish(
                exchange='controller_exchange',
                routing_key='admission_room',
                body=message
            )

        case "admin":
            message = input("Enter message: ")
            routing_key = input("Enter routing key: ")

            admin_data = {
                "message": message,
                "routing_key": routing_key
            }
            message = json.dumps(admin_data)

            channel.basic_publish(
                exchange='controller_exchange',
                routing_key='admin',
                body=message
            )

        case "exit":
            break
        case _:
            print("Invalid mode")
            continue
