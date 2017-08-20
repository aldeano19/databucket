package com.consequentialdata.rest.repository.interfaces.impl;

import com.consequentialdata.rest.model.Location;
import com.consequentialdata.rest.repository.interfaces.custom.LocationRepositoryCustom;
import com.mongodb.DBObject;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.mongodb.core.MongoTemplate;
import org.springframework.data.mongodb.core.aggregation.*;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

/**
 * Created by Eriel.Marimon on 8/19/17.
 */
public class LocationRepositoryImpl implements LocationRepositoryCustom{
    @Autowired
    private MongoTemplate mongoTemplate;

    @Override
    public Map<String, String> getUrlsMap() {

        ProjectionOperation pop = Aggregation.project("name", "clubUrl");

        List<AggregationOperation> criteria = new ArrayList<>();

        criteria.add(pop);


        TypedAggregation<Location> aggregation = Aggregation.newAggregation(Location.class, criteria);
        AggregationResults<DBObject> result = mongoTemplate.aggregate(aggregation, DBObject.class);

        Map<String, String> urlsMap = new HashMap<>();

        for(DBObject dbObject : result){
            String name = dbObject.get("name").toString();
            String clubUrl = dbObject.get("clubUrl").toString();
            urlsMap.put(name, clubUrl);
        }

        return urlsMap;
    }
}
