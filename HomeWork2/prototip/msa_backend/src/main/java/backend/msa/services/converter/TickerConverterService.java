package backend.msa.services.converter;

import backend.msa.model.Ticker;
import backend.msa.model.dto.TickerDTO;

public interface TickerConverterService {
    TickerDTO convertToTickerDTO(Ticker ticker);
}
