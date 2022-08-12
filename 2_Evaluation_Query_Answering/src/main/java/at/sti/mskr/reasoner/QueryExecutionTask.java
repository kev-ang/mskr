package at.sti.mskr.reasoner;

import at.sti.mskr.model.configuration.Query;
import java.util.concurrent.Callable;
import lombok.AllArgsConstructor;

@AllArgsConstructor
public class QueryExecutionTask implements Callable<Integer> {


    private final JenaReasoner jenaReasoner;
    private final Query query;

    @Override
    public Integer call() throws Exception {
        return jenaReasoner.executeQuery(query);
    }
}