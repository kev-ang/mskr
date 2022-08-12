package at.sti.mskr.model.results;

import java.util.HashMap;
import java.util.Map;
import javax.xml.crypto.Data;

public record EvaluationResult(String evaluationName,
                               Map<String, DatasetResult> datasetResultMap) {

    public EvaluationResult(String evaluationName) {
        this(evaluationName, new HashMap<>());
    }

    public void addDatasetResult(String dataset, DatasetResult datasetResult) {
        datasetResultMap.put(dataset, datasetResult);
    }
}