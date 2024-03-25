import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;
import java.util.regex.Pattern;
import java.util.regex.Matcher;

@RestController
public class DirectController {

    @GetMapping("/direct")
    public void direct(@RequestParam String pattern, @RequestParam String text) {
        /*
        Get the regex from the 'pattern' in the GET request,
        get the 'text' from the GET request,
        and search the 'text' with the provided regex.
        */
        Pattern compiledPattern = Pattern.compile(pattern);
        Matcher matcher = compiledPattern.matcher(text);
        matcher.find();
    }
}