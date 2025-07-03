import tiktoken
from typing import Dict, Any
from app.core.config import settings


class TokenService:
    def __init__(self):
        self.model_pricing = settings.MODEL_PRICING
        self.encoders = {}
    
    def count_tokens(self, text: str, model: str = "gpt-4") -> int:
        """
        Count tokens in text for a specific model
        """
        try:
            # Get or create encoder for the model
            if model not in self.encoders:
                if model.startswith("gpt"):
                    encoding_name = "cl100k_base"  # GPT-4 and GPT-3.5 use this
                elif model.startswith("claude"):
                    encoding_name = "cl100k_base"  # Claude models use this
                elif model.startswith("gemini"):
                    # Gemini uses a different tokenization, approximate with GPT
                    encoding_name = "cl100k_base"
                else:
                    encoding_name = "cl100k_base"  # Default
                
                self.encoders[model] = tiktoken.get_encoding(encoding_name)
            
            encoder = self.encoders[model]
            tokens = encoder.encode(text)
            return len(tokens)
        
        except Exception as e:
            # Fallback to word-based estimation
            words = text.split()
            return len(words) * 1.3  # Rough approximation
    
    def calculate_cost(self, token_count: int, model: str = "gpt-4") -> float:
        """
        Calculate cost for token count and model
        """
        if model not in self.model_pricing:
            # Use default pricing if model not found
            model = "gpt-4"
        
        pricing = self.model_pricing[model]
        input_cost_per_1k = pricing.get("input", 0.03)
        output_cost_per_1k = pricing.get("output", 0.06)
        
        # Assume 80% input, 20% output tokens for estimation
        input_tokens = int(token_count * 0.8)
        output_tokens = token_count - input_tokens
        
        input_cost = (input_tokens / 1000) * input_cost_per_1k
        output_cost = (output_tokens / 1000) * output_cost_per_1k
        
        return input_cost + output_cost
    
    def estimate_cost_savings(self, original_tokens: int, optimized_tokens: int, model: str = "gpt-4") -> Dict[str, Any]:
        """
        Estimate cost savings from token reduction
        """
        original_cost = self.calculate_cost(original_tokens, model)
        optimized_cost = self.calculate_cost(optimized_tokens, model)
        cost_savings = original_cost - optimized_cost
        
        return {
            "original_tokens": original_tokens,
            "optimized_tokens": optimized_tokens,
            "tokens_saved": original_tokens - optimized_tokens,
            "token_reduction_percentage": ((original_tokens - optimized_tokens) / original_tokens) * 100,
            "original_cost": original_cost,
            "optimized_cost": optimized_cost,
            "cost_savings": cost_savings,
            "cost_savings_percentage": (cost_savings / original_cost) * 100 if original_cost > 0 else 0
        }
    
    def compare_models(self, text: str, models: list = None) -> Dict[str, Any]:
        """
        Compare token count and cost across different models
        """
        if models is None:
            models = ["gpt-4", "gpt-3.5-turbo", "claude-3-sonnet", "gemini-pro"]
        
        comparison = {}
        
        for model in models:
            token_count = self.count_tokens(text, model)
            cost = self.calculate_cost(token_count, model)
            
            comparison[model] = {
                "token_count": token_count,
                "estimated_cost": cost,
                "cost_per_1k_tokens": cost / (token_count / 1000) if token_count > 0 else 0
            }
        
        return comparison
    
    def get_model_info(self, model: str) -> Dict[str, Any]:
        """
        Get information about a specific model
        """
        if model not in self.model_pricing:
            return {
                "model": model,
                "supported": False,
                "pricing": None
            }
        
        pricing = self.model_pricing[model]
        return {
            "model": model,
            "supported": True,
            "pricing": pricing,
            "input_cost_per_1k": pricing.get("input", 0),
            "output_cost_per_1k": pricing.get("output", 0)
        }
    
    def get_supported_models(self) -> list:
        """
        Get list of supported models
        """
        return list(self.model_pricing.keys()) 