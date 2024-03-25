import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.util.HtmlUtils;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;

@SpringBootApplication
@RestController
public class XssExampleApplication {

    public static void main(String[] args) {
        SpringApplication.run(XssExampleApplication.class, args);
    }

    @GetMapping("/view")
    public String viewName(@RequestParam(name = "name", defaultValue = "") String name) {
        String htmlContent;
        try {
            htmlContent = Files.readString(Paths.get("templates/xss_shared.html"));
        } catch (IOException e) {
            return "Error reading template file.";
        }
        // Ensure the name is escaped to prevent XSS
        String safeName = HtmlUtils.htmlEscape(name);
        return htmlContent.replace("{{ name }}", safeName);
    }
}