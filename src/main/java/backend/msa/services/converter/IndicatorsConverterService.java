package backend.msa.services.converter;
import backend.msa.model.Indicators;
import backend.msa.model.dto.IndicatorsDTO;
import org.springframework.stereotype.Service;

@Service
public interface IndicatorsConverterService {
    IndicatorsDTO convertToStockIndicatorsDTO(Indicators stockIndicators);
}