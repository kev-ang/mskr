package at.sti.mskr.model.results;

import java.util.ArrayList;
import java.util.List;

public record QueryResult(String query, List<Long> usedTime, List<Integer> numberOfResults) {

    public QueryResult(String query) {
        this(query, new ArrayList<>(), new ArrayList<>());
    }

}