package backend.msa.services.converter.impl;

import backend.msa.model.Ticker;
import backend.msa.model.dto.TickerDTO;
import backend.msa.services.converter.TickerConverterService;
import org.springframework.stereotype.Service;

@Service
public class TickerConverterServiceImpl implements TickerConverterService {
    @Override
    public TickerDTO convertToTickerDTO(Ticker ticker) {
        return new TickerDTO(ticker.getId(), ticker.getName());
    }
}