package backend.msa.services;
import backend.msa.model.Ticker;
import backend.msa.model.TickersNews;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;

public interface TickersNewsService {
    Page<TickersNews> getTickersNewsByTickerId(Pageable pageable, Long tickerId);
    Page<TickersNews> findAll(Pageable pageable);

}