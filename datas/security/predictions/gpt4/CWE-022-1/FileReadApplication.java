import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;

@SpringBootApplication
@RestController
public class FileReadApplication {

    public static void main(String[] args) {
        SpringApplication.run(FileReadApplication.class, args);
    }

    @GetMapping("/read")
    public String read(@RequestParam String filename) {
        String safeDir = "/safe/";
        Path filePath = Path.of(safeDir, filename);

        try {
            return Files.readString(filePath);
        } catch (IOException e) {
            return "Error reading file: " + e.getMessage();
        }
    }
}