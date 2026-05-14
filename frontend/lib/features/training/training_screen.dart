import 'package:flutter/material.dart';
import '../../core/app_theme.dart';
import 'workout_execution_screen.dart';

class TrainingScreen extends StatefulWidget {
  const TrainingScreen({super.key});

  @override
  State<TrainingScreen> createState() => _TrainingScreenState();
}

class _TrainingScreenState extends State<TrainingScreen> {
  String _difficulty = 'Intermediate';

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text("Training")),
      body: Column(
        children: [
          Container(
            padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 12),
            color: AppTheme.surfaceColor,
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                const Text("Pro Intensity Level:", style: TextStyle(fontWeight: FontWeight.bold, fontSize: 14, color: Colors.grey)),
                const SizedBox(height: 8),
                Row(
                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                  children: ["Beginner", "Intermediate", "Advanced"].map((String level) {
                    final isSelected = _difficulty == level;
                    return InkWell(
                      onTap: () => setState(() => _difficulty = level),
                      child: Container(
                        padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
                        decoration: BoxDecoration(
                          color: isSelected ? _getDifficultyColor(level) : Colors.transparent,
                          borderRadius: BorderRadius.circular(20),
                          border: Border.all(color: _getDifficultyColor(level).withOpacity(0.5)),
                        ),
                        child: Text(
                          level, 
                          style: TextStyle(
                            color: isSelected ? Colors.black : Colors.white, 
                            fontWeight: FontWeight.bold
                          )
                        ),
                      ),
                    );
                  }).toList(),
                ),
              ],
            ),
          ),
          Expanded(
            child: ListView(
              padding: const EdgeInsets.all(16),
              children: [
                _buildModuleCard(
                  context, 
                  "Strength", 
                  Icons.fitness_center, 
                  Colors.orangeAccent,
                  subtitle: "Hypertrophy & Power (Pro Split)"
                ),
                _buildModuleCard(
                  context, 
                  "Boxing", 
                  Icons.sports_mma, 
                  Colors.redAccent,
                  subtitle: "Technical & Conditioning"
                ),
                _buildModuleCard(
                  context, 
                  "Cardio", 
                  Icons.directions_run, 
                  Colors.blueAccent,
                  subtitle: "Endurance Protocols"
                ),
                _buildModuleCard(
                  context, 
                  "Athletics", 
                  Icons.speed, 
                  Colors.greenAccent,
                  subtitle: "Speed & Agility"
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }

  Color _getDifficultyColor(String level) {
    switch (level) {
      case 'Beginner': return Colors.green;
      case 'Intermediate': return Colors.orange;
      case 'Advanced': return Colors.red;
      default: return Colors.white;
    }
  }

  Widget _buildModuleCard(BuildContext context, String title, IconData icon, Color color, {String subtitle = "Standard Routine"}) {
    return Card(
      margin: const EdgeInsets.only(bottom: 16),
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
      child: ListTile(
        contentPadding: const EdgeInsets.all(20),
        leading: Container(
          padding: const EdgeInsets.all(12),
          decoration: BoxDecoration(
            color: color.withOpacity(0.2),
            shape: BoxShape.circle,
          ),
          child: Icon(icon, color: color, size: 28),
        ),
        title: Text(
          title, 
          style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 18)
        ),
        subtitle: Text(subtitle, style: const TextStyle(color: Colors.grey, fontSize: 12)),
        trailing: const Icon(Icons.arrow_forward_ios, size: 16),
        onTap: () {
          Navigator.push(
            context,
            MaterialPageRoute(
              builder: (context) => WorkoutExecutionScreen(
                workoutType: title,
                difficulty: _difficulty,
              ),
            ),
          );
        },
      ),
    );
  }
}
