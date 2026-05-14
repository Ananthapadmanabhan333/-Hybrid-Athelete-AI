class Injury {
  final int id;
  final int userId;
  final String bodyPart;
  final String injuryType;
  final String severity;
  final int painLevel;
  final String status;
  final String? notes;
  final DateTime createdAt;

  Injury({
    required this.id,
    required this.userId,
    required this.bodyPart,
    required this.injuryType,
    required this.severity,
    required this.painLevel,
    required this.status,
    this.notes,
    required this.createdAt,
  });

  factory Injury.fromJson(Map<String, dynamic> json) {
    return Injury(
      id: json['id'],
      userId: json['user_id'],
      bodyPart: json['body_part'],
      injuryType: json['injury_type'],
      severity: json['severity'],
      painLevel: json['pain_level'],
      status: json['status'],
      notes: json['notes'],
      createdAt: DateTime.parse(json['created_at']),
    );
  }
}

class RecoveryStatus {
  final int score;
  final String status;
  final List<String> breakdown;
  final List<String> activeInjuries;

  RecoveryStatus({
    required this.score,
    required this.status,
    required this.breakdown,
    required this.activeInjuries,
  });

  factory RecoveryStatus.fromJson(Map<String, dynamic> json) {
    return RecoveryStatus(
      score: json['score'],
      status: json['status'],
      breakdown: List<String>.from(json['breakdown'] ?? []),
      activeInjuries: List<String>.from(json['active_injuries'] ?? []),
    );
  }
}
