package com.consequentialdata.rest.repository.interfaces.impl;

import com.consequentialdata.rest.model.Item;
import com.consequentialdata.rest.repository.interfaces.custom.ItemRepositoryCustom;
import com.mongodb.DBObject;
import org.bson.types.ObjectId;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.mongodb.core.MongoTemplate;
import org.springframework.data.mongodb.core.aggregation.*;
import org.springframework.data.mongodb.core.query.Criteria;
import org.springframework.data.mongodb.core.query.Query;
import org.springframework.data.mongodb.core.query.Update;

import java.util.*;


/**
 * Created by Eriel.Marimon on 7/5/17.
 */
public class ItemRepositoryImpl implements ItemRepositoryCustom {
    private final String FIELD_ID = "_id";

    @Autowired
    private MongoTemplate mongoTemplate;
    /**
     * @inheritDoc
     */
    @Override
    public Item update(String id, String sku, String model, String onlinePrice, String delivery, String description) {

        Query query = new Query();
        query.addCriteria(Criteria.where(FIELD_ID).is(new ObjectId(id)));

        Item item = mongoTemplate.findOne(query, Item.class);

        if(sku != null){item.setSku(sku);}
        if(model != null){item.setModel(model);}
        if(onlinePrice != null){item.setOnlinePrice(onlinePrice);}
        if(delivery != null){item.setDelivery(delivery);}
        if(description != null){item.setDescription(description);}

        item.setUpdated(new Date());

        mongoTemplate.save(item);

        return item;
    }

    @Override
    public Map<String, String> getUrlsMap() {
        ProjectionOperation pop = Aggregation.project("name", "productUrl");

        List<AggregationOperation> criteria = new ArrayList<>();

        criteria.add(pop);


        TypedAggregation<Item> aggregation = Aggregation.newAggregation(Item.class, criteria);
        AggregationResults<DBObject> result = mongoTemplate.aggregate(aggregation, DBObject.class);

        Map<String, String> urlsMap = new HashMap<>();

        for(DBObject dbObject : result){
            String name = dbObject.get("name").toString();
            String productUrl = dbObject.get("productUrl").toString();
            urlsMap.put(name, productUrl);
        }

        return urlsMap;
    }

    @Override
    public Item updateAvailability(String itemName, Map<String, String> itemAvailabilityMap) {
        Query query = new Query();
        query.addCriteria(Criteria.where("name").is(itemName));

        Update update = new Update();
        update.set("availability", itemAvailabilityMap);

        /* Update operation */
        mongoTemplate.updateFirst(query, update, Item.class);

        /* Get updated operation */
        return mongoTemplate.findOne(query, Item.class);
    }
}
