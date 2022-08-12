package at.sti.mskr.model.results;

import java.text.Normalizer.Form;
import java.util.HashMap;
import java.util.Map;

public record DatasetResult(String dataset,
                            Map<String, FormalismResult> formalismResultMap) {

    public DatasetResult(String dataset) {
        this(dataset, new HashMap<>());
    }

    public void addFormalismResult(String formalism,
                                   FormalismResult formalismResult) {
        formalismResultMap.put(formalism, formalismResult);
    }
}