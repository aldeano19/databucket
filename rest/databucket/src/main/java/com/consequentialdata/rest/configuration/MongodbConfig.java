package com.consequentialdata.rest.configuration;


import com.mongodb.Mongo;
import com.mongodb.MongoClient;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.data.mongodb.config.AbstractMongoConfiguration;
import org.springframework.data.mongodb.repository.config.EnableMongoRepositories;

import java.util.Map;
import java.util.Properties;
import java.util.Set;


/**
 * Created by Eriel.Marimon on 6/21/17.
 */

@Configuration
@EnableMongoRepositories(basePackages = "com.consequentialdata.rest.repository")
public class MongodbConfig extends AbstractMongoConfiguration{

    private final String DATABASE_NAME = "data_bucket_mongodb";

    @Override
    protected String getDatabaseName() {
        return DATABASE_NAME;
    }

    @Override
    @Bean
    public Mongo mongo() throws Exception {
        String dbHost = System.getenv("DB_HOST");
        int dbPort = Integer.parseInt(System.getenv("DB_PORT"));
        return new MongoClient(dbHost, dbPort);
    }
}
