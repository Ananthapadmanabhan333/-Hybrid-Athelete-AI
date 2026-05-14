import 'package:flutter/material.dart';
import '../../core/app_theme.dart';
import '../nutrition_v2/service.dart';
import '../nutrition_v2/models.dart';
import '../nutrition_v2/widgets.dart';

class NutritionScreen extends StatefulWidget {
  const NutritionScreen({super.key});

  @override
  State<NutritionScreen> createState() => _NutritionScreenState();
}

class _NutritionScreenState extends State<NutritionScreen> {
  // Hardcoded for MVP, ideally fetched from Profile
  double _dailyTarget = 2800;
  double _consumed = 1200;
  
  // V2 Data
  final NutritionServiceV2 _v2Service = NutritionServiceV2();
  MonthlyCalorieSummary? _monthlySummary;
  NutritionInsights? _insights;

  @override
  void initState() {
    super.initState();
    _loadV2Data();
  }

  Future<void> _loadV2Data() async {
    try {
      final summary = await _v2Service.getMonthlySummary();
      final insights = await _v2Service.getInsights();
      if (mounted) {
        setState(() {
          _monthlySummary = summary;
          _insights = insights;
        });
      }
    } catch (e) {
      debugPrint("Error loading V2 data: $e");
    }
  }

  // Local list of meals
  final List<Map<String, String>> _meals = [
    {"name": "Oatmeal & Whey", "type": "Breakfast", "calories": "450"},
    {"name": "Chicken Breast & Rice", "type": "Lunch", "calories": "600"},
    {"name": "Protein Shake", "type": "Snack", "calories": "150"},
  ];

  void _addFood(String name, String calories) {
    setState(() {
      _meals.insert(0, {
        "name": name, 
        "type": "Snack", // Defaulting to Snack for simplicity
        "calories": calories
      });
      _consumed += double.tryParse(calories) ?? 0;
    });
    Navigator.pop(context);
  }

  void _showAddFoodDialog() {
    final nameController = TextEditingController();
    final caloriesController = TextEditingController();

    showModalBottomSheet(
      context: context,
      isScrollControlled: true,
      backgroundColor: AppTheme.surfaceColor,
      shape: const RoundedRectangleBorder(
        borderRadius: BorderRadius.vertical(top: Radius.circular(20)),
      ),
      builder: (context) {
        return Padding(
          padding: EdgeInsets.only(
            bottom: MediaQuery.of(context).viewInsets.bottom,
            top: 20,
            left: 20,
            right: 20
          ),
          child: Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              const Text("Add Food", style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold, color: Colors.white)),
              const SizedBox(height: 16),
              TextField(
                controller: nameController,
                style: const TextStyle(color: Colors.white),
                decoration: const InputDecoration(labelText: "Food Name"),
              ),
              const SizedBox(height: 16),
              TextField(
                controller: caloriesController,
                style: const TextStyle(color: Colors.white),
                keyboardType: TextInputType.number,
                decoration: const InputDecoration(labelText: "Calories"),
              ),
              const SizedBox(height: 24),
              ElevatedButton(
                onPressed: () => _addFood(nameController.text, caloriesController.text),
                child: const Text("ADD LOG"),
              ),
              const SizedBox(height: 24),
            ],
          ),
        );
      },
    );
  }

  @override
  Widget build(BuildContext context) {
    double progress = (_consumed / _dailyTarget).clamp(0.0, 1.0);
    
    return Scaffold(
      appBar: AppBar(title: const Text("Nutrition")),
      floatingActionButton: FloatingActionButton(
        onPressed: _showAddFoodDialog,
        backgroundColor: AppTheme.primaryColor,
        child: const Icon(Icons.add, color: Colors.black),
      ),
      body: ListView(
        padding: const EdgeInsets.all(16),
        children: [
          _buildSummaryCard(progress),
          const SizedBox(height: 24),
          const Text("Today's Logs", style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
          const SizedBox(height: 16),
          ..._meals.map((meal) => _buildMealItem(
            meal["name"]!, 
            meal["type"]!, 
            "${meal["calories"]} kcal"
          )).toList(),
        ],
      ),
    );
  }

  Widget _buildSummaryCard(double progress) {
    return Column(
      children: [
        // Legacy Daily Card
        Container(
          padding: const EdgeInsets.all(20),
          decoration: BoxDecoration(
            gradient: LinearGradient(
              colors: [AppTheme.secondaryColor.withOpacity(0.8), AppTheme.secondaryColor.withOpacity(0.4)],
              begin: Alignment.topLeft,
              end: Alignment.bottomRight,
            ),
            borderRadius: BorderRadius.circular(20),
          ),
          child: Column(
            children: [
              const Text("Daily Calorie Goal", style: TextStyle(color: Colors.white70)),
              const SizedBox(height: 8),
              Text("${_consumed.toInt()} / ${_dailyTarget.toInt()}", style: const TextStyle(fontSize: 32, fontWeight: FontWeight.bold, color: Colors.white)),
              const SizedBox(height: 16),
              LinearProgressIndicator(
                value: progress,
                backgroundColor: Colors.black26,
                valueColor: const AlwaysStoppedAnimation<Color>(Colors.white),
                minHeight: 8,
                borderRadius: BorderRadius.circular(4),
              ),
              const SizedBox(height: 16),
              const Row(
                mainAxisAlignment: MainAxisAlignment.spaceAround,
                children: [
                  Text("P: 120g", style: TextStyle(fontWeight: FontWeight.bold)),
                  Text("C: 100g", style: TextStyle(fontWeight: FontWeight.bold)),
                  Text("F: 40g", style: TextStyle(fontWeight: FontWeight.bold)),
                ],
              )
            ],
          ),
        ),
        
        const SizedBox(height: 24),
        
        // V2 Monthly Tracker
        if (_monthlySummary != null) ...[
          MonthlyCalorieTrackerCard(summary: _monthlySummary!),
          const SizedBox(height: 16),
          ProjectedWeightCard(projectedChange: _monthlySummary!.projectedWeightChange, goalType: _monthlySummary!.goalType),
          const SizedBox(height: 16),
        ],
        
        // V2 Insights
        if (_insights != null) ...[
          NutritionInsightsCard(insights: _insights!),
          const SizedBox(height: 24),
        ],
      ],
    );
  }

  Widget _buildMealItem(String name, String type, String calories) {
    return Container(
      margin: const EdgeInsets.only(bottom: 12),
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: AppTheme.surfaceColor,
        borderRadius: BorderRadius.circular(12),
      ),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceBetween,
        children: [
          Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text(name, style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 16)),
              Text(type, style: const TextStyle(color: Colors.grey, fontSize: 12)),
            ],
          ),
          Text(calories, style: const TextStyle(color: AppTheme.secondaryColor, fontWeight: FontWeight.bold)),
        ],
      ),
    );
  }
}
