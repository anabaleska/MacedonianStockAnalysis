package backend.msa.web.controller.rest;

import backend.msa.model.dto.TickerValuesDTO;
import backend.msa.services.TickerValuesService;
import backend.msa.services.converter.TickerValuesConverterService;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.data.domain.Pageable;
import org.springframework.data.domain.Page;

@RestController
@RequestMapping("/api/ticker-values")
public class TickerValuesController {
    private final TickerValuesService tickerValuesService;
    private final TickerValuesConverterService tickerValuesConverterService;

    public TickerValuesController(TickerValuesService tickerValuesService, TickerValuesConverterService tickerValuesConverterService) {
        this.tickerValuesService = tickerValuesService;
        this.tickerValuesConverterService = tickerValuesConverterService;
    }

    @GetMapping
    public Page<TickerValuesDTO> findAll(Pageable pageable) {
       return this.tickerValuesService.findAll(pageable).map(tickerValuesConverterService::convertToTickerValuesDTO);
    }
}