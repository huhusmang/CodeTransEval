import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.servlet.mvc.support.RedirectAttributes;

@Controller
public class RequestController {

    @GetMapping("/processRequest")
    public String processRequest(@RequestParam(name = "password") String password, RedirectAttributes redirectAttributes) {
        if ("myPa55word".equals(password)) {
            return "redirect:/login";
        }
        return "errorPage"; // Assuming there's an error page to handle incorrect cases
    }
}