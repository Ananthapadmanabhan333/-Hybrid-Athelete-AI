import 'package:flutter/material.dart';
import '../../../core/app_theme.dart';
import 'package:flutter_animate/flutter_animate.dart';

class AINutritionistCard extends StatelessWidget {
  final Map<String, dynamic>? insights;
  final VoidCallback onChatPressed;

  const AINutritionistCard({super.key, required this.insights, required this.onChatPressed});

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.all(20),
      decoration: BoxDecoration(
        color: AppTheme.surfaceColor,
        borderRadius: BorderRadius.circular(24),
        border: Border.all(color: AppTheme.accentColor.withOpacity(0.3)),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            children: [
              const Icon(Icons.restaurant_menu, color: AppTheme.accentColor),
              const SizedBox(width: 8),
              Text("AI NUTRITION AGENT", style: Theme.of(context).textTheme.titleMedium),
            ],
          ),
          const SizedBox(height: 16),
          
          if (insights == null)
            const Center(child: CircularProgressIndicator())
          else ...[
            Text(insights!['summary_insight'] ?? "", style: const TextStyle(height: 1.5, fontSize: 16)),
            
            if (insights!['warning'] != null && insights!['warning'].toString().toLowerCase() != 'null') ...[
              const SizedBox(height: 16),
              Container(
                padding: const EdgeInsets.all(12),
                decoration: BoxDecoration(
                  color: Colors.redAccent.withOpacity(0.1),
                  borderRadius: BorderRadius.circular(8),
                  border: Border.all(color: Colors.redAccent.withOpacity(0.5)),
                ),
                child: Row(
                  children: [
                    const Icon(Icons.warning_amber, color: Colors.redAccent, size: 20),
                    const SizedBox(width: 8),
                    Expanded(child: Text(insights!['warning'], style: const TextStyle(color: Colors.redAccent, fontSize: 12))),
                  ],
                ),
              ),
            ],

            const SizedBox(height: 16),
            const Text("Actionable Steps:", style: TextStyle(fontWeight: FontWeight.bold, color: Colors.grey)),
            const SizedBox(height: 8),
            
            if (insights!['actionable_steps'] != null)
              ...(insights!['actionable_steps'] as List).map((step) => Padding(
                padding: const EdgeInsets.only(bottom: 8.0),
                child: Row(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    const Icon(Icons.check_circle_outline, color: AppTheme.primaryColor, size: 16),
                    const SizedBox(width: 8),
                    Expanded(child: Text(step.toString(), style: const TextStyle(fontSize: 14))),
                  ],
                ),
              )).toList(),

            const SizedBox(height: 24),
            SizedBox(
              width: double.infinity,
              child: ElevatedButton.icon(
                onPressed: onChatPressed,
                icon: const Icon(Icons.chat_bubble_outline, color: Colors.black),
                label: const Text("CHAT WITH NUTRITIONIST", style: TextStyle(color: Colors.black, fontWeight: FontWeight.bold)),
                style: ElevatedButton.styleFrom(
                  backgroundColor: AppTheme.primaryColor,
                  padding: const EdgeInsets.symmetric(vertical: 16),
                ),
              ),
            ),
          ],
        ],
      ),
    ).animate().fadeIn(delay: 300.ms).slideY(begin: 0.1);
  }
}
