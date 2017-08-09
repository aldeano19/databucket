package com.consequentialdata.rest.controller;


import com.consequentialdata.rest.model.Item;
import com.consequentialdata.rest.service.interfaces.ItemService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.util.List;

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

    @RequestMapping(value="/create", method = RequestMethod.POST)
    public Item create2(Item item) throws Exception {
        return itemService.create(item);
    }

    /**
     * Create a new Item in the database.
     * @param sku Identifies an item.
     * @param model An instance of the named SKU.
     * @param name Name of the SKU (item).
     * @param imageUrl Url for the image on this item.
     * @param productUrl Url for the item on the store's website.
     * @param availabilityStores List of stores where this item could be found.
     * @param availabilityPrices Prices for this item in the respective stores. Mapping occurs 1 to 1
     *                           with availabilityStores.
     * @return  The newly created item. Note that availabilityStores and availabilityPrices will create a new object.
     * @throws Exception Generic error. Error message specifies what went wrong.
     */
    @RequestMapping(method = RequestMethod.POST)
    public Item create(@RequestParam(required=false) String sku,
                       @RequestParam(required=false) String model,
                       @RequestParam String name,
                       @RequestParam(required=false) String imageUrl,
                       @RequestParam String productUrl,
                       @RequestParam(required=false) List<String> availabilityStores,
                       @RequestParam(required=false) List<Double> availabilityPrices) throws Exception {

        return itemService.create(sku,model,name,imageUrl,productUrl,
                availabilityStores,availabilityPrices);
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
    public Item updateAvailability(@PathVariable String name,
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
