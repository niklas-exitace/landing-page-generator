#!/usr/bin/env python3
"""
Simple CLI interface for generating landing pages
"""
import json
import click
from pathlib import Path
from landing_page_generator import LandingPageGenerator, PageConfig

# Load configuration options
CONFIG_DIR = Path("config")
with open(CONFIG_DIR / "page_types.json", 'r') as f:
    PAGE_TYPES = list(json.load(f)["page_types"].keys())

with open(CONFIG_DIR / "angles.json", 'r') as f:
    ANGLES = list(json.load(f)["angles"].keys())

INDUSTRIES = [
    "fitness", "health", "beauty", "dating", "finance", "investing",
    "real_estate", "education", "saas", "ecommerce", "coaching",
    "consulting", "agency", "info_product", "supplement", "other"
]

VOICE_TONES = [
    "professional", "casual", "urgent", "friendly", "authoritative",
    "conversational", "inspirational", "direct", "empathetic"
]

@click.command()
@click.option('--product-name', prompt='Product name', help='Name of your product/service')
@click.option('--page-type', type=click.Choice(PAGE_TYPES), prompt='Page type', help='Type of landing page')
@click.option('--industry', type=click.Choice(INDUSTRIES), prompt='Industry', help='Your industry')
@click.option('--price', type=float, prompt='Price point ($)', help='Product price')
@click.option('--angle', type=click.Choice(ANGLES), prompt='Marketing angle', help='Story angle to use')
@click.option('--urgency', type=click.Choice(['low', 'medium', 'high']), default='medium', prompt='Urgency level')
@click.option('--length', type=click.Choice(['short', 'medium', 'long']), default='medium', prompt='Page length')
@click.option('--voice', type=click.Choice(VOICE_TONES), default='friendly', prompt='Voice tone')
def generate(**kwargs):
    """Generate a high-converting landing page using proven patterns"""
    
    print("\n🚀 Generating your landing page...\n")
    
    # Collect benefits
    print("Enter 3-5 key benefits (empty line to finish):")
    benefits = []
    while len(benefits) < 5:
        benefit = input(f"Benefit {len(benefits) + 1}: ").strip()
        if not benefit and len(benefits) >= 3:
            break
        elif benefit:
            benefits.append(benefit)
    
    # Collect pain points
    print("\nEnter 3-5 pain points your product solves (empty line to finish):")
    pain_points = []
    while len(pain_points) < 5:
        pain = input(f"Pain point {len(pain_points) + 1}: ").strip()
        if not pain and len(pain_points) >= 3:
            break
        elif pain:
            pain_points.append(pain)
    
    # Optional unique mechanism
    unique_mechanism = input("\nUnique mechanism/method (optional, press Enter to skip): ").strip() or None
    
    # Create configuration
    config = PageConfig(
        page_type=kwargs['page_type'],
        industry=kwargs['industry'],
        product_name=kwargs['product_name'],
        product_type="digital",  # Default, could be made configurable
        price_point=kwargs['price'],
        target_audience={
            "awareness_level": "problem_aware",
            "sophistication": "medium"
        },
        angle=kwargs['angle'],
        length=kwargs['length'],
        urgency_level=kwargs['urgency'],
        voice_tone=kwargs['voice'],
        specific_benefits=benefits,
        pain_points=pain_points,
        unique_mechanism=unique_mechanism
    )
    
    # Generate the page
    try:
        generator = LandingPageGenerator()
        result = generator.generate_page(config)
        
        print(f"\n✅ Success! Generated {config.page_type} for {config.product_name}")
        print(f"📝 Word count: {result['word_count']}")
        print(f"💾 Saved to: generated_pages/")
        print(f"\n📄 Files created:")
        print(f"   - Markdown: {config.product_name.lower().replace(' ', '_')}_{config.page_type}_*.md")
        print(f"   - JSON: {config.product_name.lower().replace(' ', '_')}_{config.page_type}_*.json")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\nMake sure you have set the ANTHROPIC_API_KEY environment variable")

if __name__ == "__main__":
    generate()