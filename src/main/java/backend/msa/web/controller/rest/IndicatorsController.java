package backend.msa.web.controller.rest;
import backend.msa.model.dto.IndicatorsDTO;
import backend.msa.services.IndicatorsService;
import backend.msa.services.converter.IndicatorsConverterService;
import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import java.util.List;

@RestController
@RequestMapping("/api/stock-indicators")

public class IndicatorsController {
    private final IndicatorsService stockIndicatorsService;
    private final IndicatorsConverterService stockIndicatorsConverterService;

    public IndicatorsController(IndicatorsService stockIndicatorsService,  @Qualifier("indicatorsConverterServiceImpl") IndicatorsConverterService stockIndicatorsConverterService) {
        this.stockIndicatorsService = stockIndicatorsService;
        this.stockIndicatorsConverterService = stockIndicatorsConverterService;
    }

    @GetMapping
    public List<IndicatorsDTO> findAll() {
        return this.stockIndicatorsService.findAll()
                .stream().map(stockIndicatorsConverterService::convertToStockIndicatorsDTO)
                .toList();
    }

    @GetMapping("/{id}")
    public List<IndicatorsDTO> findByStockId(@PathVariable Long id) {
        return this.stockIndicatorsService.findByStockId(id)
                .stream().map(stockIndicatorsConverterService::convertToStockIndicatorsDTO)
                .toList();
    }
}