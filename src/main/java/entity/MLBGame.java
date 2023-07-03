@Entity
@Table(name = "mlb_game")
public class MLBGame {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(name = "home_team")
    private String homeTeam;

    @Column(name = "away_team")
    private String awayTeam;

    @Column(name = "prediction")
    private String prediction;

    // Getters and setters
}