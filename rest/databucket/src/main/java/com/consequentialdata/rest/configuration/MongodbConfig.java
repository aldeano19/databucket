package com.consequentialdata.rest.configuration;


import com.mongodb.Mongo;
import com.mongodb.MongoClient;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.data.mongodb.config.AbstractMongoConfiguration;


/**
 * Created by Eriel.Marimon on 6/21/17.
 */

@Configuration
public class MongodbConfig extends AbstractMongoConfiguration{

    private final String DATABASE_NAME = "data_bucket_mongodb";
//    private final String DATABASE_HOST = "127.0.0.1";
//    private final int DATABASE_PORT = 27027;
    private final String DATABASE_HOST = "database";
    private final int DATABASE_PORT = 27017;


    @Override
    protected String getDatabaseName() {
        return DATABASE_NAME;
    }

    @Override
    @Bean
    public Mongo mongo() throws Exception {
        return new MongoClient(DATABASE_HOST, DATABASE_PORT);
    }
}
