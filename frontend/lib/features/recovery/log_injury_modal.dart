import 'package:flutter/material.dart';
import '../../core/app_theme.dart';
import '../../services/recovery_service.dart';
import '../../services/haptic_service.dart';
import 'package:google_fonts/google_fonts.dart';

class LogInjuryModal extends StatefulWidget {
  final VoidCallback onSaved;

  const LogInjuryModal({super.key, required this.onSaved});

  @override
  State<LogInjuryModal> createState() => _LogInjuryModalState();
}

class _LogInjuryModalState extends State<LogInjuryModal> {
  final RecoveryService _recoveryService = RecoveryService();
  final _formKey = GlobalKey<FormState>();
  
  String _selectedBodyPart = 'knee';
  String _selectedType = 'strain';
  String _selectedSeverity = 'mild';
  int _painLevel = 3;
  bool _isSubmitting = false;

  final List<String> _bodyParts = ['shoulder', 'knee', 'lower_back', 'ankle', 'wrist', 'elbow', 'hip', 'general'];
  final List<String> _types = ['strain', 'sprain', 'impact', 'overuse', 'soreness', 'surgery'];
  final List<String> _severities = ['mild', 'moderate', 'severe'];

  Future<void> _submit() async {
    if (!_formKey.currentState!.validate()) return;
    
    setState(() => _isSubmitting = true);
    HapticService().selection();

    final success = await _recoveryService.logInjury({
      'body_part': _selectedBodyPart,
      'injury_type': _selectedType,
      'severity': _selectedSeverity,
      'pain_level': _painLevel,
      'notes': 'Logged via app'
    });

    if (mounted) {
      if (success) {
        HapticService().success();
        widget.onSaved();
        Navigator.pop(context);
      } else {
        HapticService().error();
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(content: Text("Failed to log injury")),
        );
      }
      setState(() => _isSubmitting = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.all(24),
      decoration: const BoxDecoration(
        color: AppTheme.surfaceColor,
        borderRadius: BorderRadius.vertical(top: Radius.circular(30)),
      ),
      child: Form(
        key: _formKey,
        child: Column(
          mainAxisSize: MainAxisSize.min,
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Center(
              child: Container(
                width: 40, 
                height: 4, 
                decoration: BoxDecoration(color: Colors.grey[800], borderRadius: BorderRadius.circular(2)),
              ),
            ),
            const SizedBox(height: 24),
            Text("Log New Issue", style: Theme.of(context).textTheme.displayMedium?.copyWith(fontSize: 24)),
            const SizedBox(height: 24),
            
            _buildDropdown("Body Part", _bodyParts, _selectedBodyPart, (val) => setState(() => _selectedBodyPart = val!)),
            const SizedBox(height: 16),
            _buildDropdown("Issue Type", _types, _selectedType, (val) => setState(() => _selectedType = val!)),
            const SizedBox(height: 16),
            _buildDropdown("Severity", _severities, _selectedSeverity, (val) => setState(() => _selectedSeverity = val!)),
            
            const SizedBox(height: 24),
            Text("Pain Level: $_painLevel/10", style: const TextStyle(color: AppTheme.textSecondary)),
            Slider(
              value: _painLevel.toDouble(),
              min: 1,
              max: 10,
              divisions: 9,
              activeColor: AppTheme.accentColor,
              onChanged: (val) {
                setState(() => _painLevel = val.toInt());
                HapticService().lightImpact();
              },
            ),
            
            const SizedBox(height: 32),
            SizedBox(
              width: double.infinity,
              child: ElevatedButton(
                onPressed: _isSubmitting ? null : _submit,
                child: _isSubmitting 
                  ? const SizedBox(height: 20, width: 20, child: CircularProgressIndicator(strokeWidth: 2, color: Colors.black)) 
                  : const Text("SAVE RECORD"),
              ),
            ),
            const SizedBox(height: 24 + 100), // Bottom padding for keyboard/nav
          ],
        ),
      ),
    );
  }

  Widget _buildDropdown(String label, List<String> items, String current, ValueChanged<String?> onChanged) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text(label, style: const TextStyle(color: AppTheme.textSecondary, fontSize: 12)),
        const SizedBox(height: 8),
        Container(
          padding: const EdgeInsets.symmetric(horizontal: 16),
          decoration: BoxDecoration(
            color: Colors.black,
            borderRadius: BorderRadius.circular(12),
            border: Border.all(color: Colors.white10),
          ),
          child: DropdownButtonHideUnderline(
            child: DropdownButton<String>(
              value: current,
              isExpanded: true,
              dropdownColor: AppTheme.surfaceColor,
              style: GoogleFonts.outfit(color: Colors.white, fontSize: 16),
              items: items.map((e) => DropdownMenuItem(value: e, child: Text(e.toUpperCase()))).toList(),
              onChanged: onChanged,
            ),
          ),
        ),
      ],
    );
  }
}
