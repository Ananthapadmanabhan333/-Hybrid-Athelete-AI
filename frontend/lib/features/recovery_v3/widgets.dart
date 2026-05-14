
import 'package:flutter/material.dart';
import '../../core/app_theme.dart';
import 'models.dart';

class RecoveryScoreCardV3 extends StatelessWidget {
  final RecoveryScoreV3 score;

  const RecoveryScoreCardV3({super.key, required this.score});

  @override
  Widget build(BuildContext context) {
    Color scoreColor = _getScoreColor(score.totalScore);

    return Container(
      padding: const EdgeInsets.all(24),
      decoration: BoxDecoration(
        gradient: LinearGradient(
          colors: [scoreColor.withOpacity(0.2), Colors.transparent],
          begin: Alignment.topLeft,
          end: Alignment.bottomRight,
        ),
        borderRadius: BorderRadius.circular(24),
        border: Border.all(color: scoreColor.withOpacity(0.3)),
      ),
      child: Column(
        children: [
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text("RECOVERY SCORE", style: Theme.of(context).textTheme.titleSmall?.copyWith(color: Colors.grey)),
                  const SizedBox(height: 8),
                  Text(
                    score.totalScore.toStringAsFixed(0),
                    style: TextStyle(
                      fontSize: 48,
                      fontWeight: FontWeight.bold,
                      color: scoreColor,
                      height: 1.0,
                    ),
                  ),
                ],
              ),
              Container(
                padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
                decoration: BoxDecoration(
                  color: scoreColor.withOpacity(0.2),
                  borderRadius: BorderRadius.circular(20),
                  border: Border.all(color: scoreColor),
                ),
                child: Text(
                  score.category.toUpperCase(),
                  style: TextStyle(color: scoreColor, fontWeight: FontWeight.bold, fontSize: 12),
                ),
              ),
            ],
          ),
          const SizedBox(height: 24),
          const Divider(color: Colors.white10),
          const SizedBox(height: 16),
          _buildDetailRow("Sleep", score.sleepComponent, 25), // 25 is max score for sleep
          _buildDetailRow("HRV", score.hrvComponent, 20),
          _buildDetailRow("Stability", score.rhrComponent, 15),
          _buildDetailRow("Strain", score.sorenessComponent + score.stressComponent, 30),
        ],
      ),
    );
  }
  
  Widget _buildDetailRow(String label, double value, double max) {
    double progress = (value / max).clamp(0.0, 1.0);
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 4),
      child: Row(
        children: [
          SizedBox(width: 80, child: Text(label, style: const TextStyle(color: Colors.white70, fontSize: 12))),
          Expanded(
            child: LinearProgressIndicator(
              value: progress,
              backgroundColor: Colors.white10,
              valueColor: AlwaysStoppedAnimation(AppTheme.primaryColor),
              minHeight: 4,
              borderRadius: BorderRadius.circular(2),
            ),
          ),
          const SizedBox(width: 12),
          SizedBox(width: 30, child: Text("${value.toInt()}", style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 12))),
        ],
      ),
    );
  }

  Color _getScoreColor(double score) {
    if (score >= 85) return Colors.greenAccent;
    if (score >= 70) return Colors.blueAccent;
    if (score >= 50) return Colors.orangeAccent;
    return Colors.redAccent;
  }
}

class RecoveryLogForm extends StatefulWidget {
  final Function(RecoveryLogV3) onSubmit;

  const RecoveryLogForm({super.key, required this.onSubmit});

  @override
  State<RecoveryLogForm> createState() => _RecoveryLogFormState();
}

class _RecoveryLogFormState extends State<RecoveryLogForm> {
  final _formKey = GlobalKey<FormState>();
  
  // Values
  double _sleepDuration = 7.0;
  double _sleepQuality = 5.0;
  double _soreness = 3.0;
  double _stress = 3.0;
  double _hydration = 1.5;
  int _hrv = 50;
  int _rhr = 60;
  final TextEditingController _notesController = TextEditingController();

  @override
  Widget build(BuildContext context) {
    return Form(
      key: _formKey,
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text("LOG METRICS (V3)", style: Theme.of(context).textTheme.titleMedium),
          const SizedBox(height: 16),
          
          _buildSlider("Quality (1-10)", _sleepQuality, 1, 10, (v) => setState(() => _sleepQuality = v)),
          _buildSlider("Soreness (1-10)", _soreness, 1, 10, (v) => setState(() => _soreness = v)),
          _buildSlider("Stress (1-10)", _stress, 1, 10, (v) => setState(() => _stress = v)),
          
          const SizedBox(height: 16),
          
          Row(
            children: [
              Expanded(child: _buildNumInput("Hours Sleep", (v) => _sleepDuration = double.tryParse(v) ?? 7.0, "7.0")),
              const SizedBox(width: 12),
              Expanded(child: _buildNumInput("Hydration (L)", (v) => _hydration = double.tryParse(v) ?? 1.5, "1.5")),
            ],
          ),
          const SizedBox(height: 12),
          Row(
            children: [
              Expanded(child: _buildNumInput("HRV (ms)", (v) => _hrv = int.tryParse(v) ?? 50, "50")),
              const SizedBox(width: 12),
              Expanded(child: _buildNumInput("RHR (bpm)", (v) => _rhr = int.tryParse(v) ?? 60, "60")),
            ],
          ),
          
          const SizedBox(height: 24),
          SizedBox(
            width: double.infinity,
            child: ElevatedButton(
              onPressed: _submit,
              style: ElevatedButton.styleFrom(
                backgroundColor: AppTheme.primaryColor,
                padding: const EdgeInsets.symmetric(vertical: 16),
              ),
              child: const Text("CALCULATE RECOVERY SCORE", style: TextStyle(color: Colors.black, fontWeight: FontWeight.bold)),
            ),
          ),
        ],
      ),
    );
  }

  void _submit() {
    if (_formKey.currentState!.validate()) {
      final log = RecoveryLogV3(
        date: DateTime.now(),
        sleepDuration: _sleepDuration,
        sleepQuality: _sleepQuality.toInt(),
        hrv: _hrv,
        restingHeartRate: _rhr,
        muscleSoreness: _soreness.toInt(),
        stressLevel: _stress.toInt(),
        hydrationLiters: _hydration,
        mood: "Neutral",
        notes: _notesController.text,
      );
      widget.onSubmit(log);
    }
  }

  Widget _buildSlider(String label, double value, double min, double max, Function(double) onChanged) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Row(
          mainAxisAlignment: MainAxisAlignment.spaceBetween,
          children: [
            Text(label, style: const TextStyle(color: Colors.grey, fontSize: 12)),
            Text(value.toInt().toString(), style: const TextStyle(fontWeight: FontWeight.bold)),
          ],
        ),
        Slider(
          value: value,
          min: min,
          max: max,
          divisions: (max - min).toInt(),
          activeColor: AppTheme.primaryColor,
          inactiveColor: Colors.white10,
          onChanged: onChanged,
        ),
      ],
    );
  }

  Widget _buildNumInput(String label, Function(String) onSave, String hint) {
    return TextFormField(
      decoration: InputDecoration(
        labelText: label,
        labelStyle: const TextStyle(fontSize: 12),
        hintText: hint,
        border: OutlineInputBorder(borderRadius: BorderRadius.circular(12)),
        filled: true,
        fillColor: Colors.white.withOpacity(0.05),
        contentPadding: const EdgeInsets.symmetric(horizontal: 12, vertical: 8),
      ),
      keyboardType: TextInputType.number,
      style: const TextStyle(color: Colors.white, fontSize: 14),
      onChanged: onSave,
    );
  }
}

class RecoveryRecommendationsCard extends StatelessWidget {
  final List<RecoveryRecommendation> recommendations;

  const RecoveryRecommendationsCard({super.key, required this.recommendations});

  @override
  Widget build(BuildContext context) {
    if (recommendations.isEmpty) return const SizedBox.shrink();

    return Container(
      padding: const EdgeInsets.all(20),
      decoration: BoxDecoration(
        color: AppTheme.surfaceColor,
        borderRadius: BorderRadius.circular(24),
        border: Border.all(color: Colors.white.withOpacity(0.05)),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            children: [
              const Icon(Icons.auto_awesome, color: AppTheme.accentColor, size: 20),
              const SizedBox(width: 8),
              Text("AI INSIGHTS", style: Theme.of(context).textTheme.titleMedium),
            ],
          ),
          const SizedBox(height: 16),
          ...recommendations.map((rec) => Padding(
            padding: const EdgeInsets.only(bottom: 12),
            child: Row(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Icon(_getIcon(rec.type), size: 16, color: Colors.grey),
                const SizedBox(width: 12),
                Expanded(child: Text(rec.text, style: const TextStyle(height: 1.4))),
              ],
            ),
          )).toList(),
        ],
      ),
    );
  }

  IconData _getIcon(String type) {
    switch (type) {
      case 'hydration': return Icons.water_drop;
      case 'mobility': return Icons.accessibility_new;
      case 'rest': return Icons.bed;
      default: return Icons.info;
    }
  }
}
