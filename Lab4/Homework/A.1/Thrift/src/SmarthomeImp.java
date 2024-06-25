import java.util.HashMap;
import java.util.Map;
import java.util.Random;

public class SmarthomeImp implements Smarthome.Iface {

    private int ids = 0;
    public static final Map<Integer, PlayerDevice> players = new HashMap<>();
    public static final Map<Integer, ProjectorDevice> projectors = new HashMap<>();
    public static final Map<Integer, PrinterDevice> printers = new HashMap<>();


    public PlayerDevice randomPlayer() {
        PlayerDevice player = new PlayerDevice();
        player.setId(ids++);

        int playerType = new Random().nextInt(0, 2);
        switch (playerType) {
            case 0:
                player.setPlayerType(PlayerType.NONE);
                break;
            case 1:
                player.setPlayerType(PlayerType.RADIO);
                break;
        }

        int cdType = new Random().nextInt(0, 4);

        switch (cdType) {
            case 0:
                player.setCdType(MusicType.NONE);
                break;
            case 1:
                player.setCdType(MusicType.ROCK);
                break;
            case 2:
                player.setCdType(MusicType.COUNTRY);
                break;
            case 3:
                player.setCdType(MusicType.POP);
                break;
        }

        if (player.getPlayerType() == PlayerType.RADIO && cdType >= 1){
            double radio = new Random().nextDouble(0, 100);
            player.setRadioStation(radio);
        }
        double volume = new Random().nextDouble(3, 100);
        player.setVolume(volume);

        return player;
    }

    public PrinterDevice randomPrinter() {
        PrinterDevice printer = new PrinterDevice();
        printer.setId(ids++);

        double cartridgeLevel = new Random().nextDouble(3, 100);
        int paper = new Random().nextInt(3, 100);
        printer.setSheesOfPaper(paper);
        printer.setCartridgeLevel(cartridgeLevel);
        if (cartridgeLevel > 50) {
            printer.setPrinterType(PrinterType.INKJET);
        } else {
            printer.setPrinterType(PrinterType.LASER);
        }

        return printer;
    }

    public ProjectorDevice randomProjector() {
        ProjectorDevice projector = new ProjectorDevice();
        projector.setId(ids++);

        double temp = new Random().nextDouble(3, 100);
        projector.setLampTemperature(temp);

        return projector;
    }


    public void randomDevices() {

        for (int i = 0; i < 5; i++) {

            PlayerDevice player = randomPlayer();
            players.put(player.getId(), player);

            ProjectorDevice projector = randomProjector();
            projectors.put(projector.getId(), projector);

            PrinterDevice printer = randomPrinter();
            printers.put(printer.getId(), printer);
        }
    }


    @Override
    public SmarthomeDevices getAllDevices() {
        System.out.println("Server listing all devices...");
        SmarthomeDevices devices = new SmarthomeDevices();
        devices.setPlayers(players.values().stream().toList());
        devices.setPrinters(printers.values().stream().toList());
        devices.setProjectors(projectors.values().stream().toList());

        return devices;
    }
}
