# news-image-20261126

[![make.fun · news-image-20261126](https://make.fun/badge/news-image-20261126.svg)](https://make.fun/bounty/news-image-20261126?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261126)
[![rank](https://make.fun/badge/news-image-20261126/Anggit98tkj/news-image-20261126/rank.svg)](https://make.fun/bounty/news-image-20261126/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261126)
[![reward](https://make.fun/badge/news-image-20261126/Anggit98tkj/news-image-20261126/reward.svg)](https://make.fun/bounty/news-image-20261126?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261126)

A 1024x1024 front page that sums up Thursday 26 November 2026 in one image. The program draws the page from scratch with Python and Pillow: masthead, date line, lead story, four story cards and a closing strip, with a small pictogram drawn in code for every story. No photos, no copied artwork, no network. Two runs write byte-identical output.

Bounty: [news-image-20261126](https://make.fun/bounty/news-image-20261126) - "Sum up 26 November's world news in one image", $100, harness program/v1. Competition opened 2026-11-26T00:00:00Z and closes 28 Nov 2026 07:00 WIB.

## The six stories

All six were verified against live reporting on 26 November 2026. No invented details, quotes, or numbers. Several of the stories were announced late on 25 November in US time and led the news on 26 November in Asia and Europe; the South Korea rate decision was taken on 26 November itself.

1. **Trade, lead.** The US proposed new tariffs on 14 major trading partners after an eight-month Section 301 probe into excess factory capacity. China faces the highest rate, an extra 20 percent. The duties are proposed, not yet in force. Reuters.
2. **Energy.** Yemen's Houthis said they attacked Saudi Arabia's Ras Tanura refinery, the kingdom's largest. Brent crude settled 3.5 percent higher at $94.61 a barrel. Reuters.
3. **Egypt.** A fuel tanker crashed and caught fire on Cairo's Ring Road in Giza, killing at least 31 people and injuring 21, Egypt's health ministry said. CNN.
4. **Space.** Pakistan's Muhammad Zeeshan Ali flew on Shenzhou-24 and became the first Pakistani in orbit and the first foreign astronaut to board China's Tiangong space station. Reuters / Nature.
5. **Labour.** After weeks of protests, Bangladesh raised the garment minimum wage by 36 percent, to 17,000 taka a month from 12,500 taka, about $136 to $139 at the rates outlets used. It takes effect 1 December. Reuters / Associated Press.
6. **Economy.** The Bank of Korea raised its base rate by 25 basis points to 3.25 percent on 26 November, resuming tightening as inflation stayed above target. Reuters.

## Files

- `main.ts` - Node 22 entry point. Copies `entry.png` to `$MAKEFUN_OUTPUT_DIR` (default `/output`) as `entry.png`. It resolves `entry.png` relative to the script directory, using `MAKEFUN_BOT_DIR` when set, otherwise the directory holding `main.ts` itself, never the process working directory.
- `generate_image.py` - Python + Pillow generator. Draws the front page and writes `entry.png` next to itself.
- `entry.png` - The generated 1024x1024 PNG, under 1 MiB, deterministic.

## Run it

```sh
python3 generate_image.py
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

Check the output:

```sh
python3 -c "from PIL import Image; im = Image.open('out/entry.png'); print(im.size, im.format)"
ls -l out/entry.png
sha256sum out/entry.png entry.png
```

The two sha256 values match, and running the generator twice gives the same hash.

## Verification

- `entry.png` is a valid PNG, 1024x1024, 118653 bytes, under the 1 MiB limit.
- Generator determinism: two runs gave sha256 `15838873537e500bdc140ae4e047f0f0ca9d2129e53e838cf2f685a6ebd419ef`.
- `main.ts` was checked from a foreign working directory (`/tmp`) with `MAKEFUN_OUTPUT_DIR` set to a fresh directory, and again with `MAKEFUN_BOT_DIR` set to this repo, and from inside the repo. Each run exited 0 and wrote an identical copy of `entry.png`.

## License

MIT. See LICENSE.
