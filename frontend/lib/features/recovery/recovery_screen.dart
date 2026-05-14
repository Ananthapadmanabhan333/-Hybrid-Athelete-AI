
import 'package:flutter/material.dart';
import '../../core/app_theme.dart';
import 'package:flutter_animate/flutter_animate.dart';
import '../recovery_v3/service.dart';
import '../recovery_v3/models.dart';
import '../recovery_v3/widgets.dart';

class RecoveryScreen extends StatefulWidget {
  const RecoveryScreen({super.key});

  @override
  State<RecoveryScreen> createState() => _RecoveryScreenState();
}

class _RecoveryScreenState extends State<RecoveryScreen> {
  final RecoveryServiceV3 _service = RecoveryServiceV3();
  RecoveryDailySummary? _summary;
  bool _isLoading = true;

  @override
  void initState() {
    super.initState();
    _loadData();
  }

  Future<void> _loadData() async {
    try {
      final summary = await _service.getTodaySummary();
      if (mounted) {
        setState(() {
          _summary = summary;
          _isLoading = false;
        });
      }
    } catch (e) {
      if (mounted) {
        setState(() => _isLoading = false);
      }
      debugPrint("Error loading recovery data: $e");
    }
  }

  Future<void> _submitLog(RecoveryLogV3 log) async {
    setState(() => _isLoading = true);
    try {
      final summary = await _service.logRecovery(log);
      if (mounted) {
        setState(() {
          _summary = summary;
          _isLoading = false;
        });
      }
    } catch (e) {
      if (mounted) {
        setState(() => _isLoading = false);
        ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text("Error: $e")));
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    if (_isLoading) return const Center(child: CircularProgressIndicator());

    return Scaffold(
      backgroundColor: AppTheme.backgroundColor,
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(20),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text("RECOVERY STUDIO V3", style: Theme.of(context).textTheme.headlineMedium),
            const SizedBox(height: 24),
            
            if (_summary?.score != null) ...[
               RecoveryScoreCardV3(score: _summary!.score!),
               const SizedBox(height: 24),
               RecoveryRecommendationsCard(recommendations: _summary!.recommendations),
            ] else ...[
               Container(
                 padding: const EdgeInsets.all(24),
                 decoration: BoxDecoration(
                   color: AppTheme.surfaceColor,
                   borderRadius: BorderRadius.circular(24),
                   border: Border.all(color: Colors.white.withOpacity(0.05)),
                 ),
                 child: const Center(child: Text("Log your data to see your AI Recovery Score", style: TextStyle(color: Colors.grey))),
               ),
            ],

            const SizedBox(height: 32),
            
            // Allow re-logging or initial logging
            RecoveryLogForm(onSubmit: _submitLog),
              
            const SizedBox(height: 100),
          ],
        ),
      ).animate().fadeIn(),
    );
  }
}
