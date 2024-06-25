import com.rabbitmq.client.Channel;
import com.rabbitmq.client.Connection;
import com.rabbitmq.client.ConnectionFactory;

import java.io.BufferedReader;
import java.io.InputStreamReader;

public class Z1_Producer {

    public static void main(String[] argv) throws Exception {

        // info
        System.out.println("Z1 PRODUCER");

        // connection & channel
        ConnectionFactory factory = new ConnectionFactory();
        factory.setHost("localhost");
        Connection connection = factory.newConnection();
        Channel channel = connection.createChannel();

        // queue
        String QUEUE_NAME = "queue1";
        channel.queueDeclare(QUEUE_NAME, false, false, false, null);

        // zad1a
        // producer (publish msg)
        while (true) {
            // read msg
            BufferedReader br =
                    new BufferedReader(new InputStreamReader(System.in));
            System.out.println("Enter message: ");
            String message = br.readLine();

            // break condition
            if (message.equals("exit")) {
                break;
            }

            // publish
            channel.basicPublish("", QUEUE_NAME, null, message.getBytes());
            System.out.println("Sent: " + message);
        }



        //zad1b

        int timeout = 1000;
        final int SHORT_TIMEOUT = 1000;
        final int LONG_TIMEOUT = 5000;

        for (int i = 0; i < 10; i++) {

            channel.basicPublish("", QUEUE_NAME, null, String.valueOf(
                    timeout).getBytes());
            System.out.println("Sent: " + timeout + " ms");

            if (timeout == SHORT_TIMEOUT) {
                timeout = LONG_TIMEOUT;
            } else {
                timeout = SHORT_TIMEOUT;
            }
        }


        // close
        channel.close();
        connection.close();
    }
}
