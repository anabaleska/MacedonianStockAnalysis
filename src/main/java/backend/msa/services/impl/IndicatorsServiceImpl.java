package backend.msa.services.impl;
import backend.msa.model.Indicators;
import backend.msa.repository.IndicatorsRepository;
import backend.msa.services.IndicatorsService;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class IndicatorsServiceImpl implements IndicatorsService {
   private final IndicatorsRepository indicatorsRepository;

   public IndicatorsServiceImpl(IndicatorsRepository indicatorsRepository){
       this.indicatorsRepository = indicatorsRepository;
   }

    @Override
    public List<Indicators> findAll() {
        return indicatorsRepository.findAll();
    }

    @Override
    public Indicators findById(Long id) {
        return indicatorsRepository.findById(id).orElse(null);
    }

    @Override
    public List<Indicators> findByStockId(Long id) {
        return indicatorsRepository.findByStockId(id);
    }
}