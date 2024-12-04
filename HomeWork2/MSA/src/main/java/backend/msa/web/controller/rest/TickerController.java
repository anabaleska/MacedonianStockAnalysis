package backend.msa.web.controller.rest;

import backend.msa.model.dto.TickerDTO;
import backend.msa.services.TickerService;
import backend.msa.services.converter.TickerConverterService;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
@RestController
@RequestMapping("/api/tickers")

public class TickerController {
    private final TickerService tickerService;
    private final TickerConverterService tickerConverterService;

    public TickerController(TickerService tickerService, TickerConverterService tickerConverterService) {
        this.tickerService = tickerService;
        this.tickerConverterService = tickerConverterService;
    }

    @GetMapping
    public Page<TickerDTO> findAll(Pageable pageable) {
       return this.tickerService.findAll(pageable).map(tickerConverterService::convertToTickerDTO);

    }

}