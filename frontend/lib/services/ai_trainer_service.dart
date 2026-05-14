import 'dart:convert';
import 'package:http/http.dart' as http;
import '../core/constants.dart';

import 'auth_service.dart';

class AITrainerService {
  final String _baseUrl = AppConstants.apiBaseUrl;
  final AuthService _authService = AuthService();

  Future<Map<String, dynamic>> generateDailyWorkout(
      int timeAvailable, 
      List<String> equipment,
      String workoutType,
      String difficulty
  ) async {
    final token = await _authService.getToken();
    final headers = {
      "Content-Type": "application/json",
      "Authorization": "Bearer $token"
    };
    
    try {
      final response = await http.post(
        Uri.parse('$_baseUrl/ai-trainer/generate'),
        headers: headers,
        body: jsonEncode({
          "time_available_minutes": timeAvailable,
          "equipment_available": equipment,
          "workout_type": workoutType,
          "difficulty": difficulty
        }),
      );

      if (response.statusCode == 200) {
        return jsonDecode(response.body);
      } else {
        print("Backend Error: ${response.body}");
        return _getFallbackWorkout(workoutType);
      }
    } catch (e) {
      print("Network Error: $e");
      return _getFallbackWorkout(workoutType);
    }
  }

  Map<String, dynamic> _getFallbackWorkout(String type) {
     return {
        "title": "Offline $type Session",
        "focus": "Connection Issue",
        "duration": 45,
        "exercises": [
          {"name": "Jumping Jacks", "sets": 3, "reps": "50", "rest": "60s", "note": "Warmup"},
          {"name": "Pushups", "sets": 4, "reps": "15", "rest": "90s", "note": "Basic Strength"},
          {"name": "Squats", "sets": 4, "reps": "20", "rest": "90s", "note": "Basic Strength"}
        ],
        "intensity": "Low",
        "reasoning": "Could not connect to AI Brain. Loading emergency protocol."
      };
  }

  Future<void> submitFeedback(int sessionId, int rpe, int enjoyment, Map<String, int> soreness) async {
    final token = await _authService.getToken();
    await http.post(
      Uri.parse('$_baseUrl/ai-trainer/feedback'),
      headers: {
        "Content-Type": "application/json",
        "Authorization": "Bearer $token"
      },
      body: jsonEncode({
        "training_session_id": sessionId,
        "rpe": rpe,
        "enjoyment": enjoyment,
        "soreness_map": soreness
      }),
    );
  }
}
