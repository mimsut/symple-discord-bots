# SYMPLE / KKEBI — Founder & Business Context

> This file is auto-loaded by remote Claude agents (CCR) for context.
> Source: PDF documents in /Users/user/kkebimimsut/ (extracted 2026-04-20)

---

## 1. Company Overview

| Field | Detail |
|-------|--------|
| Company | **SYMPLE** |
| Product | **KKEBI** — CBT-based digital mental health platform |
| Founder | **김민수 (Minsoo Kim)**, born 2002-02-05 |
| Education | Yonsei University, Psychology (B.A.–M.A. combined, 4th year, 학석사연계과정) |
| Advisor | 정경미 교수, Yonsei University Psychology Dept. |
| Contact | min0205@yonsei.ac.kr / 010-5271-9785 |
| Location | Seoul, Korea (서대문구 연희로16길 20) |
| MVP | https://symple.kr |

---

## 2. Problem Statement

- **51%** of Korean workers experience burnout (Grant Thornton, 2024)
- **$1 trillion** annual productivity loss from depression/anxiety (WHO)
- Korean workers work **149 hours more per year** than OECD average
- EAP (Employee Assistance Program) awareness: **69%**, but actual usage: only **6–12%**
- Root cause: people recognize burnout too late; no early detection
- Existing solutions (in-person counseling, meditation apps, text chatbots) have high barriers: cost, time, stigma

**Three underserved customer segments:**
1. **Individual workers (B2C)** — feel stress but can't afford/access therapy
2. **Corporate HR (B2B)** — need employee wellness data but lack visibility
3. **Therapists/Counseling centers (B2B)** — struggle with between-session tracking and documentation burden

---

## 3. Solution: KKEBI

**Core concept:** Multimodal AI (voice + video + behavioral data) → early burnout detection → personalized CBT micro-interventions

### Three-platform architecture:
1. **Individual App** — for workers (B2C)
2. **Therapist/Counseling Center Web** — session support, client tracking, documentation
3. **Corporate Web** — anonymous org-level reports, HR dashboard

### Key features:
- **5–10 min voice check-in** — AI analysis of vocal biomarkers (pitch, rhythm, formants, MFCC, energy) vs. personal baseline
- **Micro CBT sessions** — compresses 60-min therapy into 5-10 min (S-E-T-B framework: Situation, Emotion, Thought, Behavior)
- **Daily CBT missions** — behavior activation tasks
- **Digital phenotyping** — phone usage patterns, activity data for longitudinal tracking
- **Expert referral** — connects users to real therapists when needed

### AI Technology:
- Proprietary voice AI model: temporal features (rhythm), formant features (F1/F2/F3), spectral features (MFCC, RMS energy)
- High-risk signal detection: sudden energy spikes, dark timbre, degraded clarity, rigid patterns
- Patent filed (1 registered)
- SCI papers: 2 published (IEEE JBHI and others)

---

## 4. Business Model

| Customer | Model | Price |
|----------|-------|-------|
| Corporate (B2B) | SaaS subscription | $3–5/user/month |
| Counseling centers (B2B) | SaaS | $50–100/month |
| Individual (B2C) | Freemium → Premium | $5/month |

**2028 Revenue Target: $1.5M**

**Go-to-market:** Korea B2C → Korea B2B → US B2B2C (corporate wellness)

---

## 5. Traction & Validation

- **Duck's Dream (오리의 꿈)** — predecessor mental health app; real user counseling data showing burnout/workplace stress as top issues
- **꽥꽥이 (Kkaekkwaegi)** — Kakao chatbot with real usage data confirming workplace stress demand
- **35 letters of intent (구매의향서)** secured from early customers
- **Toss mini-app launch** — ranked #4 in new apps category
- **Tumblbug crowdfunding** campaign completed
- **대한디지털치료학회 (Korean Digital Therapeutics Association)** — Best Poster Award
- **정주영창업경진대회** — participated
- **SF MARU** — 3-week visit/residency in San Francisco

---

## 6. Team

| Role | Name | Background |
|------|------|-----------|
| CEO / Co-founder | 김민수 (Minsoo Kim) | Yonsei Psych, Digital Mental Health Lab, KCI paper 1st author, patent, 1yr marketing (edtech), 1yr healthcare service planning |
| Co-founder | 김하나 | Yonsei Korean Literature, Underwood International College |
| CTO | 김승현 | Yonsei EE, AI research society president, prior startup exit |
| Designer | 신지원 | Ewha Visual Design, 2yr design agency, 4yr freelance |
| Frontend Dev | 박찬혁 | K University CS, 4yr fullstack at edtech company |
| Backend Dev | (name) | S University CS, junior systems engineer at major Korean conglomerate |

---

## 7. Roadmap

| Timeline | Milestone |
|----------|-----------|
| ~2026-05-31 | Individual app (v1) launch |
| ~2026-06-30 | Therapist/counseling center web launch |
| ~2026-07-14 | Corporate web launch |
| ~2027-05-17 | Voice AI model commercialization |
| ~2027-07-31 | US market English version |
| Long-term | KKEBI figure (IoT device) |

---

## 8. Strategic Context for Agents

**Current pivot:** Korea B2C (Duck's Dream users) → **US B2B2C** (corporate wellness, targeting HR buyers at mid-large companies)

**Key differentiation vs. competitors:**
- **vs. Calm/Headspace:** clinical CBT, not just mindfulness; voice biomarker detection
- **vs. Lyra Health/Spring Health:** app-first, low barrier; not just therapy referral
- **vs. BetterUp:** between-session tool that supplements, not replaces, coaching
- **vs. Woebot/Wysa:** multimodal (voice+video) vs. text only; real therapist integration

**What KKEBI is NOT:** a replacement for therapy. It's between-session support that makes therapists more effective.

**Current vulnerabilities (for honest founder feedback):**
- Founder is still a 4th-year student balancing 18 credits
- Team is strong technically but early on US go-to-market strategy
- 35 LOIs is promising but no paying customers yet
- Voice AI accuracy not yet validated in peer-reviewed clinical studies
- HIPAA compliance for US market not yet addressed
- Competition from well-funded US players (Lyra: $900M raised, Spring Health: $480M)
