package com.consequentialdata.rest.configuration;


import com.thetransactioncompany.cors.CORSFilter;
import org.springframework.web.WebApplicationInitializer;
import org.springframework.web.context.support.AnnotationConfigWebApplicationContext;
import org.springframework.web.servlet.DispatcherServlet;

import javax.servlet.FilterRegistration;
import javax.servlet.ServletContext;
import javax.servlet.ServletException;
import javax.servlet.ServletRegistration;

/**
 * Created by Eriel.Marimon on 8/16/17.
 */
public class WarInitializer implements WebApplicationInitializer {

    @Override
    public void onStartup(ServletContext servletContext) throws ServletException {
        AnnotationConfigWebApplicationContext ctx = new AnnotationConfigWebApplicationContext();
        ctx.register(MongodbConfig.class, DatabucketRestConfig.class, SwaggerConfig.class);
        ctx.setServletContext(servletContext);

        ServletRegistration.Dynamic dynamic = servletContext.addServlet("dispatcher", new DispatcherServlet(ctx));

        dynamic.addMapping("/");
        dynamic.setLoadOnStartup(1);
    }
}
