import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.client.RestTemplate;

@SpringBootApplication
@RestController
public class Application {

    public static void main(String[] args) {
        SpringApplication.run(Application.class, args);
    }

    @GetMapping("/partial_ssrf")
    public String partialSsrf(@RequestParam String user_id) {
        RestTemplate restTemplate = new RestTemplate();
        String url = "https://api.example.com/user_info/" + user_id;
        return restTemplate.getForObject(url, String.class);
    }
}