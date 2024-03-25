import java.security.KeyPair;
import java.security.KeyPairGenerator;
import java.security.NoSuchAlgorithmException;
import java.util.Base64;

public class Main {

    public static void main(String[] args) {
        try {
            String privateKey = createPrivateKey();
            System.out.println(privateKey);
        } catch (NoSuchAlgorithmException e) {
            e.printStackTrace();
        }
    }

    public static String createPrivateKey() throws NoSuchAlgorithmException {
        KeyPairGenerator keyGen = KeyPairGenerator.getInstance("RSA");
        keyGen.initialize(1024);
        KeyPair pair = keyGen.generateKeyPair();
        byte[] privKeyBytes = pair.getPrivate().getEncoded();
        return "-----BEGIN PRIVATE KEY-----\n" + Base64.getEncoder().encodeToString(privKeyBytes) + "\n-----END PRIVATE KEY-----";
    }
}