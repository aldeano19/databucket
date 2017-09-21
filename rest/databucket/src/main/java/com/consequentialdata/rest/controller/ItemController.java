package com.consequentialdata.rest.controller;


import com.consequentialdata.rest.constans.StoreEnum;
import com.consequentialdata.rest.model.Item;
import com.consequentialdata.rest.service.interfaces.ItemService;
import com.sun.org.apache.regexp.internal.RE;
import org.apache.catalina.Store;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.util.HashMap;
import java.util.List;
import java.util.Map;

/**
 * Created by Eriel.Marimon on 6/20/17.
 * Modified by Eriel.Marimon on 6/21/17.
 */
@RestController
@RequestMapping("/items")
public class ItemController {

    /**
     * Injection of the ItemService Bean as defined by the class ItemServiceImpl
     */
    @Autowired
    private ItemService itemService;

    /**
     * Create a new Item in the database.
     * @param item The new item to be saved.
     * @param availability The availability of this item in a separate object.
     * @return The newly saved item.
     * @throws Exception
     */
    @RequestMapping(method = RequestMethod.POST)
    public Item create(Item item, @RequestBody(required=false) Map<String, String> availability) throws Exception {
        return itemService.create(item, availability);
    }

    @RequestMapping(value="/{id}", method = RequestMethod.PUT)
    public Item update(@PathVariable String id,
                       @RequestParam(required = false) String sku,
                       @RequestParam(required = false) String model,
                       @RequestParam(required = false) String onlinePrice,
                       @RequestParam(required = false) String delivery,
                       @RequestParam(required = false) String description){
        return itemService.update(id,sku,model,onlinePrice,delivery,description);
    }


    /**
     * List all the items in the database;
     * @return List of Item objects. Ordered by more-time-without-an-update.
     */
    @RequestMapping(method = RequestMethod.GET)
    public List<Item> list(){
        return  itemService.findAll();
    }

    @RequestMapping(value = "/filter", method = RequestMethod.GET)
    public List<Item> filter(Item item) {
        return itemService.filter(item);
    }

    @RequestMapping(value="/getUrlsMap", method = RequestMethod.GET)
    public Map<String, String> getUrlsMap(){
        return itemService.getUrlsMap();
    }

    @RequestMapping(method = RequestMethod.PATCH)
    public Item updateAvailability(@RequestParam String itemName,
                                   @RequestBody Map<String,String> itemAvailabilityMap){

//        Map<String,String> itemAvailabilityMap = new HashMap<>();

        return itemService.updateAvailability(itemName, itemAvailabilityMap);
    }

    /**
     * Add or modify mappings in the availability object for item with given name.
     * @param name The name of the item for which availability should be updated.
     * @param availabilityStores List of stores where this item could be found. If a store already exists,
     *                           its price will be modified, else a new store:price mapping will be added.
     * @param availabilityPrices Prices for this item in the respective stores. Mapping occurs 1 to 1
     *                           with availabilityStores. If a store already exists, its price will be modified, else
     *                           a new store:price mapping will be added.
     * @return The modified Item.
     */
    @RequestMapping(value="/availability/{name}", method = RequestMethod.PATCH)
    public Item updateAvailability2(@PathVariable String name,
                                   @RequestParam List<String> availabilityStores,
                                   @RequestParam List<Double> availabilityPrices) throws Exception {
        return itemService.updateAvailability(name, availabilityStores, availabilityPrices);
    }

    /**
     * Get single Item with id.
     * @param id The ObjectId in mongodb of item to search.
     * @return A single Item object.
     */
    @RequestMapping(value="{id}", method=RequestMethod.GET)
    public Item getById(@PathVariable String id){
        return itemService.getById(id);
    }

    /**
     * Get single Item with id.
     * @param name The item's name as defined by the store that sells it.
     * @return A single Item object.
     */
    @RequestMapping(value="/withName/{name}", method=RequestMethod.GET)
    public Item getByName(@PathVariable String name){
        return itemService.getByName(name);
    }
}
