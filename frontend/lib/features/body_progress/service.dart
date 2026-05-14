
import 'dart:convert';
import 'package:http/http.dart' as http;
import 'package:frontend/core/api_config.dart';
import '../../services/auth_service.dart';
import 'models.dart';

class BodyProgressService {
  final AuthService _authService = AuthService();

  Future<BodyChartsResponse> getChartsData() async {
    final token = await _authService.getToken();
    final response = await http.get(
      Uri.parse('${ApiConfig.baseUrl}/body/charts'),
      headers: {
        'Authorization': 'Bearer $token',
        'Content-Type': 'application/json',
      },
    );

    if (response.statusCode == 200) {
      return BodyChartsResponse.fromJson(jsonDecode(response.body));
    } else {
      throw Exception('Failed to load charts data');
    }
  }

  Future<void> logWeight(double weight, double? bodyFat) async {
    final token = await _authService.getToken();
    final response = await http.post(
      Uri.parse('${ApiConfig.baseUrl}/body/log-weight'),
      headers: {
        'Authorization': 'Bearer $token',
        'Content-Type': 'application/json',
      },
      body: jsonEncode({
        'weight': weight,
        'body_fat_percentage': bodyFat,
      }),
    );

    if (response.statusCode != 200) {
      throw Exception('Failed to log weight');
    }
  }
}
