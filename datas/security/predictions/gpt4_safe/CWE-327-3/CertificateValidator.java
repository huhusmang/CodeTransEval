import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;

public class CertificateValidator {

    public static boolean certificateMatchesKnownHash(byte[] certificate, String knownHash) {
        try {
            MessageDigest md = MessageDigest.getInstance("MD5");
            byte[] digest = md.digest(certificate);
            StringBuilder sb = new StringBuilder();
            for (byte b : digest) {
                sb.append(String.format("%02x", b));
            }
            return sb.toString().equals(knownHash);
        } catch (NoSuchAlgorithmException e) {
            throw new RuntimeException("MD5 algorithm not found", e);
        }
    }
}