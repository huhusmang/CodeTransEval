import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.bind.annotation.SessionAttribute;
import javax.sql.DataSource;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.jdbc.core.JdbcTemplate;

@SpringBootApplication
@RestController
public class StockApplication {

    @Autowired
    private JdbcTemplate jdbcTemplate;

    public static void main(String[] args) {
        SpringApplication.run(StockApplication.class, args);
    }

    @PostMapping("/buy_order")
    public String buyStock(@RequestParam String stock_name, @RequestParam String stock_quantity, @SessionAttribute("username") String username) {
        String sql = "INSERT INTO buy_order (stock_name, stock_quantity, username) VALUES (?, ?, ?)";
        jdbcTemplate.update(sql, stock_name, stock_quantity, username);
        return "Order placed successfully";
    }
}