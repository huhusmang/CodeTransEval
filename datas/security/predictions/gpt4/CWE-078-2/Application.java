import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import java.io.BufferedReader;
import java.io.InputStreamReader;

@SpringBootApplication
@RestController
public class Application {

    public static void main(String[] args) {
        SpringApplication.run(Application.class, args);
    }

    @GetMapping("/ls")
    public String ls(@RequestParam(value = "dirname", defaultValue = ".") String dirname) {
        try {
            ProcessBuilder builder = new ProcessBuilder();
            builder.command("sh", "-c", "ls " + dirname);
            Process process = builder.start();
            StringBuilder output = new StringBuilder();
            BufferedReader reader = new BufferedReader(new InputStreamReader(process.getInputStream()));
            String line;
            while ((line = reader.readLine()) != null) {
                output.append(line).append("\n");
            }
            int exitVal = process.waitFor();
            if (exitVal == 0) {
                return output.toString();
            } else {
                return "Error in executing command";
            }
        } catch (Exception e) {
            e.printStackTrace();
            return "Exception occurred";
        }
    }
}