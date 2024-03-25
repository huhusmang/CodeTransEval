import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestHeader;
import org.springframework.web.bind.annotation.RestController;

@SpringBootApplication
@RestController
public class Application {

    public static void main(String[] args) {
        SpringApplication.run(Application.class, args);
    }

    @GetMapping("/bad")
    public String bad(@RequestHeader(value = "X-Auth-Token", required = false) String secret) {
        if ("token".equals(secret)) {
            throw new RuntimeException("bad token");
        }
        return "bad";
    }
}