import 'dart:convert';
import 'package:http/http.dart' as http;
import '../core/constants.dart';
import 'auth_service.dart';

class NutritionService {
  final String _baseUrl = AppConstants.apiBaseUrl;
  final AuthService _authService = AuthService();

  Future<void> logMeal({
    required String foodName,
    required int calories,
    required String mealType,
    double protein = 0.0,
    double carbs = 0.0,
    double fats = 0.0,
  }) async {
    final token = await _authService.getToken();
    
    try {
      final response = await http.post(
        Uri.parse('$_baseUrl/nutrition/meals'),
        headers: {
          "Content-Type": "application/json",
          "Authorization": "Bearer $token"
        },
        body: jsonEncode({
          "food_name": foodName,
          "calories": calories,
          "protein_g": protein,
          "carbs_g": carbs,
          "fats_g": fats,
          "meal_type": mealType,
        }),
      );

      if (response.statusCode != 200) {
        print("Failed to log meal: ${response.body}");
      }
    } catch (e) {
      print("Error logging meal: $e");
      rethrow;
    }
  }

  Future<List<Map<String, dynamic>>> getTodayMeals() async {
    final token = await _authService.getToken();
    
    try {
      final response = await http.get(
        Uri.parse('$_baseUrl/nutrition/meals?limit=50'),
        headers: {
          "Content-Type": "application/json",
          "Authorization": "Bearer $token"
        },
      );

      if (response.statusCode == 200) {
        final List<dynamic> data = jsonDecode(response.body);
        return data.cast<Map<String, dynamic>>();
      } else {
        print("Failed to get meals: ${response.body}");
        return [];
      }
    } catch (e) {
      print("Error getting meals: $e");
      return [];
    }
  }

  Future<Map<String, dynamic>> getMonthlyStats(int year, int month) async {
    final token = await _authService.getToken();
    
    try {
      final response = await http.get(
        Uri.parse('$_baseUrl/nutrition/monthly-stats?year=$year&month=$month'),
        headers: {
          "Content-Type": "application/json",
          "Authorization": "Bearer $token"
        },
      );

      if (response.statusCode == 200) {
        return jsonDecode(response.body);
      } else {
        print("Failed to get monthly stats: ${response.body}");
        return {
          "month": "$year-${month.toString().padLeft(2, '0')}",
          "daily_breakdown": [],
          "monthly_averages": {
            "avg_calories": 0,
            "avg_protein": 0,
            "avg_carbs": 0,
            "avg_fats": 0,
            "days_tracked": 0,
            "total_meals": 0
          }
        };
      }
    } catch (e) {
      print("Error getting monthly stats: $e");
      return {
        "month": "$year-${month.toString().padLeft(2, '0')}",
        "daily_breakdown": [],
        "monthly_averages": {}
      };
    }
  }

  Future<Map<String, dynamic>> getNutritionAnalysis({int days = 7}) async {
    final token = await _authService.getToken();
    
    try {
      final response = await http.get(
        Uri.parse('$_baseUrl/nutrition/analysis?days=$days'),
        headers: {
          "Content-Type": "application/json",
          "Authorization": "Bearer $token"
        },
      );

      if (response.statusCode == 200) {
        return jsonDecode(response.body);
      } else {
        print("Failed to get nutrition analysis: ${response.body}");
        return {
          "summary": "Unable to load analysis",
          "recommendations": [],
          "averages": {}
        };
      }
    } catch (e) {
      print("Error getting nutrition analysis: $e");
      return {
        "summary": "Error loading analysis",
        "recommendations": [],
        "averages": {}
      };
    }
  }
}
