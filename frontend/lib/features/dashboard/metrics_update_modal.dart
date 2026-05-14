import 'package:flutter/material.dart';
import '../../core/app_theme.dart';
import '../../services/daily_metrics_service.dart';

class MetricsUpdateModal extends StatefulWidget {
  final String metricType;
  final dynamic currentValue;
  final Function(dynamic) onUpdate;

  const MetricsUpdateModal({
    super.key,
    required this.metricType,
    required this.currentValue,
    required this.onUpdate,
  });

  @override
  State<MetricsUpdateModal> createState() => _MetricsUpdateModalState();
}

class _MetricsUpdateModalState extends State<MetricsUpdateModal> {
  late TextEditingController _controller;
  final DailyMetricsService _metricsService = DailyMetricsService();
  bool _isLoading = false;

  @override
  void initState() {
    super.initState();
    _controller = TextEditingController(
      text: widget.currentValue?.toString() ?? '0'
    );
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  Future<void> _saveMetric() async {
    setState(() => _isLoading = true);

    try {
      final value = _parseValue();
      
      // Update based on metric type
      Map<String, dynamic>? updates;
      switch (widget.metricType.toLowerCase()) {
        case 'calories':
        case 'workload':
          updates = await _metricsService.updateTodayMetrics(
            calories: value is int ? value : int.tryParse(value.toString())
          );
          break;
        case 'training':
          updates = await _metricsService.updateTodayMetrics(
            trainingMinutes: value is int ? value : int.tryParse(value.toString())
          );
          break;
        case 'sleep':
          updates = await _metricsService.updateTodayMetrics(
            sleepHours: value is double ? value : double.tryParse(value.toString())
          );
          break;
        case 'recovery':
          updates = await _metricsService.updateTodayMetrics(
            recoveryScore: value is int ? value : int.tryParse(value.toString())
          );
          break;
      }

      if (mounted) {
        widget.onUpdate(value);
        Navigator.pop(context);
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(content: Text('Metric updated successfully!'))
        );
      }
    } catch (e) {
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text('Failed to update: $e'))
        );
      }
    } finally {
      if (mounted) {
        setState(() => _isLoading = false);
      }
    }
  }

  dynamic _parseValue() {
    final text = _controller.text.trim();
    if (widget.metricType.toLowerCase() == 'sleep') {
      return double.tryParse(text) ?? 0.0;
    }
    return int.tryParse(text) ?? 0;
  }

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: EdgeInsets.only(
        bottom: MediaQuery.of(context).viewInsets.bottom + 20,
        top: 20,
        left: 20,
        right: 20,
      ),
      decoration: const BoxDecoration(
        color: AppTheme.surfaceColor,
        borderRadius: BorderRadius.vertical(top: Radius.circular(20)),
      ),
      child: Column(
        mainAxisSize: MainAxisSize.min,
        children: [
          Text(
            'Update ${widget.metricType}',
            style: const TextStyle(
              fontSize: 20,
              fontWeight: FontWeight.bold,
              color: Colors.white
            ),
          ),
          const SizedBox(height: 24),
          TextField(
            controller: _controller,
            keyboardType: const TextInputType.numberWithOptions(decimal: true),
            style: const TextStyle(color: Colors.white, fontSize: 18),
            decoration: InputDecoration(
              labelText: _getLabel(),
              labelStyle: const TextStyle(color: Colors.grey),
              filled: true,
              fillColor: Colors.black26,
              border: OutlineInputBorder(
                borderRadius: BorderRadius.circular(12),
                borderSide: BorderSide.none,
              ),
              contentPadding: const EdgeInsets.symmetric(horizontal: 20, vertical: 16),
            ),
            autofocus: true,
          ),
          const SizedBox(height: 24),
          SizedBox(
            width: double.infinity,
            child: ElevatedButton(
              onPressed: _isLoading ? null : _saveMetric,
              style: ElevatedButton.styleFrom(
                backgroundColor: AppTheme.primaryColor,
                padding: const EdgeInsets.symmetric(vertical: 16),
                shape: RoundedRectangleBorder(
                  borderRadius: BorderRadius.circular(12),
                ),
              ),
              child: _isLoading
                  ? const SizedBox(
                      height: 20,
                      width: 20,
                      child: CircularProgressIndicator(
                        strokeWidth: 2,
                        color: Colors.black,
                      ),
                    )
                  : const Text(
                      'SAVE',
                      style: TextStyle(
                        color: Colors.black,
                        fontWeight: FontWeight.bold,
                        fontSize: 16,
                      ),
                    ),
            ),
          ),
        ],
      ),
    );
  }

  String _getLabel() {
    switch (widget.metricType.toLowerCase()) {
      case 'calories':
      case 'workload':
        return 'Calories (kcal)';
      case 'training':
        return 'Training Time (minutes)';
      case 'sleep':
        return 'Sleep Duration (hours)';
      case 'recovery':
        return 'Recovery Score (0-100)';
      default:
        return 'Value';
    }
  }
}
