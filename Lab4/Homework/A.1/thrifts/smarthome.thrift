exception OverheatException{
    1: string message
}

enum InvalidArgumentType{
	NOCD = 1,
	WRONGDEVICETYPE = 2,
	CDALREADYIN = 3,
	WRONGRADIOSTATION = 4
}

exception InvalidArgumentException{
    1: string message
    2: InvalidArgumentType problemType
}

enum EmptyPrinterType{
    NOPAPER = 1
    NOCARTRIDGE = 2,
}

exception EmptyPrinterException{
    1: string message
    2: EmptyPrinterType problemType
}

enum SmarthomeDevicesType{
    PLAYER = 1,
    PRINTER = 2,
    PROJECTOR = 3
}


struct DeviceInfo {
    1: SmarthomeDevicesType name
    2: string message
}

service Device {
    DeviceInfo state(1: i32 id)
}

enum MusicType{
    NONE = 0,
    ROCK = 1,
    COUNTRY = 2,
    POP = 3,
}

enum PlayerType{
	NONE = 0,
	RADIO = 1
}

struct PlayerDevice{
    1: i32 id
    2: PlayerType playerType;
    3: optional MusicType cdType
    4: optional double radioStation
    5: double volume
}

service Player extends Device{
    void play(1: i32 id ) throws (1:InvalidArgumentException ex) // no CD provided
    void changeVolume(1: i32 id, 2: double volumeAdded)
    void changeCD(1:i32  id, 2: MusicType type) throws (1: InvalidArgumentException ex) //no existing CD
    void changeRadioStation(1: i32 id, 2: double radioStation ) throws (1: InvalidArgumentException ex)// radio station not in range
}


enum PrinterType{
    LASER =1
    INKJET = 2
}

struct PrinterDevice{
    1: i32 id
    2: double cartridgeLevel
    3: PrinterType printerType
    4: i32 sheesOfPaper
}

service Printer extends Device {
    void addPaper(1:i32 id, 2: i32 sheetsOfPaper)
    void printFile(1:i32 id, 2: i32 sheetOfPaperNeeded) throws (1: EmptyPrinterException ex)// no ink or papaer in printer
}

struct ProjectorDevice {
    1: i32 id
    2: double lampTemperature
}

service Projector extends Device{
    void disply(1: i32 id) throws (1: OverheatException ex) // lamp can overheat
}

struct SmarthomeDevices {
    1: list<ProjectorDevice> projectors
    2: list<PrinterDevice> printers
    3: list<PlayerDevice> players
}

service Smarthome{
    SmarthomeDevices getAllDevices()
}
