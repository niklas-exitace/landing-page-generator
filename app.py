#!/usr/bin/env python3
"""
Streamlit web interface for Landing Page Generator
"""
import streamlit as st
import json
from pathlib import Path
from datetime import datetime
import os
from landing_page_generator import LandingPageGenerator, PageConfig

# Page config
st.set_page_config(
    page_title="Landing Page Generator",
    page_icon="🚀",
    layout="wide"
)

# Load configurations
@st.cache_data
def load_configs():
    config_dir = Path("config")
    with open(config_dir / "page_types.json", 'r') as f:
        page_types = json.load(f)["page_types"]
    with open(config_dir / "angles.json", 'r') as f:
        angles = json.load(f)["angles"]
    return page_types, angles

PAGE_TYPES, ANGLES = load_configs()

# Header
st.title("🚀 Landing Page Generator")
st.markdown("Create high-converting landing pages using proven patterns from $100M+ in tracked sales")

# Initialize session state for API key
if 'api_key' not in st.session_state:
    st.session_state.api_key = None

# Check for API key in session state
if not st.session_state.api_key:
    st.warning("⚠️ API Key Required")
    st.info("To use this app, you need an Anthropic API key. Get one at https://console.anthropic.com")
    api_key_input = st.text_input("Enter your Anthropic API Key:", type="password", 
                                 help="Your key will only be used for this session and is never stored")
    if api_key_input:
        st.session_state.api_key = api_key_input
        st.success("✅ API Key set for this session!")
        st.rerun()
    st.stop()  # Stop execution until API key is provided

# Set the API key for this session only
os.environ["ANTHROPIC_API_KEY"] = st.session_state.api_key

# Sidebar for configuration
with st.sidebar:
    st.header("Page Configuration")
    
    # Add logout button at the top of sidebar
    if st.button("🔒 Logout / Clear API Key", type="secondary"):
        st.session_state.api_key = None
        if "ANTHROPIC_API_KEY" in os.environ:
            del os.environ["ANTHROPIC_API_KEY"]
        st.rerun()
    
    # Basic Info
    product_name = st.text_input("Product Name", placeholder="e.g., LooksCode Elite")
    
    page_type = st.selectbox(
        "Page Type",
        options=list(PAGE_TYPES.keys()),
        format_func=lambda x: PAGE_TYPES[x]["name"]
    )
    
    # Show description of selected page type
    if page_type:
        st.info(PAGE_TYPES[page_type]["description"])
    
    industry = st.selectbox(
        "Industry",
        ["fitness", "health", "beauty", "dating", "finance", "investing",
         "real_estate", "education", "saas", "ecommerce", "coaching",
         "consulting", "agency", "info_product", "supplement"]
    )
    
    price = st.number_input("Price Point ($)", min_value=1.0, value=97.0, step=10.0)
    
    # Marketing Angle
    angle = st.selectbox(
        "Marketing Angle",
        options=list(ANGLES.keys()),
        format_func=lambda x: ANGLES[x]["name"]
    )
    
    # Show angle description
    if angle:
        st.info(ANGLES[angle]["description"])
    
    # Advanced Options
    with st.expander("Advanced Options"):
        product_type = st.selectbox(
            "Product Type",
            ["digital", "physical", "service", "membership", "course", "software"]
        )
        
        urgency_level = st.select_slider(
            "Urgency Level",
            options=["low", "medium", "high"],
            value="medium"
        )
        
        length = st.select_slider(
            "Content Length",
            options=["short", "medium", "long"],
            value="medium"
        )
        
        voice_tone = st.selectbox(
            "Voice Tone",
            ["professional", "casual", "urgent", "friendly", "authoritative",
             "conversational", "inspirational", "direct", "empathetic"]
        )
        
        guarantee_type = st.selectbox(
            "Guarantee Type",
            ["30_day_money_back", "60_day_money_back", "90_day_money_back",
             "lifetime_guarantee", "results_based", "no_guarantee"]
        )

# Main content area
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("Benefits & Pain Points")
    
    # Benefits
    st.markdown("**Key Benefits** (3-5 required)")
    benefits = []
    for i in range(5):
        benefit = st.text_input(f"Benefit {i+1}", key=f"benefit_{i}")
        if benefit:
            benefits.append(benefit)
    
    # Pain Points
    st.markdown("**Pain Points** (3-5 required)")
    pain_points = []
    for i in range(5):
        pain = st.text_input(f"Pain Point {i+1}", key=f"pain_{i}")
        if pain:
            pain_points.append(pain)

with col2:
    st.subheader("Target Audience")
    
    # Audience configuration
    age_range = st.selectbox(
        "Age Range",
        ["18-24", "25-34", "35-44", "45-54", "55+", "All ages"]
    )
    
    gender = st.selectbox(
        "Gender",
        ["male", "female", "all"]
    )
    
    awareness = st.selectbox(
        "Awareness Level",
        ["unaware", "problem_aware", "solution_aware", "product_aware", "most_aware"]
    )
    
    sophistication = st.select_slider(
        "Market Sophistication",
        options=["low", "medium", "high"],
        value="medium"
    )
    
    # Unique Mechanism
    st.subheader("Unique Mechanism (Optional)")
    unique_mechanism = st.text_area(
        "What makes your solution unique?",
        placeholder="e.g., AI-powered analysis, proprietary method, exclusive access..."
    )

# Bonuses section
with st.expander("Add Bonuses (Optional)"):
    bonuses = []
    for i in range(3):
        col1, col2 = st.columns([3, 1])
        with col1:
            bonus_name = st.text_input(f"Bonus {i+1} Name", key=f"bonus_name_{i}")
        with col2:
            bonus_value = st.number_input(f"Value ($)", min_value=0, value=0, key=f"bonus_value_{i}")
        
        if bonus_name and bonus_value > 0:
            bonuses.append({"name": bonus_name, "value": str(bonus_value)})

# Generate button
if st.button("🚀 Generate Landing Page", type="primary", use_container_width=True):
    # Validation
    if not product_name:
        st.error("Please enter a product name")
    elif len(benefits) < 3:
        st.error("Please enter at least 3 benefits")
    elif len(pain_points) < 3:
        st.error("Please enter at least 3 pain points")
    else:
        # Create configuration
        config = PageConfig(
            page_type=page_type,
            industry=industry,
            product_name=product_name,
            product_type=product_type,
            price_point=price,
            target_audience={
                "gender": gender,
                "age_range": age_range,
                "awareness_level": awareness,
                "sophistication": sophistication
            },
            angle=angle,
            length=length,
            urgency_level=urgency_level,
            voice_tone=voice_tone,
            specific_benefits=benefits,
            pain_points=pain_points,
            unique_mechanism=unique_mechanism if unique_mechanism else None,
            guarantee_type=guarantee_type,
            bonuses=bonuses if bonuses else None
        )
        
        # Check for API key
        if not os.getenv("ANTHROPIC_API_KEY"):
            st.error("⚠️ ANTHROPIC_API_KEY not set in environment variables")
            st.info("Set your API key: `export ANTHROPIC_API_KEY='your-key-here'`")
        else:
            try:
                # Generate with progress
                with st.spinner("🤖 Generating your landing page... (this takes 30-60 seconds)"):
                    generator = LandingPageGenerator()
                    result = generator.generate_page(config)
                
                st.success(f"✅ Generated {config.page_type} for {config.product_name}!")
                
                # Display results
                st.markdown("---")
                st.subheader("Generated Landing Page")
                
                # Tabs for different views
                tab1, tab2, tab3, tab4 = st.tabs(["📄 Full Page", "📊 Sections", "🔧 JSON", "📈 Analysis"])
                
                with tab1:
                    # Full page view
                    st.markdown(result["page_content"])
                    
                    # Download button
                    st.download_button(
                        label="📥 Download as Markdown",
                        data=result["page_content"],
                        file_name=f"{product_name.lower().replace(' ', '_')}_{page_type}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md",
                        mime="text/markdown"
                    )
                
                with tab2:
                    # Sections view
                    for section_name, content in result["sections"].items():
                        with st.expander(section_name.replace("_", " ").title()):
                            st.markdown(content)
                
                with tab3:
                    # JSON view
                    st.json(result)
                    
                    # Download JSON
                    st.download_button(
                        label="📥 Download as JSON",
                        data=json.dumps(result, indent=2),
                        file_name=f"{product_name.lower().replace(' ', '_')}_{page_type}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                        mime="application/json"
                    )
                
                with tab4:
                    # Analysis
                    st.metric("Word Count", result["word_count"])
                    st.metric("Sections", len(result["sections"]))
                    
                    # Show patterns used
                    st.subheader("Patterns Applied")
                    patterns_used = result.get("patterns_used", {})
                    
                    if patterns_used.get("effectiveness_multipliers"):
                        st.markdown("**High-Impact Elements:**")
                        for mult in patterns_used["effectiveness_multipliers"].get("high_impact", []):
                            st.markdown(f"- ✅ {mult}")
                
            except Exception as e:
                st.error(f"❌ Error generating page: {str(e)}")
                st.info("Check your API key and try again")

# Footer with tips
with st.expander("💡 Pro Tips for Maximum Conversion"):
    st.markdown("""
    ### Based on our analysis of $100M+ in sales:
    
    **🎯 Headlines:** Use specific numbers and timeframes
    - ❌ "Lose Weight Fast"
    - ✅ "Drop 15 Pounds in 30 Days Without Giving Up Carbs"
    
    **🔥 Urgency:** Stack 2-3 urgency elements
    - Limited time offer
    - Bonus expiration
    - Price increase warning
    
    **💰 Value Stack:** Show 10-15x value vs price
    - Main product value
    - 3-4 bonuses with specific values
    - Support/community access
    - Guarantee value
    
    **🎭 Social Proof:** Be specific
    - ❌ "Many happy customers"
    - ✅ "Join 4,731 men who've transformed their appearance"
    
    **✍️ Copy Length:**
    - Quiz funnels: 500-1000 words per result
    - Advertorials: 2000-5000 words
    - Sales letters: 3000-7000 words
    """)

# Sidebar footer
with st.sidebar:
    st.markdown("---")
    st.markdown("### 📚 Resources")
    st.markdown("- [Pattern Library](output/pattern_library.json)")
    st.markdown("- [Swipe File](output/copy_swipe_file.json)")
    st.markdown("- [Conversion Formulas](output/conversion_formulas.json)")
    
    st.markdown("---")
    st.markdown("Built with patterns from 20 high-converting pages")
    st.markdown("🚀 Generate unlimited variations")