
import 'package:flutter/material.dart';

class HabitTracker extends StatelessWidget {
  const HabitTracker({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Habit Streaks')),
      body: ListView(
        padding: const EdgeInsets.all(16),
        children: [
          _buildHabitTile("Daily Water", 5, Icons.local_drink, Colors.blue),
          _buildHabitTile("Sleep 8h", 12, Icons.bed, Colors.purple),
          _buildHabitTile("Morning Stretch", 0, Icons.accessibility_new, Colors.orange),
          _buildHabitTile("Meditation", 3, Icons.self_improvement, Colors.green),
        ],
      ),
    );
  }

  Widget _buildHabitTile(String title, int streak, IconData icon, Color color) {
    return Card(
      child: ListTile(
        leading: Icon(icon, color: color),
        title: Text(title),
        trailing: Row(
          mainAxisSize: MainAxisSize.min,
          children: [
            const Icon(Icons.local_fire_department, color: Colors.orange),
            Text("$streak days"),
            Checkbox(value: false, onChanged: (v) {}),
          ],
        ),
      ),
    );
  }
}
