import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.client.RestTemplate;

@SpringBootApplication
@RestController
public class SsrfApplication {

    public static void main(String[] args) {
        SpringApplication.run(SsrfApplication.class, args);
    }

    @GetMapping("/full_ssrf")
    public void fullSsrf(@RequestParam String target) {
        RestTemplate restTemplate = new RestTemplate();
        String url = "https://" + sanitizeTarget(target) + ".example.com/data/";
        restTemplate.getForObject(url, String.class);
    }

    // Basic sanitization to prevent SSRF attacks
    private String sanitizeTarget(String target) {
        return target.replaceAll("[^\\w.-]", "");
    }
}