import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.bind.annotation.SessionAttribute;
import org.springframework.web.context.annotation.SessionScope;

@SpringBootApplication
@RestController
public class Application {

    private static final String aConstant = "CHANGEME1";

    public static void main(String[] args) {
        SpringApplication.run(Application.class, args);
    }

    @GetMapping("/")
    public String checkForSecretKeyValue(@SessionAttribute(required = false) Boolean logged_in) {
        return aConstant + ", " + logged_in;
    }
}