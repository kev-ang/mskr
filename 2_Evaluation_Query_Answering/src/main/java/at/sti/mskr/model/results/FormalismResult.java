package at.sti.mskr.model.results;

import java.util.HashMap;
import java.util.Map;

public record FormalismResult(String formalism,
                              Map<String, QueryResult> queryResults) {

    public FormalismResult(String formalism) {
        this(formalism, new HashMap<>());
    }

    public void addQueryResult(String queryIdentifier,
                               QueryResult queryResult) {
        queryResults.put(queryIdentifier, queryResult);
    }
}