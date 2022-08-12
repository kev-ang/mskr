package at.sti.mskr.reasoner;

import at.sti.mskr.model.configuration.Query;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.List;
import lombok.extern.slf4j.Slf4j;
import org.apache.jena.query.Dataset;
import org.apache.jena.query.QueryCancelledException;
import org.apache.jena.query.QueryExecution;
import org.apache.jena.query.QueryExecutionBuilder;
import org.apache.jena.query.QueryExecutionFactory;
import org.apache.jena.query.QueryFactory;
import org.apache.jena.query.ReadWrite;
import org.apache.jena.query.ResultSet;
import org.apache.jena.query.ResultSetFormatter;
import org.apache.jena.query.Syntax;
import org.apache.jena.rdf.model.InfModel;
import org.apache.jena.rdf.model.ModelFactory;
import org.apache.jena.reasoner.Reasoner;
import org.apache.jena.reasoner.rulesys.GenericRuleReasoner;
import org.apache.jena.reasoner.rulesys.Rule;
import org.apache.jena.tdb2.TDB2Factory;

@Slf4j
public class JenaReasoner {

    private Dataset dataset;
    private List<Rule> rules;

    private Reasoner reasoner;

    private InfModel infModel;

    public JenaReasoner(String datasetPath,
                        String rulePath) {
        dataset = TDB2Factory.connectDataset(datasetPath);
        rules =
            Rule.rulesFromURL("file:" + rulePath);
        reasoner = new GenericRuleReasoner(rules);
        infModel =
            ModelFactory.createInfModel(reasoner, dataset.getDefaultModel());

        try {
            if(dataset.isInTransaction()){
                dataset.abort();
            }
            dataset.begin(ReadWrite.READ);
            infModel.prepare();
            dataset.end();
        }catch (OutOfMemoryError e){
            dataset.close();
            log.error("Running out of memory while preparing reasoner!");
            throw new IllegalStateException("Out of memory, preparation failed!");
        }
    }

    public int executeQuery(Query query) throws IOException {
        dataset.begin(ReadWrite.READ);
        int resultCount = -1;
        QueryExecutionBuilder queryExecution = QueryExecution
            .model(
                infModel)
            .query(
                Files.readString(
                    Path.of(
                        query.queryPath())),
                Syntax.syntaxSPARQL);
        try (
            QueryExecution qexec = queryExecution.build()) {
            ResultSet results = qexec.execSelect();
            log.info("Query execution completed!");
            resultCount = countResults(results);
            log.info("Counting results completed!");
        } catch (OutOfMemoryError e) {
            log.error("Out of memory error!");
            dataset = null;
            rules = null;
            reasoner = null;
            infModel = null;
            throw new IllegalStateException();
        }
        dataset.end();
        return resultCount;
    }

    public void shutdown() {
        dataset.close();
    }

    private int countResults(ResultSet resultSet) {
        int count = 0;
        while (resultSet.hasNext()) {
            resultSet.next();
            count++;
        }
        return count;
    }
}