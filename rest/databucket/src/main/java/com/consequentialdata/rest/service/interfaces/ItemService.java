package com.consequentialdata.rest.service.interfaces;

import com.consequentialdata.rest.constans.StoreEnum;
import com.consequentialdata.rest.model.Item;

import java.util.List;
import java.util.Map;

/**
 * Created by Eriel.Marimon on 6/21/17.
 */
public interface ItemService {

    /**
     * Creates a new Item and persists it to database.
     * @param sku Identifies an item.
     * @param model An instance of the named SKU.
     * @param name Name of the SKU (item).
     * @param imageUrl Url for the image on this item.
     * @param productUrl Url for the item on the store's website.
     * @param availabilityStores List of stores where this item could be found.
     * @param availabilityPrices Prices for this item in the respective stores. Mapping occurs 1 to 1
     *                           with availabilityStores.
     * @return The newly created item.
     * @throws Exception Generic exception with detailed error message.
     */
    Item create(
            String sku, String model, String name, StoreEnum store, String imageUrl,
            String productUrl, List<String> availabilityStores, List<Double> availabilityPrices)
            throws Exception;

    /**
     * Creates a new Item and persists it to database.
     * @return The newly created item.
     * @throws Exception Generic exception with detailed error message.
     */
    Item create(Item item, Map<String, String> availability) throws Exception;

    /**
     * Gets all the items in the database;
     * @return List of Item objects. Ordered by more-time-without-an-update.
     */
    List<Item> findAll();

    /**
     * Updates the availability of an Item
     * @param name Name of the item. Used to find the item. If item with this name doesn'e exist, throws exception.
     * @param availabilityStores Stores.
     * @param availabilityPrices Prices. Map strictly 1 to 1 with Stores.
     * @return Updated Item.
     * @throws Exception Generic exception with detailed error message.
     */
    Item updateAvailability(String name, List<String> availabilityStores, List<Double> availabilityPrices)
            throws Exception;

    /**
     * Gets the Items for the id from the itemRepository.
     * @param id The ObjectId for the item.
     * @return The Item.
     */
    Item getById(String id);

    /**
     * Gets the Items for the id from the itemRepository.
     * @param name The name for the item.
     * @return The Item.
     */
    Item getByName(String name);

    /**
     * Updates the information for an already existing item.
     * @param id The mongodb id  for this item.
     * @param sku The sku (group identifier) of this item as provided by store.
     * @param model The model of the sku for this item.
     * @param onlinePrice The price shown online for this item, if any.
     * @param delivery The delivery estimate for this item if ordered online.
     * @param description A description for this item provided by the store.
     * @return The updated item.
     */
    Item update(String id, String sku, String model, String onlinePrice, String delivery, String description);

    Map<String,String> getUrlsMap();

    Item updateAvailability(String itemName, Map<String,String> itemAvailabilityMap);

    List<Item> filter(Item item);
}