package backend.msa.repository;
import backend.msa.model.Indicators;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface IndicatorsRepository extends JpaRepository<Indicators, Long> {

    @Query("""
    select s from Indicators s
    where s.stockId = :id
      and s.sma50 is not null
      and (cast(s.sma50 as string) != 'NaN')
      and s.timeframe = 'M'
""")
    List<Indicators> findByStockId(@Param("id") Long id);

}