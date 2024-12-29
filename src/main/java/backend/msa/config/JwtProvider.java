package backend.msa.config;

import backend.msa.model.enumerations.Role;
import io.jsonwebtoken.Jwts;
import io.jsonwebtoken.SignatureAlgorithm;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Component;
import java.util.Date;

@Component
public class JwtProvider {
    @Value("${jwt.secret}")  // Inject jwtSecret value from application.properties
    private String jwtSecret;

    public String createToken(String email, String role) {
        return Jwts.builder()
                .setSubject(email)
                .setIssuedAt(new Date())
                . claim("role", role)
                .signWith(SignatureAlgorithm.HS512, jwtSecret)
                .compact();
    }
}
