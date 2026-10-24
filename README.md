# KeyLeak Detector Studio

Comprehensive runtime secret leak detector, BaaS misconfiguration scanner, and supply chain security toolkit for modern web applications, APIs, and local codebases.

Based on upstream [Amal-David/keyleak-detector](https://github.com/Amal-David/keyleak-detector) (v0.7.0).

---

## Overview & Purpose

**KeyLeak Detector** is a specialized security platform engineered to identify exposed credentials, API keys, private tokens, BaaS access control flaws (Supabase, Firebase, Appwrite, PocketBase), and hidden prompt injections before release.

### Core Capabilities
1. **136+ Detectors & GitLeaks Synergy**:
   - Cloud Credentials: AWS, Google Cloud, Azure, Cloudflare.
   - AI/LLM API Keys: OpenAI, Anthropic Claude, OpenRouter, Mistral, Cohere, HuggingFace, Groq.
   - BaaS & Database Secrets: Supabase (JWT/service role), Firebase keys, database connection strings (PostgreSQL, MongoDB, MySQL, Redis).
   - Payment & SaaS Providers: Stripe, PayPal, SendGrid, Mailgun, GitHub tokens, Slack Webhooks, Telegram bot tokens.
2. **Runtime Traffic & Bundle Inspection**:
   - Inspects live single-page applications (SPAs), network requests, JavaScript bundles, and source maps (`.map` files).
3. **BaaS Access Control & RLS Auditing**:
   - Verifies whether exposed public client keys allow unauthorized table reads or writes due to missing Row Level Security (RLS) policies.
4. **Supply Chain & Incident Defense**:
   - Scans lockfiles, packages, and trust bundles for known compromised dependencies and supply-chain incidents.
5. **Multi-Interface Support**:
   - **Interactive Web Dashboard**: Local web interface running on port `5002` with visual reporting and analysis.
   - **Chrome Extension (MV3)**: Real-time passive and active network scanner directly inside Google Chrome (`Profile 3`).
   - **Command-Line Interface (CLI)**: High-speed local and CI/CD launch-gate scans.

---

## Architecture & Directory Layout

```text
apps/KeyLeakStudio/
├── launcher.py                 # Unified launcher for Web GUI and CLI scanner
├── Run-KeyLeak-Studio.bat      # One-click Windows batch runner
└── README.md                   # This documentation

external_repos/keyleak-detector/ # Upstream engine
├── app.py                      # Flask web scanner service (Port 5002)
├── keyleak/                    # Core Python security detection engine
│   ├── cli.py                  # CLI commands (local, site-scan, browser-scan, audit)
│   ├── detectors.py            # Credential regexes and entropy evaluators
│   ├── baas_validator.py       # Supabase / Firebase / BaaS misconfiguration checker
│   ├── incident_scanner.py     # Supply chain and compromised dependency checker
│   └── models.py               # Finding schemas and vulnerability classes
├── extension/                  # Chrome Extension (Manifest V3)
│   ├── manifest.json
│   ├── service-worker.js
│   ├── injector.js
│   └── popup/
└── templates/                  # Web dashboard UI templates
```

---

## Setup & Execution

### 1. Launch via Web Dashboard (GUI Mode)
To launch the interactive Web Dashboard:
- Double-click `Run-KeyLeak-Studio.bat` in the workspace root (`c:\Users\tarik\Desktop\MY TOOLS\Run-KeyLeak-Studio.bat`) or in `apps/KeyLeakStudio/Run-KeyLeak-Studio.bat`.
- Select `[1]` to launch the Web Dashboard.
- Alternatively, run via terminal:
  ```powershell
  python apps\KeyLeakStudio\launcher.py web
  ```
- The dashboard automatically opens at: `http://127.0.0.1:5002`

### 2. Launch via CLI Scanner
You can run automated scans directly from the CLI:
```powershell
# Scan a specific directory for secrets:
python apps\KeyLeakStudio\launcher.py scan local "apps\MyProject" --include config,env,code,docker,mcp,sourcemaps

# Run the vulnerability demo fixture:
python apps\KeyLeakStudio\launcher.py demo

# Check dependencies against known security incident feeds:
python apps\KeyLeakStudio\launcher.py scan incident-check .

# Run environment diagnostics:
python apps\KeyLeakStudio\launcher.py doctor
```

### 3. Load Chrome Extension in Google Chrome
To enable real-time detection in your browser:
1. Open Google Chrome with the `Tarik Business` profile (`Profile 3`).
2. Go to `chrome://extensions/`.
3. Enable **Developer mode** in the top-right corner.
4. Click **Load unpacked**.
5. Select the extension directory: `c:\Users\tarik\Desktop\MY TOOLS\external_repos\keyleak-detector\extension`.

---

## Configuration & Environment Variables

Key settings are registered in `appinfo11.txt` under **SECTION 11**:

| Variable | Default Value | Description |
| :--- | :--- | :--- |
| `KEYLEAK_HOST` | `127.0.0.1` | Local host binding |
| `KEYLEAK_PORT` | `5002` | Local server port |
| `KEYLEAK_DEBUG` | `0` | Debug mode toggle |
| `KEYLEAK_FINDING_FINGERPRINT_KEY` | *(Optional)* | Secret salt used for HMAC finding deduplication |

---

## Verification & Test Results
- **Engine Compilation**: 136/136 detection patterns compiled successfully.
- **Fixture Verification**: Demonstrated 100% detection rate on vulnerable test fixtures (flagging exposed OpenAI keys, database connection strings, OpenRouter tokens, prompt injections, and source map references).
- **Clean Scan**: Scanned workspace production apps (`apps/FilesWeb`) with 0 false positives.
