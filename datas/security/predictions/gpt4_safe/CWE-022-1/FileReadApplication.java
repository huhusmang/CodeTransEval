import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;

@SpringBootApplication
@RestController
public class FileReadApplication {

    public static void main(String[] args) {
        SpringApplication.run(FileReadApplication.class, args);
    }

    @GetMapping("/read")
    public String read(@RequestParam String filename) {
        String safeDir = "/safe/";
        Path filePath = Paths.get(safeDir, filename).normalize().toAbsolutePath();

        // Ensure the requested file is within the safe directory
        if (!filePath.startsWith(Paths.get(safeDir))) {
            return "Access Denied";
        }

        try {
            return Files.readString(filePath);
        } catch (IOException e) {
            return "Error reading file: " + e.getMessage();
        }
    }
}