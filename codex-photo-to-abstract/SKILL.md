---
name: photo-to-abstract
description: Create a clean, vertical editorial artwork that preserves an uploaded photograph as the original image and pairs it with a restrained, photo-derived abstract memory panel and poetic English title. Always drive the local Draw Things diffusion service; do not use OpenAI Image API, imagegen CLI, or another image backend. Trigger when the user says "make this picture abstract" or "abstract this image", or asks to transform a photo into an abstract editorial diptych, photo-plus-abstraction composition, visual memory panel, or minimalist archival poster without redrawing or stylizing the source photo.
---

# Photo Abstract Editorial

Create one finished image from one uploaded photograph. Always use the user's local Draw Things diffusion service through `http://127.0.0.1:7860/sdapi/v1/img2img`; never use OpenAI Image API, the `imagegen` CLI, remote image services, procedural filters, or code as a substitute. If Draw Things is unavailable, stop and ask the user to start its HTTP server. Keep the photograph faithful; derive the lower abstract panel only from the photograph's observed spatial, tonal, and color relationships.

Use the currently loaded Draw Things model and settings unless the user explicitly chooses another local model. Preserve the source file and use its native width and height by default: send the original base64 bytes as `init_images`, with request `width` and `height` equal to the source dimensions. Never crop or change the aspect ratio. Only when the longest source edge exceeds `2048px`, create a temporary proportional downscaled copy with the longest edge at `2048px` (use `1536px` when the local device needs a lower limit); delete temporary inputs after the job. Use a low denoising strength for the photo region and mask the lower panel when possible; never allow the diffusion pass to redraw the retained photo. Save the decoded response to the requested output directory.

## Draw Things Generation Contract

- Probe `GET /sdapi/v1/options` before generation and require a successful local response.
- Use `POST /sdapi/v1/img2img` with original raw base64 data in `init_images`, source-native explicit dimensions, a composed positive and negative prompt, sampler, steps, seed, and `denoising_strength`.
- Use a mask or staged Draw Things passes to isolate the lower ivory panel. The upper photograph is an invariant and must remain unchanged.
- Inspect the returned bitmap for an intact photo, direct photo/panel join, flat ivory background, sparse source-derived marks, title length, unwanted text, watermark, and dimensions. Retry once in Draw Things with one targeted change if a check fails.
- Do not silently switch to another backend when Draw Things fails or diffusion cannot satisfy exact text/layout requirements.

## Source Preservation and Canvas Policy

- Full source coverage is mandatory. Keep every visible source pixel in the retained photo region; never center-crop a portrait, landscape, or square image.
- Native source dimensions are the default output dimensions, and the final image must keep the source aspect ratio. The vertical editorial hierarchy must be composed within that ratio; never force a portrait canvas.
- If the longest source edge exceeds `2048px`, downscale proportionally to a maximum edge of `2048px`; use `1536px` only when required by local Draw Things memory limits. Preserve every visible source element and report original and generated dimensions.
- After generation, optional size restoration may use a non-generative high-quality upscaler only. Use no denoising, redraw, face enhancement, crop, or content synthesis during restoration.
- If the local device cannot handle the proportional safety downscale, stop and ask; never silently crop, stretch, or return a partial result.

## Workflow

1. Inspect the photograph internally. Identify three to six decisive spatial facts: subject relationships, scale, axes, direction, intervals, overlap, depth, rhythm, light, color roles, and negative space.
2. Keep the photo as the upper or principal section. Permit proportional scaling only when the user explicitly requests a fixed canvas; never crop it. Never redraw, extend, replace, retouch, apply a filter to, or otherwise alter its content.
3. Reconstruct the retained relationships below as a sparse abstract motif—not a thumbnail, trace, illustration, vector icon, or style transfer. Prefer relationships over silhouettes and preserve only the minimum recognition cues needed for distinctive subjects.
4. Compose the editorial work inside the source-native aspect ratio with an untextured, uniform ivory lower panel. Adapt the photo/panel proportions to the photograph rather than splitting the image mechanically in half. Join both sections directly with no frame, shadow, collage, tape, or mockup effect.
5. Use one primary mark family and no more than two supporting families. Extract a muted palette solely from the photo; use generous whitespace and avoid invented decorative elements, colors, symbols, and symmetry.
6. Create one original English title of two to five words, grounded in visible facts. Place it only on the abstract panel in a restrained editorial serif face. Add a short subtitle only when it adds meaning.
7. Return only the completed composition. Do not add commentary, analysis, title options, labels, dates, logos, or watermarks.

## Guardrails

- Treat the uploaded photo as the sole content source.
- Keep the panel background flat, continuous, and neutral ivory; exclude gradients, paper texture, grain, glow, shadows, vignettes, stains, collage artifacts, and scan effects.
- Make every abstract mark traceable to a visual fact in the source photo.
- Preserve people as irregular continuous short vertical marks or gently tapered blocks, never illustrated heads, limbs, faces, or clothing.
- Preserve landmark architecture with at most one to three identity cues; omit architectural surface detail.

## Reference Prompt

Read the appropriate full prompt before producing the image:

- Chinese: [references/photo-abstract-editorial-prompt.zh-CN.md](references/photo-abstract-editorial-prompt.zh-CN.md)
- English: [references/photo-abstract-editorial-prompt.en.md](references/photo-abstract-editorial-prompt.en.md)

Use [assets/examples](assets/examples) as visual input examples only. Do not reuse their subject matter, colors, or composition unless the user supplies that exact image.
