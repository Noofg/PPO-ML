import 'package:http/http.dart' as http;
import 'dart:convert';
import 'config.dart';
import 'package:shared_preferences/shared_preferences.dart';
class ApiService {
  // Đăng ký người dùng
  static Future<String?> registerUser(
    String name,
    String email,
    String password,
  ) async {
    try {
      final url = Uri.parse('$baseUrl/auth/register');
      final response = await http.post(
        url,
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({
          'name': name,
          'email': email,
          'password': password,
        }),
      );

      if (response.statusCode == 201) {
        return null; // Đăng ký thành công
      } else {
        final data = jsonDecode(response.body);
        return data['message'] ?? 'Đăng ký thất bại';
      }
    } catch (e) {
      return 'Lỗi kết nối: $e';
    }
  }

static Future<Map<String, dynamic>> loginUser(
    String email,
    String password,

  ) async {
    try {
      final url = Uri.parse('$baseUrl/auth/login');
      final response = await http.post(
        url,
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({
          'email': email,
          'password': password,
        }),
      );

      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);
        final token = data['token'];

        // Lưu token vào SharedPreferences
        final prefs = await SharedPreferences.getInstance();
        await prefs.setString('token', token);
        await prefs.setString('email', email);

        // Trả về thông tin token và role
        return {
          'token': token,
          'role': data['user']?['role'] ?? 'patient', // Đảm bảo role tồn tại
        };
      } else {
        final data = jsonDecode(response.body);
        return {
          'error': data['message'] ?? 'Đăng nhập thất bại',
        };
      }
    } catch (e) {
      return {
        'error': 'Lỗi kết nối: $e',
      };
    }
  }
}