
import 'package:flutter/material.dart';
import '../../core/app_theme.dart';
import 'package:fl_chart/fl_chart.dart';
import '../../shared/widgets/empty_state_card.dart';
import 'models.dart';

class GainChartWidget extends StatelessWidget {
  final List<ChartDataPoint> data;

  const GainChartWidget({super.key, required this.data});

  @override
  Widget build(BuildContext context) {
    if (data.length < 2) {
      return const EmptyStateCard(
        title: "Not Enough Data",
        subtitle: "Log at least 2 body metrics to see your Hypertrophy Trend.",
        icon: Icons.show_chart,
      );
    }

    return LineChart(
      LineChartData(
        gridData: FlGridData(show: false),
        titlesData: FlTitlesData(show: false),
        borderData: FlBorderData(show: false),
        lineBarsData: [
          // Weight Line
          LineChartBarData(
            spots: data.asMap().entries.map((e) => FlSpot(e.key.toDouble(), e.value.value)).toList(),
            isCurved: true,
            color: AppTheme.primaryColor,
            barWidth: 3,
            dotData: FlDotData(show: false),
            belowBarData: BarAreaData(show: true, color: AppTheme.primaryColor.withOpacity(0.1)),
          ),
          // Muscle Est Line
          LineChartBarData(
            spots: data.asMap().entries.map((e) => FlSpot(e.key.toDouble(), e.value.secondaryValue ?? 0)).toList(),
            isCurved: true,
            color: Colors.greenAccent.withOpacity(0.7),
            barWidth: 2,
            dotData: FlDotData(show: false),
          ),
        ],
      ),
    );
  }
}

class LossChartWidget extends StatelessWidget {
  final List<ChartDataPoint> data;

  const LossChartWidget({super.key, required this.data});

  @override
  Widget build(BuildContext context) {
    if (data.length < 2) {
      return const EmptyStateCard(
        title: "Not Enough Data",
        subtitle: "Log at least 2 body metrics to see your Fat Loss Trend.",
        icon: Icons.show_chart,
      );
    }

    return LineChart(
      LineChartData(
        gridData: FlGridData(show: false),
        titlesData: FlTitlesData(show: false),
        borderData: FlBorderData(show: false),
        lineBarsData: [
          // Weight Line
          LineChartBarData(
            spots: data.asMap().entries.map((e) => FlSpot(e.key.toDouble(), e.value.value)).toList(),
            isCurved: true,
            color: Colors.redAccent,
            barWidth: 3,
            dotData: FlDotData(show: false),
          ),
          // Fat Est Line
          LineChartBarData(
            spots: data.asMap().entries.map((e) => FlSpot(e.key.toDouble(), e.value.secondaryValue ?? 0)).toList(),
            isCurved: true,
            color: Colors.orangeAccent.withOpacity(0.6),
            barWidth: 2,
            dotData: FlDotData(show: false),
            belowBarData: BarAreaData(show: true, color: Colors.orangeAccent.withOpacity(0.1)),
          ),
        ],
      ),
    );
  }
}
