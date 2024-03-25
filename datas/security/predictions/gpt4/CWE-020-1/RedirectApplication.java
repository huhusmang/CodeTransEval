import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.servlet.view.RedirectView;

import java.util.regex.Pattern;

@SpringBootApplication
@RestController
public class RedirectApplication {

    public static void main(String[] args) {
        SpringApplication.run(RedirectApplication.class, args);
    }

    @GetMapping("/redirect_to_target")
    public RedirectView redirectToTarget(@RequestParam(name = "target") String target) {
        if (Pattern.matches("^https?://example\\.com/", target)) {
            return new RedirectView(target);
        }
        return null; // Or handle invalid target URL appropriately
    }
}