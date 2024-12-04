package backend.msa.services.impl;

import backend.msa.model.Ticker;
import backend.msa.repository.TickerRepository;
import backend.msa.services.TickerService;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.stereotype.Service;

import java.util.Optional;

@Service
public class TickerServiceImpl implements TickerService {

    private final TickerRepository tickerRepository;

    public TickerServiceImpl(TickerRepository tickerRepository) {
        this.tickerRepository = tickerRepository;
    }


    @Override
    public Optional<Ticker> findByName(String name) {
        return Optional.empty();
    }

    @Override
    public Page<Ticker> findAll(Pageable pageable) {
        return tickerRepository.findAll(pageable);
    }

    @Override
    public Ticker findById(Long id) {
        return tickerRepository.findById(id).get();
    }
}