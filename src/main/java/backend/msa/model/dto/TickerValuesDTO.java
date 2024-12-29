package backend.msa.model.dto;
import java.util.Date;

public record TickerValuesDTO(
        Long value_id,
        Long stockId,
        String tickerName,
        Date date,
        Float lastTransactionPrice,
        Float maxPrice,
        Float minPrice,
        Float averagePrice,
        Float percentageChange,
        Integer amount,
        Float best,
        Float totalVolume
) {
}