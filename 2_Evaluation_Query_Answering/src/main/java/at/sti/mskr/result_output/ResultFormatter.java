package at.sti.mskr.result_output;

import at.sti.mskr.model.results.DatasetResult;
import at.sti.mskr.model.results.EvaluationResult;
import at.sti.mskr.model.results.FormalismResult;
import at.sti.mskr.model.results.QueryResult;
import java.io.BufferedWriter;
import java.io.FileWriter;
import java.io.IOException;
import java.util.ArrayList;
import java.util.Collections;
import java.util.Comparator;
import java.util.HashSet;
import java.util.List;
import java.util.Set;

public class ResultFormatter {

    public static void out(EvaluationResult result)
        throws IOException {
        for (DatasetResult datasetResult : result.datasetResultMap().values()) {
            try (BufferedWriter writer = new BufferedWriter(
                new FileWriter(datasetResult.dataset() + ".csv"))) {
                writer.write(createHeadline());
                writer.newLine();
                for (FormalismResult formalismResult : datasetResult.formalismResultMap()
                                                                    .values()) {
                    List<Object> resultLine = new ArrayList<>();
                    resultLine.add(formalismResult.formalism());
                    formalismResult.queryResults().values().stream().sorted(
                                       Comparator.comparing(QueryResult::query))
                                   .forEach(queryResult -> {
                                       resultLine.addAll(
                                           queryResult.usedTime());
                                   });
                    writer.write(joinObjectList(";", resultLine));
                    writer.newLine();
                }
            }
        }
    }

    private static String joinObjectList(String delimiter,
                                         List<Object> elements) {
        StringBuilder builder = new StringBuilder();
        for (var i = 0; i < elements.size(); i++) {
            builder.append(elements.get(i));
            if (i < elements.size() - 1) {
                builder.append(delimiter);
            }
        }
        return builder.toString();
    }

    private static String createHeadline(){
        List<String> headline = new ArrayList<>();
        headline.add("formalism");
        for(var i = 1; i < 15; i++){
            headline.addAll(Collections.nCopies(3, "Q" + i));
        }
        return String.join(";", headline);
    }
}