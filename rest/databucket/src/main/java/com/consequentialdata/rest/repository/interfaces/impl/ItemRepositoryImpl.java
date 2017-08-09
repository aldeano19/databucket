package com.consequentialdata.rest.repository.interfaces.impl;

import com.consequentialdata.rest.model.Item;
import com.consequentialdata.rest.repository.interfaces.custom.ItemRepositoryCustom;
import org.bson.types.ObjectId;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.mongodb.core.MongoTemplate;
import org.springframework.data.mongodb.core.query.Criteria;
import org.springframework.data.mongodb.core.query.Query;

import java.util.Date;


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

        item.setSku(sku);
        item.setModel(sku);
        item.setModel(model);
        item.setOnlinePrice(onlinePrice);
        item.setDelivery(delivery);
        item.setDescription(description);
        item.setUpdated(new Date());

        mongoTemplate.save(item);

        return item;
    }
}
