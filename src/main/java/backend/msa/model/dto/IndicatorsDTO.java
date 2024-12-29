package backend.msa.model.dto;
import java.util.Date;

public record IndicatorsDTO(Long id,
                            Long stockId,
                            Date date,
                            String timeframe,
                            Double sma50,
                            Double sma200,
                            Double ema50,
                            Double ema200,
                            Double rsi,
                            Double macd,
                            Double stochasticOscillator,
                            Double cci,
                            Double williamsR,
                            Double bollingerHigh,
                            Double bollingerLow,
                            String signal) {
}