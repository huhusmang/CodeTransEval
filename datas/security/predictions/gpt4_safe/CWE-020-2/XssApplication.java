import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.util.HtmlUtils;

@SpringBootApplication
@RestController
public class XssApplication {

    public static void main(String[] args) {
        SpringApplication.run(XssApplication.class, args);
    }

    @GetMapping("/xss")
    public String xss(@RequestParam(name = "username", required = false, defaultValue = "World") String username) {
        return "Hello " + HtmlUtils.htmlEscape(username);
    }
}