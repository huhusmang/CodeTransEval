import java.security.KeyPair;
import java.security.KeyPairGenerator;
import java.security.NoSuchAlgorithmException;
import java.util.Base64;

public class KeyGenerator {

    public static String createPrivateKey() {
        try {
            KeyPairGenerator keyGen = KeyPairGenerator.getInstance("RSA");
            keyGen.initialize(1024);
            KeyPair pair = keyGen.generateKeyPair();

            // Export the private key in PEM format
            byte[] privKeyBytes = pair.getPrivate().getEncoded();
            String privKeyPEM = Base64.getEncoder().encodeToString(privKeyBytes);
            return "-----BEGIN PRIVATE KEY-----\n" + privKeyPEM + "\n-----END PRIVATE KEY-----";
        } catch (NoSuchAlgorithmException e) {
            e.printStackTrace();
            return null;
        }
    }

    public static void main(String[] args) {
        String privateKey = createPrivateKey();
        System.out.println(privateKey);
    }
}