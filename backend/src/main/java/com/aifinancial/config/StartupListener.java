package com.aifinancial.config;

import org.springframework.boot.context.event.ApplicationReadyEvent;
import org.springframework.context.ApplicationListener;
import org.springframework.stereotype.Component;

@Component
public class StartupListener implements ApplicationListener<ApplicationReadyEvent> {

    @Override
    public void onApplicationEvent(ApplicationReadyEvent event) {
        String serverPort = event.getApplicationContext().getEnvironment().getProperty("server.port", "8080");
        System.out.println("Server đang chạy trên cổng " + serverPort + ". Sẵn sàng nhận POST request!");
    }
}