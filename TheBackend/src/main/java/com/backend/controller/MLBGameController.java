@Controller
public class MLBGameController {
    @Autowired
    private MLBGameRepository mlbGameRepository;

    @GetMapping("/predictions")
    public String getPredictions(Model model) {
        List<MLBGame> predictions = mlbGameRepository.findAll();
        model.addAttribute("predictions", predictions);
        return "predictions";
    }
}
