import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;
import org.w3c.dom.Document;
import org.w3c.dom.NodeList;
import org.xml.sax.InputSource;

import javax.annotation.PostConstruct;
import javax.xml.parsers.DocumentBuilder;
import javax.xml.parsers.DocumentBuilderFactory;
import javax.xml.xpath.XPath;
import javax.xml.xpath.XPathConstants;
import javax.xml.xpath.XPathFactory;
import java.io.StringReader;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.List;

@SpringBootApplication
@RestController
public class UserLocationsApplication {

    private Document xmlDocument;

    public static void main(String[] args) {
        SpringApplication.run(UserLocationsApplication.class, args);
    }

    @PostConstruct
    public void init() {
        try {
            String xmlContent = Files.readString(Paths.get("users.xml"));
            DocumentBuilderFactory factory = DocumentBuilderFactory.newInstance();
            DocumentBuilder builder = factory.newDocumentBuilder();
            xmlDocument = builder.parse(new InputSource(new StringReader(xmlContent)));
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    @GetMapping("/user")
    public List<String> userLocations(@RequestParam String username) {
        List<String> locations = new ArrayList<>();
        try {
            XPath xPath = XPathFactory.newInstance().newXPath();
            String expression = String.format("/users/user[@name='%s']/location", username);
            NodeList nodeList = (NodeList) xPath.evaluate(expression, xmlDocument, XPathConstants.NODESET);
            for (int i = 0; i < nodeList.getLength(); i++) {
                locations.add(nodeList.item(i).getTextContent());
            }
        } catch (Exception e) {
            e.printStackTrace();
        }
        return locations;
    }
}