
class MonthlyCalorieSummary {
  final int month;
  final int year;
  final int dailyCalorieTarget;
  final int monthlyCalorieTarget;
  final int caloriesConsumedSoFar;
  final int surplusOrDeficit;
  final double projectedWeightChange;
  final String goalType;
  final double proteinCompliancePct;
  final double carbConsistencyPct;
  final double hydrationAdherencePct;
  final double micronutrientScore;
  final double monthlyNutritionScore;

  MonthlyCalorieSummary({
    required this.month,
    required this.year,
    required this.dailyCalorieTarget,
    required this.monthlyCalorieTarget,
    required this.caloriesConsumedSoFar,
    required this.surplusOrDeficit,
    required this.projectedWeightChange,
    required this.goalType,
    required this.proteinCompliancePct,
    required this.carbConsistencyPct,
    required this.hydrationAdherencePct,
    required this.micronutrientScore,
    required this.monthlyNutritionScore,
  });

  factory MonthlyCalorieSummary.fromJson(Map<String, dynamic> json) {
    return MonthlyCalorieSummary(
      month: json['month'],
      year: json['year'],
      dailyCalorieTarget: json['daily_calorie_target'],
      monthlyCalorieTarget: json['monthly_calorie_target'],
      caloriesConsumedSoFar: json['calories_consumed_so_far'],
      surplusOrDeficit: json['surplus_or_deficit'],
      projectedWeightChange: json['projected_weight_change'].toDouble(),
      goalType: json['goal_type'],
      proteinCompliancePct: json['protein_compliance_pct'].toDouble(),
      carbConsistencyPct: json['carb_consistency_pct'].toDouble(),
      hydrationAdherencePct: json['hydration_adherence_pct'].toDouble(),
      micronutrientScore: json['micronutrient_score'].toDouble(),
      monthlyNutritionScore: json['monthly_nutrition_score'].toDouble(),
    );
  }
}

class NutritionInsights {
  final List<String> insights;
  final List<String> actionableTips;
  final String status;

  NutritionInsights({required this.insights, required this.actionableTips, required this.status});

  factory NutritionInsights.fromJson(Map<String, dynamic> json) {
    return NutritionInsights(
      insights: List<String>.from(json['insights']),
      actionableTips: List<String>.from(json['actionable_tips']),
      status: json['status'],
    );
  }
}
