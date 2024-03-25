import io.jsonwebtoken.Jwts;

public class JwtDecoder {
    public static void main(String[] args) {
        String payload = "your.jwt.token.here";
        String key = "somekey";

        // Decode JWT payload without verifying the signature
        String decodedPayload = Jwts.parserBuilder()
                .setSigningKey(key.getBytes())
                .build()
                .parseClaimsJws(payload)
                .getBody()
                .toString();

        System.out.println(decodedPayload);
    }
}