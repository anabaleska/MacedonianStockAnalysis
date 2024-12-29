package backend.msa.model.exceptions;

public class TickerNotFoundException extends RuntimeException{
    public TickerNotFoundException(Long id) {
        super(String.format("Ticker with id %d not found", id));
    }
}
