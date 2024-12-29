package backend.msa.services.converter.impl;
import backend.msa.model.Indicators;
import backend.msa.model.dto.IndicatorsDTO;
import backend.msa.services.converter.IndicatorsConverterService;
import org.springframework.stereotype.Service;

@Service("indicatorsConverterServiceImpl")
public class IndicatorsConverterServiceImpl implements IndicatorsConverterService {
    @Override
    public IndicatorsDTO convertToStockIndicatorsDTO(Indicators stockIndicators) {
        return new IndicatorsDTO(
                stockIndicators.getId(),
                stockIndicators.getStockId(),
                stockIndicators.getDate(),
                stockIndicators.getTimeframe(),
                stockIndicators.getSma50(),
                stockIndicators.getSma200(),
                stockIndicators.getEma50(),
                stockIndicators.getEma200(),
                stockIndicators.getRsi(),
                stockIndicators.getMacd(),
                stockIndicators.getStochasticOscillator(),
                stockIndicators.getCci(),
                stockIndicators.getWilliamsR(),
                stockIndicators.getBollingerHigh(),
                stockIndicators.getBollingerLow(),
                stockIndicators.getSignal()
        );
    }
}
