# LLM Prompts for Image Generation

Meta-prompts for using LLMs to generate and optimize image prompts.

---

## Prompt Generation

### Generate Image Prompt from Description

```
You are an expert image prompt engineer. Convert the user's description into an optimized prompt for {model} image generation.

Follow this structure:
1. Subject: Clear, specific description of the main subject
2. Style: Art style, photography type, or aesthetic
3. Lighting: Light source, quality, direction
4. Composition: Framing, perspective, layout
5. Details: Specific elements, textures, colors
6. Technical: Resolution, quality keywords

Output ONLY the prompt, no explanations.

User description: {user_description}
```

### Generate Multiple Variations

```
Generate {n} distinct prompt variations for this image concept: {concept}

Each variation should:
- Explore a different artistic direction
- Maintain the core concept
- Be optimized for {model} generation
- Include full prompt structure (subject, style, lighting, composition, details, technical)

Format as numbered list with just the prompts.
```

### Improve Existing Prompt

```
Analyze and improve this image generation prompt:

Original: {original_prompt}

Improvements to make:
1. Add missing elements (subject, style, lighting, composition, details, technical)
2. Replace vague terms with specific descriptions
3. Add quality-enhancing keywords
4. Ensure coherent, non-conflicting instructions

Provide:
1. Analysis of what's missing or weak
2. Improved prompt
3. Key changes explained
```

---

## Style Conversion

### Apply Art Style

```
Transform this image description into a prompt in {style_name} style:

Description: {description}

Consider:
- Key visual characteristics of {style_name}
- Appropriate lighting and color palette
- Composition techniques typical of this style
- Technical specifications that enhance the style

Output the complete, optimized prompt.
```

### Style Reference List

| Style | Key Keywords |
|-------|--------------|
| Photorealistic | photorealistic, highly detailed photograph, DSLR, professional photography |
| Digital Art | digital art, vibrant colors, clean lines, professional illustration |
| Oil Painting | oil painting, textured brushstrokes, rich colors, gallery quality |
| Watercolor | watercolor painting, soft edges, fluid, transparent layers |
| Anime | anime style, cel shading, manga aesthetic, Japanese animation |
| 3D Render | 3D render, octane render, unreal engine, highly detailed CGI |
| Concept Art | concept art, game/film design, detailed environment |
| Minimalist | minimalist, clean lines, simple, negative space |
| Vintage | vintage, retro, film grain, nostalgic color grading |
| Cyberpunk | cyberpunk, neon lights, futuristic, dark atmosphere |

---

## Content-Specific Prompts

### E-commerce Product

```
Generate an e-commerce product photography prompt for: {product}

Requirements:
- Professional product photography style
- Clean, neutral or contextual background
- Optimal lighting to show product features
- Hero angle that best represents the product
- High resolution, commercial quality

Consider the product category and typical customer expectations.
Output the complete prompt.
```

### Social Media Content

```
Create an image prompt for {platform} post about {topic}.

Platform requirements:
- Instagram: Aesthetic, lifestyle-focused, trendy
- LinkedIn: Professional, clean, business-appropriate
- Twitter: Eye-catching, bold, shareable
- TikTok: Trendy, dynamic, youth-oriented

Include appropriate:
- Visual style for the platform
- Mood and atmosphere
- Composition for the format (square, story, landscape)
- Elements that drive engagement

Output the optimized prompt.
```

### Marketing Campaign

```
Generate image prompts for a {campaign_type} campaign:

Brand: {brand_name}
Product/Service: {product_service}
Target Audience: {audience}
Key Message: {message}
Brand Colors: {colors}
Brand Personality: {personality}

Create {n} prompts for:
1. Hero image
2. Supporting visuals
3. Social media adaptations

Each prompt should:
- Align with brand guidelines
- Communicate the key message
- Appeal to the target audience
- Maintain visual consistency
```

---

## Technical Optimization

### Optimize for Specific Model

```
Optimize this prompt for {model}:

Original prompt: {prompt}

Model-specific considerations:
- DALL-E 3: Understands natural language well, vivid/natural style options
- Stable Diffusion: Benefits from keyword-style prompts, negative prompts important
- Flux: Excellent with detailed descriptions, good anatomy
- Midjourney: Style references, parameters like --ar, --style

Output the model-optimized prompt.
```

### Add Technical Specifications

```
Enhance this prompt with appropriate technical specifications:

Prompt: {prompt}
Use Case: {use_case}
Output Size: {size}

Add relevant:
- Resolution keywords (4K, 8K, ultra detailed)
- Camera/lens references if photographic
- Lighting specifications
- Quality modifiers

Output the enhanced prompt.
```

---

## Batch Generation

### Generate Campaign Set

```
Create a cohesive set of {n} image prompts for {campaign_name}:

Campaign Brief:
{brief}

Requirements:
- Visual consistency across all images
- Variety in composition and angle
- Cover all required formats: {formats}
- Maintain brand voice and style

Output as numbered list with:
- Prompt
- Intended use/format
- Key differentiating element
```

### A/B Test Variations

```
Generate A/B test variations for this image concept:

Original concept: {concept}
Variable to test: {variable}

Create 2-4 variations that:
- Keep all elements constant except the test variable
- Are distinct enough to measure preference
- Could realistically perform differently

Output variations with:
- Prompt
- What's being tested
- Hypothesis for performance
```

---

## Analysis and Iteration

### Analyze Failed Generation

```
Analyze why this image generation may have failed or produced poor results:

Prompt: {prompt}
Issue: {issue_description}

Consider:
- Conflicting instructions
- Vague or ambiguous terms
- Content policy triggers
- Technical impossibilities
- Model limitations

Provide:
1. Likely cause of issue
2. Corrected prompt
3. Prevention tips for future
```

### Iterate Based on Result

```
The previous generation produced this result (described): {result_description}

Original prompt: {original_prompt}
Desired changes: {desired_changes}

Create an updated prompt that:
- Addresses the specific issues
- Maintains what worked well
- Is more specific about desired changes
- Includes clearer instructions

Output the refined prompt.
```

---

## Structured Output Prompts

### JSON Output Format

```
Generate an image prompt with metadata in JSON format:

Concept: {concept}
Purpose: {purpose}

Output format:
{
  "prompt": "full optimized prompt",
  "style": "primary style name",
  "mood": "emotional tone",
  "colors": ["primary", "secondary", "accent"],
  "composition": "composition type",
  "technical": {
    "resolution": "recommended",
    "quality": "standard/hd",
    "aspect_ratio": "recommended"
  },
  "negative_prompt": "what to avoid (for SD)",
  "model_recommendation": "best model for this"
}
```

### Prompt with Parameters

```python
# Use with function calling

GENERATE_PROMPT_FUNCTION = {
    "name": "generate_image_prompt",
    "description": "Generate an optimized image generation prompt",
    "parameters": {
        "type": "object",
        "properties": {
            "prompt": {
                "type": "string",
                "description": "The complete image generation prompt"
            },
            "model": {
                "type": "string",
                "enum": ["dall-e-3", "stable-diffusion", "flux", "midjourney"],
                "description": "Recommended model"
            },
            "size": {
                "type": "string",
                "description": "Recommended size (e.g., 1024x1024)"
            },
            "style": {
                "type": "string",
                "enum": ["vivid", "natural"],
                "description": "DALL-E 3 style parameter"
            },
            "quality": {
                "type": "string",
                "enum": ["standard", "hd"],
                "description": "Quality setting"
            },
            "negative_prompt": {
                "type": "string",
                "description": "Negative prompt for SD models"
            }
        },
        "required": ["prompt", "model"]
    }
}
```

---

## Quality Assurance

### Prompt Review Checklist

```
Review this image prompt against quality criteria:

Prompt: {prompt}

Check for:
[ ] Clear subject identification
[ ] Specific style reference
[ ] Lighting description
[ ] Composition guidance
[ ] Color/mood indication
[ ] Technical specifications
[ ] No conflicting instructions
[ ] Content policy compliance
[ ] Appropriate for target model

Rate each criterion and provide:
1. Overall score (1-10)
2. Missing elements
3. Suggested improvements
4. Final optimized prompt
```

### Consistency Check

```
Review these prompts for visual consistency:

{prompts_list}

Evaluate:
- Style consistency
- Color palette alignment
- Mood/atmosphere match
- Technical specification alignment
- Brand voice consistency

Identify:
1. Inconsistencies
2. Suggested standardizations
3. Revised prompts with consistency improvements
```
