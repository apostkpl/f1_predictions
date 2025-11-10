package com.apostkpl.springff1;

import com.apostkpl.springff1.model.Prediction;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.client.RestTemplate;

import java.util.Arrays;
import java.util.List;

@Controller
@RequestMapping("/f1")
public class PredictionController {
    private static final String FLASK_API_BASE_URL = "http://127.0.0.1:5000/predict/next-race";
    private final RestTemplate restTemplate = new RestTemplate();

    // Test get request
    @GetMapping("/hello")
    public String sayHello() {
        return "Hello. Does this Spring App even work?!";
    }

    // Actual Mapping for our predictions
    @GetMapping("/predictions")
    public String getF1Predictions(
        @RequestParam(name = "grid", defaultValue = "false") boolean grid, Model model
        ) {
        String flaskUrl = FLASK_API_BASE_URL + "?grid=" + grid;

        // Get the response from Flask and map it to a class
        Prediction[] predictionsArray = restTemplate.getForObject(
            flaskUrl,
            Prediction[].class
        );

        List<Prediction> predictions = (predictionsArray != null) ? Arrays.asList(predictionsArray) : List.of();
        
        model.addAttribute("predictions", predictions);
        model.addAttribute("gridMode", grid);


        return "predictions";
    }
}