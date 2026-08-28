---
name: travel-memory-sticker-card
description: Transform a user-uploaded photograph into one horizontal collectible memory card with a large quiet editorial illustration, six integrated journaling-sticker motifs, three small English keywords beneath the left illustration, tactile paper grain, and deliberately clumsy flat color fields. Use when Codex needs to P图, edit, redraw, stylize, or turn a travel, street, landscape, lifestyle, portrait, or pet photo into a minimalist postcard-like card or sticker-card in this visual language. Always drive the local Draw Things diffusion service; do not use OpenAI Image API, imagegen CLI, or another image backend. Preserve recognition through one same-medium identification anchor and optionally one exact place-defining landmark text shown once; never retain an unintended photorealistic patch, signature, or watermark.
---

# Travel Memory Sticker Card

Turn one user photo into one finished bitmap memory card. Always use the user's local Draw Things diffusion service through its local HTTP API, normally `http://127.0.0.1:7860/sdapi/v1/img2img`. Do not use OpenAI Image API, the `imagegen` CLI, remote image services, procedural filters, or code as a substitute for generation. If Draw Things is unavailable, stop and ask the user to start its HTTP server; do not silently switch backends.

Use Draw Things' currently loaded model and settings unless the user explicitly chooses a different local model. Send the source photo as an `img2img` input, preserve the original file, and save the returned bitmap to the requested output directory. Default to the source image's native width and height: submit the original base64 bytes directly, with request `width` and `height` equal to the source dimensions. Never crop or change the aspect ratio. Only when the longest source edge exceeds `2048px`, create a temporary proportional downscaled copy with the longest edge at `2048px` (use `1536px` when the local device needs a lower limit); never create a cropped or lossy project-local input merely to satisfy a card ratio. Delete temporary inputs after the job. Use moderate-to-high denoising for the full matte redraw, but keep the source recognizable. Treat the skill's art direction below as the canonical positive and negative prompt specification for Draw Things.

## Draw Things Generation Contract

- Before generation, probe `GET /sdapi/v1/options` and confirm the local Draw Things service responds.
- Use `POST /sdapi/v1/img2img` with one source image per job. Send the original raw base64 image data in `init_images`; set request `width` and `height` to the source image's native dimensions. Include the composed prompt, negative prompt, steps, sampler, seed, and `denoising_strength`.
- Keep prompt content faithful to this skill: matte gouache/cut-paper, broad source-derived shapes, warm paper, exact sticker and keyword counts, and the negative constraints below.
- After each response, decode the returned image and inspect dimensions, subject recognition, layout, sticker count, keyword count, unwanted text, and watermark absence. Retry once in Draw Things with one targeted prompt change if a quality check fails.
- Do not claim exact text or object counts are guaranteed by diffusion. If they remain wrong after one retry, report the issue rather than using a different backend.

## Source Preservation and Canvas Policy

- Full source coverage is the default requirement. Preserve every visible source element; do not center-crop or trim portrait, landscape, or square inputs.
- Native source dimensions are the default Draw Things request dimensions, and the generated result must keep the source aspect ratio. The 3:2 card system describes internal hierarchy, not permission to alter the canvas ratio.
- If the longest source edge exceeds `2048px`, downscale proportionally to a maximum edge of `2048px`; use `1536px` only when required by local Draw Things memory limits. Preserve every visible source element and record both original and generated dimensions.
- After generation, optional size restoration may use a non-generative high-quality upscaler only. Use no denoising, redraw, face enhancement, crop, or content synthesis during restoration.
- If the local device cannot handle the proportional safety downscale, stop and ask; never silently crop, stretch, or return a partial result.

## Workflow

1. Inspect the source image at full useful detail.
2. Identify the scene structure, emotional center, dominant spatial gesture, and one compact identification anchor.
3. Decide whether any source text is truly a landmark anchor. Default to NONE; retain one exact text item only when it materially identifies the remembered place.
4. Select exactly six source-derived sticker motifs and exactly three concise English keywords.
5. Read [references/style-guide.md](references/style-guide.md), then generate from the source photo.
6. Inspect the result. Regenerate once if the first read is detail rather than large shapes and quiet space, if the image looks photographic or painterly, if the sticker count is wrong, or if required text is wrong.

## Fixed card system

- Use the source image's original aspect ratio on warm off-white uncoated paper with a continuous 4–5% outer margin. Do not stretch, crop, pad, or force a 3:2 canvas unless the user explicitly overrides the source-preservation policy.
- Build the left 66–68% as one vertical unit: a large near-square, unframed illustration above a shallow exposed-paper keyword footer. The illustration must rest directly on the card paper with a subtly rough edge: no outline, keyline, mat, inner card, rounded frame, shadow, or sticker edge.
- Center exactly three short scene-derived English keywords once beneath the illustration, separated by small centered dots: `[keyword 1] · [keyword 2] · [keyword 3]`. Keep them small, quiet, and unboxed. Never place them inside the illustration or below the sticker column.
- Place exactly six separate die-cut stickers in the right 30–32%, using the full composition height. Make two or three stickers larger and the remainder smaller; stagger them with calm, irregular spacing.
- Give every sticker a thick irregular warm-white hand-cut border and a subtle flat paper shadow.
- Do not add a title, caption, date, writing area, postal marks, address lines, subtitle, or readable text beyond the keywords and one optional landmark text anchor.

## Identification and landmark text

- Preserve one compact identification anchor through its silhouette, proportion, placement, relationship, and signature colors. Render it in the same matte gouache, cut-paper, grainy medium as the full card; never retain a photographic patch.
- Preserve zero or one source-visible landmark text only when it genuinely locates the memory. Reject generic advertising, menus, prices, directions, timestamps, and product labels. If retained, copy it exactly once in the main illustration with the same coarse grainy medium; abstract all other source text.

## Art direction

- Rebuild the entire scene from 5–8 broad matte color families.
- Make the first read 3–6 oversized blunt shapes and quiet negative space. Favor deliberate omission over descriptive completeness.
- Use opaque gouache, cut-paper, risograph, or screen-print-like fills with fine uniform paper tooth. Keep edges uneven, hand-cut, chalky, or dry-brushed; allow slight pigment-density variation and soft misregistration.
- Expand one source-supported quiet field such as sky, water, road, snow, wall, sand, or ground.
- Compress vegetation into 1–3 lumpy tonal masses; buildings and geology into planes; people and animals into compact faceless silhouettes. Never use detailed leaves, repeated grooves, masonry, anatomy, or decorative filler.
- Use restrained, low-saturation source-derived colors with one or two accents. Prefer flat color shadows over gradients and use near-black sparingly.
- Keep the mood observational, spacious, humane, slow, and lightly nostalgic.
- Never use visible marker strokes, watercolor washes, wet blooms, photographic texture, glossy 3D, dramatic lighting, smooth gradients, polished vector art, anime, or clip art.

## Stickers and keywords

- Select six meaningful visible motifs only: a main-subject fragment, a grouped or paired variation when present, an environmental form, a structural fragment, a functional object, and a small atmospheric or scale cue.
- Keep stickers coarse, source-derived, and stylistically identical to the main image. If a sticker repeats a landmark sign, remove its lettering.
- Write three precise English keywords grounded in the scene, light, object, or spatial feeling. Prefer `Crater Smoke`, `Blue Summit`, or `Quiet Ridge` over generic words such as `Travel` or `Beautiful`.

## Prompt skeleton

> Create one 3:2 horizontal collectible memory card from the supplied photo on warm off-white textured paper. Preserve a continuous 4–5% outer paper margin. Build the left 66–68% as a large near-square unframed illustration with a shallow exposed-paper footer below it. Center exactly these three English keywords once beneath the illustration, separated by centered dots: [keywords]. Place exactly six source-derived die-cut journaling stickers in the right 30–32%, with irregular warm-white borders, subtle flat shadows, and calm staggered spacing. Preserve [identification anchor] through silhouette, position, relationship, and signature colors, rendered in the same matte gouache, cut-paper, grainy medium as the rest of the card. Preserve this landmark text exactly once in the main illustration: [verbatim text or NONE]. Rebuild the scene from 5–8 broad matte color families. Make the first read 3–6 oversized blunt shapes and quiet negative space, using [palette and dominant quiet field]. Simplify [source elements] into naive, slightly misproportioned color planes with hand-cut chalky edges and fine uniform paper grain. Include these six stickers: [motifs]. Add no other readable text, title, caption, date, writing area, postal marks, watermark, or signature. No visible marker strokes, watercolor wash, painterly photo filter, photorealism, glossy 3D, gradients, anime, polished vector art, or unrelated objects.

## Quality checks

- The scene is identifiable at a glance, but its first read is large shapes and quiet space rather than detail.
- The whole artwork has one cohesive matte gouache/cut-paper/grain medium; no area looks photographic, marker-drawn, or watercolor-painted.
- The left illustration dominates and is completely unframed; the right column has exactly six separated stickers with a clear size hierarchy.
- Exactly three small English keywords appear once on exposed paper beneath the left illustration, separated by centered dots.
- Warm paper remains visible around the full composition, and no other readable text, watermark, signature, or incidental source text remains.

## Delivery

Show the finished image. Briefly name the identification anchor, the six sticker choices, the three English keywords, and the saved path when available.
