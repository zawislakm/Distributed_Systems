import java.io.*;
import java.io.InputStreamReader;
import java.util.Scanner;

// https://github.com/grpc/grpc-java/tree/master/examples/example-reflection

public class Client {

    public static String readFileToString(String path) throws IOException {
        File file = new File(path);
        BufferedReader reader = new BufferedReader(new FileReader(file));
        StringBuilder stringBuilder = new StringBuilder();
        String line;
        while ((line = reader.readLine()) != null) {
            stringBuilder.append(line);
        }
        reader.close();
        return stringBuilder.toString();
    }

    public static String readProcessOutput(Process process) throws IOException {
        BufferedReader reader = new BufferedReader(new InputStreamReader(process.getInputStream()));
        StringBuilder stringBuilder = new StringBuilder();
        String line;
        while ((line = reader.readLine()) != null) {
            stringBuilder.append(line + " ");
        }
        return stringBuilder.toString();
    }

    public static void listMethods() throws IOException {

        String[] getMethodsCreate = {
                "grpcurl",
                "-plaintext",
                "localhost:50051",
                "list",
                "StoreService"
        };

        Process getMethodsProcess = new ProcessBuilder(getMethodsCreate)
                .redirectErrorStream(true)
                .start();

        String response = readProcessOutput(getMethodsProcess);
        System.out.print("ListMethods: ");
        System.out.println(response);
    }

    public static void newOrder() throws IOException {
        String path = "src/NewOrder.json";
        String request = readFileToString(path);

        String[] newOrderCreate = {
                "grpcurl",
                "-plaintext",
                "-d", request,
                "localhost:50051",
                "StoreService/CreateOrder"
        };
        Process newOrderProcess = new ProcessBuilder(newOrderCreate)
                .redirectErrorStream(true)
                .start();

        String response = readProcessOutput(newOrderProcess);
        System.out.print("NewOrder: ");
        System.out.println(response);
    }

    public static void getOrder() throws IOException {
        String path = "src/GetOrder.json";
        String request = readFileToString(path);

        String[] getOrderCreate = {
                "grpcurl",
                "-plaintext",
                "-d", request,
                "localhost:50051",
                "StoreService/GetOrder"
        };
        Process getOrderProcess = new ProcessBuilder(getOrderCreate)
                .redirectErrorStream(true)
                .start();

        System.out.print("GetOrder: ");
        String response = readProcessOutput(getOrderProcess);
        System.out.println(response);

    }

    public static void addItemsToOrder() throws IOException {
        String path = "src/AddToOrder.json";
        String request = readFileToString(path);

        String[] addToOrderCreate = {
                "grpcurl",
                "-plaintext",
                "-d", request,
                "localhost:50051",
                "StoreService/AddItemsToOrder"
        };

        Process addToOrderProcess = new ProcessBuilder(addToOrderCreate)
                .redirectErrorStream(true)
                .start();
        System.out.print("AddItemsToOrder: ");
        String response = readProcessOutput(addToOrderProcess);
        System.out.println(response);
    }

    public static void main(String[] args) throws IOException {


        Scanner scanner = new Scanner(System.in);
        while (true){
            System.out.print("Enter command: ");
            String command = scanner.nextLine();

            switch (command){
                case "list":
                    listMethods();
                    break;
                case "newOrder":
                    newOrder();
                    break;
                case "getOrder":
                    getOrder();
                    break;
                case "addOrder":
                    addItemsToOrder();
                    break;
                case "exit":
                    System.out.println("exiting...");
                    System.exit(0);
                    break;
                default:
                    System.out.println("Invalid command");
                    break;
            }

        }

    }
}
