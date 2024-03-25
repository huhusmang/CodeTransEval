import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

@SpringBootApplication
@RestController
public class Application {

    public static void main(String[] args) {
        SpringApplication.run(Application.class, args);
    }

    @GetMapping("/")
    public String index(@RequestParam String module) {
        // Importing modules dynamically as done in Python is not a direct feature in Java.
        // Java does not support eval or exec for importing modules.
        // A safer approach is to validate the input and use conditional logic or reflection based on the requirement.
        // Here, we'll demonstrate a simple validation approach to avoid executing arbitrary code.
        
        if ("3".equals(module)) {
            // Simulate importing urllib3, Java does not support dynamic imports like Python
            // In a real scenario, you would use the appropriate Java library or method based on the module
            return "Simulated importing of urllib3";
        } else {
            return "Unsupported module";
        }
    }
}