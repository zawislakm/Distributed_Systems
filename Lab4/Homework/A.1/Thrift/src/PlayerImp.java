public class PlayerImp implements Player.Iface {
    @Override
    public void play(int id) throws InvalidArgumentException {
        PlayerDevice player = SmarthomeImp.players.get(id);

        if (player.getCdType() == MusicType.NONE) {
            throw new InvalidArgumentException("No CD inserted", InvalidArgumentType.NOCD);
        }

        System.out.println("Player " + player.getId() + ", playing....");

        SmarthomeImp.players.put(player.getId(), player);
    }

    @Override
    public void changeVolume(int id, double volumeAdded) {
        PlayerDevice player = SmarthomeImp.players.get(id);

        if (player.getVolume() + volumeAdded > 100) {
            player.setVolume(100);
        } else if (player.getVolume() + volumeAdded < 0) {
            player.setVolume(0);
        } else {
            player.setVolume(player.getVolume() + volumeAdded);
        }

        System.out.println("Player " + player.getId() + ", changing volume....");

        SmarthomeImp.players.put(player.getId(), player);

    }


    @Override
    public void changeCD(int id, MusicType type) throws InvalidArgumentException {

        PlayerDevice player = SmarthomeImp.players.get(id);


        if (player.getCdType() == type) {
            throw new InvalidArgumentException("CD already inserted", InvalidArgumentType.CDALREADYIN);
        }

        player.setCdType(type);

        System.out.println("Player " + player.getId() + ", changing CD....");

        SmarthomeImp.players.put(player.getId(), player);

    }

    @Override
    public void changeRadioStation(int id, double radioStation) throws InvalidArgumentException {

        PlayerDevice player = SmarthomeImp.players.get(id);

        if (player.getPlayerType() != PlayerType.RADIO) {
            throw new InvalidArgumentException("Player has no RADIO option", InvalidArgumentType.WRONGDEVICETYPE);
        }

        if (radioStation < 0 || radioStation > 100) {
            throw new InvalidArgumentException("Invalid radio station", InvalidArgumentType.WRONGRADIOSTATION);
        }
        player.setRadioStation(radioStation);

        System.out.println("Player " + player.getId() + ", changing radio station....");

        SmarthomeImp.players.put(player.getId(), player);

    }

    @Override
    public DeviceInfo state(int id) {
        PlayerDevice player = SmarthomeImp.players.get(id);
        String message = "Player with id: " + player.getId();
        return new DeviceInfo(SmarthomeDevicesType.PLAYER, message);
    }
}
