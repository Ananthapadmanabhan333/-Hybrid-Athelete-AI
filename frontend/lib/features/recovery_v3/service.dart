
import 'dart:convert';
import 'package:http/http.dart' as http;
import 'package:frontend/core/api_config.dart';
import '../../services/auth_service.dart';
import 'models.dart';

class RecoveryServiceV3 {
  final AuthService _authService = AuthService();

  Future<RecoveryDailySummary> getTodaySummary() async {
    final token = await _authService.getToken();
    final response = await http.get(
      Uri.parse('${ApiConfig.baseUrl}/recovery/v3/today'),
      headers: {
        'Authorization': 'Bearer $token',
        'Content-Type': 'application/json',
      },
    );

    if (response.statusCode == 200) {
      return RecoveryDailySummary.fromJson(jsonDecode(response.body));
    } else {
      throw Exception('Failed to load recovery summary');
    }
  }

  Future<RecoveryDailySummary> logRecovery(RecoveryLogV3 log) async {
    final token = await _authService.getToken();
    final response = await http.post(
      Uri.parse('${ApiConfig.baseUrl}/recovery/v3/log'),
      headers: {
        'Authorization': 'Bearer $token',
        'Content-Type': 'application/json',
      },
      body: jsonEncode(log.toJson()),
    );

    if (response.statusCode == 200) {
      return RecoveryDailySummary.fromJson(jsonDecode(response.body));
    } else {
      throw Exception('Failed to submit recovery log');
    }
  }
}
