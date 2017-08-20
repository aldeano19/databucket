package com.consequentialdata.rest.service;

import com.consequentialdata.rest.model.Location;
import com.consequentialdata.rest.repository.interfaces.LocationRepository;
import com.consequentialdata.rest.service.interfaces.LocationService;
import org.bson.types.ObjectId;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.Date;
import java.util.List;
import java.util.Map;

/**
 * Created by Eriel.Marimon on 8/19/17.
 */
@Service
public class LocationServiceImpl implements LocationService{
    /**
     * Injection of the LocationRepository Bean as defined by the class LocationRepositoryImpl
     */
    @Autowired
    LocationRepository locationRepository;

    @Override
    public Location update(Location location) {
        Location old = locationRepository.findByName(location.getName());
        if (old != null){
            /* If exists, keep id and creation date. */
            location.setId(new ObjectId(old.getId()));
            location.setCreated(old.getCreated());
        }else{
            location.setCreated(new Date());
        }
        location.setUpdated(new Date());

        return locationRepository.save(location);
    }

    @Override
    public List<Location> findAll() {
        return locationRepository.findAll();
    }

    @Override
    public Map<String, String> getUrlsMap() {
        return locationRepository.getUrlsMap();
    }
}
