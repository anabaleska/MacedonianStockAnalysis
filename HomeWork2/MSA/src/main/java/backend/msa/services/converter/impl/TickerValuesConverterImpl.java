package backend.msa.services.converter.impl;

import backend.msa.model.TickerValues;
import backend.msa.model.dto.TickerValuesDTO;
import backend.msa.services.TickerService;
import backend.msa.services.converter.TickerValuesConverterService;
import org.springframework.stereotype.Service;

@Service
public class TickerValuesConverterImpl implements TickerValuesConverterService {

    private final TickerService tickerService;

    public TickerValuesConverterImpl(TickerService tickerService) {
        this.tickerService = tickerService;
    }

    @Override
    public TickerValuesDTO convertToTickerValuesDTO(TickerValues tickerValues) {
        return new TickerValuesDTO(tickerValues.getValue_id(),
                tickerValues.getStockId(),
                tickerService.findById(tickerValues.getStockId()).getName(),
                tickerValues.getDate(),
                tickerValues.getLastTransactionPrice(),
                tickerValues.getMaxPrice(),
                tickerValues.getMinPrice(),
                tickerValues.getAveragePrice(),
                tickerValues.getPercentageChange(),
                tickerValues.getAmount(),
                tickerValues.getBest(),
                tickerValues.getTotalVolume());
    }
}
