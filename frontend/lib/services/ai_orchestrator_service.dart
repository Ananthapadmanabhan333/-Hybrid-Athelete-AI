import 'dart:convert';
import 'package:http/http.dart' as http;
import '../core/constants.dart';
import 'auth_service.dart';

class AIOrchestratorService {
  final String _baseUrl = AppConstants.apiBaseUrl;
  final AuthService _authService = AuthService();

  Future<Map<String, dynamic>> getDashboardPayload() async {
    final token = await _authService.getToken();
    final headers = {
      "Content-Type": "application/json",
      "Authorization": "Bearer $token"
    };

    try {
      final response = await http.get(
        Uri.parse('$_baseUrl/ai-orchestrator/dashboard-payload'),
        headers: headers,
      );

      if (response.statusCode == 200) {
        return jsonDecode(response.body);
      } else {
        print("Backend Error: ${response.body}");
        return {};
      }
    } catch (e) {
      print("Network Error: $e");
      return {};
    }
  }

  Future<Map<String, dynamic>> sendCoachChat(String message) async {
    final token = await _authService.getToken();
    final headers = {
      "Content-Type": "application/json",
      "Authorization": "Bearer $token"
    };

    try {
      final response = await http.post(
        Uri.parse('$_baseUrl/nutrition/v2/medical-coach/chat'),
        headers: headers,
        body: jsonEncode({"message": message}),
      );

      return jsonDecode(response.body);
    } catch (e) {
      return {"reply": "Sorry, I'm having trouble connecting right now."};
    }
  }
}
