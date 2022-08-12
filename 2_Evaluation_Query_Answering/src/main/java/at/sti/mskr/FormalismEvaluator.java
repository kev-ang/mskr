package at.sti.mskr;

import at.sti.mskr.benchmark.FormalismBenchmark;
import at.sti.mskr.model.configuration.Configuration;
import at.sti.mskr.model.results.EvaluationResult;
import at.sti.mskr.result_output.ResultFormatter;
import com.fasterxml.jackson.databind.ObjectMapper;
import java.io.File;
import java.io.IOException;
import lombok.extern.slf4j.Slf4j;

@Slf4j
public class FormalismEvaluator {

    public static void main(String[] args) throws IOException {
        if (args.length != 1) {
            log.error("Provide only the path to the configuration file!");
        }

        ObjectMapper om = new ObjectMapper();
        Configuration config = om.readValue(new File(
                                                args[0]),
                                            Configuration.class);
        EvaluationResult evaluationResult = FormalismBenchmark.execute(config);
        log.info(om.writeValueAsString(evaluationResult));
        ResultFormatter.out(evaluationResult);
        log.info("Evaluation done!");
    }

}