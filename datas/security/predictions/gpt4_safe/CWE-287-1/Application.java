import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.bind.annotation.SessionAttribute;
import org.springframework.web.bind.annotation.SessionAttributes;
import org.springframework.web.context.request.RequestContextHolder;
import org.springframework.web.context.request.ServletRequestAttributes;

import javax.servlet.http.HttpSession;

@SpringBootApplication
@RestController
@SessionAttributes("logged_in")
public class Application {

    private static final String SECRET_KEY = "CHANGEME1";

    public static void main(String[] args) {
        SpringApplication.run(Application.class, args);
    }

    @GetMapping("/")
    public String DEB_EX(@SessionAttribute(name = "logged_in", required = false) String loggedIn) {
        HttpSession session = ((ServletRequestAttributes) RequestContextHolder.currentRequestAttributes()).getRequest().getSession(true);
        if (loggedIn == null) {
            session.setAttribute("logged_in", "value");
        }
        return SECRET_KEY + ", " + session.getAttribute("logged_in").toString();
    }
}