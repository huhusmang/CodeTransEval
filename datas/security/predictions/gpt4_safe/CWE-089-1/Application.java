import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.jdbc.core.JdbcTemplate;
import javax.annotation.PostConstruct;
import java.util.List;
import java.util.Map;

@SpringBootApplication
@RestController
public class Application {

    @Autowired
    private JdbcTemplate jdbcTemplate;

    public static void main(String[] args) {
        SpringApplication.run(Application.class, args);
    }

    @GetMapping("/unsubscribe")
    public List<Map<String, Object>> unsubscribe(@RequestParam String email) {
        String query = "SELECT * FROM users WHERE email = ?";
        return jdbcTemplate.queryForList(query, new Object[]{email});
    }

    @PostConstruct
    private void initDb() {
        jdbcTemplate.execute("CREATE TABLE IF NOT EXISTS users (id SERIAL, email VARCHAR(255))");
    }
}