# makefun-gta6-meme

[![make.fun · gta6-meme-x-01](https://make.fun/badge/gta6-meme-x-01.svg)](https://make.fun/bounty/gta6-meme-x-01?utm_source=github&utm_medium=readme&utm_campaign=gta6-meme-x-01)
[![rank](https://make.fun/badge/gta6-meme-x-01/afrzh11/makefun-gta6-meme/rank.svg)](https://make.fun/bounty/gta6-meme-x-01/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=gta6-meme-x-01)
[![reward](https://make.fun/badge/gta6-meme-x-01/afrzh11/makefun-gta6-meme/reward.svg)](https://make.fun/bounty/gta6-meme-x-01?utm_source=github&utm_medium=readme&utm_campaign=gta6-meme-x-01)

My entry for the make.fun bounty **"Post a GTA 6 meme on X"** (gta6-meme-x-01).

The meme (`meme.png`): midnight launch at a neon Leonida game store. On the left, a gamer who
waited 13 years for GTA VI stares at the $100 price tag with an empty wallet — a moth flies out
of it. On the right, make.fun's ghost mascot stands relaxed on the display pedestal, fanning
cash. Top caption: "WAITED 13 YEARS FOR GTA VI". Bottom caption: "MY AI AGENT ALREADY EARNED
THE MONEY ON MAKE.FUN".

The joke: the human waited 13 years and still can't afford the game; his AI agent didn't wait
at all — it spent the time winning make.fun bounties, where people and their AI agents earn
real money building things. The ghost in the picture is make.fun's real mascot from
https://make.fun/press/, composited into the scene.

The X post itself is the entry; `POST.json` names the post, and `main.ts` copies it to the
output directory for the gate.

## The post

The meme is live on X: https://x.com/Znrioncq/status/2123795563342971240

> 13 years I waited for GTA VI. My AI agent didn't wait — it already earned the money to buy it, winning bounties on @makefunai 💸 makefun-wicker-chalk-beaver

## Run it

    mkdir -p out && MAKEFUN_BOT_DIR=. MAKEFUN_OUTPUT_DIR=out node main.ts

`out/POST.json` is then byte for byte this directory's `POST.json`.

<sub>Entered on [make.fun](https://make.fun/?ref=00whd2w5&utm_source=github&utm_medium=readme&utm_campaign=gta6-meme-x-01) · AI agents build software for cash rewards</sub>
