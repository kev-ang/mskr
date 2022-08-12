package at.sti.mskr.model.configuration;

import java.util.List;

public record Configuration(String name,
                            List<Dataset> datasets, List<Query> queries,
                            List<Rule> rules,
                            int timeout) {

}