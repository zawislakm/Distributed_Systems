package sr.serialization;

import sr.proto.AddressBookProtos.Person;

import java.io.FileOutputStream;
import java.io.IOException;

public class ProtoSerialization {

    public static void main(String[] args) {
        try {
            new ProtoSerialization().testProto();
        } catch (IOException e) {
            // TODO Auto-generated catch block
            e.printStackTrace();
        }
    }

    public void testProto() throws IOException {
        Person p1 =
                Person.newBuilder()
                        .setId(123456)
                        .setName("Włodzimierz Wróblewski")
                        .setEmail("wrobel@poczta.com")
                        .addIncome(1.3f)
                        .addIncome(3f)
                        .addIncome(4f)
                        .addPhones(
                                Person.PhoneNumber.newBuilder()
                                        .setNumber("+48-12-555-4321")
                                        .setType(Person.PhoneType.HOME))
                        .addPhones(
                                Person.PhoneNumber.newBuilder()
                                        .setNumber("+48-699-989-796")
                                        .setType(Person.PhoneType.MOBILE))

                        .build();

        byte[] p1ser = null;


        long n = 1000;
        long startTime = System.nanoTime();

        System.out.println("Performing proto serialization " + n + " times...");
        for (long i = 0; i < n; i++) {
            p1ser = p1.toByteArray();
        }
        long endTime = System.nanoTime();
        double durationMillis = (double) (endTime - startTime) / 1_000_000;

        System.out.println("... finished.");
        System.out.println("Loop work for: " + durationMillis + " millisecond");

        //print data as hex values
        for (byte b : p1ser) {
            System.out.print(String.format("%02X", b));
        }

        //serialize again (only once) and write to a file
        FileOutputStream file = new FileOutputStream("person2.ser");
        file.write(p1.toByteArray());
        file.close();

    }
}
//0A1857C5826F647A696D6965727A205772C3B3626C6577736B6910C0C4071A1177726F62656C40706F637A74612E636F6D22130A0F2B34382D31322D3535352D34333231100122110A0F2B34382D3639392D3938392D3739362A0C0000803F0000404000008040
//0A1857C5826F647A696D6965727A205772C3B3626C6577736B6910C0C4071A1177726F62656C40706F637A74612E636F6D22130A0F2B34382D31322D3535352D34333231100122110A0F2B34382D3639392D3938392D373936