import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.context.request.RequestContextHolder;
import org.springframework.web.context.request.ServletRequestAttributes;

import javax.servlet.http.HttpServletRequest;

@SpringBootApplication
@RestController
public class IpCheckApplication {

    public static void main(String[] args) {
        SpringApplication.run(IpCheckApplication.class, args);
    }

    @GetMapping("/check_ip")
    public String checkIp() {
        HttpServletRequest request = ((ServletRequestAttributes) RequestContextHolder.currentRequestAttributes()).getRequest();
        String clientIp = request.getHeader("x-forwarded-for");
        if (clientIp == null || !clientIp.startsWith("192.168.")) {
            throw new RuntimeException("ip illegal");
        }
        return "ip legal";
    }
}