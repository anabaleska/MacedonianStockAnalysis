package backend.msa.services.impl;

import backend.msa.model.TickersNews;
import backend.msa.repository.TickersNewsRepository;
import backend.msa.services.TickersNewsService;
import java.util.List;
import java.util.stream.Collectors;

import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.stereotype.Service;

@Service
public class TickersNewsServiceImpl implements TickersNewsService {
    private final TickersNewsRepository tickersNewsRepository;

    public TickersNewsServiceImpl(TickersNewsRepository tickersNewsRepository) {
        this.tickersNewsRepository = tickersNewsRepository;
    }

    @Override
    public Page<TickersNews> getTickersNewsByTickerId(Pageable pageable, Long tickerId) {
        return tickersNewsRepository.getTickersNewsByTickerId( pageable, tickerId);
    }

    @Override
    public Page<TickersNews> findAll(Pageable pageable) {
        return tickersNewsRepository.findAll(pageable);
    }


}