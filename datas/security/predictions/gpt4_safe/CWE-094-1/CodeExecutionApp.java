import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;
import java.util.Base64;

@SpringBootApplication
@RestController
public class CodeExecutionApp {

    public static void main(String[] args) {
        SpringApplication.run(CodeExecutionApp.class, args);
    }

    @GetMapping("/code_execution")
    public String codeExecution(@RequestParam String first_name) {
        try {
            String decodedName = new String(Base64.getDecoder().decode(first_name));
            // Safely call setname with decodedName
            setname(decodedName);
            return "Name set successfully";
        } catch (IllegalArgumentException e) {
            return "Error: Invalid input";
        }
    }

    public void setname(String first_name) {
        // Implementation to safely handle first_name
        System.out.println("Name set to: " + first_name);
    }
}