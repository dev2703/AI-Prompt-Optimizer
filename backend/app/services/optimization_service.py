import time
from typing import Dict, Any, Optional
from sqlalchemy.orm import Session
from app.core.config import settings
from app.models.prompt import Prompt, Optimization, OptimizationType
from app.services.token_service import TokenService
from app.services.ai_service import AIService
from app.services.quality_service import QualityService


class OptimizationService:
    def __init__(self):
        self.token_service = TokenService()
        self.ai_service = AIService()
        self.quality_service = QualityService()
    
    async def optimize_prompt(
        self,
        prompt_id: int,
        user_id: int,
        optimization_type: OptimizationType,
        target_model: Optional[str] = None,
        reduction_target: Optional[float] = None,
        quality_threshold: Optional[float] = None,
        db: Session = None
    ) -> Dict[str, Any]:
        """
        Optimize a prompt using AI
        """
        start_time = time.time()
        
        # Get the prompt
        prompt = db.query(Prompt).filter(Prompt.id == prompt_id).first()
        if not prompt:
            raise ValueError("Prompt not found")
        
        original_prompt = prompt.original_prompt
        original_tokens = self.token_service.count_tokens(original_prompt, target_model or settings.DEFAULT_MODEL)
        
        # Determine optimization strategy
        if optimization_type == OptimizationType.TOKEN_REDUCTION:
            optimized_prompt = await self._reduce_tokens(
                original_prompt, 
                reduction_target or settings.DEFAULT_TOKEN_REDUCTION_TARGET,
                target_model
            )
        elif optimization_type == OptimizationType.QUALITY_ENHANCEMENT:
            optimized_prompt = await self._enhance_quality(
                original_prompt,
                quality_threshold or 8.0,
                target_model
            )
        elif optimization_type == OptimizationType.CLARITY_IMPROVEMENT:
            optimized_prompt = await self._improve_clarity(
                original_prompt,
                target_model
            )
        elif optimization_type == OptimizationType.MODEL_ADAPTATION:
            optimized_prompt = await self._adapt_for_model(
                original_prompt,
                target_model
            )
        else:
            raise ValueError(f"Unsupported optimization type: {optimization_type}")
        
        # Calculate metrics
        optimized_tokens = self.token_service.count_tokens(optimized_prompt, target_model or settings.DEFAULT_MODEL)
        token_reduction = original_tokens - optimized_tokens
        token_reduction_percentage = (token_reduction / original_tokens) * 100 if original_tokens > 0 else 0
        
        # Calculate costs
        original_cost = self.token_service.calculate_cost(original_tokens, target_model or settings.DEFAULT_MODEL)
        optimized_cost = self.token_service.calculate_cost(optimized_tokens, target_model or settings.DEFAULT_MODEL)
        cost_savings = original_cost - optimized_cost
        
        # Quality assessment
        quality_scores = await self.quality_service.assess_prompt_quality(optimized_prompt)
        
        processing_time = time.time() - start_time
        
        # Create optimization record
        optimization = Optimization(
            prompt_id=prompt_id,
            user_id=user_id,
            optimization_type=optimization_type,
            model_used=target_model or settings.DEFAULT_MODEL,
            original_prompt=original_prompt,
            optimized_prompt=optimized_prompt,
            original_tokens=original_tokens,
            optimized_tokens=optimized_tokens,
            token_reduction=token_reduction,
            token_reduction_percentage=token_reduction_percentage,
            quality_score=quality_scores.get('overall', 0),
            clarity_score=quality_scores.get('clarity', 0),
            specificity_score=quality_scores.get('specificity', 0),
            original_cost=original_cost,
            optimized_cost=optimized_cost,
            cost_savings=cost_savings,
            cost_savings_percentage=(cost_savings / original_cost) * 100 if original_cost > 0 else 0,
            processing_time=processing_time
        )
        
        db.add(optimization)
        db.commit()
        db.refresh(optimization)
        
        # Update prompt
        prompt.optimized_prompt = optimized_prompt
        prompt.original_tokens = original_tokens
        prompt.optimized_tokens = optimized_tokens
        prompt.token_reduction_percentage = token_reduction_percentage
        prompt.clarity_score = quality_scores.get('clarity', 0)
        prompt.specificity_score = quality_scores.get('specificity', 0)
        prompt.overall_quality_score = quality_scores.get('overall', 0)
        prompt.status = "completed"
        
        db.commit()
        
        return {
            "id": optimization.id,
            "prompt_id": prompt_id,
            "optimization_type": optimization_type,
            "model_used": target_model or settings.DEFAULT_MODEL,
            "original_prompt": original_prompt,
            "optimized_prompt": optimized_prompt,
            "original_tokens": original_tokens,
            "optimized_tokens": optimized_tokens,
            "token_reduction": token_reduction,
            "token_reduction_percentage": token_reduction_percentage,
            "quality_score": quality_scores.get('overall', 0),
            "clarity_score": quality_scores.get('clarity', 0),
            "specificity_score": quality_scores.get('specificity', 0),
            "original_cost": original_cost,
            "optimized_cost": optimized_cost,
            "cost_savings": cost_savings,
            "cost_savings_percentage": (cost_savings / original_cost) * 100 if original_cost > 0 else 0,
            "processing_time": processing_time
        }
    
    async def _reduce_tokens(self, prompt: str, reduction_target: float, model: str) -> str:
        """Reduce token count while maintaining quality"""
        system_prompt = f"""
        You are an expert at optimizing prompts to reduce token usage while maintaining effectiveness.
        Reduce the token count by approximately {reduction_target * 100:.0f}% while preserving the core meaning and intent.
        
        Guidelines:
        - Remove redundant words and phrases
        - Use more concise language
        - Maintain clarity and specificity
        - Preserve all essential information
        - Use abbreviations where appropriate
        
        Return only the optimized prompt, no explanations.
        """
        
        return await self.ai_service.generate_text(system_prompt, prompt, model)
    
    async def _enhance_quality(self, prompt: str, quality_threshold: float, model: str) -> str:
        """Enhance prompt quality and effectiveness"""
        system_prompt = f"""
        You are an expert at improving prompt quality and effectiveness.
        Enhance the prompt to achieve a quality score of at least {quality_threshold}/10.
        
        Focus on:
        - Clarity and precision
        - Specificity and context
        - Logical structure
        - Actionable instructions
        - Appropriate tone and style
        
        Return only the enhanced prompt, no explanations.
        """
        
        return await self.ai_service.generate_text(system_prompt, prompt, model)
    
    async def _improve_clarity(self, prompt: str, model: str) -> str:
        """Improve prompt clarity and understandability"""
        system_prompt = """
        You are an expert at improving prompt clarity and understandability.
        Make the prompt clearer, more specific, and easier to understand.
        
        Focus on:
        - Clear and unambiguous language
        - Specific instructions and requirements
        - Logical flow and structure
        - Removing ambiguity
        - Adding context where needed
        
        Return only the improved prompt, no explanations.
        """
        
        return await self.ai_service.generate_text(system_prompt, prompt, model)
    
    async def _adapt_for_model(self, prompt: str, target_model: str) -> str:
        """Adapt prompt for specific AI model"""
        system_prompt = f"""
        You are an expert at adapting prompts for different AI models.
        Adapt this prompt specifically for {target_model} to maximize effectiveness.
        
        Consider:
        - Model-specific capabilities and limitations
        - Optimal prompt structure for this model
        - Model-specific best practices
        - Token efficiency for this model
        
        Return only the adapted prompt, no explanations.
        """
        
        return await self.ai_service.generate_text(system_prompt, prompt, target_model) 