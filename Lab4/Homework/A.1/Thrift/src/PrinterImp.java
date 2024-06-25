public class PrinterImp implements Printer.Iface {

    @Override
    public void addPaper(int id, int sheetsOfPaper) {
        PrinterDevice printer = SmarthomeImp.printers.get(id);

        printer.setSheesOfPaper(printer.getSheesOfPaper() + sheetsOfPaper);

        System.out.println("Printer " + printer.getId() + ", added " + sheetsOfPaper + " sheets of paper....");

        SmarthomeImp.printers.put(printer.getId(), printer);
    }

    @Override
    public void printFile(int id, int sheetOfPaperNeeded) throws EmptyPrinterException {

        PrinterDevice printer = SmarthomeImp.printers.get(id);

        if (printer.getSheesOfPaper() < sheetOfPaperNeeded) {
            throw new EmptyPrinterException("No enough paper to print", EmptyPrinterType.NOPAPER);
        }

        int inkNeededForPaper = 1;

        if (printer.getPrinterType() == PrinterType.LASER) {
            inkNeededForPaper = 3;
        }
        if (printer.getPrinterType() == PrinterType.INKJET) {
            inkNeededForPaper = 2;
        }

        if (printer.getCartridgeLevel() < inkNeededForPaper * sheetOfPaperNeeded) {
            throw new EmptyPrinterException("Not enough ink to print", EmptyPrinterType.NOCARTRIDGE);
        }

        printer.setSheesOfPaper(printer.getSheesOfPaper() - sheetOfPaperNeeded);
        printer.setCartridgeLevel(printer.getCartridgeLevel() - inkNeededForPaper * sheetOfPaperNeeded);

        System.out.println("Printer " + printer.getId() + ", printing file....");

        SmarthomeImp.printers.put(printer.getId(), printer);
    }

    @Override
    public DeviceInfo state(int id) {
        PrinterDevice printer = SmarthomeImp.printers.get(id);
        String message = "Printer with id: " + printer.getId();
        return new DeviceInfo(SmarthomeDevicesType.PRINTER, message);
    }
}
