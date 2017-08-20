package com.consequentialdata.rest.controller;

import com.consequentialdata.rest.model.Location;
import com.consequentialdata.rest.service.interfaces.LocationService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.RestController;

import java.util.HashMap;
import java.util.List;
import java.util.Map;


/**
 * Created by Eriel.Marimon on 8/19/17.
 */
@RestController
@RequestMapping("/locations")
public class LocationController {
    @Autowired
    private LocationService locationService;

    @RequestMapping(method = RequestMethod.PUT)
    public Location update(Location location) throws Exception {
        return locationService.update(location);
    }

    @RequestMapping(method = RequestMethod.GET)
    public List<Location> list() throws Exception {
        return locationService.findAll();
    }

    @RequestMapping(value = "getUrlsMap", method = RequestMethod.GET)
    public Map<String, String> getUrlsMap(){
        return locationService.getUrlsMap();
    }
}
