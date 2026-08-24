---
name: photo-to-desktop-pet
description: Create a consistent desktop-pet character package from 3-9 photos of the same person or animal, then build a runnable desktop pet only when the user says "make this a desktop pet". Trigger asset creation with "make this a pet" or "make my friend pet" and support the optional styles -pixel, -manga, -3d, -western, and -kpop. Prefer front, side, and back references. Preserve identity, clothing for people, natural appearance for animals, and shared food and water bowl props across turnarounds and actions.
---

# Photo to Desktop Pet

Turn 3-9 reference photos of one person or one animal into a consistent desktop-pet character package. Build the runnable desktop pet only after the user explicitly requests `make this a desktop pet`.

## Trigger modes

- `make this a pet`
- `make my friend pet`
- `make this a pet -<style>`
- `make this a desktop pet`

`make this a pet` creates the character and animation assets. It must not create the desktop application yet.

`make this a desktop pet` builds the application only after the character turnaround and action assets have been reviewed and approved. If the assets have not been approved, stop and request approval before implementation.

Treat an optional style flag as user input. Supported flags are `-pixel`, `-manga`, `-3d`, `-western`, and `-kpop`; read [references/style-guide.md](references/style-guide.md) before generating. Do not invent a default style. Preserve the selected style consistently once the user provides it.

## Input requirements

- Accept 3-9 photos.
- All photos must show the same person or the same animal.
- Prefer a complete front view, one or both side views, and a back view.
- Use the clearest available images to establish identity and proportions.
- Ask for missing or unusable references when the subject, silhouette, clothing, markings, or important features cannot be established reliably.
- Do not merge multiple people or animals into one character.
- If clothing differs across human references, ask which outfit should be locked. Do not change a person's clothing between outputs after it is selected.
- Do not add clothing to animals unless the user explicitly requests it.

## Phase 1: isolate and lock the main figure

This phase must happen before generating the turnaround, props, or action poses.

1. Inspect all references as a multi-view set for one subject.
2. Identify the main person or animal and reject images with multiple competing subjects unless the user clearly identifies one subject.
3. Remove the source background from each usable reference. Keep the complete visible person or animal, including hair, ears, tail, feet, paws, and other silhouette-defining edges. Do not retain scenery, furniture, unrelated people, text, logos, or accidental objects.
4. Produce an isolated main-figure or main-pet preview on a transparent background. Do not stylize, redesign, crop away important anatomy, or add props at this step.
5. Inspect the cutout for missing limbs, clipped fur or hair, halos, background fragments, incorrect holes, and identity loss. Repair the mask or request a clearer source image when necessary.
6. Present the isolated figure preview for user review. Do not continue to the turnaround phase until the main figure is accepted.

The accepted isolated figure is the source of truth for all later work. Preserve its identity anchors, proportions, hair or coat, markings, selected human clothing, and animal appearance.

## Phase 2: character package

Only after the isolated figure is accepted:

1. Identify stable identity anchors: face or head shape, hair or coat pattern, body proportions, ears, tail, markings, footwear, accessories, and selected clothing.
2. Generate a character sheet with:
   - front view
   - left or right side view
   - opposite side view when references support it
   - back view
   - transparent or neutral background
   - no extra characters, watermark, or unrelated readable text
3. Include the shared props in the character package:
   - one food bowl
   - one water bowl
4. Generate key-pose previews before producing animation frames.
5. Present the turnaround, props, and key poses for review. Treat approved outputs as the locked character source of truth.

If a view is not present in the references, mark that view as inferred and avoid inventing distinctive details. Ask for more photos when the missing view would materially affect identity or animation.

## Phase 3: required action set

Only after the isolated figure and character package are approved, create key-pose previews, then fixed animation assets, for these actions:

- `idle`: quiet standing behavior with subtle movement
- `stand`: neutral standing pose
- `walk`: movement along the bottom of the screen
- `sit`: seated behavior
- `crawl`: low playful movement
- `jump`: short jump with a clear landing
- `eat`: interacting with the food bowl
- `drink`: interacting with the water bowl
- `sleep`: sleeping behavior
- `reaction`: response to clicking or dragging
- `poop`: exaggerated, silly, harmless cartoon gag behavior
- `chaos`: rare high-energy behavior sequence

The `poop` action must remain non-explicit. Use exaggerated anticipation, a comic pose, a simple symbolic or prop-based gag, and a humorous recovery. Do not show anatomical or graphic detail.

Both people and animals receive the food bowl and water bowl. Keep these props visually consistent in every relevant action.

## Asset approval and locking

Do not generate the turnaround until the user approves the isolated main figure. Do not generate the final animation set until the user approves the turnaround, props, and key-pose previews. After each approval gate, lock the following across every view and frame:

- identity anchors
- silhouette and body proportions
- hair, coat, and markings
- selected human clothing and accessories
- animal appearance without added clothing
- food bowl and water bowl design
- canvas size, anchor point, and scale
- the user-selected style, when provided

When references conflict, prefer the clearest view and ask the user to resolve ambiguity rather than silently changing the character.

## Phase 2: desktop pet application

Run this phase only for `make this a desktop pet` after asset approval.

Create a runnable desktop pet that:

- uses a transparent, borderless window
- keeps the character primarily in the bottom region of the active screen
- supports idle, walking, sitting, sleeping, eating, drinking, reactions, and the approved gag actions
- supports click and drag interaction
- provides pause, mute, scale, behavior-frequency, reset-position, and quit controls
- stores position, scale, audio, and behavior settings locally
- does not open windows, type text, change system settings, or obstruct the user's work for an extended period

Use the approved animation assets rather than regenerating the character during application implementation. Keep the application layer separate from the image-generation layer.

## Long-cycle behavior

Normal behavior should favor `idle`, `walk`, `sit`, and `sleep`, with occasional eating and drinking. The pet may trigger `poop` at a low frequency using the approved animation.

`chaos` is a rare, long-cycle event. It may include rapid running, bouncing, rolling, playful crawling, exaggerated bowl interactions, and a short comic reaction before returning to normal behavior. Schedule it with randomized timing over a long active period, approximately every 2-8 hours by default. Provide a setting to pause or reduce this behavior.

The behavior system must always have a pause control and must recover to a normal state after a chaos sequence.

## Delivery

For the asset phase, show the isolated main figure first and wait for approval. Then show the character sheet, props, and action key-pose previews, listing which assets are awaiting approval. After approval, show or save the fixed animation assets and manifests.

For the desktop-pet phase, provide the runnable application project or package, the animation manifest, and the local configuration defaults. Mention any platform limitations when a packaged desktop application cannot be produced in the current environment.

Do not choose or describe a visual tone or style unless the user supplies one.
