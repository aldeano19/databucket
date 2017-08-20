package com.consequentialdata.rest.service.interfaces;

import com.consequentialdata.rest.model.Location;

import java.util.List;
import java.util.Map;

/**
 * Created by Eriel.Marimon on 8/19/17.
 */
public interface LocationService {
    /**
     * Updates a location if exists (determined by name). Creates if it doesn't.
     * @param location New Location data.
     * @return The updated Location.
     */
    Location update(Location location);

    List<Location> findAll();

    Map<String,String> getUrlsMap();
}
