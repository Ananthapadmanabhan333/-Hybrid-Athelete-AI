import 'dart:convert';
import 'package:http/http.dart' as http;
import '../core/constants.dart';
import 'auth_service.dart';

class DailyMetricsService {
  final String _baseUrl = AppConstants.apiBaseUrl;
  final AuthService _authService = AuthService();

  Future<Map<String, dynamic>> getTodayMetrics() async {
    final token = await _authService.getToken();
    
    try {
      final response = await http.get(
        Uri.parse('$_baseUrl/daily-metrics/today'),
        headers: {
          "Content-Type": "application/json",
          "Authorization": "Bearer $token"
        },
      );

      if (response.statusCode == 200) {
        return jsonDecode(response.body);
      } else {
        print("Failed to get today's metrics: ${response.body}");
        return _getDefaultMetrics();
      }
    } catch (e) {
      print("Error getting today's metrics: $e");
      return _getDefaultMetrics();
    }
  }

  Future<Map<String, dynamic>> updateTodayMetrics({
    int? calories,
    int? trainingMinutes,
    double? sleepHours,
    int? mood,
    int? sorenessLevel,
    int? recoveryScore,
  }) async {
    final token = await _authService.getToken();
    
    final Map<String, dynamic> updates = {};
    if (calories != null) updates['total_calories_in'] = calories;
    if (trainingMinutes != null) updates['total_training_minutes'] = trainingMinutes;
    if (sleepHours != null) updates['sleep_hours'] = sleepHours;
    if (mood != null) updates['mood'] = mood;
    if (sorenessLevel != null) updates['soreness_level'] = sorenessLevel;
    if (recoveryScore != null) updates['recovery_score'] = recoveryScore;
    
    try {
      final response = await http.put(
        Uri.parse('$_baseUrl/daily-metrics/today'),
        headers: {
          "Content-Type": "application/json",
          "Authorization": "Bearer $token"
        },
        body: jsonEncode(updates),
      );

      if (response.statusCode == 200) {
        return jsonDecode(response.body);
      } else {
        print("Failed to update metrics: ${response.body}");
        throw Exception("Failed to update metrics");
      }
    } catch (e) {
      print("Error updating metrics: $e");
      rethrow;
    }
  }

  Future<Map<String, dynamic>> getTodayInsights() async {
    final token = await _authService.getToken();
    
    try {
      final response = await http.get(
        Uri.parse('$_baseUrl/daily-metrics/today/insights'),
        headers: {
          "Content-Type": "application/json",
          "Authorization": "Bearer $token"
        },
      );

      if (response.statusCode == 200) {
        return jsonDecode(response.body);
      } else {
        print("Failed to get insights: ${response.body}");
        return _getDefaultInsights();
      }
    } catch (e) {
      print("Error getting insights: $e");
      return _getDefaultInsights();
    }
  }

  Map<String, dynamic> _getDefaultMetrics() {
    return {
      "id": 0,
      "user_id": 0,
      "date": DateTime.now().toIso8601String().split('T')[0],
      "total_calories_in": 0,
      "total_training_minutes": 0,
      "recovery_score": 0,
      "sleep_hours": 0.0,
      "mood": null,
      "soreness_level": null,
      "notes": null
    };
  }

  Map<String, dynamic> _getDefaultInsights() {
    return {
      "today": {},
      "insights": {
        "summary": "Start tracking your metrics to get personalized insights!",
        "priority_recommendations": ["Log your daily activities"],
        "motivational_message": "Every journey starts with a single step!"
      },
      "patterns": {
        "issues": [],
        "positive_patterns": []
      },
      "weekly_averages": {}
    };
  }
}
