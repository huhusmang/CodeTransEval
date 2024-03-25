import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;
import java.util.regex.Pattern;
import java.util.regex.Matcher;

@SpringBootApplication
@RestController
public class RegexApplication {

    public static void main(String[] args) {
        SpringApplication.run(RegexApplication.class, args);
    }

    @GetMapping("/direct")
    public String direct(@RequestParam String pattern, @RequestParam String text) {
        try {
            Pattern compiledPattern = Pattern.compile(pattern);
            Matcher matcher = compiledPattern.matcher(text);
            if (matcher.find()) {
                return "Match found";
            } else {
                return "No match found";
            }
        } catch (Exception e) {
            return "Error: " + e.getMessage();
        }
    }
}