import io.jsonwebtoken.Jwts;

public class JwtDemo {
    public static void main(String[] args) {
        String payload = "your.jwt.token.here"; // Replace with your JWT token
        String key = "somekey";

        // Decoding the JWT token without verifying the signature
        String decodedPayload = Jwts.parserBuilder()
                .setSigningKey(key.getBytes())
                .build()
                .parseClaimsJws(payload)
                .getBody()
                .toString();

        System.out.println("Decoded JWT payload: " + decodedPayload);
    }
}