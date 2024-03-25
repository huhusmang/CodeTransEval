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
        restTemplate.getForObject("https://" + target + ".example.com/data/", String.class);
    }
}