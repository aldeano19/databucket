package com.consequentialdata.rest.repository.interfaces.custom;

import com.consequentialdata.rest.model.Item;

import java.util.Map;

/**
 * Created by Eriel.Marimon on 6/21/17.
 */
public interface ItemRepositoryCustom {

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

    Item updateAvailability(String itemName, Map<String, String> itemAvailabilityMap);
}
