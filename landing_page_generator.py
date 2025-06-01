#!/usr/bin/env python3
"""
Landing Page Generator - Creates high-converting landing pages using proven patterns
"""
import os
import json
import logging
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime
from dataclasses import dataclass
import anthropic

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@dataclass
class PageConfig:
    """Configuration for generating a landing page"""
    page_type: str  # quiz_funnel, advertorial, vsl_page, sales_letter
    industry: str  # fitness, saas, finance, etc.
    product_name: str
    product_type: str  # physical, digital, service, membership
    price_point: float
    target_audience: Dict[str, Any]  # demographics, sophistication, awareness
    angle: str  # transformation_story, authority_expert, etc.
    length: str  # short, medium, long
    urgency_level: str  # low, medium, high
    voice_tone: str  # professional, casual, urgent, friendly
    specific_benefits: List[str]
    pain_points: List[str]
    unique_mechanism: Optional[str] = None
    guarantee_type: Optional[str] = "30_day_money_back"
    bonuses: Optional[List[Dict[str, str]]] = None

class PatternLibrary:
    """Loads and manages the pattern library"""
    
    def __init__(self, config_dir: str = "config"):
        self.config_dir = Path(config_dir)
        self.page_types = self._load_json("page_types.json")
        self.angles = self._load_json("angles.json")
        self.pattern_rules = self._load_json("pattern_rules.json")
        
        # Load analysis patterns if available
        analysis_dir = Path("../output")
        if analysis_dir.exists():
            self.copy_swipes = self._load_json("copy_swipe_file.json", analysis_dir)
            self.conversion_formulas = self._load_json("conversion_formulas.json", analysis_dir)
        else:
            self.copy_swipes = {}
            self.conversion_formulas = {}
    
    def _load_json(self, filename: str, directory: Optional[Path] = None) -> Dict:
        """Load JSON configuration file"""
        dir_path = directory or self.config_dir
        filepath = dir_path / filename
        
        if filepath.exists():
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        else:
            logger.warning(f"Configuration file not found: {filepath}")
            return {}
    
    def get_page_structure(self, page_type: str) -> List[str]:
        """Get the structure for a specific page type"""
        return self.page_types.get("page_types", {}).get(page_type, {}).get("structure", [])
    
    def get_angle_elements(self, angle: str) -> Dict[str, Any]:
        """Get elements for a specific angle"""
        return self.angles.get("angles", {}).get(angle, {})
    
    def get_relevant_patterns(self, config: PageConfig) -> Dict[str, Any]:
        """Get patterns relevant to the configuration"""
        patterns = {
            "page_structure": self.get_page_structure(config.page_type),
            "angle_elements": self.get_angle_elements(config.angle),
            "universal_patterns": self.pattern_rules.get("universal_patterns", {}),
            "page_rules": self.pattern_rules.get("page_specific_rules", {}).get(config.page_type, {}),
            "effectiveness_multipliers": self.pattern_rules.get("effectiveness_multipliers", {})
        }
        
        # Add relevant swipes if available
        if self.copy_swipes:
            patterns["headline_examples"] = self.copy_swipes.get("headlines", {}).get("main_headlines", [])[:5]
            patterns["cta_examples"] = self.copy_swipes.get("ctas", {}).get("high_converting", [])[:5]
            patterns["guarantee_examples"] = self.copy_swipes.get("guarantees", {}).get("strong_guarantees", [])[:3]
        
        return patterns

class PromptEngine:
    """Builds prompts for Claude API based on patterns and configuration"""
    
    def __init__(self, patterns: PatternLibrary):
        self.patterns = patterns
    
    def build_master_prompt(self, config: PageConfig, relevant_patterns: Dict[str, Any]) -> str:
        """Build the master prompt for page generation"""
        
        prompt = f"""You are an expert copywriter creating a {config.page_type} landing page.

You have access to proven patterns from analyzing high-converting pages:
- Page structure elements to include
- Psychological triggers that convert
- Specific formulas and templates that work

CONTEXT:
- Product: {config.product_name} ({config.product_type})
- Price: ${config.price_point}
- Industry: {config.industry}
- Target Audience: {json.dumps(config.target_audience)}
- Angle: {config.angle}
- Length: {config.length}
- Voice/Tone: {config.voice_tone}

KEY BENEFITS TO EMPHASIZE:
{chr(10).join([f'- {benefit}' for benefit in config.specific_benefits])}

PAIN POINTS TO ADDRESS:
{chr(10).join([f'- {pain}' for pain in config.pain_points])}

{"UNIQUE MECHANISM: " + config.unique_mechanism if config.unique_mechanism else ""}

PROVEN PATTERNS TO USE:

1. Page Structure (include all these sections):
{chr(10).join([f'- {section}' for section in relevant_patterns['page_structure']])}

2. Angle Elements:
- Emotional Arc: {relevant_patterns['angle_elements'].get('emotional_arc', [])}
- Key Elements: {relevant_patterns['angle_elements'].get('key_elements', [])}

3. Universal Patterns:
- Use 2-3 psychological triggers from: {relevant_patterns['universal_patterns'].get('psychological_triggers', {}).get('mandatory', [])}
- Follow trust sequence: {relevant_patterns['universal_patterns'].get('trust_sequence', [])}
- Apply value stacking formula with 10-15x value

4. Effectiveness Multipliers to Include:
{chr(10).join([f'- {mult}' for mult in relevant_patterns['effectiveness_multipliers'].get('high_impact', [])])}

SPECIFIC REQUIREMENTS:
- Urgency Level: {config.urgency_level} (include {"2-3" if config.urgency_level == "high" else "1-2"} urgency elements)
- Include specific numbers and timeframes
- Write in {config.voice_tone} tone
- Length: {config.length} ({"1500-2000" if config.length == "short" else "3000-4000" if config.length == "medium" else "5000+"} words)
- Include {config.guarantee_type.replace("_", " ")} guarantee

EXAMPLES OF HIGH-CONVERTING ELEMENTS:
{self._format_examples(relevant_patterns)}

Now create the complete landing page following the structure and patterns provided. Make it specific to {config.product_name} and highly compelling.

Format the output with clear section headers using ### for each major section."""

        return prompt
    
    def _format_examples(self, patterns: Dict[str, Any]) -> str:
        """Format examples from pattern library"""
        examples = []
        
        if patterns.get("headline_examples"):
            examples.append("Headlines that converted:")
            for h in patterns["headline_examples"][:3]:
                examples.append(f'- "{h.get("text", "")}"')
        
        if patterns.get("cta_examples"):
            examples.append("\nCTAs that converted:")
            for c in patterns["cta_examples"][:3]:
                examples.append(f'- "{c.get("text", "")}"')
        
        return "\n".join(examples) if examples else "Use proven formulas from the patterns provided."
    
    def build_refinement_prompt(self, initial_copy: str, config: PageConfig) -> str:
        """Build prompt for refining the generated copy"""
        
        return f"""Review and enhance this landing page copy for maximum conversion:

{initial_copy}

ENHANCEMENT CHECKLIST:
1. Ensure {config.urgency_level} urgency with specific elements (timers, limits, deadlines)
2. Verify value stack shows 10-15x value vs ${config.price_point} price
3. Add more specific numbers, percentages, and timeframes
4. Strengthen emotional journey from pain to transformation
5. Ensure CTAs appear every 500-750 words
6. Add power words that trigger action
7. Make guarantee more compelling and risk-free
8. Ensure social proof is specific and believable

Enhance the copy while maintaining the same structure and voice. Make it impossible to resist."""

class LandingPageGenerator:
    """Main generator class that orchestrates the page creation"""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise ValueError("Anthropic API key required. Set ANTHROPIC_API_KEY environment variable.")
        
        self.client = anthropic.Anthropic(api_key=self.api_key)
        self.patterns = PatternLibrary()
        self.prompt_engine = PromptEngine(self.patterns)
    
    def generate_page(self, config: PageConfig) -> Dict[str, Any]:
        """Generate a complete landing page"""
        logger.info(f"Generating {config.page_type} for {config.product_name}")
        
        # Get relevant patterns
        relevant_patterns = self.patterns.get_relevant_patterns(config)
        
        # Build initial prompt
        initial_prompt = self.prompt_engine.build_master_prompt(config, relevant_patterns)
        
        # Generate initial copy
        logger.info("Generating initial copy...")
        initial_copy = self._call_claude(initial_prompt, max_tokens=8000)
        
        # Refine for maximum conversion
        logger.info("Refining for conversion...")
        refinement_prompt = self.prompt_engine.build_refinement_prompt(initial_copy, config)
        final_copy = self._call_claude(refinement_prompt, max_tokens=8000)
        
        # Structure the output
        result = {
            "config": config.__dict__,
            "generated_at": datetime.now().isoformat(),
            "page_content": final_copy,
            "patterns_used": relevant_patterns,
            "word_count": len(final_copy.split()),
            "sections": self._extract_sections(final_copy)
        }
        
        # Save output
        self._save_output(result, config)
        
        return result
    
    def _call_claude(self, prompt: str, max_tokens: int = 4000) -> str:
        """Call Claude API"""
        try:
            response = self.client.messages.create(
                model="claude-opus-4-20250514",  # Claude Opus 4 - most capable model
                max_tokens=max_tokens,
                temperature=0.7,
                messages=[{
                    "role": "user",
                    "content": prompt
                }]
            )
            return response.content[0].text
        except Exception as e:
            logger.error(f"Claude API error: {e}")
            raise
    
    def _extract_sections(self, content: str) -> Dict[str, str]:
        """Extract sections from generated content"""
        sections = {}
        current_section = "intro"
        current_content = []
        
        for line in content.split('\n'):
            if line.startswith('###'):
                if current_content:
                    sections[current_section] = '\n'.join(current_content).strip()
                current_section = line.replace('#', '').strip().lower().replace(' ', '_')
                current_content = []
            else:
                current_content.append(line)
        
        if current_content:
            sections[current_section] = '\n'.join(current_content).strip()
        
        return sections
    
    def _save_output(self, result: Dict[str, Any], config: PageConfig):
        """Save generated page to file"""
        output_dir = Path("generated_pages")
        output_dir.mkdir(exist_ok=True)
        
        filename = f"{config.product_name.lower().replace(' ', '_')}_{config.page_type}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        # Save full JSON
        with open(output_dir / f"{filename}.json", 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        
        # Save markdown version
        with open(output_dir / f"{filename}.md", 'w', encoding='utf-8') as f:
            f.write(f"# {config.product_name} - {config.page_type.replace('_', ' ').title()}\n\n")
            f.write(f"Generated: {result['generated_at']}\n\n")
            f.write("---\n\n")
            f.write(result['page_content'])
        
        logger.info(f"Saved to: {output_dir / filename}")


def main():
    """Example usage"""
    
    # Example configuration for LooksCode quiz funnel
    config = PageConfig(
        page_type="quiz_funnel",
        industry="mens_appearance",
        product_name="LooksCode Elite",
        product_type="membership",
        price_point=497,
        target_audience={
            "gender": "male",
            "age_range": "25-45",
            "income": "high",
            "sophistication": "medium-high",
            "awareness_level": "problem_aware"
        },
        angle="transformation_story",
        length="medium",
        urgency_level="high",
        voice_tone="informed_friend",
        specific_benefits=[
            "Look 5-10 years younger without surgery",
            "Get personalized appearance optimization roadmap",
            "Access to vetted aesthetic providers",
            "Save thousands on trial and error",
            "Boost confidence and social presence"
        ],
        pain_points=[
            "Looking tired despite good sleep",
            "Aging faster than peers",
            "Not knowing what treatments actually work",
            "Wasting money on ineffective solutions",
            "Feeling invisible or overlooked"
        ],
        unique_mechanism="AI-powered facial analysis with medical team insights",
        guarantee_type="60_day_transformation",
        bonuses=[
            {"name": "Personal Consultation", "value": "497"},
            {"name": "Provider Black Book", "value": "297"},
            {"name": "Lifetime Updates", "value": "997"}
        ]
    )
    
    # Initialize generator
    generator = LandingPageGenerator()
    
    # Generate the page
    result = generator.generate_page(config)
    
    print(f"\nGenerated {config.page_type} for {config.product_name}")
    print(f"Word count: {result['word_count']}")
    print(f"Saved to: generated_pages/")


if __name__ == "__main__":
    main()