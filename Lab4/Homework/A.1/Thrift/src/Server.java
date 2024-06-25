import org.apache.thrift.TMultiplexedProcessor;
import org.apache.thrift.protocol.TBinaryProtocol;
import org.apache.thrift.protocol.TProtocolFactory;
import org.apache.thrift.server.TServer;
import org.apache.thrift.server.TSimpleServer;
import org.apache.thrift.transport.TServerSocket;
import org.apache.thrift.transport.TServerTransport;

import java.io.BufferedReader;
import java.io.InputStreamReader;

public class Server {


    public static void main(String[] args) {

        try {
            System.out.println("Enter the port number: ");
            BufferedReader reader = new BufferedReader(new InputStreamReader(System.in));
            String portStr = reader.readLine();
            int port = Integer.parseInt(portStr);
            Runnable multiplex = new Runnable() {
                public void run() {
                    multiplex(port);
                }
            };
            new Thread(multiplex).start();
        } catch (Exception x) {
            x.printStackTrace();
        }
    }

    public static void multiplex(int port) {
        try {
            SmarthomeImp smarthome = new SmarthomeImp();
            smarthome.randomDevices();

            Smarthome.Processor<SmarthomeImp> smarthomeProcessor = new Smarthome.Processor<>(smarthome);
            Player.Processor<PlayerImp> playerProcessor = new Player.Processor<>(new PlayerImp());
            Projector.Processor<ProjectorImp> projectorProcessor = new Projector.Processor<>(new ProjectorImp());
            Printer.Processor<PrinterImp> printerProcessor = new Printer.Processor<>(new PrinterImp());


            TServerTransport serverTransport = new TServerSocket(port);

            TProtocolFactory protocolFactory = new TBinaryProtocol.Factory();

            TMultiplexedProcessor multiplex = new TMultiplexedProcessor();

            multiplex.registerProcessor("Smarthome", smarthomeProcessor);
            multiplex.registerProcessor("Printer", printerProcessor);
            multiplex.registerProcessor("Projector", projectorProcessor);
            multiplex.registerProcessor("Player", playerProcessor);

            TServer server = new TSimpleServer(new TServer.Args(serverTransport).protocolFactory(protocolFactory).processor(multiplex));

            System.out.println("Starting the multiplex server...");
            server.serve();
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
