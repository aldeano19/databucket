package com.consequentialdata.rest.service;

import com.consequentialdata.rest.model.Item;
import com.consequentialdata.rest.repository.interfaces.ItemRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import com.consequentialdata.rest.service.interfaces.ItemService;

import java.util.Date;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

/**
 * Created by Eriel.Marimon on 6/21/17.
 */
@Service
public class ItemServiceImpl implements ItemService{

    /**
     * Injection of the ItemRepository Bean as defined by the class ItemRepositoryImpl
     */
    @Autowired
    ItemRepository itemRepository;

    @Override
    public Item create(Item item){
        item.setCreated(new Date());
        item.setUpdated(new Date());
        return itemRepository.save(item);
    }

    /**
     * @inheritDoc
     *
     * Uses availabilityStores and availabilityPrices to create availability for item.
     */
    @Override
    public Item create(
            String sku, String model, String name, String imageUrl,
            String productUrl, List<String> availabilityStores, List<Double> availabilityPrices)
            throws Exception {

        Map<String, String> availability = new HashMap<>();

        Date created = new Date();

        Item newItem = new Item(sku, model, name, imageUrl, productUrl, availability, created, created);
        return itemRepository.save(newItem);
    }


    @Override
    public Map<String, String> getUrlsMap() {
        return itemRepository.getUrlsMap();
    }

    @Override
    public Item updateAvailability(String itemName, Map<String,String> itemAvailabilityMap) {

        return itemRepository.updateAvailability(itemName, itemAvailabilityMap);
    }

    /**
     * @inheritDoc
     */
    @Override
    public List<Item> findAll() {
        return itemRepository.findAllByOrderByUpdated();
    }

    /**
     * @inheritDoc
     * @deprecated
     * Uses availabilityStores and availabilityPrices to update the availability for item.
     */
    @Override
    public Item updateAvailability(String name, List<String> availabilityStores, List<Double> availabilityPrices)
            throws Exception {
        return null;
    }

    /**
     * @inheritDoc
     */
    @Override
    public Item getById(String id) {
        return itemRepository.findById(id);
    }

    /**
     * @inheritDoc
     */
    @Override
    public Item getByName(String name) {
        return itemRepository.findByName(name);
    }

    /**
     * @inheritDoc
     */
    @Override
    public Item update(String id, String sku, String model, String onlinePrice, String delivery, String description) {
        return itemRepository.update(id,sku,model,onlinePrice,delivery,description);
    }
}
