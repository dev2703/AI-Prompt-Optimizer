import re
from typing import Dict, Any
from app.services.ai_service import AIService


class QualityService:
    def __init__(self):
        self.ai_service = AIService()
    
    async def assess_prompt_quality(self, prompt: str) -> Dict[str, float]:
        """
        Assess the quality of a prompt across multiple dimensions
        """
        try:
            # Get AI-based quality assessment
            ai_analysis = await self.ai_service.analyze_text(prompt, "quality")
            
            # Get rule-based assessments
            clarity_score = self._assess_clarity(prompt)
            specificity_score = self._assess_specificity(prompt)
            structure_score = self._assess_structure(prompt)
            
            # Combine AI and rule-based scores
            overall_score = self._calculate_overall_score(
                ai_analysis.get('overall', 5.0),
                clarity_score,
                specificity_score,
                structure_score
            )
            
            return {
                "overall": round(overall_score, 2),
                "clarity": round(clarity_score, 2),
                "specificity": round(specificity_score, 2),
                "structure": round(structure_score, 2),
                "ai_assessment": ai_analysis
            }
        
        except Exception as e:
            # Fallback to rule-based assessment only
            clarity_score = self._assess_clarity(prompt)
            specificity_score = self._assess_specificity(prompt)
            structure_score = self._assess_structure(prompt)
            overall_score = self._calculate_overall_score(5.0, clarity_score, specificity_score, structure_score)
            
            return {
                "overall": round(overall_score, 2),
                "clarity": round(clarity_score, 2),
                "specificity": round(specificity_score, 2),
                "structure": round(structure_score, 2),
                "error": str(e)
            }
    
    def _assess_clarity(self, prompt: str) -> float:
        """
        Assess prompt clarity using rule-based metrics
        """
        score = 5.0  # Base score
        
        # Length assessment
        word_count = len(prompt.split())
        if 10 <= word_count <= 100:
            score += 1.0
        elif word_count < 10:
            score -= 1.0
        elif word_count > 200:
            score -= 0.5
        
        # Sentence structure
        sentences = re.split(r'[.!?]+', prompt)
        avg_sentence_length = sum(len(s.split()) for s in sentences) / len(sentences) if sentences else 0
        
        if 5 <= avg_sentence_length <= 20:
            score += 0.5
        elif avg_sentence_length > 30:
            score -= 0.5
        
        # Clarity indicators
        clarity_indicators = ['clearly', 'specifically', 'precisely', 'exactly', 'in detail']
        clarity_count = sum(1 for indicator in clarity_indicators if indicator in prompt.lower())
        score += min(clarity_count * 0.3, 1.0)
        
        # Ambiguity indicators
        ambiguity_indicators = ['maybe', 'perhaps', 'possibly', 'might', 'could', 'somehow']
        ambiguity_count = sum(1 for indicator in ambiguity_indicators if indicator in prompt.lower())
        score -= min(ambiguity_count * 0.2, 1.0)
        
        return max(1.0, min(10.0, score))
    
    def _assess_specificity(self, prompt: str) -> float:
        """
        Assess prompt specificity using rule-based metrics
        """
        score = 5.0  # Base score
        
        # Specific details
        specific_indicators = ['numbers', 'dates', 'names', 'locations', 'quantities']
        specificity_count = 0
        
        # Check for numbers
        if re.search(r'\d+', prompt):
            specificity_count += 1
        
        # Check for dates
        if re.search(r'\d{4}|\d{1,2}/\d{1,2}|\d{1,2}-\d{1,2}', prompt):
            specificity_count += 1
        
        # Check for proper nouns (capitalized words)
        proper_nouns = len(re.findall(r'\b[A-Z][a-z]+\b', prompt))
        if proper_nouns > 0:
            specificity_count += 1
        
        # Check for specific quantities
        quantity_indicators = ['exactly', 'precisely', 'specifically', 'in particular']
        if any(indicator in prompt.lower() for indicator in quantity_indicators):
            specificity_count += 1
        
        score += min(specificity_count * 0.5, 2.0)
        
        # Vague terms penalty
        vague_terms = ['thing', 'stuff', 'something', 'anything', 'everything', 'nothing']
        vague_count = sum(1 for term in vague_terms if term in prompt.lower())
        score -= min(vague_count * 0.3, 1.5)
        
        return max(1.0, min(10.0, score))
    
    def _assess_structure(self, prompt: str) -> float:
        """
        Assess prompt structure and organization
        """
        score = 5.0  # Base score
        
        # Paragraph structure
        paragraphs = prompt.split('\n\n')
        if 1 <= len(paragraphs) <= 3:
            score += 0.5
        
        # Bullet points or numbered lists
        if re.search(r'^\s*[-*•]\s|^\s*\d+\.', prompt, re.MULTILINE):
            score += 0.5
        
        # Logical connectors
        connectors = ['because', 'therefore', 'however', 'although', 'furthermore', 'additionally']
        connector_count = sum(1 for connector in connectors if connector in prompt.lower())
        score += min(connector_count * 0.2, 1.0)
        
        # Question structure
        if '?' in prompt:
            score += 0.3
        
        # Action-oriented language
        action_verbs = ['create', 'generate', 'write', 'analyze', 'explain', 'describe', 'compare']
        action_count = sum(1 for verb in action_verbs if verb in prompt.lower())
        score += min(action_count * 0.2, 1.0)
        
        return max(1.0, min(10.0, score))
    
    def _calculate_overall_score(self, ai_score: float, clarity: float, specificity: float, structure: float) -> float:
        """
        Calculate overall quality score
        """
        # Weighted average: AI assessment gets higher weight
        weights = {
            'ai': 0.4,
            'clarity': 0.25,
            'specificity': 0.2,
            'structure': 0.15
        }
        
        overall = (
            ai_score * weights['ai'] +
            clarity * weights['clarity'] +
            specificity * weights['specificity'] +
            structure * weights['structure']
        )
        
        return max(1.0, min(10.0, overall))
    
    def get_quality_breakdown(self, prompt: str) -> Dict[str, Any]:
        """
        Get detailed quality breakdown
        """
        return {
            "word_count": len(prompt.split()),
            "sentence_count": len(re.split(r'[.!?]+', prompt)),
            "avg_sentence_length": len(prompt.split()) / len(re.split(r'[.!?]+', prompt)) if prompt else 0,
            "paragraph_count": len(prompt.split('\n\n')),
            "has_numbers": bool(re.search(r'\d+', prompt)),
            "has_dates": bool(re.search(r'\d{4}|\d{1,2}/\d{1,2}|\d{1,2}-\d{1,2}', prompt)),
            "has_proper_nouns": len(re.findall(r'\b[A-Z][a-z]+\b', prompt)),
            "has_questions": '?' in prompt,
            "has_lists": bool(re.search(r'^\s*[-*•]\s|^\s*\d+\.', prompt, re.MULTILINE))
        } 