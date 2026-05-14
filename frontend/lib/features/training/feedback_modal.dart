import 'package:flutter/material.dart';
import '../../core/app_theme.dart';
import 'package:google_fonts/google_fonts.dart';

class FeedbackModal extends StatefulWidget {
  final Function(int rpe, int enjoyment, Map<String, int> soreness) onSubmit;

  const FeedbackModal({super.key, required this.onSubmit});

  @override
  State<FeedbackModal> createState() => _FeedbackModalState();
}

class _FeedbackModalState extends State<FeedbackModal> {
  int _rpe = 5;
  int _enjoyment = 3;
  Map<String, int> _soreness = {
    "Shoulders": 0,
    "Chest": 0,
    "Back": 0,
    "Legs": 0,
    "Arms": 0,
  };

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.all(24),
      decoration: const BoxDecoration(
        color: AppTheme.backgroundColor,
        borderRadius: BorderRadius.vertical(top: Radius.circular(30)),
      ),
      child: SingleChildScrollView(
        child: Column(
          mainAxisSize: MainAxisSize.min,
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            Text("Session Complete!", textAlign: TextAlign.center, style: Theme.of(context).textTheme.displayMedium),
            const SizedBox(height: 8),
            Text("Help us adapt your next workout.", textAlign: TextAlign.center, style: Theme.of(context).textTheme.bodyMedium),
            const SizedBox(height: 32),
            
            _buildSliderSection("Rate Perceived Exertion (RPE)", _rpe.toDouble(), 1, 10, (val) {
              setState(() => _rpe = val.toInt());
            }),
            
            _buildSliderSection("Enjoyment", _enjoyment.toDouble(), 1, 5, (val) {
              setState(() => _enjoyment = val.toInt());
            }),
            
            const SizedBox(height: 24),
            Text("Soreness Check", style: Theme.of(context).textTheme.titleLarge),
            const SizedBox(height: 16),
            Wrap(
              spacing: 8,
              runSpacing: 8,
              children: _soreness.keys.map((part) {
                int level = _soreness[part]!;
                bool isSore = level > 0;
                return ChoiceChip(
                  label: Text(isSore ? "$part ($level)" : part),
                  selected: isSore,
                  selectedColor: AppTheme.secondaryColor,
                  onSelected: (selected) {
                    setState(() {
                      _soreness[part] = selected ? 3 : 0; // Default to mild soreness
                    });
                  },
                );
              }).toList(),
            ),
            
            const SizedBox(height: 40),
            ElevatedButton(
              onPressed: () {
                widget.onSubmit(_rpe, _enjoyment, _soreness);
                Navigator.pop(context);
              },
              child: const Text("SUBMIT FEEDBACK"),
            ),
            const SizedBox(height: 24),
          ],
        ),
      ),
    );
  }

  Widget _buildSliderSection(String title, double value, double min, double max, Function(double) onChanged) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Row(
          mainAxisAlignment: MainAxisAlignment.spaceBetween,
          children: [
            Text(title, style: const TextStyle(fontWeight: FontWeight.bold)),
            Text(value.toInt().toString(), style: const TextStyle(color: AppTheme.primaryColor, fontWeight: FontWeight.bold, fontSize: 18)),
          ],
        ),
        Slider(
          value: value,
          min: min,
          max: max,
          divisions: (max - min).toInt(),
          activeColor: AppTheme.primaryColor,
          onChanged: onChanged,
        ),
      ],
    );
  }
}
