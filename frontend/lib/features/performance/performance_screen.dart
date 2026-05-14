import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:flutter_animate/flutter_animate.dart';
import 'package:http/http.dart' as http;
import '../../core/app_theme.dart';
import '../../core/constants.dart';
import '../../services/auth_service.dart';
import '../training/animations/training_animations.dart';

class PerformanceScreen extends StatefulWidget {
  const PerformanceScreen({super.key});

  @override
  State<PerformanceScreen> createState() => _PerformanceScreenState();
}

class _PerformanceScreenState extends State<PerformanceScreen> {
  final AuthService _authService = AuthService();
  Map<String, dynamic>? _perfData;
  bool _loading = true;

  @override
  void initState() {
    super.initState();
    _fetchPerformance();
  }

  Future<void> _fetchPerformance() async {
    try {
      final token = await _authService.getToken();
      final resp = await http.get(
        Uri.parse('${AppConstants.apiBaseUrl}/ai-orchestrator/summary'),
        headers: {"Authorization": "Bearer $token"},
      );
      if (resp.statusCode == 200) {
        setState(() { _perfData = jsonDecode(resp.body); _loading = false; });
      } else {
        setState(() => _loading = false);
      }
    } catch (_) {
      setState(() => _loading = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: AppTheme.backgroundColor,
      appBar: AppBar(
        title: const Text("Performance Command Center"),
        backgroundColor: AppTheme.surfaceColor,
      ),
      body: _loading
          ? const Center(child: CircularProgressIndicator())
          : SingleChildScrollView(
              padding: const EdgeInsets.all(20),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  // Score Header Row
                  _buildScoreHeader(),
                  const SizedBox(height: 28),

                  // STRENGTH
                  _buildSectionHeader("💪 STRENGTH PROGRESSION", Colors.orangeAccent),
                  const SizedBox(height: 12),
                  _buildStrengthSection(),
                  const SizedBox(height: 28),

                  // CARDIO
                  _buildSectionHeader("💓 CARDIO ENDURANCE", Colors.blueAccent),
                  const SizedBox(height: 12),
                  _buildCardioSection(),
                  const SizedBox(height: 28),

                  // BOXING
                  _buildSectionHeader("🥊 BOXING POWER", Colors.redAccent),
                  const SizedBox(height: 12),
                  _buildBoxingSection(),
                  const SizedBox(height: 28),

                  // ATHLETICS
                  _buildSectionHeader("⚡ ATHLETIC CONDITIONING", Colors.greenAccent),
                  const SizedBox(height: 12),
                  _buildAthleticsSection(),
                  const SizedBox(height: 40),
                ],
              ),
            ),
    );
  }

  Widget _buildScoreHeader() {
    final recoveryScore = _safeDouble('recovery_score', 82.0);
    final adherence = _safeDouble('adherence_pct', 75.0);

    return Row(
      children: [
        Expanded(child: _buildScoreTile("Performance", adherence, Colors.orangeAccent, Icons.speed)),
        const SizedBox(width: 12),
        Expanded(child: _buildScoreTile("Recovery", recoveryScore, Colors.greenAccent, Icons.battery_charging_full)),
      ],
    ).animate().fadeIn(duration: 600.ms);
  }

  Widget _buildScoreTile(String label, double score, Color color, IconData icon) {
    return Container(
      padding: const EdgeInsets.all(20),
      decoration: BoxDecoration(
        color: AppTheme.surfaceColor,
        borderRadius: BorderRadius.circular(20),
        border: Border.all(color: color.withOpacity(0.3)),
      ),
      child: Column(
        children: [
          Icon(icon, color: color, size: 28),
          const SizedBox(height: 8),
          TweenAnimationBuilder<double>(
            tween: Tween(begin: 0, end: score),
            duration: const Duration(milliseconds: 1200),
            curve: Curves.easeOutCubic,
            builder: (_, v, __) => Text(
              v.toInt().toString(),
              style: TextStyle(fontSize: 42, fontWeight: FontWeight.bold, color: color, height: 1),
            ),
          ),
          const SizedBox(height: 4),
          Text(label, style: const TextStyle(color: Colors.grey, fontSize: 13)),
        ],
      ),
    );
  }

  Widget _buildSectionHeader(String title, Color color) {
    return Text(title, style: TextStyle(fontWeight: FontWeight.bold, fontSize: 16, color: color, letterSpacing: 1));
  }

  Widget _buildStrengthSection() {
    return Container(
      padding: const EdgeInsets.all(20),
      decoration: BoxDecoration(
        color: AppTheme.surfaceColor,
        borderRadius: BorderRadius.circular(20),
        border: Border.all(color: Colors.orangeAccent.withOpacity(0.2)),
      ),
      child: Column(
        children: [
          StrengthProgressBar(label: "Squat Volume", value: 4200, max: 6000, color: Colors.orangeAccent),
          StrengthProgressBar(label: "Deadlift Volume", value: 3800, max: 5500, color: Colors.deepOrange),
          StrengthProgressBar(label: "Upper Body Push", value: 2900, max: 4000, color: Colors.amber),
          StrengthProgressBar(label: "Pull / Row", value: 3200, max: 4500, color: Colors.orange),
          const SizedBox(height: 8),
          const Text("Weekly volume (kg) vs target", style: TextStyle(color: Colors.grey, fontSize: 11)),
        ],
      ),
    ).animate().fadeIn(delay: 100.ms).slideY(begin: 0.1);
  }

  Widget _buildCardioSection() {
    return Container(
      padding: const EdgeInsets.all(20),
      decoration: BoxDecoration(
        color: AppTheme.surfaceColor,
        borderRadius: BorderRadius.circular(20),
        border: Border.all(color: Colors.blueAccent.withOpacity(0.2)),
      ),
      child: Column(
        children: [
          const CardioHeartbeatVisual(load: 0.68, zone: "Zone 3"),
          const SizedBox(height: 24),
          const Divider(color: Colors.white10),
          const SizedBox(height: 12),
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceAround,
            children: [
              _buildCardioStat("Avg HR", "142 bpm", Colors.blueAccent),
              _buildCardioStat("VO2 Est.", "48 ml", Colors.lightBlueAccent),
              _buildCardioStat("Sessions", "3 / wk", Colors.cyanAccent),
            ],
          ),
        ],
      ),
    ).animate().fadeIn(delay: 200.ms).slideY(begin: 0.1);
  }

  Widget _buildCardioStat(String label, String val, Color c) {
    return Column(children: [
      Text(val, style: TextStyle(color: c, fontWeight: FontWeight.bold, fontSize: 18)),
      const SizedBox(height: 4),
      Text(label, style: const TextStyle(color: Colors.grey, fontSize: 11)),
    ]);
  }

  Widget _buildBoxingSection() {
    return Container(
      padding: const EdgeInsets.all(20),
      decoration: BoxDecoration(
        color: AppTheme.surfaceColor,
        borderRadius: BorderRadius.circular(20),
        border: Border.all(color: Colors.redAccent.withOpacity(0.2)),
      ),
      child: Column(
        children: [
          const BoxingVelocityGauge(power: 0.72),
          const SizedBox(height: 16),
          const Divider(color: Colors.white10),
          const SizedBox(height: 12),
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceAround,
            children: [
              _buildCardioStat("Combos/min", "38", Colors.redAccent),
              _buildCardioStat("Session Avg", "42 min", Colors.pinkAccent),
              _buildCardioStat("Rounds", "8 / wk", Colors.deepOrangeAccent),
            ],
          ),
        ],
      ),
    ).animate().fadeIn(delay: 300.ms).slideY(begin: 0.1);
  }

  Widget _buildAthleticsSection() {
    return Container(
      padding: const EdgeInsets.all(20),
      decoration: BoxDecoration(
        color: AppTheme.surfaceColor,
        borderRadius: BorderRadius.circular(20),
        border: Border.all(color: Colors.greenAccent.withOpacity(0.2)),
      ),
      child: Column(
        children: [
          StrengthProgressBar(label: "Speed Capacity", value: 0.71 * 100, max: 100, color: Colors.greenAccent),
          StrengthProgressBar(label: "Agility Score", value: 0.65 * 100, max: 100, color: Colors.lightGreenAccent),
          StrengthProgressBar(label: "Endurance Index", value: 0.78 * 100, max: 100, color: Colors.tealAccent),
          const SizedBox(height: 8),
          const Text("Composite index (0-100 scale)", style: TextStyle(color: Colors.grey, fontSize: 11)),
        ],
      ),
    ).animate().fadeIn(delay: 400.ms).slideY(begin: 0.1);
  }

  double _safeDouble(String key, double fallback) {
    if (_perfData == null) return fallback;
    return double.tryParse(_perfData![key]?.toString() ?? '') ?? fallback;
  }
}
