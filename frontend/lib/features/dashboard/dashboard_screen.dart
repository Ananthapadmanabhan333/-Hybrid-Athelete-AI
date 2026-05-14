import 'package:flutter/material.dart';
import 'package:flutter_animate/flutter_animate.dart';
import 'package:fl_chart/fl_chart.dart';
import 'package:google_fonts/google_fonts.dart';
import '../../core/app_theme.dart';
import '../../shared/widgets/three_rings_widget.dart';
import '../../features/training/training_screen.dart';
import '../../features/nutrition/nutrition_screen.dart';
import '../../features/coach/coach_screen.dart';
import '../../features/recovery/recovery_screen.dart';
import '../../features/dashboard/profile_screen.dart';
import '../../services/ai_trainer_service.dart';
import '../../features/training/workout_execution_screen.dart';
import 'daily_tasks_widget.dart';
import 'morning_briefing_widget.dart';
import 'context_banner_widget.dart';
import '../../features/performance/performance_screen.dart';
import '../../features/nutrition_advanced/nutrition_dashboard.dart';
import '../../features/medical/medical_dashboard.dart';
import '../../features/community/community_feed.dart';
import '../../features/habits/habit_tracker.dart';

import '../../features/body_progress/service.dart';
import '../../features/body_progress/models.dart';
import '../../features/body_progress/widgets.dart';
import '../../features/body_progress/animated_body_indicator.dart';
import '../../shared/widgets/empty_state_card.dart';

import '../../services/ai_orchestrator_service.dart';
import 'adaptive_stats_card.dart';
import 'recovery_score_gauge.dart';
import 'ai_action_center.dart';

import '../../services/ai_orchestrator_v5_service.dart';
import '../../services/athlete_level_service.dart';
import '../../services/user_service.dart';
import '../../services/daily_metrics_service.dart';
import 'hybrid_level_badge.dart';
import 'projection_panel.dart';
import 'health_status_section.dart';

class DashboardScreen extends StatefulWidget {
  const DashboardScreen({super.key});

  @override
  State<DashboardScreen> createState() => _DashboardScreenState();
}

class _DashboardScreenState extends State<DashboardScreen> {
  int _currentIndex = 0;
  final AITrainerService _aiService = AITrainerService();
  final AIOrchestratorService _orchestratorService = AIOrchestratorService();
  final AIOrchestratorV5Service _orchestratorV5Service = AIOrchestratorV5Service();
  final BodyProgressService _bodyService = BodyProgressService();
  final AthleteLevelService _athleteLevelService = AthleteLevelService();
  final UserService _userService = UserService();
  final DailyMetricsService _metricsService = DailyMetricsService();
  
  Map<String, dynamic>? _dailyWorkout;
  Map<String, dynamic>? _orchestratorPayload;
  Map<String, dynamic>? _v5Summary;
  Map<String, dynamic>? _athleteLevel;
  Map<String, dynamic>? _userProfile;
  Map<String, dynamic>? _todayMetrics;
  BodyChartsResponse? _bodyCharts;
  bool _isLoadingWorkout = true;

  @override
  void initState() {
    super.initState();
    _fetchDailyWorkout();
    _fetchBodyProgress();
    _fetchOrchestratorData();
    _fetchV5Data();
    _fetchAthleteLevel();
    _fetchUserProfile();
    _fetchTodayMetrics();
  }

  Future<void> _fetchTodayMetrics() async {
    final metrics = await _metricsService.getTodayMetrics();
    if (mounted) setState(() => _todayMetrics = metrics);
  }

  Future<void> _fetchUserProfile() async {
    final profile = await _userService.getUserProfile();
    if (mounted) setState(() => _userProfile = profile);
  }
  
  Future<void> _fetchAthleteLevel() async {
    final level = await _athleteLevelService.getAthleteLevel();
    if (mounted) setState(() => _athleteLevel = level);
  }
  
  Future<void> _fetchV5Data() async {
    try {
      final summary = await _orchestratorV5Service.getV5Summary();
      debugPrint("--- V5 SUMMARY RESPONSE ---");
      debugPrint(summary.toString());
      if (mounted) setState(() => _v5Summary = summary);
    } catch (e) {
      debugPrint("Error loading v5 summary: $e");
    }
  }
  
  Future<void> _fetchOrchestratorData() async {
    try {
      final payload = await _orchestratorService.getDashboardPayload();
      if (mounted) setState(() => _orchestratorPayload = payload);
    } catch (e) {
      debugPrint("Error loading orchestrator data: $e");
    }
  }
  
  Future<void> _fetchBodyProgress() async {
    try {
      final charts = await _bodyService.getChartsData();
      if (mounted) setState(() => _bodyCharts = charts);
    } catch (e) {
      debugPrint("Error loading body charts: $e");
    }
  }

  Future<void> _fetchDailyWorkout() async {
    // FORCE PROFESSIONAL PARAMS FOR DEMO
    // This ensures the user sees the new "Pro Split" logic immediately
    final workout = await _aiService.generateDailyWorkout(60, ["dumbbells", "barbell", "pullup_bar"], "Strength", "Advanced");
    if (mounted) {
      setState(() {
        _dailyWorkout = workout;
        _isLoadingWorkout = false;
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    final screens = [
      _buildHomeView(),
      const TrainingScreen(),
      const NutritionScreen(),
      const RecoveryScreen(),
      const CoachScreen(),
    ];

    return Scaffold(
      extendBody: true, // For transparency behind navbar
      backgroundColor: AppTheme.backgroundColor,
      appBar: _currentIndex == 0 ? AppBar(
        title: Text("HYBRID ATHLETE AI", style: Theme.of(context).appBarTheme.titleTextStyle),
        actions: [
          IconButton(
            icon: CircleAvatar(
              backgroundColor: AppTheme.surfaceColor,
              child: const Icon(Icons.person, color: Colors.white, size: 20),
            ),
            onPressed: () {
              Navigator.push(context, MaterialPageRoute(builder: (context) => const ProfileScreen()));
            },
          ).animate().scale(duration: 500.ms),
          const SizedBox(width: 8),
        ],
      ) : null,
      body: SafeArea(
        child: screens[_currentIndex],
      ),
      bottomNavigationBar: _buildGlassNavBar(),
    );
  }

  Widget _buildGlassNavBar() {
    return Container(
      decoration: BoxDecoration(
        color: AppTheme.surfaceColor.withOpacity(0.9),
        border: Border(top: BorderSide(color: Colors.white.withOpacity(0.05))),
      ),
      child: BottomNavigationBar(
        currentIndex: _currentIndex,
        onTap: (index) => setState(() => _currentIndex = index),
        backgroundColor: Colors.transparent, // Transparent to show container color
        elevation: 0,
        selectedItemColor: AppTheme.primaryColor,
        unselectedItemColor: Colors.grey,
        type: BottomNavigationBarType.fixed,
        showSelectedLabels: false,
        showUnselectedLabels: false,
        items: [
          BottomNavigationBarItem(icon: Icon(Icons.dashboard_rounded, size: 28).animate().scale(duration: 200.ms), label: 'Home'),
          BottomNavigationBarItem(icon: Icon(Icons.fitness_center_rounded, size: 28), label: 'Train'),
          BottomNavigationBarItem(icon: Icon(Icons.restaurant_menu_rounded, size: 28), label: 'Eat'),
          BottomNavigationBarItem(icon: Icon(Icons.bed_rounded, size: 28), label: 'Recover'),
          BottomNavigationBarItem(icon: Icon(Icons.psychology_rounded, size: 28), label: 'Coach'),
        ],
      ),
    );
  }

  dynamic _safeMapAccess(Map<String, dynamic>? data, String section, String key, dynamic defaultValue) {
    if (data == null) return defaultValue;
    if (!data.containsKey(section) || data[section] == null || data[section] is! Map) {
      return defaultValue;
    }
    final sectionMap = data[section] as Map<String, dynamic>;
    return sectionMap.containsKey(key) && sectionMap[key] != null ? sectionMap[key] : defaultValue;
  }

  Widget _buildHomeView() {
    return SingleChildScrollView(
      padding: const EdgeInsets.all(20),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,

        children: [
          // Context Aware Banner (Dynamic in real app)
          if (_v5Summary != null) ...[
            Center(
              child: HybridLevelBadge(
                level: _safeMapAccess(_v5Summary, 'summary', 'hybrid_level', 72) as int
              ).animate().scale(duration: 600.ms, curve: Curves.elasticOut),
            ),
            const SizedBox(height: 24),
            HealthStatusSection(
              alerts: _v5Summary!.containsKey('health_alerts') && _v5Summary!['health_alerts'] != null 
                  ? List<String>.from(_v5Summary!['health_alerts']) 
                  : [],
            ).animate().fadeIn(delay: 200.ms),
            const SizedBox(height: 24),
          ],
          
          if (_orchestratorPayload != null && _orchestratorPayload!['status_message'] != null)
            ContextBannerWidget(
              message: _orchestratorPayload!['status_message'],
              type: _orchestratorPayload!['status_message'].toString().toLowerCase().contains("injury") ? ContextBannerType.warning : ContextBannerType.info,
              actionLabel: "Details",
            ),
          const SizedBox(height: 24),

          // Replaced static header with Smart Briefing
          MorningBriefingWidget(
            userName: _userProfile?['full_name']?.split(' ')[0] ?? "Champion",
            sleepHours: (_todayMetrics?['sleep_hours'] ?? 7.5).toInt(),
            recoveryScore: _orchestratorPayload?['recovery_score'] != null ? (double.tryParse(_orchestratorPayload!['recovery_score'].toString())?.toInt() ?? 85) : 85,
            primaryGoal: "Hybrid Performance",
          ),
          
          const SizedBox(height: 32),
          
          if (_orchestratorPayload != null) ...[
            Row(
              children: [
                Expanded(
                  flex: 2,
                  child: RecoveryScoreGauge(
                    score: _orchestratorPayload!['recovery_score'] != null ? (double.tryParse(_orchestratorPayload!['recovery_score'].toString()) ?? 0.0) : 0.0,
                  ),
                ),
                const SizedBox(width: 16),
                Expanded(
                  flex: 3,
                  child: Column(
                    children: [
                      AdaptiveStatsCard(
                        adherence: _orchestratorPayload!['adherence_pct'] != null ? (double.tryParse(_orchestratorPayload!['adherence_pct'].toString()) ?? 0.0) : 0.0,
                        status: _orchestratorPayload!['status_message'] ?? "Analyzing...",
                      ),
                    ],
                  ),
                ),
              ],
            ).animate().fadeIn(duration: 600.ms),
            const SizedBox(height: 24),
            AIActionCenter(
              insights: List<String>.from(_orchestratorPayload!['insights'] ?? []),
            ).animate().fadeIn(delay: 200.ms),
            const SizedBox(height: 32),
          ],
          
          _buildAthleteStats(),
          const SizedBox(height: 32),
          
          Center(
            child: ThreeRingsWidget(
              workProgress: _orchestratorPayload != null && _orchestratorPayload!['adherence_pct'] != null ? (num.tryParse(_orchestratorPayload!['adherence_pct'].toString())?.toDouble() ?? 50.0) / 100 : 0.0, 
              trainProgress: _dailyWorkout != null ? 0.0 : 1.0, // Simplistic representation of "Train" progress 
              recoverProgress: _orchestratorPayload != null && _orchestratorPayload!['recovery_score'] != null ? (num.tryParse(_orchestratorPayload!['recovery_score'].toString())?.toDouble() ?? 80.0) / 100 : 0.0, 
            ).animate().scale(duration: 800.ms, curve: Curves.elasticOut),
          ),
          
          const SizedBox(height: 40),
          
          
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              Text("BODY PROGRESS", style: Theme.of(context).textTheme.titleLarge),
              Text("Analyzing 60 Days", style: TextStyle(color: AppTheme.accentColor, fontSize: 12)),
            ],
          ).animate().fadeIn(delay: 400.ms),
          const SizedBox(height: 16),

          // Body Progress Charts & Animation
          if (_bodyCharts != null) ...[
            if (_bodyCharts!.gainChart.isNotEmpty && _bodyCharts!.lossChart.isNotEmpty) ...[
              AnimatedBodyIndicator(
                weightStart: _bodyCharts!.gainChart.first.value,
                weightEnd: _bodyCharts!.gainChart.last.value,
                muscleStart: _bodyCharts!.gainChart.first.secondaryValue ?? 0,
                muscleEnd: _bodyCharts!.gainChart.last.secondaryValue ?? 0,
                fatStart: _bodyCharts!.lossChart.first.secondaryValue ?? 0,
                fatEnd: _bodyCharts!.lossChart.last.secondaryValue ?? 0,
              ),
              const SizedBox(height: 16),
            ],
            Container(
              height: 250,
              padding: const EdgeInsets.all(20),
              decoration: BoxDecoration(
                color: AppTheme.surfaceColor,
                borderRadius: BorderRadius.circular(24),
                border: Border.all(color: Colors.white.withOpacity(0.05)),
              ),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  const Text("HYPERTROPHY TREND (Weight vs Muscle Est.)", style: TextStyle(color: Colors.grey, fontSize: 12, fontWeight: FontWeight.bold)),
                  const SizedBox(height: 8),
                  Expanded(child: GainChartWidget(data: _bodyCharts!.gainChart)),
                ],
              ),
            ).animate().fadeIn(delay: 600.ms).slideY(begin: 0.2),
            const SizedBox(height: 16),
            Container(
              height: 250,
              padding: const EdgeInsets.all(20),
              decoration: BoxDecoration(
                color: AppTheme.surfaceColor,
                borderRadius: BorderRadius.circular(24),
                border: Border.all(color: Colors.white.withOpacity(0.05)),
              ),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  const Text("FAT LOSS TREND (Weight vs Fat Est.)", style: TextStyle(color: Colors.grey, fontSize: 12, fontWeight: FontWeight.bold)),
                  const SizedBox(height: 8),
                  Expanded(child: LossChartWidget(data: _bodyCharts!.lossChart)),
                ],
              ),
            ).animate().fadeIn(delay: 700.ms).slideY(begin: 0.2),
          ] else if (_bodyCharts != null && _bodyCharts!.gainChart.length < 2) ...[
             EmptyStateCard(
               title: "Log Your First Body Metric",
               subtitle: "Track your weight and body composition to unlock trend charts and the animated body progress indicator.",
               icon: Icons.monitor_weight_outlined,
               buttonLabel: "Log Body Metrics",
               onActionPressed: () {},
             ),
          ] else ...[
             const EmptyStateCard(
               title: "Loading Body Progress...",
               subtitle: "Please wait a moment while we fetch your data.",
               icon: Icons.hourglass_top,
             ),
          ],

          if (_v5Summary != null) ...[
             const SizedBox(height: 32),
             ProjectionPanel(
               projections: _safeMapAccess(_v5Summary, 'summary', 'projections_formatted', {
                 "weight_4w": "84.2",
                 "strength_8w_pct": "12",
                 "cond_index": "Elite"
               }) as Map<String, dynamic>,
             ).animate().fadeIn(delay: 700.ms).slideY(begin: 0.1),
             const SizedBox(height: 32),
          ],
          
          const DailyTasksWidget(),

          const SizedBox(height: 32),
          
          _buildDailyWorkoutCard(),
          _buildTodayMetrics(),
          
          const SizedBox(height: 32),
          Text("EXTENDED FEATURES", style: Theme.of(context).textTheme.titleLarge),
          const SizedBox(height: 16),
          SingleChildScrollView(
            scrollDirection: Axis.horizontal,
            child: Row(
              children: [
                _buildFeatureCard(context, "Performance", Icons.speed, Colors.redAccent, const PerformanceScreen()),
                const SizedBox(width: 12),
                _buildFeatureCard(context, "Medical AI", Icons.medical_services, Colors.teal, const MedicalDashboard()),
                const SizedBox(width: 12),
                _buildFeatureCard(context, "Community", Icons.people, Colors.orange, const CommunityFeed()),
                const SizedBox(width: 12),
                _buildFeatureCard(context, "Habits", Icons.check_circle, Colors.purple, const HabitTracker()),
                const SizedBox(width: 12),
                _buildFeatureCard(context, "Adv. Nutrition", Icons.restaurant, Colors.green, const NutritionDashboard()),
                const SizedBox(width: 12),
                _buildFeatureCard(context, "Recovery V3", Icons.battery_charging_full, Colors.lightBlue, _buildPlaceholderScreen(context, "Recovery V3")),
                const SizedBox(width: 12),
                _buildFeatureCard(context, "Body Progress Tools", Icons.straighten, Colors.pinkAccent, _buildPlaceholderScreen(context, "Body Progress Tools")),
              ],
            ),
          ),

          const SizedBox(height: 100), // Bottom padding for navbar
        ],
      ),
    );
  }
  Widget _buildTodayMetrics() {
    int kcalWorkload = 0;
    if (_orchestratorPayload != null && _orchestratorPayload!['macro_targets'] != null) {
       final macs = _orchestratorPayload!['macro_targets'];
       final p = (macs['p'] ?? 0) as num;
       final c = (macs['c'] ?? 0) as num;
       final f = (macs['f'] ?? 0) as num;
       // Quick estimate of KCAL based on macro recommendation
       kcalWorkload = ((p * 4) + (c * 4) + (f * 9)).toInt();
    }
    final recoveryScr = _orchestratorPayload?['recovery_score'] != null ? (double.tryParse(_orchestratorPayload!['recovery_score'].toString())?.toInt() ?? 85) : 85;
    final trainingMins = _todayMetrics?['total_training_minutes'] ?? _dailyWorkout?['duration'] ?? 45;
    final sleepHrs = _todayMetrics?['sleep_hours'] ?? 7.5; 

    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
          Text("TODAY'S METRICS", style: Theme.of(context).textTheme.titleLarge).animate().fadeIn(delay: 800.ms),
          const SizedBox(height: 16),
          
          Row(
            children: [
              Expanded(child: _buildStatCard("Workload Target", kcalWorkload > 0 ? kcalWorkload.toString() : "2,450", "kcal", AppTheme.accentColor, 1)),
              const SizedBox(width: 16),
              Expanded(child: _buildStatCard("Recovery", recoveryScr.toString(), "%", AppTheme.primaryColor, 2)),
            ],
          ),
          const SizedBox(height: 16),
          Row(
            children: [
              Expanded(child: _buildStatCard("Training", trainingMins.toString(), "min", Colors.orangeAccent, 3)),
              const SizedBox(width: 16),
              Expanded(child: _buildStatCard("Sleep", sleepHrs.toString(), "hrs", Colors.purpleAccent, 4)),
            ],
          ),
      ],
    );
  }

  Widget _buildStreakCounter() {
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
      decoration: BoxDecoration(
        color: AppTheme.secondaryColor.withOpacity(0.2),
        borderRadius: BorderRadius.circular(20),
        border: Border.all(color: AppTheme.secondaryColor.withOpacity(0.5)),
      ),
      child: const Row(
        children: [
          Icon(Icons.local_fire_department, color: AppTheme.secondaryColor, size: 20),
          SizedBox(width: 4),
          Text("12 Day Streak", style: TextStyle(fontWeight: FontWeight.bold, color: AppTheme.secondaryColor)),
        ],
      ),
    );
  }

  Widget _buildStatCard(String title, String value, String unit, Color color, int index) {
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
          Icon(Icons.circle, size: 12, color: color),
          const SizedBox(height: 12),
          Text(title, style: Theme.of(context).textTheme.bodyMedium),
          const SizedBox(height: 8),
          RichText(
            text: TextSpan(
              children: [
                TextSpan(text: value, style: Theme.of(context).textTheme.displayMedium),
                TextSpan(text: " $unit", style: Theme.of(context).textTheme.bodySmall),
              ],
            ),
          ),
        ],
      ),
    ).animate().fadeIn(delay: (800 + (index * 100)).ms).slideX();
  }

  Widget _buildDailyWorkoutCard() {
    if (_dailyWorkout == null) {
      if (_isLoadingWorkout) return const Center(child: CircularProgressIndicator());
      return const SizedBox.shrink();
    }

    return Container(
      width: double.infinity,
      padding: const EdgeInsets.all(24),
      margin: const EdgeInsets.symmetric(vertical: 20),
      decoration: BoxDecoration(
        color: AppTheme.surfaceColor,
        borderRadius: BorderRadius.circular(24),
        border: Border.all(color: AppTheme.primaryColor.withOpacity(0.5)),
        boxShadow: [
          BoxShadow(
            color: AppTheme.primaryColor.withOpacity(0.1),
            blurRadius: 20,
            offset: const Offset(0, 5),
          )
        ],
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              Container(
                padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 6),
                decoration: BoxDecoration(
                  color: AppTheme.primaryColor,
                  borderRadius: BorderRadius.circular(20),
                ),
                child: Text(
                  "AI RECOMMENDED", 
                  style: GoogleFonts.outfit(color: Colors.black, fontWeight: FontWeight.bold, fontSize: 12)
                ),
              ),
              const Icon(Icons.auto_awesome, color: AppTheme.primaryColor),
            ],
          ),
          const SizedBox(height: 16),
          Text(
            _dailyWorkout!['title'] ?? "Adaptive Session", 
            style: Theme.of(context).textTheme.displayMedium
          ),
          const SizedBox(height: 8),
          Text(
            _dailyWorkout!['reasoning'] ?? "Based on your recent activity.", 
            style: Theme.of(context).textTheme.bodyMedium?.copyWith(fontStyle: FontStyle.italic)
          ),
          const SizedBox(height: 24),
          Row(
            children: [
              _buildMetricBadge(Icons.timer, "${_dailyWorkout!['duration']} min"),
              const SizedBox(width: 16),
              _buildMetricBadge(Icons.flash_on, _dailyWorkout!['intensity'] ?? "Moderate"),
            ],
          ),
          const SizedBox(height: 24),
          SizedBox(
            width: double.infinity,
            child: ElevatedButton(
              onPressed: () {
                Navigator.push(
                  context,
                  MaterialPageRoute(
                    builder: (context) => WorkoutExecutionScreen(
                      workoutType: _dailyWorkout!['title'],
                      difficulty: "Intermediate",
                    ),
                  ),
                );
              },
              child: const Text("START ADAPTIVE SESSION"),
            ),
          ),
        ],
      ),
    ).animate().fadeIn(duration: 800.ms).slideY(begin: 0.2);
  }

  Widget _buildPlaceholderScreen(BuildContext context, String title) {
    return Scaffold(
      backgroundColor: AppTheme.backgroundColor,
      appBar: AppBar(title: Text(title)),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Icon(Icons.construction, size: 64, color: AppTheme.primaryColor),
            const SizedBox(height: 24),
            Text("$title Module", style: Theme.of(context).textTheme.displayMedium),
            const SizedBox(height: 8),
            const Text("Under active development", style: TextStyle(color: Colors.grey)),
          ],
        ),
      ),
    );
  }

  Widget _buildFeatureCard(BuildContext context, String title, IconData icon, Color color, Widget screen) {
    return GestureDetector(
      onTap: () => Navigator.push(context, MaterialPageRoute(builder: (context) => screen)),
      child: Container(
        width: 100,
        height: 100,
        decoration: BoxDecoration(
          color: AppTheme.surfaceColor,
          borderRadius: BorderRadius.circular(16),
          border: Border.all(color: Colors.white.withOpacity(0.05)),
        ),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Icon(icon, color: color, size: 32),
            const SizedBox(height: 8),
            Text(title, style: const TextStyle(fontSize: 12, fontWeight: FontWeight.bold), textAlign: TextAlign.center),
          ],
        ),
      ),
    );
  }

  Widget _buildMetricBadge(IconData icon, String label) {
    return Row(
      children: [
        Icon(icon, color: Colors.grey, size: 16),
        const SizedBox(width: 4),
        Text(label, style: const TextStyle(color: Colors.white70, fontWeight: FontWeight.bold)),
      ],
    );
  }
  Widget _buildAthleteStats() {
    final strengthLevel = _athleteLevel?['strength_level'] ?? "Advanced";
    final boxingLevel = _athleteLevel?['boxing_level'] ?? "Amateur";
    final hybridLabel = _athleteLevel?['hybrid_label'] ?? "Level 3";

    return Container(
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: AppTheme.surfaceColor,
        borderRadius: BorderRadius.circular(16),
        border: Border.all(color: Colors.white.withOpacity(0.05)),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              Text("ATHLETE PROFILE", style: Theme.of(context).textTheme.titleMedium),
              IconButton(
                icon: const Icon(Icons.refresh, size: 16, color: Colors.grey),
                onPressed: () async {
                  await _athleteLevelService.recalculateLevel();
                  _fetchAthleteLevel();
                },
              )
            ]
          ),
          const SizedBox(height: 16),
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceAround,
            children: [
              _buildLevelIndicator(Icons.fitness_center, "Strength", strengthLevel, Colors.redAccent),
              _buildLevelIndicator(Icons.sports_mma, "Boxing", boxingLevel, Colors.blueAccent),
              _buildLevelIndicator(Icons.bolt, "Hybrid", hybridLabel, AppTheme.accentColor),
            ],
          ),
        ],
      ),
    ).animate().fadeIn(delay: 300.ms).slideX();
  }

  Widget _buildLevelIndicator(IconData icon, String label, String value, Color color) {
    return Column(
      children: [
        Container(
          padding: const EdgeInsets.all(12),
          decoration: BoxDecoration(
            shape: BoxShape.circle,
            color: color.withOpacity(0.1),
            border: Border.all(color: color.withOpacity(0.5)),
          ),
          child: Icon(icon, color: color, size: 24),
        ),
        const SizedBox(height: 8),
        Text(value, style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 14)),
        Text(label, style: const TextStyle(color: Colors.grey, fontSize: 10)),
      ],
    );
  }
}
