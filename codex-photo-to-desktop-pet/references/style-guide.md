# Style Options

Style remains user-selected. Do not infer a style from the subject or reference photos. Accept exactly one optional style flag and apply it consistently to the isolated figure, character turnaround, food bowl, water bowl, action poses, animation frames, and desktop-pet application assets.

Supported style flags:

## `-pixel`

Pixel-art desktop-pet rendering with deliberate pixel clusters, a fixed pixel grid, hard edges, limited palette control, and no smoothing or anti-aliasing. Keep every animation frame aligned to the same grid and canvas anchor.

## `-manga`

Japanese manga style with expressive ink linework, intentional panel-like visual clarity, manga character proportions, controlled screentone or hatching where appropriate, and Japanese manga-inspired facial and motion conventions. Keep the result as a standalone character or action asset, not a comic page, unless the user asks for panels.

## `-3d`

East Asian ancient fantasy style interpreted as a stylized 3D character direction. Use historically inspired East Asian fantasy clothing, motifs, props, materials, and environment cues only when compatible with the person or animal reference. Preserve the subject's identity and do not invent specific historical claims. Keep lighting, materials, camera angle, and proportions consistent across all views and frames.

## `-western`

Middle Eastern tone and drawing style, using regionally inspired line, shape, color, ornament, clothing, and visual storytelling cues without stereotyping or combining unrelated cultures. Preserve the user's selected clothing and the subject's identity. Keep props and animation assets consistent with the same direction.

## `-kpop`

Highly polished, shining K-pop-inspired styling with luminous highlights, carefully designed hair and clothing details, glossy accents, vivid but controlled color, and a performance-oriented presentation. Keep the character readable at desktop-pet scale and preserve the person's actual identity and selected clothing unless the user requests a redesign.

## Style rules

- Use one style flag at a time. If the user provides multiple style flags, ask them to choose one.
- If no style flag is provided, ask the user to select a style before generating the styled character package. Do not choose a default.
- A style changes rendering direction, not the subject's identity, body structure, clothing decision, animal markings, or action list.
- Do not mix style directions across the isolated figure, turnaround, props, key poses, animation frames, or application assets.
- For `-pixel`, preserve integer-grid alignment and disable smoothing.
- For `-manga`, use Japanese manga direction as requested, while keeping the character assets separate from comic-page layout.
- For `-3d`, keep the East Asian ancient fantasy direction consistent across views; the actual deliverable may be rendered 2D assets unless a 3D model pipeline is explicitly requested.
- For `-western`, interpret the requested Middle Eastern visual direction respectfully and specifically; do not use generic "exotic" decoration.
- For `-kpop`, keep shine and polish controlled enough that small animation frames remain legible.
