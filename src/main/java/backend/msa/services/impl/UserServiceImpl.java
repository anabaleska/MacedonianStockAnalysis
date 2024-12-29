package backend.msa.services.impl;


import backend.msa.model.User;
import backend.msa.model.enumerations.Role;
import backend.msa.model.exceptions.InvalidUserCredentialException;
import backend.msa.model.exceptions.PasswordsDoNotMatchException;
import backend.msa.model.exceptions.UsernameExistsException;
import backend.msa.repository.UserRepository;
import backend.msa.services.UserService;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.security.core.userdetails.UsernameNotFoundException;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;

@Service
public class UserServiceImpl implements UserService {

    private final UserRepository userRepository;
    private final PasswordEncoder passwordEncoder;

    public UserServiceImpl(UserRepository userRepository, PasswordEncoder passwordEncoder) {
        this.userRepository = userRepository;
        this.passwordEncoder = passwordEncoder;
    }

    @Override
    public void register(String username, String password, String repeatPassword, String email, Role role) {
        if (username == null || password == null || username.isEmpty() || password.isEmpty()) {
            throw new InvalidUserCredentialException();
        }

        if (!password.equals(repeatPassword)) {
            throw new PasswordsDoNotMatchException();
        }

        if (this.userRepository.findByUsername(username).isPresent()) {
            throw new UsernameExistsException(username);
        }

        User user = new User(username, passwordEncoder.encode(password),email,role);

        userRepository.save(user);
    }

    @Override
    public UserDetails loadUserByUsername(String username) throws UsernameNotFoundException {
        return userRepository.findByUsername(username).orElseThrow(() -> new UsernameNotFoundException(username));
    }
}
