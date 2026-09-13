# PhishGuard — Smart Link Protection for SMS, DMs & OS Integrations

> **Stop the scam before the click.**

PhishGuard is a mobile-first, hyper-local security engine built to detect zero-day phishing links across SMS, social media DMs (WhatsApp, Instagram, Facebook, TikTok), and system-wide device vectors. Unlike traditional caller-ID tools that rely on stale phone number databases, PhishGuard inspects the **destination URL and infrastructure metadata** in real time—catching attackers using fresh burner SIMs before users interact with malicious links.

---

## The Problem

In South Africa and emerging mobile markets, digital fraud has migrated from traditional email to mobile messaging channels. Citizens are targeted daily by deceptive links across multiple vectors:

1. **SMS & Banking Scams:** Messages impersonating high-trust institutions (e.g., *"SARS refund available"*, *"FNB account suspended"*, *"PostNet package delivery failed"*).
2. **Social Media Impersonation:** Fake security alerts in DMs (e.g., *"Your Instagram account will be deleted"*, *"Facebook copyright violation"*, *"Is this you in this video?"*).
3. **System-Wide & Physical Vectors:** Malicious links copied to the clipboard, deceptive push notifications, links embedded in PDFs/emails, and tampered QR code stickers (*"Quishing"*).

### Why Existing Solutions Fail

Traditional anti-spam solutions rely on **sender-based reporting**. Attackers easily bypass this by rotating cheap SIM cards, VoIP gateways, and burner accounts daily. By the time a phone number is reported and flagged, thousands of users have already clicked. Furthermore, existing tools are blind inside social media DMs, fail to analyze outbound link destinations, and offer black-box blocking without teaching users *why* a link is dangerous.

---

## The Solution

**PhishGuard** shifts the security paradigm from **WHO sent the message** to **WHERE the link goes**. By analyzing destination URLs the moment they are generated or encountered across the OS, PhishGuard catches zero-day scam domains on day zero—before global threat databases or caller-ID registries update.

### Core Capabilities

* **Destination-First Analysis:** Evaluates domain registration age (WHOIS), SSL certificate metadata, and multi-hop shortlink redirects (`bit.ly`, `tinyurl.com`).
* **Typosquatting & Lookalike Detection:** Uses Levenshtein distance matching against an authoritative registry of South African institutions (`sars.gov.za`, `fnb.co.za`, `capitecbank.co.za`, `postnet.co.za`).
* **Multi-Vector Ingestion Layer:** Dedicated heuristic pipelines for **Bank/SMS Mode**, **Social Media Mode**, **System Clipboard Monitoring**, and **QR Code Scanning**.
* **Clear, Educational Output:** Returns a simple **GREEN (Safe)**, **YELLOW (Caution)**, or **RED (Phishing)** status paired with plain-language explanations and immediate actionable advice.

---

## Key Features

* **Real-Time URL Resolution:** Traces obfuscated links through all redirect layers to expose final landing destinations.
* **System-Wide Auto-Detection:** Automatically inspects links copied to the clipboard, intercepted via QR code scans, or tapped within external applications.
* **3-Tier Risk Rating:** Replaces technical jargon with easy-to-understand explanations that build long-term digital literacy.
* **AI-Powered Inspection Pipeline:** Combines fast lexical ML feature classification, headless vision analysis for visual clone detection, and lightweight LLMs for context-aware risk breakdowns.

---

## System Architecture

```
                               ┌─────────────────────────────────────────────────┐
                               │                 INGESTION LAYER                 │
                               ├──────────────┬────────────────┬─────────────────┤
                               │ Android SMS  │ System         │ QR Code         │
                               │ Listener     │ Clipboard      │ Camera Scanner  │
                               └──────┬───────┴────────┬───────┴────────┬────────┘
                                      │                │                │
                                      └────────────────┼────────────────┘
                                                       │
                                                       ▼
                               ┌─────────────────────────────────────────────────┐
                               │           Phase 1: Unroll & Resolve             │
                               │     (Shortlink Unrolling & HTTP Tracing)        │
                               └─────────────────────────────────────────────────┘
                                                       │
                                                       ▼
                               ┌─────────────────────────────────────────────────┐
                               │        Phase 2: Lexical & Metadata Rules        │
                               │   (Levenshtein Distance, WHOIS Age, SSL Certs)  │
                               └─────────────────────────────────────────────────┘
                                                       │
                                                       ▼
                               ┌─────────────────────────────────────────────────┐
                               │         Phase 3: AI Explanation Pipeline        │
                               │    (Visual Clone Matching & Contextual LLM)     │
                               └─────────────────────────────────────────────────┘
                                                       │
                                                       ▼
                                  [ GREEN Safe | YELLOW Caution | RED Phishing ]

```

---

## Tech Stack

* **Core Backend Engine:** Python 3.11+, FastAPI
* **Heuristics & String Matching:** `Levenshtein`, `tldextract`, `python-whois`
* **Headless Visual Inspector:** Playwright (Python)
* **AI & Machine Learning:** LightGBM (Lexical), Vector Embeddings (Visual Matching), Small Language Models (Contextual Explanations)
* **Frontend & Mobile Layer:** Next.js, Tailwind CSS, Android Native (Kotlin/Java)

---

## Quickstart Guide

### Prerequisites

* Python 3.11+
* Node.js 18+
* `pip` and `npm`

### 1. Repository Setup

```bash
git clone https://github.com/your-username/phishguard.git
cd phishguard

```

### 2. Backend Setup

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install backend dependencies
cd backend
pip install -r requirements.txt

# Run development server
uvicorn main:app --reload --port 8000

```

### 3. Frontend Setup

```bash
# Open a new terminal session
cd frontend
npm install
npm run dev

```

The web client will be running on `http://localhost:3000` and connecting to the API backend at `http://localhost:8000`.

---

## API Reference

### Analyze URL Endpoint

* **URL:** `/api/v1/scan`
* **Method:** `POST`
* **Content-Type:** `application/json`

#### Request Payload

```json
{
  "url": "http://sars-gov-za-refund.co.za/login",
  "source": "clipboard",
  "raw_message_text": "Click here to claim your SARS refund of R3,500."
}

```

#### Sample Response

```json
{
  "verdict": "RED",
  "confidence_score": 0.96,
  "target_brand": "South African Revenue Service (SARS)",
  "reasons": [
    "Domain 'sars-gov-za-refund.co.za' was created 2 days ago.",
    "Calculated lookalike distance against official 'sars.gov.za' domain.",
    "The link copied to your clipboard mimics SARS, but resolves to an offshore IP address."
  ],
  "recommended_action": "Do not enter your credentials or banking details. Delete the message immediately."
}

```

---

## Development Roadmap

* [x] **Phase 1 (Core Engine):** Web App & Rule Pipeline (Domain age, similarity distance, shortlink resolution).
* [ ] **Phase 2 (Social & SMS):** Android Background SMS Listener and OS Share-Sheet Integration for WhatsApp/Social DMs.
* [ ] **Phase 3 (System-Wide Protection):**
* Background Clipboard Monitor (Auto-scan on link copy).
* QR Code / "Quishing" Camera Scanner.
* System-wide OS URL Handler for Email & PDF links.


* [ ] **Phase 4 (Enterprise):** On-device TFLite execution & B2B Brand Protection Takedown API.

---

---

**PhishGuard** — *Stop the scam before the click.*

Protecting mobile ecosystems and digital identities against zero-day phishing attacks.

[Report Phishing Domain](https://www.google.com/search?q=https://github.com/your-username/phishguard/issues) • [API Documentation](https://www.google.com/search?q=%23api-reference) • [Privacy Policy](https://www.google.com/search?q=PRIVACY.md) • [Contribution Guidelines](https://www.google.com/search?q=CONTRIBUTING.md)

© 2026 PhishGuard. Distributed under the MIT License.
