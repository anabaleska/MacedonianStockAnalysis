package backend.msa.services;
import backend.msa.model.Indicators;

import java.util.List;

public interface IndicatorsService {
    List<Indicators> findAll();

    Indicators findById(Long id);

    List<Indicators> findByStockId(Long id);
}