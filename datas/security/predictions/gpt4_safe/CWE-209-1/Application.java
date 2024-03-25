import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

@SpringBootApplication
@RestController
public class Application {

    private static final Logger logger = LoggerFactory.getLogger(Application.class);

    public static void main(String[] args) {
        SpringApplication.run(Application.class, args);
    }

    @GetMapping("/bad")
    public String serverBad() {
        try {
            doComputation();
        } catch (Exception e) {
            // Log the exception to avoid exposing sensitive details
            logger.error("An error occurred", e);
            // Return a generic error message
            return "An error occurred. Please try again later.";
        }
        return "This should never be reached.";
    }

    private void doComputation() throws Exception {
        throw new Exception("Secret info");
    }
}