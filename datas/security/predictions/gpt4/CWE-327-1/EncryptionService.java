import javax.crypto.Cipher;
import javax.crypto.spec.SecretKeySpec;
import java.security.Key;

public class EncryptionService {
    private static final String SECRET_KEY = "12345678";
    private static final String ALGORITHM = "DES";
    private Cipher cipher;
    private Key key;

    public EncryptionService() throws Exception {
        key = new SecretKeySpec(SECRET_KEY.getBytes(), ALGORITHM);
        cipher = Cipher.getInstance(ALGORITHM);
    }

    public void sendEncrypted(Channel channel, String message) throws Exception {
        cipher.init(Cipher.ENCRYPT_MODE, key);
        byte[] encryptedMessage = cipher.doFinal(message.getBytes());
        channel.send(encryptedMessage);
    }

    interface Channel {
        void send(byte[] data);
    }
}