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
            throw new RuntimeException("DSA algorithm not available", e);
        }
    }

    public static void main(String[] args) {
        KeyPair keyPair = generatePrivateKey();
        // The private key can be retrieved from keyPair.getPrivate()
        // However, Java does not directly support exporting keys in OpenSSH format natively.
        // Additional steps would be required to export the key in such a format.
        System.out.println("Private Key: " + keyPair.getPrivate());
    }
}