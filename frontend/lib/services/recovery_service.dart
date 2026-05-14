import 'dart:convert';
import 'package:http/http.dart' as http;
import '../core/constants.dart';
import '../models/injury_model.dart';
import 'auth_service.dart';

class RecoveryService {
  final String _baseUrl = AppConstants.apiBaseUrl;
  final AuthService _authService = AuthService();

  Future<Map<String, String>> _getHeaders() async {
    final token = await _authService.getToken();
    return {
      'Content-Type': 'application/json',
      'Authorization': 'Bearer $token',
    };
  }

  Future<RecoveryStatus?> getRecoveryStatus() async {
    try {
      final headers = await _getHeaders();
      final response = await http.get(Uri.parse('$_baseUrl/recovery/status'), headers: headers);
      
      if (response.statusCode == 200) {
        return RecoveryStatus.fromJson(jsonDecode(response.body));
      }
      return null;
    } catch (e) {
      print("Error fetching recovery status: $e");
      return null;
    }
  }

  Future<List<Injury>> getActiveInjuries() async {
    try {
      final headers = await _getHeaders();
      final response = await http.get(Uri.parse('$_baseUrl/recovery/injuries'), headers: headers);
      
      if (response.statusCode == 200) {
        final List<dynamic> data = jsonDecode(response.body);
        return data.map((json) => Injury.fromJson(json)).toList();
      }
      return [];
    } catch (e) {
      print("Error fetching injuries: $e");
      return [];
    }
  }

  Future<bool> logInjury(Map<String, dynamic> injuryData) async {
    try {
      final headers = await _getHeaders();
      final response = await http.post(
        Uri.parse('$_baseUrl/recovery/injuries'),
        headers: headers,
        body: jsonEncode(injuryData),
      );
      return response.statusCode == 200;
    } catch (e) {
      print("Error logging injury: $e");
      return false;
    }
  }
}
