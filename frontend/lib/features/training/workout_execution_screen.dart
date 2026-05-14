import 'dart:async';
import 'package:flutter/material.dart';
import 'package:video_player/video_player.dart';
import 'package:chewie/chewie.dart';
import '../../core/app_theme.dart';
import 'feedback_modal.dart';
import '../../services/ai_trainer_service.dart';

class WorkoutExecutionScreen extends StatefulWidget {
  final String workoutType;
  final String difficulty;
  const WorkoutExecutionScreen({super.key, required this.workoutType, required this.difficulty});

  @override
  State<WorkoutExecutionScreen> createState() => _WorkoutExecutionScreenState();
}

class _WorkoutExecutionScreenState extends State<WorkoutExecutionScreen> {
  final AITrainerService _aiTrainerService = AITrainerService();
  bool _isLoading = true;
  Map<String, dynamic>? _workoutPlan;
  
  Timer? _timer;
  int _secondsElapsed = 0;
  bool _isActive = false;

  @override
  void initState() {
    super.initState();
    _fetchWorkout();
  }

  Future<void> _fetchWorkout() async {
    // Default equipment simulation
    List<String> equipment = ["bodyweight", "dumbbells"]; 
    if (widget.workoutType == "Boxing") equipment.add("boxing_gloves");
    if (widget.workoutType == "Strength") equipment.add("barbell");

    final plan = await _aiTrainerService.generateDailyWorkout(
      45, // Default time
      equipment,
      widget.workoutType,
      widget.difficulty
    );

    if (mounted) {
      setState(() {
        _workoutPlan = plan;
        _isLoading = false;
      });
    }
  }

  void _toggleTimer() {
    setState(() {
      _isActive = !_isActive;
    });

    if (_isActive) {
      _timer = Timer.periodic(const Duration(seconds: 1), (timer) {
        setState(() {
          _secondsElapsed++;
        });
      });
    } else {
      _timer?.cancel();
    }
  }

  void _finishWorkout() {
    _timer?.cancel();
    showModalBottomSheet(
      context: context, 
      isScrollControlled: true,
      backgroundColor: Colors.transparent,
      builder: (context) => FeedbackModal(
        onSubmit: (rpe, enjoyment, soreness) {
           Navigator.pop(context); // Close feedback
           Navigator.pop(context); // Close workout screen
        },
      )
    );
  }

  String _formatTime(int seconds) {
    int minutes = seconds ~/ 60;
    int remainingSeconds = seconds % 60;
    return '${minutes.toString().padLeft(2, '0')}:${remainingSeconds.toString().padLeft(2, '0')}';
  }

  @override
  void dispose() {
    _timer?.cancel();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text("${widget.difficulty} ${widget.workoutType}")),
      body: _isLoading 
        ? const Center(child: CircularProgressIndicator(color: AppTheme.primaryColor))
        : Column(
            children: [
              // Header Context
              Container(
                padding: const EdgeInsets.all(16),
                color: AppTheme.surfaceColor,
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(_workoutPlan?['title'] ?? "Workout", style: const TextStyle(fontSize: 20, fontWeight: FontWeight.bold, color: Colors.white)),
                    const SizedBox(height: 8),
                    Text(_workoutPlan?['reasoning'] ?? "", style: const TextStyle(fontSize: 14, color: Colors.grey)),
                  ],
                ),
              ),
              // Timer Display
              Container(
                height: 100,
                alignment: Alignment.center,
                child: Text(
                  _formatTime(_secondsElapsed),
                  style: TextStyle(
                    fontSize: 48, 
                    fontWeight: FontWeight.bold, 
                    color: _isActive ? AppTheme.primaryColor : Colors.white
                  ),
                ),
              ),
              // Controls
              Row(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  IconButton(icon: const Icon(Icons.stop_circle, color: Colors.red, size: 48), onPressed: _finishWorkout),
                  const SizedBox(width: 32),
                  IconButton(
                    icon: Icon(_isActive ? Icons.pause_circle : Icons.play_circle, color: AppTheme.primaryColor, size: 64), 
                    onPressed: _toggleTimer
                  ),
                ],
              ),
              const Divider(color: Colors.grey),
              // Exercise List
              Expanded(
                child: ListView.builder(
                  padding: const EdgeInsets.all(16),
                  itemCount: (_workoutPlan?['exercises'] as List).length,
                  itemBuilder: (context, index) {
                    final exercise = _workoutPlan!['exercises'][index];
                    return Card(
                      color: Colors.black45,
                      margin: const EdgeInsets.only(bottom: 12),
                      child: ListTile(
                        leading: CircleAvatar(
                          backgroundColor: AppTheme.primaryColor.withOpacity(0.2),
                          child: Text("${index + 1}", style: const TextStyle(color: AppTheme.primaryColor)),
                        ),
                        title: Text(exercise['name'], style: const TextStyle(color: Colors.white, fontWeight: FontWeight.bold)),
                        subtitle: Text("${exercise['sets']} sets x ${exercise['reps']} • Rest: ${exercise['rest'] ?? '60s'}", style: const TextStyle(color: Colors.white70)),
                        trailing: exercise['note'] != null 
                          ? Tooltip(message: exercise['note'], child: const Icon(Icons.info_outline, color: Colors.grey))
                          : null,
                      ),
                    );
                  },
                ),
              ),
            ],
          ),
    );
  }
  Widget _buildMainButton() {
    return GestureDetector(
      onTap: _toggleTimer,
      child: Container(
        width: 80,
        height: 80,
        decoration: BoxDecoration(
          color: _isActive ? Colors.orange : AppTheme.primaryColor,
          shape: BoxShape.circle,
        ),
        child: Icon(
          _isActive ? Icons.pause : Icons.play_arrow,
          size: 40,
          color: Colors.black,
        ),
      ),
    );
  }

  Widget _buildControlButton(IconData icon, Color color, VoidCallback onTap) {
    return IconButton(
      onPressed: onTap,
      icon: Icon(icon, color: color, size: 32),
    );
  }
}
