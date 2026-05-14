from typing import Dict, List, Any
from sqlalchemy.orm import Session
from datetime import datetime, timedelta, date
from app.models.user import User
from app.models.daily_log import DailyLog
from app.models.nutrition import NutritionLog
from app.models.training import TrainingSession
from app.ai_engine.llm_service import LLMService

class AIAnalyzer:
    """
    AI-powered comprehensive user analysis service.
    Analyzes patterns across training, nutrition, and recovery to provide insights.
    """
    
    def __init__(self):
        self.llm = LLMService()
    
    def analyze_user_comprehensive(self, user: User, db: Session, days: int = 7) -> Dict[str, Any]:
        """
        Perform comprehensive AI analysis of user data.
        Returns insights, recommendations, and warnings.
        """
        # Gather data from last N days
        end_date = date.today()
        start_date = end_date - timedelta(days=days)
        
        # Get daily logs
        daily_logs = db.query(DailyLog).filter(
            DailyLog.user_id == user.id,
            DailyLog.date >= start_date,
            DailyLog.date <= end_date
        ).order_by(DailyLog.date).all()
        
        # Get nutrition logs
        nutrition_logs = db.query(NutritionLog).filter(
            NutritionLog.user_id == user.id,
            NutritionLog.timestamp >= datetime.combine(start_date, datetime.min.time())
        ).all()
        
        # Get training sessions
        training_sessions = db.query(TrainingSession).filter(
            TrainingSession.user_id == user.id,
            TrainingSession.date >= start_date
        ).all()
        
        # Calculate metrics
        metrics = self._calculate_metrics(daily_logs, nutrition_logs, training_sessions)
        
        # Detect patterns and issues
        patterns = self._detect_patterns(metrics, daily_logs)
        
        # Generate AI insights
        insights = self._generate_ai_insights(user, metrics, patterns)
        
        return {
            "metrics": metrics,
            "patterns": patterns,
            "insights": insights,
            "analysis_period": f"{days} days",
            "generated_at": datetime.utcnow().isoformat()
        }
    
    def _calculate_metrics(self, daily_logs: List[DailyLog], nutrition_logs: List[NutritionLog], 
                          training_sessions: List[TrainingSession]) -> Dict[str, Any]:
        """Calculate aggregate metrics from user data."""
        
        if not daily_logs:
            return {
                "avg_calories": 0,
                "avg_training_minutes": 0,
                "avg_sleep_hours": 0,
                "avg_recovery_score": 0,
                "total_workouts": 0,
                "nutrition_consistency": 0
            }
        
        # Daily log metrics
        total_calories = sum(log.total_calories_in for log in daily_logs)
        total_training = sum(log.total_training_minutes for log in daily_logs)
        total_sleep = sum(log.sleep_hours for log in daily_logs if log.sleep_hours)
        total_recovery = sum(log.recovery_score for log in daily_logs if log.recovery_score)
        
        sleep_count = len([log for log in daily_logs if log.sleep_hours and log.sleep_hours > 0])
        recovery_count = len([log for log in daily_logs if log.recovery_score and log.recovery_score > 0])
        
        # Nutrition metrics
        days_with_nutrition = len(set(log.timestamp.date() for log in nutrition_logs))
        nutrition_consistency = (days_with_nutrition / len(daily_logs) * 100) if daily_logs else 0
        
        return {
            "avg_calories": round(total_calories / len(daily_logs), 1) if daily_logs else 0,
            "avg_training_minutes": round(total_training / len(daily_logs), 1) if daily_logs else 0,
            "avg_sleep_hours": round(total_sleep / sleep_count, 1) if sleep_count > 0 else 0,
            "avg_recovery_score": round(total_recovery / recovery_count, 1) if recovery_count > 0 else 0,
            "total_workouts": len(training_sessions),
            "nutrition_consistency": round(nutrition_consistency, 1),
            "days_analyzed": len(daily_logs)
        }
    
    def _detect_patterns(self, metrics: Dict[str, Any], daily_logs: List[DailyLog]) -> Dict[str, Any]:
        """Detect patterns and potential issues in user data."""
        
        issues = []
        positive_patterns = []
        
        # Check for overtraining
        if metrics["avg_training_minutes"] > 90 and metrics["avg_recovery_score"] < 60:
            issues.append({
                "type": "overtraining",
                "severity": "high",
                "message": "High training volume with low recovery scores detected"
            })
        
        # Check for under-eating
        if metrics["avg_calories"] > 0 and metrics["avg_calories"] < 1800 and metrics["avg_training_minutes"] > 60:
            issues.append({
                "type": "nutrition",
                "severity": "medium",
                "message": "Calorie intake may be too low for training volume"
            })
        
        # Check for poor sleep
        if metrics["avg_sleep_hours"] > 0 and metrics["avg_sleep_hours"] < 6.5:
            issues.append({
                "type": "recovery",
                "severity": "high",
                "message": "Insufficient sleep detected - aim for 7-9 hours"
            })
        
        # Check for good consistency
        if metrics["nutrition_consistency"] > 80:
            positive_patterns.append({
                "type": "nutrition",
                "message": "Excellent nutrition tracking consistency"
            })
        
        if metrics["total_workouts"] >= 4 and metrics["avg_recovery_score"] > 70:
            positive_patterns.append({
                "type": "training",
                "message": "Great training consistency with good recovery"
            })
        
        # Detect trends
        trends = self._analyze_trends(daily_logs)
        
        return {
            "issues": issues,
            "positive_patterns": positive_patterns,
            "trends": trends
        }
    
    def _analyze_trends(self, daily_logs: List[DailyLog]) -> Dict[str, str]:
        """Analyze trends in daily metrics."""
        
        if len(daily_logs) < 3:
            return {}
        
        trends = {}
        
        # Sleep trend
        sleep_values = [log.sleep_hours for log in daily_logs if log.sleep_hours and log.sleep_hours > 0]
        if len(sleep_values) >= 3:
            if sleep_values[-1] > sleep_values[0]:
                trends["sleep"] = "improving"
            elif sleep_values[-1] < sleep_values[0]:
                trends["sleep"] = "declining"
            else:
                trends["sleep"] = "stable"
        
        # Recovery trend
        recovery_values = [log.recovery_score for log in daily_logs if log.recovery_score and log.recovery_score > 0]
        if len(recovery_values) >= 3:
            if recovery_values[-1] > recovery_values[0]:
                trends["recovery"] = "improving"
            elif recovery_values[-1] < recovery_values[0]:
                trends["recovery"] = "declining"
            else:
                trends["recovery"] = "stable"
        
        return trends
    
    def _generate_ai_insights(self, user: User, metrics: Dict[str, Any], 
                             patterns: Dict[str, Any]) -> Dict[str, Any]:
        """Generate AI-powered insights using LLM."""
        
        # Build context for AI
        context = f"""
        User Profile:
        - Name: {user.full_name}
        - Weight: {user.current_weight_kg}kg
        - Activity Level: {user.activity_level}
        
        Recent Metrics (7 days):
        - Average Calories: {metrics['avg_calories']} kcal/day
        - Average Training: {metrics['avg_training_minutes']} min/day
        - Average Sleep: {metrics['avg_sleep_hours']} hours/night
        - Average Recovery Score: {metrics['avg_recovery_score']}/100
        - Total Workouts: {metrics['total_workouts']}
        - Nutrition Tracking: {metrics['nutrition_consistency']}% consistent
        
        Detected Issues:
        {', '.join([issue['message'] for issue in patterns['issues']]) if patterns['issues'] else 'None'}
        
        Positive Patterns:
        {', '.join([p['message'] for p in patterns['positive_patterns']]) if patterns['positive_patterns'] else 'None'}
        """
        
        prompt = """Based on the user data above, provide:
        1. A brief overall assessment (2-3 sentences)
        2. Top 3 actionable recommendations
        3. One motivational insight
        
        Be specific, professional, and encouraging. Focus on what matters most."""
        
        try:
            ai_response = self.llm.generate_response(context, prompt)
            
            return {
                "summary": ai_response,
                "priority_recommendations": self._extract_recommendations(patterns),
                "motivational_message": self._generate_motivation(patterns, metrics)
            }
        except Exception as e:
            print(f"AI insight generation failed: {e}")
            return {
                "summary": "Keep up the great work! Your consistency is key to progress.",
                "priority_recommendations": self._extract_recommendations(patterns),
                "motivational_message": "Every workout counts. Stay focused on your goals!"
            }
    
    def _extract_recommendations(self, patterns: Dict[str, Any]) -> List[str]:
        """Extract top recommendations from patterns."""
        
        recommendations = []
        
        for issue in patterns.get("issues", []):
            if issue["type"] == "overtraining":
                recommendations.append("Consider adding a rest day or reducing training volume")
            elif issue["type"] == "nutrition":
                recommendations.append("Increase calorie intake to match training demands")
            elif issue["type"] == "recovery":
                recommendations.append("Prioritize 7-9 hours of sleep for optimal recovery")
        
        if not recommendations:
            recommendations.append("Maintain your current routine - you're doing great!")
            recommendations.append("Consider progressive overload in your training")
            recommendations.append("Stay consistent with nutrition tracking")
        
        return recommendations[:3]
    
    def _generate_motivation(self, patterns: Dict[str, Any], metrics: Dict[str, Any]) -> str:
        """Generate motivational message based on user performance."""
        
        if patterns.get("positive_patterns"):
            return "Your consistency is impressive! Keep building on this momentum."
        elif metrics["total_workouts"] >= 3:
            return "You're showing up and putting in the work. That's what champions do!"
        else:
            return "Every journey starts with a single step. You've got this!"
