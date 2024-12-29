package backend.msa.repository;
import backend.msa.model.TickersNews;
import java.util.List;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;


@Repository
public interface TickersNewsRepository extends JpaRepository<TickersNews, Long> {
    Page<TickersNews> getTickersNewsByTickerId(Pageable pageable,Long tickerId);
    List<TickersNews> findAllByTickerId(Long tickerId);
}
