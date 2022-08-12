package at.sti.mskr.benchmark;

import at.sti.mskr.model.configuration.Configuration;
import at.sti.mskr.model.configuration.Dataset;
import at.sti.mskr.model.configuration.Query;
import at.sti.mskr.model.configuration.Rule;
import at.sti.mskr.model.results.DatasetResult;
import at.sti.mskr.model.results.EvaluationResult;
import at.sti.mskr.model.results.FormalismResult;
import at.sti.mskr.model.results.QueryResult;
import at.sti.mskr.reasoner.JenaReasoner;
import at.sti.mskr.reasoner.QueryExecutionTask;
import java.util.Collections;
import java.util.concurrent.ExecutionException;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.Future;
import java.util.concurrent.TimeUnit;
import java.util.concurrent.TimeoutException;
import lombok.extern.slf4j.Slf4j;

@Slf4j
public class FormalismBenchmark {

    public static EvaluationResult execute(Configuration configuration) {
        ExecutorService executor = Executors.newSingleThreadExecutor();
        EvaluationResult result = new EvaluationResult(configuration.name());

        for (Dataset dataset : configuration.datasets()) {
            log.info("Preparing dataset {}",
                     dataset.identifier());
            DatasetResult datasetResult =
                new DatasetResult(dataset.identifier());
            result.addDatasetResult(dataset.identifier(), datasetResult);

            for (Rule rules : configuration.rules()) {
                log.info(
                    "Setting up reasoner using formalism '{}' with dataset '{}'",
                    rules.formalism(), dataset.identifier());
                JenaReasoner reasoner = null;

                long start = System.currentTimeMillis();
                try {
                    reasoner = new JenaReasoner(dataset.datasetPath(),
                                                rules.rulePath());
                } catch (OutOfMemoryError | IllegalStateException e) {
                    log.error("Error while setting up reasoner!", e);
                    continue;
                }
                long end = System.currentTimeMillis();

                FormalismResult formalismResult = new FormalismResult(
                    rules.formalism());
                datasetResult.addFormalismResult(rules.formalism(),
                                                 formalismResult);

                QueryResult queryResult =
                    new QueryResult("Prep");
                queryResult.usedTime().add(end - start);
                formalismResult.addQueryResult("Prep",
                                               queryResult);

                for (Query query : configuration.queries()) {
                    log.info("Executing query '{}'", query.identifier());
                    queryResult =
                        new QueryResult(query.identifier());

                    for (var i = 0; i < 3; i++) {
                        Future<Integer> resultFuture = null;
                        int numberOfResults = -1;
                        try {
                            start = System.currentTimeMillis();
                            resultFuture =
                                executor.submit(
                                    new QueryExecutionTask(reasoner, query));
                            numberOfResults = resultFuture.get(
                                configuration.timeout(), TimeUnit.MINUTES);
                            end = System.currentTimeMillis();
                            queryResult.usedTime().add(end - start);
                            queryResult.numberOfResults().add(numberOfResults);
                            log.info(
                                "Query execution took {}ms resulting in {} results.",
                                (end - start), numberOfResults);
                        } catch (TimeoutException | InterruptedException |
                                 ExecutionException e) {
                            log.error("TIMEOUT!");
                            resultFuture.cancel(true);

                            queryResult.usedTime().addAll(Collections.nCopies(
                                3 - queryResult.usedTime().size(), -1L));
                            queryResult.numberOfResults().add(numberOfResults);
                            break;
                        } catch (IllegalStateException e) {
                            log.error("Application is in an illegal state!");
                            reasoner = new JenaReasoner(dataset.datasetPath(),
                                                        rules.rulePath());

                            resultFuture.cancel(true);
                            queryResult.usedTime().addAll(Collections.nCopies(
                                3 - queryResult.usedTime().size(), -1L));
                            queryResult.numberOfResults().add(numberOfResults);
                            break;
                        }
                    }
                    formalismResult.addQueryResult(query.identifier(),
                                                   queryResult);
                }
                reasoner.shutdown();
            }
        }
        return result;
    }
}