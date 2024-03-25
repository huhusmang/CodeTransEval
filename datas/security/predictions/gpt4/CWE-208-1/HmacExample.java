import javax.crypto.Mac;
import javax.crypto.spec.SecretKeySpec;
import java.security.InvalidKeyException;
import java.security.NoSuchAlgorithmException;

public class HmacExample {

    private static final String key = "e179017a-62b0-4996-8a38-e91aa9f1";
    private static final String msg = "Test";

    public static byte[] sign(String preKey, String imsg, String alg) {
        try {
            SecretKeySpec keySpec = new SecretKeySpec(preKey.getBytes(), alg);
            Mac mac = Mac.getInstance(alg);
            mac.init(keySpec);
            return mac.doFinal(imsg.getBytes());
        } catch (NoSuchAlgorithmException | InvalidKeyException e) {
            throw new RuntimeException(e);
        }
    }

    public static boolean verify(String msg, byte[] sig) {
        return java.util.Arrays.equals(sig, sign(key, msg, "HmacSHA256"));
    }

    public static void main(String[] args) {
        byte[] signature = sign(key, msg, "HmacSHA256");
        System.out.println(verify(msg, signature)); // Should print true
    }
}