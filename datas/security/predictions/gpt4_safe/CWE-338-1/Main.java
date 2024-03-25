import java.security.SecureRandom;

public class Main {

    public static void main(String[] args) {
        System.out.println(generatePassword());
    }

    public static double generatePassword() {
        SecureRandom random = new SecureRandom();
        return random.nextDouble();
    }
}