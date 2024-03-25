import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import javax.servlet.http.HttpSession;
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.PreparedStatement;

@SpringBootApplication
@RestController
public class StockApplication {

    public static void main(String[] args) {
        SpringApplication.run(StockApplication.class, args);
    }

    @PostMapping("/buy_order")
    public String buyStock(@RequestParam String stock_name, @RequestParam String stock_quantity, HttpSession session) {
        String username = (String) session.getAttribute("username");
        try {
            Connection conn = DriverManager.getConnection("jdbc:mysql://localhost:3306/db", "root", "root");
            String query = "INSERT INTO buy_order (stock_name, stock_quantity, username) VALUES (?, ?, ?)";
            PreparedStatement preparedStmt = conn.prepareStatement(query);
            preparedStmt.setString(1, stock_name);
            preparedStmt.setString(2, stock_quantity);
            preparedStmt.setString(3, username);
            preparedStmt.execute();
            conn.close();
        } catch (Exception e) {
            e.printStackTrace();
            return "Error";
        }
        return "Order placed";
    }
}