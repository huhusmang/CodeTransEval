import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.servlet.view.RedirectView;

@SpringBootApplication
@RestController
public class Application {

    public static void main(String[] args) {
        SpringApplication.run(Application.class, args);
    }

    @GetMapping("/")
    public RedirectView hello(@RequestParam(name = "target", defaultValue = "") String target) {
        // Ensure the redirect URL is safe to prevent open redirects
        if (!target.startsWith("http://") && !target.startsWith("https://")) {
            target = "/";
        }
        return new RedirectView(target);
    }
}