package backend.msa.web.controller.rest;

import backend.msa.model.dto.TickersNewsDTO;
import backend.msa.services.TickersNewsService;
import backend.msa.services.converter.TickersNewsConverterService;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api/ticker-news")

public class TickersNewsController {

    private final TickersNewsService tickersNewsService;
    private final TickersNewsConverterService tickersNewsConverterService;

    public TickersNewsController(TickersNewsService tickersNewsService, TickersNewsConverterService tickersNewsConverterService) {
        this.tickersNewsService = tickersNewsService;
        this.tickersNewsConverterService = tickersNewsConverterService;
    }

    @GetMapping
    public Page<TickersNewsDTO> getLatestNews(Pageable pageable) {
        return tickersNewsService.findAll(pageable)
                .map(tickersNewsConverterService::convertToTickersNewsDTO);
    }

    @GetMapping("/{tickerId}")
    public Page<TickersNewsDTO> getLatestNewsByStockId(Pageable pageable, @PathVariable Long tickerId) {
        return tickersNewsService.getTickersNewsByTickerId(pageable, tickerId)
                .map(tickersNewsConverterService::convertToTickersNewsDTO);
    }
}