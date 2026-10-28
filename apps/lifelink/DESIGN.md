# LifeLink prototype: design decisions

Prototype of the LifeLink app described in the 32 LifeLink papers (Core Specification, Tablet, Daily
Implementation, the 23 strategies and the four wearables), built to show what can be made **today**,
with **today's** open technology, while keeping every safety rule already published on the website.

## 1. What it is

A Progressive Web App (PWA) at peopleoftheworld.net/plan-to-end-poverty/lifelink/app/. One codebase runs on phones,
tablets and computers (Android, iOS, Windows, macOS, ChromeOS, Linux), installs to the home screen,
and works offline. No account, no server, no tracking: everything a person enters stays on their
device, encrypted. Phase 2 wraps the same code as a native app (for the app stores, Apple Health and
Android Health Connect, NFC and the phone's secure chip); Phase 3 runs it on LifeLink hardware.

## 2. Principles carried from the papers into the code

| Principle (source) | How the prototype honours it |
|---|---|
| You own your data (Ethical AI & Privacy Framework) | Stored only on the device; export everything (JSON, and health as FHIR IPS); delete everything in one step |
| Biometrics stay on your device (LifeLink safety rules) | Fingerprint/face sign-in through passkeys (WebAuthn); the biometric never leaves the phone's secure hardware; a PIN always works |
| Encryption (Core Spec 6.1) | AES-256-GCM vault; key derived from the PIN with Argon2id; signing keys are non-extractable |
| Quantum resistance (Core Spec 6.1) | AES-256 at rest; credentials carry a second, post-quantum signature (ML-DSA, NIST FIPS 204) beside the classical one |
| Offline ID and QR verification (Core Spec 4.1) | Credentials signed with selective disclosure (IETF SD-JWT, RFC 9901): show "over 18" without showing a birth date; any phone verifies offline |
| AI assists, never rules; explainable (Ethical AI Framework) | The learning guide is rule-based and always says why it suggests something; on-device AI is used only where the browser offers it, never sends data away |
| No one shut out (website safeguards) | Works on old phones, offline, without biometrics; a PEC worker can always override; large text, read-aloud, simple mode |
| Know needs, not movements (Counted, not tracked) | Area alerts are matched on the device; needs surveys use randomised response (local differential privacy), so planners see totals, never a person |
| Safety you switch on (safety rules) | SOS only when the user triggers it; you choose who is told; location is shared once, for the emergency |
| Every look is logged (Data stays with the person) | An access log records every time a record is opened or shared |
| Transparent public money (Civic Credits) | Wallet ledger is hash-chained, so any tampering is detectable; "Where public money goes" view |

## 3. Modules (from the Core Specification, section 4, and A Day with LifeLink)

1. **Today**: the day at a glance (credits, a lesson, a health check-in, local alerts, an evening reflection).
2. **Identity**: create a LifeLink ID, unlock by passkey or PIN, show a QR credential, verify someone else's.
3. **Wallet (Civic Credits, demonstration)**: balance, earn opportunities, pay or receive by QR (works offline), tamper-evident ledger.
4. **Learn (the AI Teacher)**: a learning map from first letters to university and trades, built from vetted free sources; built-in lessons with quizzes and spaced review; a skills passport of signed certificates.
5. **Health**: an emergency Medical ID, a portable health record (FHIR IPS export), wellbeing check-ins, vitals including live readings from Bluetooth health devices, trusted information, where to get care, crisis lines.
6. **Safety**: SOS with trusted contacts, area alerts, reporting.
7. **Voice**: local proposals in plain language, vote with a receipt, anonymous needs survey.
8. **My data**: what is stored, access log, consents, export, delete.
9. **Devices**: what works today (Bluetooth health devices, phone motion sensors) and the road to the LifeLink Watch, Ring, Buds and Glasses.

## 4. Honest limits (shown in the app, not hidden)

- Civic Credits in the prototype are demonstration credits with no value.
- Nothing is sent to the police, emergency services or a government. SOS prepares a message the user sends.
- No symptom checker: diagnosing needs clinical validation and regulation as a medical device. The app points to trusted services instead.
- Web Bluetooth works in Chrome, Edge and Android browsers, not Safari on iPhone (Phase 2 native app fixes this).
- Passkey sign-in that unlocks encrypted data needs the WebAuthn PRF feature (Chrome, Edge, Android, Safari 18+); otherwise the PIN is used.
- On-device AI in the browser is currently desktop-only and needs a powerful computer; the guide works without it.
- Coursera's free audit ended in August 2025 and edX audit access is now time-limited; the learning map lists what is genuinely free.

## 5. Technology

TypeScript, Preact, Vite (pinned, long-established versions); hand-written service worker; IndexedDB;
Web Crypto (AES-GCM, ECDSA P-256, SHA-256); hash-wasm (Argon2id); @noble/post-quantum (ML-DSA);
qrcode and jsQR (with the browser's BarcodeDetector when present); Web Bluetooth (GATT Heart Rate,
Blood Pressure, Health Thermometer, Weight Scale, Pulse Oximeter); DeviceMotion; Geolocation;
Web Speech (read-aloud, voice); Web Share. Tested with Playwright at phone, tablet and desktop widths,
offline, and with axe-core for accessibility.

## 6. Road from prototype to LifeLink

| Phase | What changes |
|---|---|
| 1. Prototype (this) | Demonstrates every module on any device; all data local |
| 2. Pilot app | Native wrapper (Capacitor) for app stores, Health Connect / HealthKit, NFC; real issuers (a PEC issues IDs and certificates using OpenID4VCI); presentations through the browser Digital Credentials API; Civic Credit ledger run by the pilot's council; independent security audit |
| 3. Pilot hardware | The LifeLink Tablet and wearables; secure-element keys; mesh networking |
