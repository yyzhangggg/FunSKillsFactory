# Style Options

Style remains user-selected. Do not infer a style from the subject or reference photos. Accept exactly one optional style flag and apply it consistently to the isolated figure, character turnaround, food bowl, water bowl, action poses, animation frames, and desktop-pet application assets.

Supported style flags:

## `-pixel`

Pixel-art desktop-pet rendering with deliberate pixel clusters, a fixed pixel grid, hard edges, limited palette control, and no smoothing or anti-aliasing. Keep every animation frame aligned to the same grid and canvas anchor.

### Draw Things model rule

Automatically enable **Pixel Art XL v1.1** (`pixel-art-xl-v1.1.safetensors`) from [Civitai model 120096](https://civitai.com/models/120096). It is an **SDXL 1.0 LoRA**, so it requires an SDXL base checkpoint in Draw Things; do not apply it to SD 1.5 or Flux checkpoints. Use LoRA weight `0.8-1.0`, disable the refiner, generate at an integer multiple of the final pixel grid, then downscale with nearest-neighbor sampling. Do not rely on the diffusion model to produce final pixel-perfect edges at full resolution.

## `-manga`

Japanese manga style with expressive ink linework, intentional panel-like visual clarity, manga character proportions, controlled screentone or hatching where appropriate, and Japanese manga-inspired facial and motion conventions. Keep the result as a standalone character or action asset, not a comic page, unless the user asks for panels.

## `-3d`

East Asian ancient fantasy style interpreted as a stylized 3D character direction. Use historically inspired East Asian fantasy clothing, motifs, props, materials, and environment cues only when compatible with the person or animal reference. Preserve the subject's identity and do not invent specific historical claims. Keep lighting, materials, camera angle, and proportions consistent across all views and frames.

### Draw Things model rule

Automatically enable **3D Style XL** (`3D XL.safetensors`) from [Civitai model 119303](https://civitai.com/models/119303). It is an **SDXL 1.0 LoRA**, so it requires an SDXL base checkpoint in Draw Things; do not apply it to SD 1.5 or Flux checkpoints. The LoRA has no required trigger word. Start at weight `0.65-0.8`; use `3D render` in the prompt only when a stronger CGI result is needed. Keep denoising low enough to preserve the supplied person or pet identity.

## `-western`

Middle Eastern tone and drawing style, using regionally inspired line, shape, color, ornament, clothing, and visual storytelling cues without stereotyping or combining unrelated cultures. Preserve the user's selected clothing and the subject's identity. Keep props and animation assets consistent with the same direction.

## `-kpop`

Highly polished, shining K-pop-inspired styling with luminous highlights, carefully designed hair and clothing details, glossy accents, vivid but controlled color, and a performance-oriented presentation. Keep the character readable at desktop-pet scale and preserve the person's actual identity and selected clothing unless the user requests a redesign.

## Draw Things Model Selection

- `-pixel` and `-3d` are the only flags that automatically select a documented local LoRA.
- For `-manga`, `-western`, `-kpop`, or no style flag, keep the user's currently selected Draw Things checkpoint and LoRA unchanged. Do not query Civitai, download weights, or substitute another model.
- Before enabling an automatic LoRA, verify that the active Draw Things checkpoint uses the matching SDXL 1.0 architecture. If it does not, stop and ask the user to switch to an SDXL base checkpoint.
- Record the selected local LoRA filename, source URL, base architecture, weight, and generation date in the asset manifest.
- Do not redistribute downloaded model weights. Check the current Civitai license before distributing a desktop-pet application that includes generated assets commercially.

## Style rules

- Use one style flag at a time. If the user provides multiple style flags, ask them to choose one.
- If no style flag is provided, do not choose or change a Draw Things model or LoRA. Use the user's manual local selection and preserve it for the entire package.
- A style changes rendering direction, not the subject's identity, body structure, clothing decision, animal markings, or action list.
- Do not mix style directions across the isolated figure, turnaround, props, key poses, animation frames, or application assets.
- For `-pixel`, preserve integer-grid alignment and disable smoothing.
- For `-manga`, use Japanese manga direction as requested, while keeping the character assets separate from comic-page layout.
- For `-3d`, keep the East Asian ancient fantasy direction consistent across views; the actual deliverable may be rendered 2D assets unless a 3D model pipeline is explicitly requested.
- For `-western`, interpret the requested Middle Eastern visual direction respectfully and specifically; do not use generic "exotic" decoration.
- For `-kpop`, keep shine and polish controlled enough that small animation frames remain legible.
