"""
AI service for generating ad copy using Google Gemini.
"""
import google.generativeai as genai
from typing import List, Optional
import json
import logging
from app.core.config import settings
from app.schemas.schemas import AdVariation

logger = logging.getLogger(__name__)

# Configure Gemini
genai.configure(api_key=settings.GEMINI_API_KEY)


class AIService:
    """Service for AI-powered ad copy generation."""
    
    def __init__(self):
        self.model = genai.GenerativeModel(settings.GEMINI_MODEL)
    
    async def generate_ad_copy(
        self,
        product_name: str,
        value_props: List[str],
        brand_voice: str,
        scraped_content: Optional[str] = None
    ) -> List[AdVariation]:
        """
        Generate ad copy variations using Gemini.
        
        Args:
            product_name: Name of the product/service
            value_props: List of value propositions
            brand_voice: Desired brand voice/tone
            scraped_content: Optional scraped website content
            
        Returns:
            List of ad copy variations
        """
        try:
            # Build the prompt
            prompt = self._build_prompt(product_name, value_props, brand_voice, scraped_content)
            
            # Generate content
            response = self.model.generate_content(
                prompt,
                generation_config=genai.GenerationConfig(
                    temperature=0.8,
                    top_p=0.95,
                    top_k=40,
                    max_output_tokens=2048,
                )
            )
            
            # Parse the response
            variations = self._parse_response(response.text)
            return variations
            
        except Exception as e:
            logger.error(f"AI generation failed: {str(e)}")
            raise
    
    def _build_prompt(
        self,
        product_name: str,
        value_props: List[str],
        brand_voice: str,
        scraped_content: Optional[str]
    ) -> str:
        """Build the prompt for Gemini."""
        prompt = f"""You are an expert ad copywriter. Generate 5 different ad copy variations for the following product.

Product: {product_name}
Value Propositions: {', '.join(value_props)}
Brand Voice: {brand_voice}
"""
        
        if scraped_content:
            prompt += f"\nWebsite Content Context:\n{scraped_content[:1000]}\n"
        
        prompt += """
Generate 5 ad copy variations with different strategies. Each variation should include:
- headline: 30-90 characters, attention-grabbing
- body: 90-180 characters, compelling message
- cta: 15-30 characters, clear call-to-action
- strategy: Brief description of the approach used

Return ONLY valid JSON in this exact format:
{
  "variations": [
    {
      "headline": "...",
      "body": "...",
      "cta": "...",
      "strategy": "..."
    }
  ]
}
"""
        return prompt
    
    def _parse_response(self, response_text: str) -> List[AdVariation]:
        """Parse the AI response into AdVariation objects."""
        try:
            # Extract JSON from response (handle markdown code blocks)
            text = response_text.strip()
            if text.startswith("```json"):
                text = text[7:]
            if text.startswith("```"):
                text = text[3:]
            if text.endswith("```"):
                text = text[:-3]
            text = text.strip()
            
            # Parse JSON
            data = json.loads(text)
            variations = [AdVariation(**var) for var in data.get("variations", [])]
            
            if not variations:
                raise ValueError("No variations found in response")
            
            return variations
            
        except Exception as e:
            logger.error(f"Failed to parse AI response: {str(e)}")
            # Return a fallback variation
            return [
                AdVariation(
                    headline=f"Discover {product_name}",
                    body="Transform your experience with our innovative solution. Get started today.",
                    cta="Learn More",
                    strategy="Fallback generic copy"
                )
            ]
