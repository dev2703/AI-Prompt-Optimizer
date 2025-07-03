import openai
import anthropic
import google.generativeai as genai
from typing import Dict, Any, Optional
from app.core.config import settings


class AIService:
    def __init__(self):
        # Initialize OpenAI client
        if settings.OPENAI_API_KEY:
            openai.api_key = settings.OPENAI_API_KEY
        
        # Initialize Anthropic client
        if settings.ANTHROPIC_API_KEY:
            self.anthropic_client = anthropic.Anthropic(api_key=settings.ANTHROPIC_API_KEY)
        
        # Initialize Google AI client
        if settings.GOOGLE_API_KEY:
            genai.configure(api_key=settings.GOOGLE_API_KEY)
    
    async def generate_text(
        self, 
        system_prompt: str, 
        user_prompt: str, 
        model: str = "gpt-4",
        max_tokens: int = 2000,
        temperature: float = 0.7
    ) -> str:
        """
        Generate text using the specified AI model
        """
        try:
            if model.startswith("gpt"):
                return await self._generate_openai(system_prompt, user_prompt, model, max_tokens, temperature)
            elif model.startswith("claude"):
                return await self._generate_anthropic(system_prompt, user_prompt, model, max_tokens, temperature)
            elif model.startswith("gemini"):
                return await self._generate_google(system_prompt, user_prompt, model, max_tokens, temperature)
            else:
                # Default to OpenAI
                return await self._generate_openai(system_prompt, user_prompt, "gpt-4", max_tokens, temperature)
        
        except Exception as e:
            raise Exception(f"AI generation failed: {str(e)}")
    
    async def _generate_openai(self, system_prompt: str, user_prompt: str, model: str, max_tokens: int, temperature: float) -> str:
        """Generate text using OpenAI"""
        if not settings.OPENAI_API_KEY:
            raise Exception("OpenAI API key not configured")
        
        try:
            response = await openai.ChatCompletion.acreate(
                model=model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                max_tokens=max_tokens,
                temperature=temperature
            )
            
            return response.choices[0].message.content.strip()
        
        except Exception as e:
            raise Exception(f"OpenAI API error: {str(e)}")
    
    async def _generate_anthropic(self, system_prompt: str, user_prompt: str, model: str, max_tokens: int, temperature: float) -> str:
        """Generate text using Anthropic Claude"""
        if not settings.ANTHROPIC_API_KEY:
            raise Exception("Anthropic API key not configured")
        
        try:
            # Combine system and user prompts for Claude
            full_prompt = f"{system_prompt}\n\n{user_prompt}"
            
            response = await self.anthropic_client.messages.create(
                model=model,
                max_tokens=max_tokens,
                temperature=temperature,
                messages=[
                    {"role": "user", "content": full_prompt}
                ]
            )
            
            return response.content[0].text.strip()
        
        except Exception as e:
            raise Exception(f"Anthropic API error: {str(e)}")
    
    async def _generate_google(self, system_prompt: str, user_prompt: str, model: str, max_tokens: int, temperature: float) -> str:
        """Generate text using Google Gemini"""
        if not settings.GOOGLE_API_KEY:
            raise Exception("Google API key not configured")
        
        try:
            # Combine system and user prompts for Gemini
            full_prompt = f"{system_prompt}\n\n{user_prompt}"
            
            model_instance = genai.GenerativeModel(model)
            response = await model_instance.generate_content_async(
                full_prompt,
                generation_config=genai.types.GenerationConfig(
                    max_output_tokens=max_tokens,
                    temperature=temperature
                )
            )
            
            return response.text.strip()
        
        except Exception as e:
            raise Exception(f"Google AI API error: {str(e)}")
    
    async def analyze_text(self, text: str, analysis_type: str, model: str = "gpt-4") -> Dict[str, Any]:
        """
        Analyze text for various purposes (quality, sentiment, etc.)
        """
        system_prompts = {
            "quality": "Analyze the quality of this prompt. Consider clarity, specificity, and effectiveness. Return a JSON with scores from 1-10 for clarity, specificity, and overall quality.",
            "sentiment": "Analyze the sentiment of this text. Return a JSON with sentiment (positive/negative/neutral) and confidence score.",
            "complexity": "Analyze the complexity of this text. Return a JSON with readability score and complexity level.",
            "intent": "Analyze the intent and purpose of this prompt. Return a JSON with intent classification and confidence."
        }
        
        system_prompt = system_prompts.get(analysis_type, system_prompts["quality"])
        
        try:
            result = await self.generate_text(system_prompt, text, model, max_tokens=500, temperature=0.3)
            # Parse JSON response
            import json
            return json.loads(result)
        
        except Exception as e:
            return {"error": str(e)}
    
    def get_available_models(self) -> Dict[str, list]:
        """
        Get available models for each provider
        """
        return {
            "openai": ["gpt-4", "gpt-4-turbo", "gpt-3.5-turbo"],
            "anthropic": ["claude-3-opus", "claude-3-sonnet", "claude-3-haiku"],
            "google": ["gemini-pro", "gemini-pro-vision"]
        }
    
    def is_model_available(self, model: str) -> bool:
        """
        Check if a model is available
        """
        available_models = []
        for models in self.get_available_models().values():
            available_models.extend(models)
        
        return model in available_models 