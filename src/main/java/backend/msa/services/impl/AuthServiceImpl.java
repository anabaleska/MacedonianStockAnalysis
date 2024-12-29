package backend.msa.services.impl;


import backend.msa.config.JwtProvider;
import backend.msa.model.User;
import backend.msa.repository.UserRepository;
import backend.msa.services.AuthService;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;

@Service
public class AuthServiceImpl implements AuthService {
    private final UserRepository userRepository;
    private final PasswordEncoder passwordEncoder;
    private final JwtProvider jwtProvider;

    public AuthServiceImpl(UserRepository userRepository, PasswordEncoder passwordEncoder, JwtProvider jwtProvider) {
        this.userRepository = userRepository;
        this.passwordEncoder = passwordEncoder;
        this.jwtProvider = jwtProvider;
    }

    @Override
    public String login(String email, String password) {
        User user = userRepository.findByEmail(email)
                .orElseThrow(() -> new RuntimeException("Invalid user credentials"));

        if (!passwordEncoder.matches(password, user.getPassword())) {
            throw new RuntimeException("Invalid user credentials");
        }
        String role= user.getUsername().equals("admin") ? "ADMIN" :"USER";
        String token = jwtProvider.createToken(email,role);  // Assuming jwtProvider is responsible for generating JWT
        return token;
    }
}