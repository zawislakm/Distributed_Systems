import java.util.Random;

public class ProjectorImp implements Projector.Iface {
    @Override
    public void disply(int id) throws OverheatException {

        ProjectorDevice projector = SmarthomeImp.projectors.get(id);

        double temp = new Random().nextDouble(0, 100);
        projector.setLampTemperature(temp);

        if (projector.getLampTemperature() > 75) {
            String message = "Projector " + projector.getId() + ", overheating";
            System.out.println(message);
            throw new OverheatException(message);
        }

        System.out.println("Projector " + projector.getId() + ", displaying...");

        SmarthomeImp.projectors.put(projector.getId(), projector);
    }

    @Override
    public DeviceInfo state(int id) {
        ProjectorDevice projector = SmarthomeImp.projectors.get(id);
        String message = "Projector with id: " + projector.getId();
        return new DeviceInfo(SmarthomeDevicesType.PROJECTOR, message);
    }
}
