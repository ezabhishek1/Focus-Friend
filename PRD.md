# Product Requirements Document (PRD): Focus Friend

**Project Name:** Focus Friend  
**Status:** Hacktoberfest 2026 / Production MVP  
**Target Friend:** "The Overwhelmed Professional" (Alex, a colleague with ADHD/Neurodivergence experiencing task paralysis due to communication overload).  
**Design Aesthetic:** Aesthetic Neo-Brutalism UI  

---

## 1. Executive Summary
**Focus Friend** is a minimalist, local-first executive function assistant that uses local, open-weight AI to distill "walls of text" (emails, Slack threads, Discord pings) into three digestible data points: **Tone, Timeline, and Task.** By running locally, Focus Friend ensures total privacy for sensitive work communications and provides a zero-latency experience to prevent focus-drift.

## 2. Problem Statement
For many people, particularly those with ADHD, a long, unstructured email or a busy chat thread creates "Cognitive Friction." The brain struggles to filter relevant tasks from social fluff or atmospheric noise, leading to **Task Paralysis.** 
* **The Problem with Current Solutions:** Cloud-based AIs (ChatGPT, Claude) require data to be sent to third-party servers, which is a privacy risk for work emails. Furthermore, the UI of these tools is often "chat-heavy," which can lead to further distraction.

## 3. Goals & Objectives
* **Primary Goal:** Reduce the time from "reading a message" to "starting a task."
* **Privacy Goal:** Ensure 0% of the friend’s data leaves their local machine.
* **Accessibility Goal:** Provide a "Calm UI" styled in high-contrast Neo-Brutalism that eliminates cognitive overwhelm.
* **Open Source Goal:** Utilize open-weight models (Phi-3) and local inference engines (Ollama) to demonstrate the power of the open AI ecosystem.

## 4. User Persona: "The Overwhelmed Friend"
* **Name:** Alex (Representing real-world neurodivergent professionals).
* **Context:** Receives 50+ Slack messages a day across multiple channels.
* **Pain Point:** Alex sees a long message, gets anxious about missing a detail, hides the notification, and then forgets the task entirely.
* **Desired Outcome:** A way to "scan" the message without actually having to read the fluff.

## 5. Functional Requirements

### FR1: Local Text Processing
The system accepts raw text input and processes it using a local LLM (Phi-3-mini) via Ollama, with an embedded zero-cloud fallback. It does not require an internet connection to function.

### FR2: The "Signal" Extraction
The AI strictly formats the output into three specific fields:
1. **THE VIBE:** A one-sentence summary of the emotional context (e.g., "The boss is happy but needs this soon" or "Low-priority FYI").
2. **THE DEADLINE:** Any dates or timeframes mentioned.
3. **THE ACTION ITEM:** A single, clear, imperative-verb-starting bullet point.

### FR3: One-Click Interface
Minimalist UI. A single text area for input and high-contrast color-coded cards for the output. No settings mazes, no clutter, zero account creation.

---

## 6. Technical Architecture (The Open-Source Stack)

* **Model:** `Phi-3-mini-4k-instruct` (Open-weights by Microsoft). Chosen for its high reasoning capabilities relative to its tiny 2.3GB footprint.
* **Inference Engine:** `Ollama`. Acts as the local server managing the model weights and API calls.
* **Backend:** FastAPI REST API (`/api/v1/extract`, `/api/v1/health`, `/api/v1/models`, `/api/v1/presets`) with clean service layer separation, threadpool concurrency, and global error handling.
* **Frontend:** Modular vanilla ES modules with centralized reactive store (`frontend/js/state/store.js`), decoupled utilities (`frontend/js/utils/`), and Neo-Brutalist CSS tokens (`frontend/css/`).
* **Design Grammar:** Neo-Brutalism UI (high contrast, bold black borders, hard drop shadows, tactile press states, ADHD-accessible color coding).

---

## 7. User Experience (UX) Flow
1. **Input:** Alex copies a confusing 4-paragraph email and pastes it into Focus Friend.
2. **Action:** Alex clicks "Extract Signal" (or presses Cmd/Ctrl+Enter).
3. **Processing:** A calm, steady breathing progress bar appears.
4. **Output:** The UI presents three color-coded Neo-Brutalist cards:
   * **Cyan (The Vibe):** "Collaborative request for feedback."
   * **Coral (The Deadline):** "End of Day Friday."
   * **Lime (The Action Item):** "Review the attached PDF and list 3 bugs."
5. **Completion:** Alex copies the action item with 1 click, closes the app, task paralysis averted.
