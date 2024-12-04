package backend.msa.repository;

import backend.msa.model.TickerValues;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import backend.msa.repository.TickerValuesRepository;
@Repository
public interface TickerValuesRepository extends JpaRepository<TickerValues,Long> {
    Page<TickerValues> findAll(Pageable pageable);
}
