#!/usr/bin/env python3
"""
Batch generation script for creating multiple landing pages
"""
import json
import click
from pathlib import Path
from datetime import datetime
import time
from landing_page_generator import LandingPageGenerator, PageConfig

@click.command()
@click.option('--config', '-c', type=click.Path(exists=True), required=True, help='JSON config file')
@click.option('--delay', '-d', type=int, default=5, help='Delay between generations (seconds)')
def batch_generate(config, delay):
    """Generate multiple landing pages from a configuration file"""
    
    # Load batch configuration
    with open(config, 'r') as f:
        batch_config = json.load(f)
    
    # Extract defaults and pages
    defaults = batch_config.get('defaults', {})
    pages = batch_config.get('pages', [])
    
    if not pages:
        print("❌ No pages defined in configuration")
        return
    
    print(f"\n🚀 Batch Landing Page Generator")
    print(f"📄 Loaded {len(pages)} page configurations")
    print(f"⏱️  Delay between pages: {delay} seconds\n")
    
    # Initialize generator
    try:
        generator = LandingPageGenerator()
    except ValueError as e:
        print(f"❌ Error: {e}")
        print("Make sure ANTHROPIC_API_KEY is set")
        return
    
    # Track results
    results = []
    successful = 0
    failed = 0
    
    # Generate each page
    for i, page_config in enumerate(pages, 1):
        # Merge with defaults
        merged_config = {**defaults, **page_config}
        
        print(f"\n[{i}/{len(pages)}] Generating: {merged_config['product_name']} - {merged_config['page_type']}")
        
        try:
            # Create PageConfig
            config = PageConfig(
                page_type=merged_config['page_type'],
                industry=merged_config['industry'],
                product_name=merged_config['product_name'],
                product_type=merged_config.get('product_type', 'digital'),
                price_point=merged_config['price_point'],
                target_audience=merged_config.get('target_audience', {
                    "awareness_level": "problem_aware",
                    "sophistication": "medium"
                }),
                angle=merged_config['angle'],
                length=merged_config.get('length', 'medium'),
                urgency_level=merged_config.get('urgency_level', 'medium'),
                voice_tone=merged_config.get('voice_tone', 'friendly'),
                specific_benefits=merged_config['benefits'],
                pain_points=merged_config['pain_points'],
                unique_mechanism=merged_config.get('unique_mechanism'),
                guarantee_type=merged_config.get('guarantee_type', '30_day_money_back'),
                bonuses=merged_config.get('bonuses')
            )
            
            # Generate page
            result = generator.generate_page(config)
            
            results.append({
                "product": merged_config['product_name'],
                "type": merged_config['page_type'],
                "status": "success",
                "word_count": result['word_count'],
                "file": f"{config.product_name.lower().replace(' ', '_')}_{config.page_type}_*.md"
            })
            
            successful += 1
            print(f"✅ Success! Word count: {result['word_count']}")
            
        except Exception as e:
            failed += 1
            results.append({
                "product": merged_config['product_name'],
                "type": merged_config['page_type'],
                "status": "failed",
                "error": str(e)
            })
            print(f"❌ Failed: {e}")
        
        # Delay between generations (except for last one)
        if i < len(pages) and delay > 0:
            print(f"⏳ Waiting {delay} seconds...")
            time.sleep(delay)
    
    # Summary report
    print(f"\n{'='*50}")
    print(f"BATCH GENERATION COMPLETE")
    print(f"{'='*50}")
    print(f"✅ Successful: {successful}")
    print(f"❌ Failed: {failed}")
    print(f"📁 Output directory: generated_pages/")
    
    # Save batch report
    report = {
        "timestamp": datetime.now().isoformat(),
        "total_pages": len(pages),
        "successful": successful,
        "failed": failed,
        "results": results
    }
    
    report_path = Path("generated_pages") / f"batch_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(report_path, 'w') as f:
        json.dump(report, f, indent=2)
    
    print(f"\n📊 Detailed report saved to: {report_path}")

if __name__ == "__main__":
    batch_generate()