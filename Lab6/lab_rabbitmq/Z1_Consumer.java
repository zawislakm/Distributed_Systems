import com.rabbitmq.client.*;

import java.io.IOException;


//Zmodyfikuj konsumenta, aby obsługiwał wiadomość przez zadany czas (podany w sek.)
//int timeToSleep = Integer.parseInt(message);
//Thread.sleep(timeToSleep * 1000);

public class Z1_Consumer {

    public static void main(String[] argv) throws Exception {

        // info
        System.out.println("Z1 CONSUMER");

        // connection & channel
        ConnectionFactory factory = new ConnectionFactory();
        factory.setHost("localhost");
        Connection connection = factory.newConnection();
        Channel channel = connection.createChannel();

        // queue
        String QUEUE_NAME = "queue1";
        channel.queueDeclare(QUEUE_NAME, false, false, false, null);
//        channel.basicQos(1);
        // consumer (handle msg)
        Consumer consumer = new DefaultConsumer(channel) {
            @Override
            public void handleDelivery(String consumerTag, Envelope envelope, AMQP.BasicProperties properties, byte[] body) throws IOException {
                String message = new String(body, "UTF-8");
                System.out.println("Received: " + message);

                try {
                    System.out.println("Processing message...");
                    int timeToSleep = Integer.parseInt(message);
//                    Thread.sleep(timeToSleep * 1000L);
                    Thread.sleep(timeToSleep);
                    System.out.println("Message processed");

                } catch (InterruptedException e) {
                    e.printStackTrace();
                }

//                channel.basicAck(envelope.getDeliveryTag(), false);

            }
        };

        // lepsza nie zawodnosc gdy potwierdzenie jest robione po przeslaniu wiadomosci
        // jak nie bedzei akpectacji to wiadmosci nie przetwarzaja sie

        // start listening
        System.out.println("Waiting for messages...");

        // acknowledge messages automatically
        channel.basicConsume(QUEUE_NAME, true,consumer);
        // acknowledge messages manually
//        channel.basicConsume(QUEUE_NAME, false, consumer);

        // close
//        channel.close();
//        connection.close();
    }
}
