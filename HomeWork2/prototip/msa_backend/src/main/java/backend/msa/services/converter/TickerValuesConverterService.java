package backend.msa.services.converter;

import backend.msa.model.TickerValues;
import backend.msa.model.dto.TickerValuesDTO;

public interface TickerValuesConverterService {
    TickerValuesDTO convertToTickerValuesDTO(TickerValues tickerValues);
}
