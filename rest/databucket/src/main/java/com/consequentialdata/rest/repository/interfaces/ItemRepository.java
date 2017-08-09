package com.consequentialdata.rest.repository.interfaces;

import com.consequentialdata.rest.model.Item;
import com.consequentialdata.rest.repository.interfaces.custom.ItemRepositoryCustom;
import org.springframework.data.mongodb.repository.MongoRepository;

import java.util.List;

/**
 * Created by Eriel.Marimon on 6/21/17.
 *
 * Spring data framework automatically implements any method defined here.
 *
 * To search an Item by one of its properties:
 *      Item findItemBy{property}(T property)
 *
 * To search an Item by multiple properties with &&(AND) operator:
 *      Item findItemBy{property}And{property}
 *
 * To search an Item by multiple properties with ||(OR) operator:
 *      Item findItemBy{property}OR{property}
 */
public interface ItemRepository extends MongoRepository<Item, String>, ItemRepositoryCustom {

    Item findByName(String name);

    Item findById(String id);

    List<Item> findAllByOrderByUpdated();
}
