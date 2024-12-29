package backend.msa.services.converter.impl;
import backend.msa.model.TickersNews;
import backend.msa.model.dto.TickersNewsDTO;
import backend.msa.services.converter.TickersNewsConverterService;
import org.springframework.stereotype.Service;

@Service
public class TickersNewsConverterServiceImpl implements TickersNewsConverterService {
    @Override
    public TickersNewsDTO convertToTickersNewsDTO(TickersNews tickersNews) {
        return new TickersNewsDTO(tickersNews.getId(), tickersNews.getTickerId(),
                tickersNews.getNewsId(), tickersNews.getDate(),tickersNews.getSentiment());
    }
}