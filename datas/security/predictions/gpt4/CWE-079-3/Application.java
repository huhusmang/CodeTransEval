import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.servlet.ModelAndView;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;

@SpringBootApplication
@RestController
public class Application {

    public static void main(String[] args) {
        SpringApplication.run(Application.class, args);
    }

    @GetMapping("/view")
    public ModelAndView viewName(@RequestParam(name = "name", defaultValue = "") String name) throws IOException {
        String htmlContent = new String(Files.readAllBytes(Paths.get("templates/xss_shared.html")));
        htmlContent = htmlContent.replace("{{ name }}", name);
        return new ModelAndView("template").addObject("content", htmlContent);
    }
}