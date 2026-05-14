
class ChartDataPoint {
  final DateTime date;
  final double value;
  final double? secondaryValue;

  ChartDataPoint({required this.date, required this.value, this.secondaryValue});

  factory ChartDataPoint.fromJson(Map<String, dynamic> json) {
    return ChartDataPoint(
      date: DateTime.parse(json['date']),
      value: json['value'].toDouble(),
      secondaryValue: json['secondary_value']?.toDouble(),
    );
  }
}

class BodyChartsResponse {
  final List<ChartDataPoint> gainChart;
  final List<ChartDataPoint> lossChart;

  BodyChartsResponse({required this.gainChart, required this.lossChart});

  factory BodyChartsResponse.fromJson(Map<String, dynamic> json) {
    return BodyChartsResponse(
      gainChart: (json['gain_chart'] as List).map((e) => ChartDataPoint.fromJson(e)).toList(),
      lossChart: (json['loss_chart'] as List).map((e) => ChartDataPoint.fromJson(e)).toList(),
    );
  }
}
