import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.multipart.MultipartFile;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;

import java.util.regex.Pattern;

@SpringBootApplication
@RestController
public class Application {

    public static void main(String[] args) {
        SpringApplication.run(Application.class, args);
    }

    @RequestMapping(value = "/upload", method = RequestMethod.GET)
    public String upload(@RequestParam("username") String username, @RequestParam("attachment") MultipartFile attachment) {
        try {
            String filename = attachment.getOriginalFilename();
            if (filename != null && Pattern.compile(Pattern.quote(username)).matcher(filename).find()) {
                return "Username found in filename";
            } else {
                return "Username not found in filename";
            }
        } catch (Exception e) {
            return "An error occurred";
        }
    }
}