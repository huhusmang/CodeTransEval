import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;
import org.xml.sax.InputSource;

import javax.xml.xpath.XPath;
import javax.xml.xpath.XPathConstants;
import javax.xml.xpath.XPathExpressionException;
import javax.xml.xpath.XPathFactory;
import java.io.StringReader;

@SpringBootApplication
public class Application {

    public static void main(String[] args) {
        SpringApplication.run(Application.class, args);
    }
}

@RestController
class XmlController {

    @GetMapping("/a")
    public String a(@RequestParam String xpath) {
        String xml = "<foo><bar></bar></foo>";
        XPathFactory xpathFactory = XPathFactory.newInstance();
        XPath xpathObj = xpathFactory.newXPath();
        try {
            InputSource source = new InputSource(new StringReader(xml));
            String expression = String.format("/foo/bar[@id='%s']", xpath);
            return (String) xpathObj.evaluate(expression, source, XPathConstants.STRING);
        } catch (XPathExpressionException e) {
            return "Error: " + e.getMessage();
        }
    }
}