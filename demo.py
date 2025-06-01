#!/usr/bin/env python3
"""
Demo script to show how the Landing Page Generator works (no API key required)
"""
import json
from pathlib import Path
from landing_page_generator import PatternLibrary, PromptEngine, PageConfig

def main():
    print("\n🚀 Landing Page Generator Demo")
    print("="*50)
    
    # Load pattern library
    patterns = PatternLibrary()
    prompt_engine = PromptEngine(patterns)
    
    # Example configuration
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
        guarantee_type="60_day_transformation"
    )
    
    print("\n📋 Configuration:")
    print(f"Product: {config.product_name}")
    print(f"Type: {config.page_type}")
    print(f"Price: ${config.price_point}")
    print(f"Angle: {config.angle}")
    
    # Get relevant patterns
    print("\n🔍 Loading relevant patterns...")
    relevant_patterns = patterns.get_relevant_patterns(config)
    
    print("\n📐 Page Structure:")
    for i, section in enumerate(relevant_patterns['page_structure'], 1):
        print(f"{i}. {section.replace('_', ' ').title()}")
    
    print("\n🎯 Effectiveness Multipliers:")
    for mult in relevant_patterns['effectiveness_multipliers']['high_impact']:
        print(f"• {mult}")
    
    print("\n🧠 Psychological Triggers to Use:")
    triggers = relevant_patterns['universal_patterns']['psychological_triggers']
    print(f"Mandatory: {', '.join(triggers['mandatory'])}")
    print(f"Recommended: {', '.join(triggers['recommended'])}")
    
    # Show the prompt that would be sent
    print("\n📝 Generated Prompt Preview:")
    print("-"*50)
    prompt = prompt_engine.build_master_prompt(config, relevant_patterns)
    print(prompt[:1000] + "...\n[Truncated for demo]")
    
    print("\n✨ What happens next:")
    print("1. This prompt is sent to Claude AI")
    print("2. Claude generates the complete landing page")
    print("3. A refinement pass optimizes for conversion")
    print("4. The final page is saved as Markdown and JSON")
    
    print("\n💡 To generate real pages:")
    print("1. Set your ANTHROPIC_API_KEY environment variable")
    print("2. Run: python generate_cli.py")
    print("   Or: streamlit run app.py")
    
    # Show available page types and angles
    print("\n📚 Available Options:")
    
    print("\nPage Types:")
    for key, details in patterns.page_types.get("page_types", {}).items():
        print(f"• {key}: {details['name']}")
    
    print("\nMarketing Angles:")
    for key, details in patterns.angles.get("angles", {}).items():
        print(f"• {key}: {details['name']}")
    
    print("\n🎉 Ready to generate high-converting landing pages!")

if __name__ == "__main__":
    main()