import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestHeader;
import org.springframework.web.bind.annotation.RestController;

@SpringBootApplication
@RestController
public class Application {

    public static void main(String[] args) {
        SpringApplication.run(Application.class, args);
    }

    @GetMapping("/check_ip")
    public String checkIp(@RequestHeader(value = "x-forwarded-for", required = false) String clientIp) {
        if (!"127.0.0.1".equals(clientIp)) {
            throw new SecurityException("ip illegal");
        }
        return "ip legal";
    }
}