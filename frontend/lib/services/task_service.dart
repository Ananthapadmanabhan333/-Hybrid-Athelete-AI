import 'dart:convert';
import 'package:http/http.dart' as http;
import '../core/constants.dart';
import 'auth_service.dart';

class TaskService {
  final String _baseUrl = AppConstants.apiBaseUrl;
  final AuthService _authService = AuthService();

  Future<List<Map<String, dynamic>>> getDailyTasks() async {
    try {
      final token = await _authService.getToken();
      if (token == null) return [];

      final response = await http.get(
        Uri.parse('$_baseUrl/tasks/today'),
        headers: {
          "Content-Type": "application/json",
          "Authorization": "Bearer $token"
        },
      );
      if (response.statusCode == 200) {
        return List<Map<String, dynamic>>.from(jsonDecode(response.body));
      }
      return [];
    } catch (e) {
      print("Error fetching tasks: $e");
      return [];
    }
  }

  Future<bool> completeTask(int taskId) async {
    try {
      final token = await _authService.getToken();
      final response = await http.post(
        Uri.parse('$_baseUrl/tasks/$taskId/complete'),
        headers: {
          "Content-Type": "application/json",
          "Authorization": "Bearer $token"
        },
      );
      return response.statusCode == 200;
    } catch (e) {
      return false;
    }
  }
}
