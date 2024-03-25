import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;

import java.io.ByteArrayInputStream;
import java.io.ObjectInput;
import java.io.ObjectInputStream;

@SpringBootApplication
@RestController
public class DeserializationApplication {

    public static void main(String[] args) {
        SpringApplication.run(DeserializationApplication.class, args);
    }

    @PostMapping("/")
    public Object deserialize(@RequestBody byte[] pickled) {
        try (ByteArrayInputStream bis = new ByteArrayInputStream(pickled);
             ObjectInput in = new ObjectInputStream(bis)) {
            return in.readObject();
        } catch (Exception e) {
            throw new RuntimeException("Deserialization error", e);
        }
    }
}