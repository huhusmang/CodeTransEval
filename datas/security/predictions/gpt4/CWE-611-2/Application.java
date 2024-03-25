import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.multipart.MultipartFile;
import org.w3c.dom.Document;
import org.w3c.dom.Element;
import org.xml.sax.InputSource;

import javax.xml.parsers.DocumentBuilder;
import javax.xml.parsers.DocumentBuilderFactory;
import java.io.StringReader;

@SpringBootApplication
@RestController
public class Application {

    public static void main(String[] args) {
        SpringApplication.run(Application.class, args);
    }

    @PostMapping("/upload")
    public String upload(@RequestParam("xml") MultipartFile xml) {
        try {
            DocumentBuilderFactory factory = DocumentBuilderFactory.newInstance();
            DocumentBuilder builder = factory.newDocumentBuilder();
            Document doc = builder.parse(new InputSource(new StringReader(new String(xml.getBytes()))));
            Element root = doc.getDocumentElement();
            String userid = root.getElementsByTagName("userid").item(0).getTextContent();
            String password = root.getElementsByTagName("password").item(0).getTextContent();
            if (checkPassword(userid, password)) {
                return "OK";
            } else {
                return "ERROR";
            }
        } catch (Exception e) {
            return "ERROR";
        }
    }

    private boolean checkPassword(String userid, String password) {
        // Implement password check logic here
        return false;
    }
}