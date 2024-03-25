import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RestController;
import java.util.Base64;

@SpringBootApplication
public class DeserializationApplication {

    public static void main(String[] args) {
        SpringApplication.run(DeserializationApplication.class, args);
    }
}

@RestController
class DeserializationController {

    @PostMapping("/{object}")
    public Object deserialize(@PathVariable("object") String object) throws Exception {
        byte[] data = Base64.getDecoder().decode(object);
        try (var ois = new java.io.ObjectInputStream(new java.io.ByteArrayInputStream(data))) {
            return ois.readObject();
        }
    }
}