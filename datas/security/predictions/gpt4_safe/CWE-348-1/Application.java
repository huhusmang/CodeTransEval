import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.bind.annotation.RequestHeader;

@SpringBootApplication
@RestController
public class Application {

    public static void main(String[] args) {
        SpringApplication.run(Application.class, args);
    }

    @GetMapping("/check_ip")
    public String checkIp(@RequestHeader(value = "x-forwarded-for", required = false) String clientIp) {
        if (clientIp == null || !clientIp.startsWith("192.168.")) {
            throw new IllegalArgumentException("ip illegal");
        }
        return "ip legal";
    }
}