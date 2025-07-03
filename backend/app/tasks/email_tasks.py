from celery import current_task
from datetime import datetime
from app.core.celery_app import celery_app
from app.core.config import settings


@celery_app.task(bind=True)
def send_welcome_email_task(self, user_email: str, user_name: str):
    """
    Send welcome email to new users
    """
    try:
        # This would integrate with your email service
        # For now, we'll just log the email
        print(f"Sending welcome email to {user_email} for user {user_name}")
        
        # Example email content
        email_content = {
            "to": user_email,
            "subject": "Welcome to AI Prompt Optimizer!",
            "body": f"""
            Hi {user_name},
            
            Welcome to AI Prompt Optimizer! We're excited to help you optimize your AI prompts and save on token costs.
            
            Here's what you can do:
            - Optimize prompts for token reduction
            - Enhance prompt quality and clarity
            - Compare costs across different AI models
            - Track your usage and savings
            
            Get started by creating your first prompt optimization!
            
            Best regards,
            The AI Prompt Optimizer Team
            """
        }
        
        # In production, you would send this via your email service
        # send_email(email_content)
        
        return {
            "status": "Welcome email sent successfully",
            "user_email": user_email
        }
    
    except Exception as e:
        current_task.update_state(
            state='FAILURE',
            meta={
                'status': 'Welcome email failed',
                'error': str(e)
            }
        )
        raise


@celery_app.task(bind=True)
def send_usage_alert_email_task(self, user_email: str, user_name: str, usage_percentage: float):
    """
    Send usage alert email when user approaches limits
    """
    try:
        if usage_percentage >= 90:
            subject = "⚠️ You're approaching your usage limit"
            urgency = "high"
        elif usage_percentage >= 75:
            subject = "📊 Usage Update - Consider upgrading"
            urgency = "medium"
        else:
            return {"status": "No alert needed"}
        
        email_content = {
            "to": user_email,
            "subject": subject,
            "body": f"""
            Hi {user_name},
            
            You've used {usage_percentage:.1f}% of your monthly optimization limit.
            
            To continue optimizing without interruption, consider upgrading to our Pro plan:
            - 1,000 optimizations per month
            - Advanced models and features
            - Priority support
            
            Upgrade now to unlock unlimited potential!
            
            Best regards,
            The AI Prompt Optimizer Team
            """
        }
        
        # In production, you would send this via your email service
        # send_email(email_content)
        
        return {
            "status": "Usage alert email sent successfully",
            "user_email": user_email,
            "usage_percentage": usage_percentage,
            "urgency": urgency
        }
    
    except Exception as e:
        current_task.update_state(
            state='FAILURE',
            meta={
                'status': 'Usage alert email failed',
                'error': str(e)
            }
        )
        raise


@celery_app.task(bind=True)
def send_weekly_report_email_task(self, user_email: str, user_name: str, report_data: dict):
    """
    Send weekly usage report email
    """
    try:
        email_content = {
            "to": user_email,
            "subject": "📈 Your Weekly AI Prompt Optimizer Report",
            "body": f"""
            Hi {user_name},
            
            Here's your weekly optimization report:
            
            📊 Weekly Summary:
            - Total Optimizations: {report_data.get('total_optimizations', 0)}
            - Tokens Saved: {report_data.get('total_tokens_saved', 0):,}
            - Cost Savings: ${report_data.get('total_cost_savings', 0):.4f}
            - Average Quality Score: {report_data.get('average_quality_score', 0):.1f}/10
            - Success Rate: {report_data.get('success_rate', 0):.1f}%
            
            🎯 Top Models Used:
            {self._format_model_usage(report_data.get('model_usage', {}))}
            
            Keep optimizing and saving!
            
            Best regards,
            The AI Prompt Optimizer Team
            """
        }
        
        # In production, you would send this via your email service
        # send_email(email_content)
        
        return {
            "status": "Weekly report email sent successfully",
            "user_email": user_email
        }
    
    except Exception as e:
        current_task.update_state(
            state='FAILURE',
            meta={
                'status': 'Weekly report email failed',
                'error': str(e)
            }
        )
        raise


@celery_app.task(bind=True)
def send_optimization_complete_email_task(self, user_email: str, user_name: str, optimization_data: dict):
    """
    Send email notification when optimization is complete
    """
    try:
        email_content = {
            "to": user_email,
            "subject": "✅ Your prompt optimization is complete!",
            "body": f"""
            Hi {user_name},
            
            Your prompt optimization is complete!
            
            📊 Results:
            - Token Reduction: {optimization_data.get('token_reduction_percentage', 0):.1f}%
            - Tokens Saved: {optimization_data.get('token_reduction', 0)}
            - Cost Savings: ${optimization_data.get('cost_savings', 0):.4f}
            - Quality Score: {optimization_data.get('quality_score', 0):.1f}/10
            
            View your optimized prompt in the dashboard.
            
            Best regards,
            The AI Prompt Optimizer Team
            """
        }
        
        # In production, you would send this via your email service
        # send_email(email_content)
        
        return {
            "status": "Optimization complete email sent successfully",
            "user_email": user_email
        }
    
    except Exception as e:
        current_task.update_state(
            state='FAILURE',
            meta={
                'status': 'Optimization complete email failed',
                'error': str(e)
            }
        )
        raise


def _format_model_usage(self, model_usage: dict) -> str:
    """Format model usage for email"""
    if not model_usage:
        return "No models used this week"
    
    formatted = []
    for model, count in sorted(model_usage.items(), key=lambda x: x[1], reverse=True):
        formatted.append(f"- {model}: {count} optimizations")
    
    return "\n".join(formatted) 