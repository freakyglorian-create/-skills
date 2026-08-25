---
name: postop-nasal-splint-identity
description: Create postoperative recovery photos from supplied person images while preserving the face and adding or preserving one exact nasal splint/tape design. Use when the user asks for a nasal-splint recovery image, postoperative nasal-reference photo, or background/clothing variants without facial beautification.
---

# Postoperative Nasal-Splint Identity

Use the supplied person images as the only identity reference and the supplied nasal image as the only treatment reference. The default operation is to keep the original face, hair, background, clothing, and framing, and add or preserve only the nasal splint, tape, dressing, and matching recovery state. If the user explicitly requests scene or clothing changes, change only those requested elements.

## Required inputs and reference roles

- Identify the face references and the nasal-treatment reference before generating anything.
- If a local input has not been shown in the conversation, load it with `view_image` first.
- Prefer a full, sharp nose reference. If no nose reference is supplied, use `assets/nasal-splint-reference.png` only for a frontal image when its splint geometry and tape pattern are suitable. For a different angle, device type, tape arrangement, or dressing state, ask for a matching nose reference instead of inventing one.
- Do not use unrelated people, stock faces, or previous subjects as identity references.

## Identity invariants

Preserve facial proportions, face outline, eye spacing, brow shape, eyelids, lips, skin tone, natural asymmetry, moles, marks, hairline, and hairstyle. Do not slim the face, enlarge the eyes, reshape the nose or lips, smooth skin, alter skin color, add glam makeup, or mix faces. Keep the original expression unless the user requests a small natural change such as calm, tired, or understated smile.

## Nasal-treatment invariants

Treat the nose region as protected reference material. Preserve the exact splint material, color, shape, width, length, hole layout, tape color, tape placement, overlap, edges, tip exposure, dressing texture, and visible residue or marks. Do not add or remove tape, change the splint type, clean up the device, change the nose contour, or remove postoperative elements. Keep bruising, swelling, and puffiness at the level shown by the nasal reference; never exaggerate them.

The built-in image generator can strongly preserve a reference but cannot guarantee mathematical pixel identity. State this briefly when the user asks for literal pixel-for-pixel copying. Never claim that a generated result is a clinical record or exact medical documentation.

## Generation workflow

1. Inspect the inputs and label their roles in the prompt: face reference(s), nasal-treatment reference, and optional scene reference.
2. If the user says “只增加鼻夹板” or equivalent, preserve the original scene, clothing, crop, and lighting; edit only the nose treatment and the matching subtle recovery state.
3. If the user asks for variants, create separate prompts and separate built-in `image_gen` calls. Default to four variants only when multiple scenes are requested; otherwise make one focused result.
4. Use the `identity-preserve` image-editing mode. Put the scene/background instructions before the subject details, then repeat the protected face and nose invariants at the end of every prompt.
5. Use soft natural diffuse light and ordinary phone-camera texture unless the user requests another look. Keep frontal outputs centered, level-eyed, and free of unnecessary pose changes.
6. Inspect every output for face drift, beautification, altered eye spacing, changed hair, missing tape, changed hole pattern, added medical devices, or exaggerated swelling. Regenerate only with a targeted correction when an invariant fails.
7. Save outputs non-destructively. When source paths are available, create a sibling folder named `术后鼻夹板输出` or a versioned equivalent; never overwrite source photos.

## Prompt skeleton

```text
Use case: identity-preserve
Asset type: photorealistic postoperative recovery photo
Input images: face reference(s); exact nasal-treatment reference; optional scene reference
Primary request: change only <requested elements>
Identity constraints: preserve the supplied person's face, hair, skin texture, marks, and proportions; no beautification or face reshaping
Nose constraints: copy the supplied nasal splint, tape, dressing, hole layout, edges, and tip exposure; no redraw, addition, removal, or redesign
Composition: <preserve source framing or requested angle>
Lighting: <natural diffuse phone light>
Avoid: face mixing, beauty filters, smoothing, altered features, changed nasal device, extra medical equipment, text, watermark
```

When `F:\AI素材需求\提示词库.html` exists and the user requests library scenes, read only the relevant PW-004/PW-005/PW-006 entries and use them as scene guidance; they must not override the supplied identity or nasal-treatment reference.

