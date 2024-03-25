import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.servlet.view.RedirectView;
import org.springframework.stereotype.Controller;

@Controller
public class RedirectController {

    @GetMapping("/flask_redirect")
    public RedirectView flaskRedirect(@RequestParam("next") String url) {
        // Ensure the URL is safe to redirect to, to prevent open redirect vulnerabilities
        // This is a basic check. In a real application, more sophisticated validation is needed.
        if (url != null && (url.startsWith("http://") || url.startsWith("https://"))) {
            return new RedirectView(url);
        } else {
            // Redirect to a safe default if the URL is not valid
            return new RedirectView("/");
        }
    }
}