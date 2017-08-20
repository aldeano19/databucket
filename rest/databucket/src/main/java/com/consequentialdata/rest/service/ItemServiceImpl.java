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

        // Availability HashMap to be populated with availabilityStores and availabilityPrices
        Map<String, Double> availability = new HashMap<>();

        // If either availability list is null, ignore both
        if(availabilityStores != null && availabilityPrices != null){
            // Assert that availabilityStores is same size as availabilityPrices
            if(availabilityPrices.size() != availabilityStores.size()){
                throw new Exception("availabilityStores and availabilityPrices should have same amount of data.");
            }

            // build availability hash map from availabilityStores and availabilityPrices
            for(int i = 0; i < availabilityPrices.size(); i++){
                availability.put(availabilityStores.get(i), availabilityPrices.get(i));
            }
        }

        Date created = new Date();

        Item newItem = new Item(sku, model, name, imageUrl, productUrl, availability, created, created);
        return itemRepository.save(newItem);
    }


    @Override
    public Map<String, String> getUrlsMap() {
        return itemRepository.getUrlsMap();
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
     *
     * Uses availabilityStores and availabilityPrices to update the availability for item.
     */
    @Override
    public Item updateAvailability(String name, List<String> availabilityStores, List<Double> availabilityPrices)
            throws Exception {
        // Assert that item exists
        Item item = itemRepository.findByName(name);
        if(item == null){
            throw new Exception("Item not found name=" + name);
        }

        // Assert that availabilityStores is same size as availabilityPrices
        if(availabilityPrices.size() != availabilityStores.size()){
            throw new Exception("availabilityStores and availabilityPrices should have same amount of data.");
        }

        // build availability hash map from availabilityStores and availabilityPrices
        Map<String, Double> availabilityPatch = new HashMap<>();
        for(int i = 0; i < availabilityPrices.size(); i++){
            availabilityPatch.put(availabilityStores.get(i), availabilityPrices.get(i));
        }

        // update old availability with new
        Map<String, Double> itemAvailability = item.getAvailability();
        for (String store : availabilityPatch.keySet()) {
            itemAvailability.put(store, availabilityPatch.get(store));
        }

        // update item's 'availability' field
        item.setAvailability(itemAvailability);

        // update item's 'updated' field
        item.setUpdated(new Date());

        return itemRepository.save(item);
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
