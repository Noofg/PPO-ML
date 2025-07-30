package com.aifinancial.controller;

import com.aifinancial.model.User;
import com.aifinancial.servic.AuthService;
import jakarta.validation.Valid;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.validation.BindingResult;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/auth")
public class AuthController {

    @Autowired
    private AuthService authService;

    @PostMapping("/register")
    public ResponseEntity<String> register(@Valid @RequestBody User user, BindingResult result) {
        if (result.hasErrors()) {
            return ResponseEntity.badRequest().body(result.getFieldError().getDefaultMessage());
        }

        // Gán vai trò mặc định nếu không có
        if (user.getRole() == null || user.getRole().isEmpty()) {
            user.setRole("CLIENT");
        }

        String response = authService.registerUser(user);
        return ResponseEntity.ok(response);
    }
}
