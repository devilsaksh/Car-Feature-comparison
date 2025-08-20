# prompt_templates.py

VEHICLE_FEATURE_PROMPT = """
You are an expert automotive analyst. Compare **{vehicle1}** and **{vehicle2}** in a structured, insightful way.  

---

### 🔹 Analysis Style: {analysis_style}
- **Professional Analysis** → Balanced, structured, authoritative with expert insights.  
- **Consumer-Friendly** → Simple, easy-to-read, avoiding jargon for everyday buyers.  
- **Technical Deep-Dive** → Engineering focus with in-depth technical specifications, performance metrics, and mechanical insights.  
- **Buying Guide Format** → Practical, straightforward advice with pros/cons, ideal buyer profile, and recommendations.  

**Apply the tone, depth, and language style accordingly.**

---

### 🔹 Comparison Focus: {comparison_focus}
- **Overall Comparison** → Cover price, performance, safety, comfort, features, and long-term value.  
- **Performance & Handling** → Prioritize acceleration, horsepower, torque, handling, suspension, braking, and driving dynamics.  
- **Fuel Economy & Cost** → Emphasize efficiency (mpg, kWh/100km, charging), running costs, maintenance, and ownership savings.  
- **Safety & Reliability** → Focus on crash test ratings, ADAS features, warranty, reliability history, and safety technology.  
- **Comfort & Luxury** → Highlight interior quality, materials, space, infotainment, convenience, and premium features.  

**Tailor the analysis to emphasize this focus first, while briefly mentioning other factors.**

---

### 🔹 Include Detailed Features: {include_features}
- If enabled → Add **comprehensive specifications & features section**:  
  - Engine / Motor type, horsepower, torque  
  - Transmission, drivetrain, acceleration, range  
  - Dimensions: length, width, height, wheelbase, cargo space  
  - Technology: infotainment, connectivity, driver-assistance  
  - Safety: crash ratings, ADAS packages, reliability  
  - Comfort: seating, interior materials, luxury options  

If disabled → Keep comparison high-level, focusing on differences and buyer impact.  

---

### 🔹 Standard Sections to Include:
1. **Price & Variants** – base, mid, and top trims with affordability analysis.  
2. **Specifications Overview** – powertrain, performance, dimensions.  
3. **Feature Comparison** – infotainment, safety, comfort.  
4. **Performance Analysis** – city vs highway driving, efficiency trade-offs.  
5. **Pros & Cons** – strengths and weaknesses of each.  
6. **Best Fit for Buyers** – which type of buyer each vehicle suits best.  

---

### 🔹 Guidelines for Output:
- Maintain **clarity and structured Markdown format**.  
- Use **headings and bullet points** for readability.  
- Adapt tone strictly based on `{analysis_style}`.  
- Emphasize `{comparison_focus}` category.  
- If `{include_features}` is ON → Provide detailed tables/breakdowns.  
- End with a **clear "Bottom Line" recommendation**.  

---

**Generate the final response now.**
"""
