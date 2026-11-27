# Changelog

All notable releases and repository updates for `icom-custom-firmware` are recorded here.

## [Unreleased]

- Documentation & Branding: Added SVG logo and light/dark README banners (`docs/assets/`), Mermaid pipeline diagram, table of contents, and `CHANGELOG.md`.
- Web Patcher UX: Added header logo and section jump links, placed Step 1 directly below the safety notice with collapsible technical details, added an in-memory light/dark theme toggle (preserving the zero-cookie/zero-storage privacy model), added one-click MD5 copy buttons, revoked stale Blob URLs across builds, and linked each release in `docs/patches/index.json` to its matching SD-apps bundle and SHA-256 checksum.
- Tooling & CI: Extended `tools/build_index.py` to validate `apps_bundle` files and record SHA-256 digests, added Python unit tests (`tests/test_python_tools.py`), and added GitHub Actions CI (`.github/workflows/ci.yml`).

## [20261119v14] - 2026-11-20

- Supported radios: `IC-9700 E` (`9700E150.dat`), `IC-705 E` (`705E140.dat`), and `IC-705 J` (`705J140.dat`).
- Verified QSO mode on IC-705 E and IC-9700 (FT8, Q65, JT4) with `QSO: wait 1 s, tap again` feedback when tapping `TX?` early.
- Increased hold time from red (beacon) frame to green (CQ) frame (~3x longer) to prevent accidental CQ arming.
- Added `TX refused: <reason>` status messages on the `DECODE` screen.
- Added `APRS` GPS TX mode (`MENU > SET > GPS > GPS TX Mode`, 1200 Bd AFSK on FM) and `APRS.APP` (MIT) in the SD-apps bundles, logging received stations to RX History and `Apps\APRS.LOG`.
- Confirmed installation and HF TX unlock on `IC-705 J` (2 m / 70 cm TX remains hardware-limited above 146.000 MHz).

## [20261119v13] - 2026-11-19

- Added QSO mode and WSPR-2 decoding support across IC-705 E and IC-9700 builds.

## [20261119v6 / 20261119v8] - 2026-11-19

- Added on-radio period-aligned beacon (long-press mode tile, red frame) and PSKReporter spotting.

## [20261118v4] - 2026-11-18

- Added ICAP digital-mode SD-card decoders (Q65, FT8, JT4, PI4, WSPR) and automatic PSKReporter spotting on top of transverter, scope dB/div, and A/B bootloader support.

## [20261113v1 / 20261113v3] - 2026-11-13

- Added `Scope dB/div` (`10 / 6 / 3 / 1 dB`) for IC-705 E/J (`v1`) and IC-9700 (`v3`) with per-MAIN/SUB transverter selection and DUAL/SAT mode handling.
