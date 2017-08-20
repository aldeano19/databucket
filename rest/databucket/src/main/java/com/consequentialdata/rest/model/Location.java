package com.consequentialdata.rest.model;

import io.swagger.annotations.ApiModelProperty;
import org.bson.types.ObjectId;
import org.springframework.data.annotation.Id;
import org.springframework.data.mongodb.core.index.Indexed;
import org.springframework.data.mongodb.core.mapping.Document;
import org.springframework.format.annotation.DateTimeFormat;

import java.util.Date;
import java.util.Map;

/**
 * Created by Eriel.Marimon on 8/19/17.
 */
@Document(collection="locations")
public class Location {
    /**
     * Auto-generated. Unique id of a Location in mongodb.
     */
    @Id
    private ObjectId id;

    /**
     * Human readable name of a Location. Unique in database.
     */
    @Indexed(unique=true)
    private String name;

    /**
     * The name of the Retailer to which this location belongs.
     * Ex: BJ's, Costco, Publix
     */
    private String retailer;

    /**
     * Street address.
     */
    private String streetAddress;

    /**
     * Address' state.
     */
    private String state;

    /**
     * Address' city
     */
    private String city;

    /**
     * Address' zip.
     */
    private String zip;

    /**
     * Url for this club location.
     */
    private String clubUrl;


    /**
     * The ours which this Location operates every day of the week.
     */
    private Map<String, String> clubHours;

    /**
     * Date this record was created.
     */
    @ApiModelProperty(hidden = true)
    @DateTimeFormat(pattern="MM/dd/yyyy")
    private Date created;

    /**
     * Last date this record was updated.
     */
    @ApiModelProperty(hidden = true)
    @DateTimeFormat(pattern="MM/dd/yyyy")
    private Date updated;

    public Location(){}

    public Location(
            ObjectId id,
            String name,
            String retailer,
            String streetAddress,
            String state,
            String city,
            String zip,
            String clubUrl,
            Map<String, String> clubHours,
            Date created,
            Date updated) {
        this.id = id;
        this.name = name;
        this.retailer = retailer;
        this.streetAddress = streetAddress;
        this.state = state;
        this.city = city;
        this.zip = zip;
        this.clubUrl = clubUrl;
        this.clubHours = clubHours;
        this.created = created;
        this.updated = updated;
    }

    /**
     * A little hack, using JsonSerializer is more common.
     * @return The mongodb id as a string
     */
    public String getId() {
        return id.toString();
    }

    public void setId(ObjectId id) {
        this.id = id;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public String getRetailer() {
        return retailer;
    }

    public void setRetailer(String retailer) {
        this.retailer = retailer;
    }

    public String getStreetAddress() {
        return streetAddress;
    }

    public void setStreetAddress(String streetAddress) {
        this.streetAddress = streetAddress;
    }

    public String getState() {
        return state;
    }

    public void setState(String state) {
        this.state = state;
    }

    public String getCity() {
        return city;
    }

    public void setCity(String city) {
        this.city = city;
    }

    public String getZip() {
        return zip;
    }

    public void setZip(String zip) {
        this.zip = zip;
    }

    public String getClubUrl() {
        return clubUrl;
    }

    public void setClubUrl(String clubUrl) {
        this.clubUrl = clubUrl;
    }

    public Map<String, String> getClubHours() {
        return clubHours;
    }

    public void setClubHours(Map<String, String> clubHours) {
        this.clubHours = clubHours;
    }

    public Date getCreated() {
        return created;
    }

    public void setCreated(Date created) {
        this.created = created;
    }

    public Date getUpdated() {
        return updated;
    }

    public void setUpdated(Date updated) {
        this.updated = updated;
    }
}
