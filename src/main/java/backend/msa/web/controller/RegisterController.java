package backend.msa.web.controller;

import backend.msa.model.dto.UserDTO;
import backend.msa.model.enumerations.Role;
import backend.msa.services.UserService;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/register")

public class RegisterController {
    private final UserService userService;

    public RegisterController(UserService userService) {
        this.userService = userService;
    }


    @PostMapping
    public void register(@RequestBody UserDTO userDTO) {
        try { Role role=Role.ROLE_USER;
            if(userDTO.username().equals("admin"))
                role=Role.ROLE_ADMIN;
            this.userService.register(userDTO.username(), userDTO.password(), userDTO.repeatedPassword(), userDTO.email(), role);
        } catch (RuntimeException ex) {
            System.out.println(ex.getMessage());
        }
    }
}
