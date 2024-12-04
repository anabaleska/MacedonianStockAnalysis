package backend.msa.model;

import jakarta.persistence.*;
import lombok.Data;
import lombok.Getter;
import lombok.NoArgsConstructor;
import java.util.Date;


@Entity
@NoArgsConstructor
@Table(name = "ticker_data")
public class TickerValues {


    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long value_id;


    @Column(name = "id")
    private Long stockId;

    @Column(name = "date")
    private Date date;


    @Column(name= "last_transaction")
    private Float lastTransactionPrice;


    @Column(name="max")
    private Float maxPrice;


    @Column(name="min")
    private Float minPrice;

    @Column(name="avg")
    private Float averagePrice;

    @Column(name="prom")
    private Float percentageChange;

    @Column (name="amount")
    private Integer amount;


    @Column (name="best")
    private Float best;


    @Column (name="total")
    private Float totalVolume;

    public Long getValue_id() {
        return value_id;
    }

    public Long getStockId() {
        return stockId;
    }

    public Date getDate() {
        return date;
    }

    public Float getLastTransactionPrice() {
        return lastTransactionPrice;
    }

    public Float getMaxPrice() {
        return maxPrice;
    }

    public Float getMinPrice() {
        return minPrice;
    }

    public Float getAveragePrice() {
        return averagePrice;
    }

    public Float getPercentageChange() {
        return percentageChange;
    }

    public Integer getAmount() {
        return amount;
    }

    public Float getBest() {
        return best;
    }

    public Float getTotalVolume() {
        return totalVolume;
    }

}
