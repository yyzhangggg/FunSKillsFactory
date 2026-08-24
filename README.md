# FunSKillsFactory

A collection of Codex skills for creative image workflows and desktop-pet experiments. Some skills are written here for fun; others are adapted from community projects.

## Skills

### `photo-to-abstract`

Creates a vertical editorial composition from a photo and a restrained abstract panel.

Triggers:

- `make this picture abstract`
- `abstract this image`

### `image-to-sticker`

Turns an uploaded photo into a collectible image-to-sticker memory card with six source-derived stickers and three English keywords.

Triggers:

- `make this iamge a sticker`
- `make sticker`

### `photo-to-desktop-pet`

Creates a consistent desktop-pet character package from 3-9 photos of one person or animal. Use front, side, and back references when available. Humans retain selected clothing; animals do not receive clothing by default. Both can use a food bowl and water bowl.

The workflow has two stages:

1. `make this a pet` or `make my friend pet` creates the character turnaround and action assets for approval.
2. `make this a desktop pet` builds the runnable desktop-pet application only after the character and actions are approved.

Supported actions include standing, sitting, walking, crawling, jumping, eating, drinking, sleeping, reacting, an exaggerated comic `poop` action, and rare long-cycle `chaos` behavior.

Available style flags:

- `-pixel`: pixel-art rendering
- `-manga`: Japanese manga style
- `-3d`: East Asian ancient fantasy direction
- `-western`: Middle Eastern tone and drawing style
- `-kpop`: highly polished, shining K-pop-inspired style

Use one style flag at a time. If no style is supplied, choose one before generating styled assets.

## Installation

Copy the skill folders into your Codex user skills directory:

```text
~/.codex/skills/
```

For example:

```zsh
cp -R codex-photo-to-desktop-pet ~/.codex/skills/
```

Restart Codex or start a new session after installing a skill.

## Credits

The sticker skill was adapted from:

https://github.com/carolinaaafy/travel-memory-sticker-card
