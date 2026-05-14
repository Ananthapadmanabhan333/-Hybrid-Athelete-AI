
import 'package:flutter/material.dart';
import '../../core/app_theme.dart';
import 'models.dart';

class MonthlyCalorieTrackerCard extends StatelessWidget {
  final MonthlyCalorieSummary summary;

  const MonthlyCalorieTrackerCard({super.key, required this.summary});

  @override
  Widget build(BuildContext context) {
    double progress = (summary.caloriesConsumedSoFar / summary.monthlyCalorieTarget).clamp(0.0, 1.0);
    int remaining = summary.monthlyCalorieTarget - summary.caloriesConsumedSoFar;

    return Container(
      padding: const EdgeInsets.all(20),
      decoration: BoxDecoration(
        color: AppTheme.surfaceColor,
        borderRadius: BorderRadius.circular(20),
        border: Border.all(color: Colors.white.withOpacity(0.05)),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              Text("MONTHLY BUDGET", style: Theme.of(context).textTheme.titleSmall?.copyWith(color: Colors.grey)),
              Text("${(progress * 100).toInt()}%", style: const TextStyle(fontWeight: FontWeight.bold, color: AppTheme.accentColor)),
            ],
          ),
          const SizedBox(height: 16),
          LinearProgressIndicator(
            value: progress,
            backgroundColor: Colors.white10,
            color: progress > 1.0 ? Colors.redAccent : AppTheme.primaryColor,
            minHeight: 12,
            borderRadius: BorderRadius.circular(6),
          ),
          const SizedBox(height: 16),
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              _buildStat("Consumed", "${summary.caloriesConsumedSoFar}", Colors.white),
              _buildStat("Target", "${summary.monthlyCalorieTarget}", Colors.grey),
              _buildStat("Remaining", "$remaining", remaining < 0 ? Colors.redAccent : Colors.greenAccent),
            ],
          ),
        ],
      ),
    );
  }

  Widget _buildStat(String label, String value, Color color) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text(value, style: TextStyle(fontWeight: FontWeight.bold, fontSize: 16, color: color)),
        Text(label, style: const TextStyle(color: Colors.grey, fontSize: 10)),
      ],
    );
  }
}

class ProjectedWeightCard extends StatelessWidget {
  final double projectedChange;
  final String goalType;

  const ProjectedWeightCard({super.key, required this.projectedChange, required this.goalType});

  @override
  Widget build(BuildContext context) {
    bool isPositive = projectedChange > 0;
    Color color = isPositive 
        ? (goalType == 'bulk' ? Colors.greenAccent : Colors.redAccent)
        : (goalType == 'cut' ? Colors.greenAccent : Colors.redAccent);

    return Container(
      padding: const EdgeInsets.all(20),
      decoration: BoxDecoration(
        color: AppTheme.surfaceColor,
        borderRadius: BorderRadius.circular(20),
      ),
      child: Row(
        children: [
          Container(
            padding: const EdgeInsets.all(12),
            decoration: BoxDecoration(shape: BoxShape.circle, color: color.withOpacity(0.1)),
            child: Icon(isPositive ? Icons.trending_up : Icons.trending_down, color: color),
          ),
          const SizedBox(width: 16),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text("PROJECTED CHANGE", style: Theme.of(context).textTheme.bodySmall?.copyWith(color: Colors.grey)),
                const SizedBox(height: 4),
                Text(
                  "${isPositive ? '+' : ''}${projectedChange.toStringAsFixed(2)} kg",
                  style: Theme.of(context).textTheme.headlineSmall?.copyWith(color: color, fontWeight: FontWeight.bold),
                ),
                Text("Based on this month's surplus/deficit", style: TextStyle(color: Colors.white30, fontSize: 10)),
              ],
            ),
          ),
        ],
      ),
    );
  }
}

class NutritionInsightsCard extends StatelessWidget {
  final NutritionInsights insights;

  const NutritionInsightsCard({super.key, required this.insights});

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.all(20),
      decoration: BoxDecoration(
        color: AppTheme.surfaceColor,
        borderRadius: BorderRadius.circular(20),
        border: Border.all(color: AppTheme.primaryColor.withOpacity(0.2)),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            children: [
              const Icon(Icons.lightbulb, color: Colors.yellowAccent, size: 20),
              const SizedBox(width: 8),
              Text("AI NUTRITIONIST", style: Theme.of(context).textTheme.titleMedium),
            ],
          ),
          const SizedBox(height: 16),
          ...insights.insights.map((text) => Padding(
            padding: const EdgeInsets.only(bottom: 8),
            child: Row(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                const Icon(Icons.arrow_right, color: Colors.grey),
                Expanded(child: Text(text, style: const TextStyle(color: Colors.white70))),
              ],
            ),
          )),
          const Divider(color: Colors.white10, height: 24),
          ...insights.actionableTips.map((text) => Padding(
            padding: const EdgeInsets.only(bottom: 8),
            child: Row(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                const Icon(Icons.check_circle_outline, color: AppTheme.accentColor, size: 16),
                const SizedBox(width: 8),
                Expanded(child: Text(text, style: const TextStyle(color: Colors.white, fontWeight: FontWeight.w500))),
              ],
            ),
          )),
        ],
      ),
    );
  }
}
