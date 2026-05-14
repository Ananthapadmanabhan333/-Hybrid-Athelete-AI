import 'package:flutter/material.dart';

class ProjectionPanel extends StatelessWidget {
  final Map<String, dynamic> projections;

  const ProjectionPanel({Key? key, required this.projections}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.all(20),
      decoration: BoxDecoration(
        color: Colors.white.withOpacity(0.03),
        borderRadius: BorderRadius.circular(24),
        border: Border.all(color: Colors.white.withOpacity(0.08)),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          const Text(
            "PERFORMANCE PROJECTIONS",
            style: TextStyle(fontSize: 12, fontWeight: FontWeight.bold, color: Colors.grey),
          ),
          const SizedBox(height: 20),
          _buildProjectionRow("Weight Forecast (4w)", "${projections['weight_4w'] ?? '--'} kg"),
          const Divider(color: Colors.white10),
          _buildProjectionRow("Strength Trend (8w)", "+${projections['strength_8w_pct'] ?? '0'}%"),
          const Divider(color: Colors.white10),
          _buildProjectionRow("Conditioning Index", "${projections['cond_index'] ?? '--'}"),
        ],
      ),
    );
  }

  Widget _buildProjectionRow(String label, String value) {
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 8.0),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceBetween,
        children: [
          Text(label, style: const TextStyle(fontSize: 14, color: Colors.white70)),
          Text(value, style: const TextStyle(fontSize: 16, fontWeight: FontWeight.bold, color: Colors.cyanAccent)),
        ],
      ),
    );
  }
}
