import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;
import java.util.Base64;

@SpringBootApplication
@RestController
public class Application {

    public static void main(String[] args) {
        SpringApplication.run(Application.class, args);
    }

    @GetMapping("/code_execution")
    public void codeExecution(@RequestParam String first_name) {
        String decodedFirstName = new String(Base64.getDecoder().decode(first_name));
        // call setname on first_name
        try {
            this.getClass().getDeclaredMethod("setname", String.class).invoke(this, decodedFirstName);
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    public void setname(String first_name) {
        // Placeholder method
    }
}