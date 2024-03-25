import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;
import java.util.regex.Pattern;
import java.util.regex.Matcher;

@RestController
public class DirectController {

    @GetMapping("/direct")
    public boolean direct(@RequestParam String pattern, @RequestParam String text) {
        try {
            Pattern compiledPattern = Pattern.compile(pattern);
            Matcher matcher = compiledPattern.matcher(text);
            return matcher.find();
        } catch (Exception e) {
            // Log the exception or handle it as per your application's requirement
            return false;
        }
    }
}