package backend.msa.model;

import jakarta.persistence.*;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.util.Date;

@Entity
@Data
@NoArgsConstructor
@Table(name = "tickers_news")
public class TickersNews {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Column(name = "id")
    private Long id;

    @Column(name = "ticker_id")
    private Long tickerId;

    @Column(name = "news_id")
    private Long newsId;

    private Date date;

    private String prediction;

    public Long getId() {
        return id;
    }

    public Long getTickerId() {
        return tickerId;
    }

    public Long getNewsId() {
        return newsId;
    }

    public Date getDate() {
        return date;
    }

    public String getSentiment() {
        return prediction;
    }

}