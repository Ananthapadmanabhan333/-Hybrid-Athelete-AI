
import 'dart:convert';
import 'package:http/http.dart' as http;
import 'package:frontend/core/api_config.dart';
import '../../services/auth_service.dart';
import 'models.dart';

class NutritionServiceV2 {
  final AuthService _authService = AuthService();

  Future<MonthlyCalorieSummary> getMonthlySummary() async {
    final token = await _authService.getToken();
    final response = await http.get(
      Uri.parse('${ApiConfig.baseUrl}/nutrition/v2/monthly-summary'),
      headers: {
        'Authorization': 'Bearer $token',
        'Content-Type': 'application/json',
      },
    );

    if (response.statusCode == 200) {
      return MonthlyCalorieSummary.fromJson(jsonDecode(response.body));
    } else {
      throw Exception('Failed to load monthly summary');
    }
  }

  Future<NutritionInsights> getInsights() async {
    final token = await _authService.getToken();
    final response = await http.get(
      Uri.parse('${ApiConfig.baseUrl}/nutrition/v2/insights'),
      headers: {
        'Authorization': 'Bearer $token',
        'Content-Type': 'application/json',
      },
    );

    if (response.statusCode == 200) {
      return NutritionInsights.fromJson(jsonDecode(response.body));
    } else {
      throw Exception('Failed to load insights');
    }
  }
}
