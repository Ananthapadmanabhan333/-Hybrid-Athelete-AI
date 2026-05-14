
import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import '../../core/constants.dart';
import '../../services/auth_service.dart';
import 'widgets/ai_nutritionist_card.dart';
import 'widgets/nutrition_chat_window.dart';

class NutritionDashboard extends StatefulWidget {
  const NutritionDashboard({super.key});

  @override
  State<NutritionDashboard> createState() => _NutritionDashboardState();
}

class _NutritionDashboardState extends State<NutritionDashboard> {
  Map<String, dynamic>? _insights;
  final AuthService _authService = AuthService();

  @override
  void initState() {
    super.initState();
    _fetchInsights();
  }

  Future<void> _fetchInsights() async {
    try {
      final token = await _authService.getToken();
      final response = await http.post(
        Uri.parse('${AppConstants.apiBaseUrl}/agents/nutrition/analyze'),
        headers: {"Authorization": "Bearer $token"},
      );
      if (response.statusCode == 200) {
        setState(() {
          _insights = jsonDecode(response.body);
        });
      } else {
        setState(() {
          _insights = {"summary_insight": "Failed to load active insights. Status: ${response.statusCode}"};
        });
      }
    } catch (e) {
      setState(() {
        _insights = {"summary_insight": "Connection Error: $e"};
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Nutrition Intelligence')),
      body: SingleChildScrollView(
        child: Column(
          children: [
            _buildMacroSummary(),
            const SizedBox(height: 16),
            Padding(
              padding: const EdgeInsets.symmetric(horizontal: 16),
              child: AINutritionistCard(
                insights: _insights,
                onChatPressed: () {
                  Navigator.push(context, MaterialPageRoute(builder: (c) => const NutritionChatWindow()));
                },
              ),
            ),
            const SizedBox(height: 16),
            const Divider(),
            _buildFeatureTile(context, "Log Meal", Icons.add_a_photo),
            _buildFeatureTile(context, "Micronutrient Check", Icons.science),
            _buildFeatureTile(context, "Generate Shopping List", Icons.shopping_cart),
          ],
        ),
      ),
    );
  }

  Widget _buildMacroSummary() {
    return Container(
      padding: const EdgeInsets.all(16),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceAround,
        children: const [
          Column(children: [Text("Protein"), Text("120g/180g")]),
          Column(children: [Text("Carbs"), Text("200g/250g")]),
          Column(children: [Text("Fats"), Text("60g/80g")]),
        ],
      ),
    );
  }

  Widget _buildFeatureTile(BuildContext context, String title, IconData icon) {
    return ListTile(
      leading: Icon(icon),
      title: Text(title),
      trailing: const Icon(Icons.arrow_forward_ios),
      onTap: () {},
    );
  }
}
