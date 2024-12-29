package backend.msa.web.controller;

import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.client.HttpClientErrorException;
import org.springframework.web.client.RestTemplate;

import java.util.Map;

@RestController
@RequestMapping("/api")
public class PredictionController {

    @PostMapping("/predict")
    public ResponseEntity<?> getPrediction(@RequestBody Map<String, Object> request) {
        try {
            RestTemplate restTemplate = new RestTemplate();
            String pythonApiUrl = "http://127.0.0.1:5001/predict";

            // Logging the request to help debug
            System.out.println("Sending request to Python API at: " + pythonApiUrl);
            System.out.println("Request body: " + request);

            // Make the POST request to the Python API
            ResponseEntity<Map> response = restTemplate.postForEntity(pythonApiUrl, request, Map.class);

            // Log the response
            System.out.println("Received response: " + response.getBody());

            return ResponseEntity.ok(response.getBody());
        } catch (HttpClientErrorException e) {
            // Log error details for debugging
            System.err.println("Client error: " + e.getResponseBodyAsString());
            return ResponseEntity.status(e.getStatusCode()).body(e.getResponseBodyAsString());
        } catch (Exception e) {
            // Log the complete stack trace
            e.printStackTrace();
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body("Error: " + e.getMessage());
        }
    }
}
