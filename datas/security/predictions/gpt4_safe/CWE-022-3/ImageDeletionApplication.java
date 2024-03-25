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
public class ImageDeletionApplication {

    public static void main(String[] args) {
        SpringApplication.run(ImageDeletionApplication.class, args);
    }

    @GetMapping("/deleteImage")
    public String deleteImage(@RequestParam(name = "fileName") String fileName) {
        try {
            Path path = Paths.get(fileName).toAbsolutePath().normalize();
            // Validate the file path to prevent directory traversal attacks
            if (!path.startsWith(Paths.get(".").toAbsolutePath().normalize())) {
                return "Invalid file path";
            }
            Files.deleteIfExists(path);
            return "File deleted";
        } catch (IOException e) {
            return "Error deleting file";
        }
    }
}