# 🎨 Visual Identity & Design Rationale: Portfolio System

**Assignment:** Week 3 — Consistency, Not Talent (and Frame, Not Upstage)  
**Track:** General AI Fluency | **Phase:** Foundations  
**Author:** Muhammad Akbar Pradana (Machine Learning Intern @ FlyRank AI)  
**Live Site:** `https://akbarprdna.my.id` / `akbarpradana.netlify.app`  

---

## 1. Executive Summary & Design Philosophy
This document establishes the visual identity and design judgment principles for my applied Machine Learning and Data Science portfolio. Rather than relying on decorative artistic talent or flashy animations, the design strictly adheres to the principle of **"Frame, Not Upstage"** — the interface acts as a minimalist frame that puts real empirical evidence, code artifacts, and ML benchmark metrics at the center of the user's attention.

---

## 2. Core Design Principle 1: Consistency, Not Talent
Professional visual perception is created through strict typographic and spatial consistency:
- **Typography Pairing:** Standard, highly legible sans-serif / serif hierarchy for prose coupled with monospace font (`Courier` / `Fira Code`) for numerical metrics, code snippets, and dataset columns.
- **Color Palette (60-30-10 Rule):**
  - *60% Dominant Background:* Clean, high-contrast monochrome surface (White `#FFFFFF` or Deep Slate `#0F172A`).
  - *30% Text & Structural Elements:* Dark Slate (`#1E293B`) for body text, ensuring WCAG AAA legibility.
  - *10% Focal Accent:* Deep Blue (`#2563EB`) reserved strictly for interactive links, primary action buttons, and active tabs.
- **Uniform Spacing Grid:** 8px baseline grid across all card paddings, margins, and column layouts.

---

## 3. Core Design Principle 2: Frame, Not Upstage
A technical portfolio exists to prove engineering competence, not to showcase visual gimmicks:
- **Zero Decorative Fluff:** No distracting animated particle meshes, spinning 3D globes, or rainbow gradient headline fills that obscure technical copy.
- **Scannable Hierarchy:** Recruiters and engineering leads spend ~30 seconds per profile. Key metrics (e.g., *Precision@50 = 76.0%*, *30k rows evaluated*, *Client-Holdout validation*) are surfaced immediately in clean summary callouts.
- **Subdued Containers:** Cards and tables use simple 0.5px solid borders rather than heavy nested boxes or glowing outlines.

---

## 4. Core Design Principle 3: Real Proof Over AI Fluff
When selecting imagery for project case studies, empirical artifacts always supersede generic AI-generated imagery:
- **Avoided:** Generic AI-generated stock illustrations (e.g., glowing robotic brains, neon neural net spheres) which signal amateurish filler.
- **Prioritized (Real Artifacts):**
  1. Real terminal run logs and CLI execution loops.
  2. Structured model benchmark comparison tables (Logistic Regression vs Decision Tree vs Random Forest vs Baseline).
  3. System architecture flowcharts (ReAct agent tool calling pipeline).
  4. Real dataset distribution percentile tables.

---

## 5. Implementation Verification Checklist
- [x] Tested across mobile, tablet, and desktop viewports with zero horizontal overflow.
- [x] Verified high-contrast text readability in dark and light modes.
- [x] Verified working outbound links to LinkedIn, GitHub, CV, and booking calendar.
- [x] Replaced all placeholder illustrations with authentic case study artifacts and benchmark figures.
