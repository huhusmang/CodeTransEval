import javax.crypto.Cipher;
import javax.crypto.spec.SecretKeySpec;
import java.security.Key;
import java.nio.charset.StandardCharsets;

public class EncryptionService {

    private static final String SECRET_KEY = "12345678";
    private static final String ALGORITHM = "DES";
    private Cipher cipher;
    private Key key;

    public EncryptionService() throws Exception {
        key = new SecretKeySpec(SECRET_KEY.getBytes(StandardCharsets.UTF_8), ALGORITHM);
        cipher = Cipher.getInstance(ALGORITHM);
    }

    public byte[] encrypt(String message) throws Exception {
        cipher.init(Cipher.ENCRYPT_MODE, key);
        return cipher.doFinal(message.getBytes(StandardCharsets.UTF_8));
    }

    // Assuming Channel is an interface with a send method. You need to implement this interface based on your specific requirements.
    public void sendEncrypted(Channel channel, String message) throws Exception {
        byte[] encryptedMessage = encrypt(message);
        channel.send(encryptedMessage);
    }

    // Example Channel interface
    public interface Channel {
        void send(byte[] data);
    }
}