import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.servlet.mvc.support.RedirectAttributes;
import org.springframework.web.servlet.view.RedirectView;

@Controller
public class RequestController {

    @GetMapping("/processRequest")
    public RedirectView processRequest(@RequestParam("password") String password, RedirectAttributes attributes) {
        if ("myPa55word".equals(password)) {
            return new RedirectView("login");
        }
        return null; // Or redirect to another view as per requirement
    }
}