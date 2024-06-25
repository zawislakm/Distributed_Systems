import sys

sys.path.append("gen-py")

from smarthome import Smarthome, Projector, Player, Printer
from smarthome.ttypes import OverheatException, EmptyPrinterException, EmptyPrinterType, InvalidArgumentException, \
    InvalidArgumentType, MusicType, DeviceInfo, SmarthomeDevicesType

from thrift.protocol import TMultiplexedProtocol
from thrift.protocol.TBinaryProtocol import TBinaryProtocol
from thrift.transport import TSocket
from thrift.transport.TTransport import TBufferedTransport

smarthomeClient = None
printerClient = None
projectorClient = None
playerClient = None

port = None


def handelOverheatException(overheatException: OverheatException):
    print("ERROR: ", end="")
    print(overheatException.__getattribute__("message"))


def handleEmptyPrinterException(emptyPrinterException: EmptyPrinterException):
    problemType = emptyPrinterException.__getattribute__("problemType")
    msg = emptyPrinterException.__getattribute__("message")

    print("ERROR: ", end="")
    if problemType == EmptyPrinterType.NOPAPER:
        print("No paper: ", msg)
    elif problemType == EmptyPrinterType.NOCARTRIDGE:
        print("No ink: ", msg)
    else:
        print("Other problem: ", msg)


def handleInvalidArgumentException(invalidArgumentException: InvalidArgumentException):
    problemType = invalidArgumentException.__getattribute__("problemType")
    msg = invalidArgumentException.__getattribute__("message")

    print("ERROR: ", end="")
    match problemType:

        case InvalidArgumentType.NOCD:
            print("No CD provided to play: ", msg)
        case InvalidArgumentType.WRONGDEVICETYPE:
            print("Device has not RADIO option: ", msg)
        case InvalidArgumentType.CDALREADYIN:
            print("This CD already in: ", msg)
        case InvalidArgumentType.WRONGRADIOSTATION:
            print("Radio station not in range: ", msg)
        case _:
            print("Other problem: ", msg)


def remove_connection(port: str):
    global smarthomeClient, printerClient, projectorClient, playerClient

    smarthomeClient = None
    printerClient = None
    projectorClient = None
    playerClient = None

    print("Connection removed on: ", port)


def connect_to_server(port: int):
    global smarthomeClient, printerClient, projectorClient, playerClient

    transport = TBufferedTransport(TSocket.TSocket('localhost', int(port)))
    transport.open()

    protocol = TBinaryProtocol(transport)

    smarthomeClient = Smarthome.Client(TMultiplexedProtocol.TMultiplexedProtocol(protocol, "Smarthome"))
    printerClient = Printer.Client(TMultiplexedProtocol.TMultiplexedProtocol(protocol, "Printer"))
    projectorClient = Projector.Client(TMultiplexedProtocol.TMultiplexedProtocol(protocol, "Projector"))
    playerClient = Player.Client(TMultiplexedProtocol.TMultiplexedProtocol(protocol, "Player"))

    print("Connection established on port: ", port)


def get_all_devices():
    global smarthomeClient

    if smarthomeClient is None:
        print("Connection with server not established")
        return

    all_devices = smarthomeClient.getAllDevices()
    print("All devices:")

    print("Projectors:")
    for projector in all_devices.projectors:
        print(projector)

    print("Printers:")
    for printer in all_devices.printers:
        print(printer)

    print("Players:")
    for player in all_devices.players:
        print(player)


def display_device_state(state: DeviceInfo):
    print(f"Device type: {SmarthomeDevicesType._VALUES_TO_NAMES[state.name]}, message: {state.message}")


def projector_loop():
    print("Working on projectors")
    while True:

        client_input = input("Enter command and id: ")
        if client_input == "exit":
            break
        if len(client_input.split(" ")) != 2:
            print("Invalid input")
            continue
        command, id = client_input.split(" ")
        id = int(id)

        match command:

            case "display":
                try:
                    projectorClient.disply(id)
                except OverheatException as ohe:
                    handelOverheatException(ohe)
            case "state":
                state = projectorClient.state(id)
                display_device_state(state)
            case "exit":
                break
            case _:
                print("Invalid command")
                continue
    print("Leaving working on projectors")


def printer_loop():
    print("Working on printers")

    while True:

        client_input = input("Enter command and id: ")
        if client_input == "exit":
            break
        if len(client_input.split(" ")) != 2:
            print("Invalid input")
            continue
        command, id = client_input.split(" ")
        id = int(id)

        match command:

            case "print":
                sheetsOfPaper = int(input("Enter size of file:"))

                try:
                    printerClient.printFile(id, sheetsOfPaper)
                except EmptyPrinterException as epe:
                    handleEmptyPrinterException(epe)
            case "add-paper":
                sheetsOfPaper = int(input("Enter sheets of paper:"))
                printerClient.addPaper(id, sheetsOfPaper)
            case "state":
                state = printerClient.state(id)
                display_device_state(state)
            case "exit":
                break
            case _:
                print("Invalid command")
                continue

    print("Leaving working on printers")


def display_CD_types():
    for number, name in MusicType._VALUES_TO_NAMES.items():
        print(f"{number} - {name}")


def player_loop():
    print("Working on players")

    while True:

        client_input = input("Enter command and id: ")
        if client_input == "exit":
            break
        if len(client_input.split(" ")) != 2:
            print("Invalid input")
            continue
        command, id = client_input.split(" ")
        id = int(id)

        match command:

            case "play":
                try:
                    playerClient.play(id)
                except InvalidArgumentException as iae:
                    handleInvalidArgumentException(iae)
            case "change-vol":
                new_volume = int(input("Enter new volume added: "))
                playerClient.changeVolume(id, new_volume)

            case "change-cd":
                display_CD_types()
                cd_type = int(input("Enter CD type: "))

                while cd_type not in MusicType._VALUES_TO_NAMES.keys():
                    print("Wrong CD type")
                    cd_type = int(input("Enter CD type: "))

                try:
                    playerClient.changeCD(id, cd_type)
                except InvalidArgumentException as iae:
                    handleInvalidArgumentException(iae)

            case "change-radio":

                new_radio_station = int(input("Enter new radio station: "))
                try:
                    playerClient.changeRadioStation(id, new_radio_station)
                except InvalidArgumentException as iae:
                    handleInvalidArgumentException(iae)
            case "state":
                state = playerClient.state(id)
                display_device_state(state)
            case "exit":
                break
            case _:
                print("Invalid command")
                continue

    print("Leaving working on players")


def enter_port_loop():
    global smarthomeClient, port

    while smarthomeClient is None:
        port = int(input("Enter port number: "))
        connect_to_server(port)


def client():
    global port
    enter_port_loop()

    while True:

        command = input("Enter command: ")

        match command:

            case "list":
                get_all_devices()
            case "change-server":
                remove_connection(port)
                enter_port_loop()
            case "projectors":
                projector_loop()
            case "printers":
                printer_loop()
            case "players":
                player_loop()
            case "exit":
                break
            case _:
                print("Invalid command")
                continue


if __name__ == "__main__":
    # os.system('cls')
    # scriptdir = os.path.dirname(os.path.abspath(sys.argv[0]))
    # sys.path.append(scriptdir)
    client()
