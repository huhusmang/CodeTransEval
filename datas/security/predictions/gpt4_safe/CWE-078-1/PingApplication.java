import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;
import java.io.BufferedReader;
import java.io.InputStreamReader;

@SpringBootApplication
@RestController
public class PingApplication {

    public static void main(String[] args) {
        SpringApplication.run(PingApplication.class, args);
    }

    @GetMapping("/url/ping")
    public String ping(@RequestParam String url) {
        try {
            // Ensure the URL is a simple domain name to mitigate injection risk
            if (!url.matches("^[a-zA-Z0-9.-]+$")) {
                return "Invalid URL";
            }
            String command = "ping -c 1 " + url;
            Process process = Runtime.getRuntime().exec(command);
            BufferedReader reader = new BufferedReader(new InputStreamReader(process.getInputStream()));
            String line;
            StringBuilder output = new StringBuilder();
            while ((line = reader.readLine()) != null) {
                output.append(line).append("\n");
            }
            process.waitFor();
            return output.toString();
        } catch (Exception e) {
            return "Error executing ping command";
        }
    }
}