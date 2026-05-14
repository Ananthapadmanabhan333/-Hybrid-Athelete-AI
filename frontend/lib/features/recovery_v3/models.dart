
class RecoveryLogV3 {
  final int? id;
  final DateTime date;
  final double sleepDuration;
  final int sleepQuality;
  final int hrv;
  final int restingHeartRate;
  final int muscleSoreness;
  final int stressLevel;
  final double hydrationLiters;
  final String? mood;
  final String? notes;

  RecoveryLogV3({
    this.id,
    required this.date,
    required this.sleepDuration,
    required this.sleepQuality,
    required this.hrv,
    required this.restingHeartRate,
    required this.muscleSoreness,
    required this.stressLevel,
    required this.hydrationLiters,
    this.mood,
    this.notes,
  });

  Map<String, dynamic> toJson() {
    return {
      'sleep_duration': sleepDuration,
      'sleep_quality': sleepQuality,
      'hrv': hrv,
      'resting_heart_rate': restingHeartRate,
      'muscle_soreness': muscleSoreness,
      'stress_level': stressLevel,
      'hydration_liters': hydrationLiters,
      'mood': mood,
      'notes': notes,
    };
  }

  factory RecoveryLogV3.fromJson(Map<String, dynamic> json) {
    return RecoveryLogV3(
      id: json['id'],
      date: DateTime.parse(json['date']),
      sleepDuration: json['sleep_duration'].toDouble(),
      sleepQuality: json['sleep_quality'],
      hrv: json['hrv'],
      restingHeartRate: json['resting_heart_rate'],
      muscleSoreness: json['muscle_soreness'],
      stressLevel: json['stress_level'],
      hydrationLiters: json['hydration_liters'].toDouble(),
      mood: json['mood'],
      notes: json['notes'],
    );
  }
}

class RecoveryScoreV3 {
  final double totalScore;
  final String category;
  final double sleepComponent;
  final double hrvComponent;
  final double rhrComponent;
  final double sorenessComponent;
  final double stressComponent;
  final double hydrationComponent;

  RecoveryScoreV3({
    required this.totalScore,
    required this.category,
    required this.sleepComponent,
    required this.hrvComponent,
    required this.rhrComponent,
    required this.sorenessComponent,
    required this.stressComponent,
    required this.hydrationComponent,
  });

  factory RecoveryScoreV3.fromJson(Map<String, dynamic> json) {
    return RecoveryScoreV3(
      totalScore: json['total_score'].toDouble(),
      category: json['category'],
      sleepComponent: json['sleep_component'].toDouble(),
      hrvComponent: json['hrv_component'].toDouble(),
      rhrComponent: json['rhr_component'].toDouble(),
      sorenessComponent: json['soreness_component'].toDouble(),
      stressComponent: json['stress_component'].toDouble(),
      hydrationComponent: json['hydration_component'].toDouble(),
    );
  }
}

class RecoveryRecommendation {
  final String text;
  final String type;
  final int priority;

  RecoveryRecommendation({required this.text, required this.type, required this.priority});

  factory RecoveryRecommendation.fromJson(Map<String, dynamic> json) {
    return RecoveryRecommendation(
      text: json['recommendation_text'],
      type: json['type'],
      priority: json['priority'],
    );
  }
}

class RecoveryDailySummary {
  final RecoveryScoreV3? score;
  final List<RecoveryRecommendation> recommendations;

  RecoveryDailySummary({this.score, required this.recommendations});

  factory RecoveryDailySummary.fromJson(Map<String, dynamic> json) {
    return RecoveryDailySummary(
      score: json['score'] != null ? RecoveryScoreV3.fromJson(json['score']) : null,
      recommendations: (json['recommendations'] as List).map((e) => RecoveryRecommendation.fromJson(e)).toList(),
    );
  }
}
