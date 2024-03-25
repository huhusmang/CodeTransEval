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
        try {
            // Dynamically loading the class based on the module parameter
            Class.forName("java.net.http.HttpClient" + module);
            return "Module imported";
        } catch (ClassNotFoundException e) {
            return "Module not found";
        }
    }
}