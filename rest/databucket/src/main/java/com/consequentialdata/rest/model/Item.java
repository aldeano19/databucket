package com.consequentialdata.rest.model;

import com.consequentialdata.rest.constans.StoreEnum;
import org.bson.types.ObjectId;
import org.springframework.data.annotation.Id;
import org.springframework.data.mongodb.core.index.Indexed;
import org.springframework.data.mongodb.core.mapping.Document;
import org.springframework.format.annotation.DateTimeFormat;

import java.util.Date;
import java.util.Map;

/**
 * Created by Eriel.Marimon on 6/20/17.
 */
@Document(collection="items")
public class Item {
    /**
     * Auto-generated. Unique id of an item in mongodb.
     */
    @Id
    private ObjectId id;

    /**
     * Human readable name of an item. Unique in database.
     */
    @Indexed(unique=true)
    private String name;

    /**
     * SKU of this item.
     */
    private String sku;

    /**
     * The store where this item is found.
     */
    private StoreEnum store;

    /**
     * Unique identifier of the item within the SKU.
     */
    private String model;

    /**
     * Direct url to the item's image on the web
     */
    private String imageUrl;

    /**
     * Direct url to the product on the store's website.
     */
    private String productUrl;

    /**
     * The availability of the item. Formatted as a map of StoreNames to Prices. Ex {"Costco":1.50,"BJs":3.40}
     */
    private Map<String, String> availability;

    /**
     * Date this record was created.
     */
    private Date created;

    /**
     * Last date this record was updated.
     */
    @DateTimeFormat(pattern="MM/dd/yyyy")
    private Date updated;

    /**
     * Price shown online for the item.
     */
    private String onlinePrice;

    /**
     * Estimated delivery if item is order online.
     */
    private String delivery;

    /**
     * Description provided online for the item.
     */
    private String description;

    public Item(){}

    public Item(
            String sku,
            String model,
            String name,
            StoreEnum store, String imageUrl,
            String productUrl,
            Map<String, String> availability,
            Date created,
            Date updated) {
        this.sku = sku;
        this.model = model;
        this.name = name;
        this.store = store;
        this.imageUrl = imageUrl;
        this.productUrl = productUrl;
        this.availability = availability;
        this.created = created;
        this.updated = updated;
    }

    public String getOnlinePrice() {
        return onlinePrice;
    }

    public void setOnlinePrice(String onlinePrice) {
        this.onlinePrice = onlinePrice;
    }

    public String getDelivery() {
        return delivery;
    }

    public void setDelivery(String delivery) {
        this.delivery = delivery;
    }

    public String getDescription() {
        return description;
    }

    public void setDescription(String description) {
        this.description = description;
    }

    public String getImageUrl() {
        return imageUrl;
    }

    public void setImageUrl(String imageUrl) {
        this.imageUrl = imageUrl;
    }

    public String getProductUrl() {
        return productUrl;
    }

    public void setProductUrl(String productUrl) {
        this.productUrl = productUrl;
    }

    public void setCreated(Date created) {
        this.created = created;
    }

    public void setUpdated(Date updated) {
        this.updated = updated;
    }

    public void setId(ObjectId id) {
        this.id = id;
    }

    public void setSku(String sku) {
        this.sku = sku;
    }

    public void setModel(String model) {
        this.model = model;
    }

    public void setName(String name) {
        this.name = name;
    }

    public void setAvailability(Map<String, String> availability) {
        this.availability = availability;
    }

    public String getId() {
        return id.toString();
    }

    public String getSku() {
        return sku;
    }

    public String getModel() {
        return model;
    }

    public String getName() {
        return name;
    }

    public Map<String, String> getAvailability() {
        return availability;
    }

    public long getCreated() {
        return created.getTime();
    }

    public long getUpdated() {
        return updated.getTime();
    }

    public StoreEnum getStore() {
        return store;
    }

    public void setStore(StoreEnum store) {
        this.store = store;
    }
}
