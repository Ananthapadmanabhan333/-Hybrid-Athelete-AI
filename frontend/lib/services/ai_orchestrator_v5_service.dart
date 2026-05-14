import 'dart:convert';
import 'package:http/http.dart' as http;
import '../core/constants.dart';
import 'auth_service.dart';

class AIOrchestratorV5Service {
  final String _baseUrl = AppConstants.apiBaseUrl;
  final AuthService _authService = AuthService();

  Future<Map<String, dynamic>> getV5Summary() async {
    final token = await _authService.getToken();
    final headers = {
      "Content-Type": "application/json",
      "Authorization": "Bearer $token"
    };

    try {
      final response = await http.get(
        Uri.parse('$_baseUrl/ai-orchestrator/v5/summary'),
        headers: headers,
      );

      if (response.statusCode == 200) {
        return jsonDecode(response.body);
      } else {
        return {};
      }
    } catch (e) {
      return {};
    }
  }

  Future<Map<String, dynamic>> getWeeklyInsights() async {
    final token = await _authService.getToken();
    final headers = {"Authorization": "Bearer $token"};
    final response = await http.get(Uri.parse('$_baseUrl/insights/weekly-report'), headers: headers);
    return jsonDecode(response.body);
  }
}
