import 'package:flutter/material.dart';
import '../../core/app_theme.dart';
import '../../services/task_service.dart';
import '../../services/haptic_service.dart';
import 'package:flutter_animate/flutter_animate.dart';

class DailyTasksWidget extends StatefulWidget {
  const DailyTasksWidget({super.key});

  @override
  State<DailyTasksWidget> createState() => _DailyTasksWidgetState();
}

class _DailyTasksWidgetState extends State<DailyTasksWidget> {
  final TaskService _taskService = TaskService();
  final HapticService _hapticService = HapticService();
  List<Map<String, dynamic>> _tasks = [];
  bool _isLoading = true;

  @override
  void initState() {
    super.initState();
    _fetchTasks();
  }

  Future<void> _fetchTasks() async {
    final tasks = await _taskService.getDailyTasks();
    if (mounted) {
      setState(() {
        _tasks = tasks;
        _isLoading = false;
      });
    }
  }

  Future<void> _toggleTask(int id, bool isCompleted) async {
    if (isCompleted) return; // Already done
    
    _hapticService.success(); // Premium feel
    
    // Optimistic update
    setState(() {
      final index = _tasks.indexWhere((t) => t['id'] == id);
      if (index != -1) {
        _tasks[index]['is_completed'] = true;
      }
    });

    await _taskService.completeTask(id);
  }

  @override
  Widget build(BuildContext context) {
    if (_isLoading) return const SizedBox.shrink();
    if (_tasks.isEmpty) return const SizedBox.shrink();

    // Sort: Pending High Priority first
    _tasks.sort((a, b) {
      if (a['is_completed'] == b['is_completed']) return 0;
      return a['is_completed'] ? 1 : -1;
    });

    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text("TASKS & GOALS", style: Theme.of(context).textTheme.titleLarge),
        const SizedBox(height: 16),
        ..._tasks.map((task) => _buildTaskItem(task)),
      ],
    ).animate().fadeIn(duration: 600.ms);
  }

  Widget _buildTaskItem(Map<String, dynamic> task) {
    bool isDone = task['is_completed'];
    Color priorityColor = _getPriorityColor(task['priority']);
    
    return Container(
      margin: const EdgeInsets.only(bottom: 12),
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: AppTheme.surfaceColor,
        borderRadius: BorderRadius.circular(16),
        border: Border.all(
          color: isDone ? Colors.green.withOpacity(0.3) : priorityColor.withOpacity(0.5),
        ),
      ),
      child: Row(
        children: [
          GestureDetector(
            onTap: () => _toggleTask(task['id'], isDone),
            child: AnimatedContainer(
              duration: const Duration(milliseconds: 300),
              width: 24,
              height: 24,
              decoration: BoxDecoration(
                color: isDone ? Colors.green : Colors.transparent,
                shape: BoxShape.circle,
                border: Border.all(color: isDone ? Colors.green : Colors.grey),
              ),
              child: isDone ? const Icon(Icons.check, size: 16, color: Colors.white) : null,
            ),
          ),
          const SizedBox(width: 16),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  task['title'],
                  style: TextStyle(
                    fontWeight: FontWeight.bold,
                    decoration: isDone ? TextDecoration.lineThrough : null,
                    color: isDone ? Colors.grey : Colors.white,
                  ),
                ),
                Text(
                  task['message'],
                  style: TextStyle(
                    fontSize: 12,
                    color: isDone ? Colors.grey : Colors.white70,
                  ),
                ),
              ],
            ),
          ),
          if (!isDone)
            Container(
              padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
              decoration: BoxDecoration(
                color: priorityColor.withOpacity(0.2),
                borderRadius: BorderRadius.circular(8),
              ),
              child: Text(
                task['category'].toString().toUpperCase(),
                style: TextStyle(fontSize: 10, color: priorityColor, fontWeight: FontWeight.bold),
              ),
            ),
        ],
      ),
    );
  }

  Color _getPriorityColor(String priority) {
    switch (priority.toLowerCase()) {
      case 'high': return Colors.redAccent;
      case 'medium': return Colors.orangeAccent;
      default: return Colors.blueAccent;
    }
  }
}
