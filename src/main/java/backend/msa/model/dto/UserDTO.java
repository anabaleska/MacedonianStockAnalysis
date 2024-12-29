package backend.msa.model.dto;
import lombok.NonNull;

public record UserDTO(@NonNull String username,
                      @NonNull String password,
                      @NonNull String repeatedPassword,
                      @NonNull String email) {
}