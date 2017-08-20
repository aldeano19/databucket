package com.consequentialdata.rest.repository.interfaces;

import com.consequentialdata.rest.model.Location;
import com.consequentialdata.rest.repository.interfaces.custom.LocationRepositoryCustom;
import org.springframework.data.mongodb.repository.MongoRepository;

/**
 * Created by Eriel.Marimon on 8/19/17.
 */
public interface LocationRepository extends MongoRepository<Location, String>, LocationRepositoryCustom {
    Location findByName(String name);
}
