import java.security.KeyPair;
import java.security.KeyPairGenerator;
import java.security.NoSuchAlgorithmException;

public class KeyGenerator {

    public static KeyPair generatePrivateKey() {
        try {
            KeyPairGenerator keyGen = KeyPairGenerator.getInstance("DSA");
            keyGen.initialize(1024);
            return keyGen.generateKeyPair();
        } catch (NoSuchAlgorithmException e) {
            e.printStackTrace();
            return null;
        }
    }

    public static void main(String[] args) {
        KeyPair keyPair = generatePrivateKey();
        if (keyPair != null) {
            System.out.println("Private key generated.");
        } else {
            System.out.println("Failed to generate private key.");
        }
    }
}