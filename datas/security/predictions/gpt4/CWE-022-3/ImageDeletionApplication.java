import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;

@SpringBootApplication
@RestController
public class ImageDeletionApplication {

    public static void main(String[] args) {
        SpringApplication.run(ImageDeletionApplication.class, args);
    }

    @GetMapping("/deleteImage")
    public String deleteImage(@RequestParam String fileName) {
        try {
            Files.deleteIfExists(Paths.get(fileName));
            return "File deleted";
        } catch (IOException e) {
            e.printStackTrace();
            return "Error deleting file";
        }
    }
}