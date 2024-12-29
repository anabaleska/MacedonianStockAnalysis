package backend.msa.services.converter;
import backend.msa.model.TickersNews;
import backend.msa.model.dto.TickersNewsDTO;

public interface TickersNewsConverterService {
    TickersNewsDTO convertToTickersNewsDTO(TickersNews tickersNews);
}
