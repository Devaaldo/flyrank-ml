# ⚡ Make It Do Something: Dynamic Contact & Ingestion Feature

**Assignment:** Week 6 — Make It Do Something  
**Track:** General AI Fluency | **Phase:** Submit  
**Author:** Muhammad Akbar Pradana (Machine Learning Intern @ FlyRank AI)  
**Live Target System:** `https://akbarprdna.my.id` / `akbarpradana.netlify.app`  

---

## 1. Feature Selection & Purpose
A static portfolio operates merely as a digital poster. To transform the portfolio into an active, functional tool, I implemented a **Serverless Contact & Project Collaboration Pipeline** operating on a zero-cost tier (Formspree / Netlify Forms API). This enables hiring managers, recruiters, and collaborators to submit direct inquiries that trigger automated real-time email routing to my primary inbox with zero server maintenance overhead.

---

## 2. Plain-Words Explanation: What is a Backend?
In web architecture, the **Frontend** is what the user sees and interacts with in their web browser (the visual layout, text, buttons, and input fields built with HTML, CSS, and JavaScript). 

The **Backend** is the invisible engine running on a remote cloud server that performs the heavy lifting the browser cannot or should not do alone:
- Securely handling credentials and API keys away from public inspection.
- Validating and sanitizing user inputs to prevent malicious attacks or spam.
- Interfacing with third-party networks (e.g., Simple Mail Transfer Protocol [SMTP] servers or relational databases) to permanently record and dispatch data.

---

## 3. End-to-End Data Flow Architecture

The data lifecycle follows a 5-step asynchronous request-response cycle:

```text
[1. User Input in Browser] 
          │
          ▼ (User clicks "Send Inquiry")
[2. HTTP POST Request (JSON Payload)]
          │
          ▼
[3. Serverless Backend Endpoint (Formspree/Netlify Gateway)]
          │
          ├──► (Sanitizes input, verifies anti-spam honeypot)
          │
          ├──► [4. Dispatches SMTP Payload -> Inbox Delivery (akbar@domain)]
          │
          ▼
[5. HTTP 200 Response -> Frontend Renders "Message Sent Successfully!"]
```

### Step 1: Input Capture
The user enters their name, email address, inquiry topic, and message into the client-side HTML `<form>`.

### Step 2: Asynchronous Dispatch
Upon form submission, JavaScript intercepts the event, serializes the form fields into an `application/json` payload, and dispatches an asynchronous `HTTP POST` request to the backend API endpoint.

### Step 3: Serverless Ingestion & Sanitization
The cloud backend receives the POST request, validates email syntax, checks for rate-limiting abuses, and verifies that the hidden anti-bot honeypot field is untouched.

### Step 4: Downstream Notification
Upon successful validation, the backend triggers an automated SMTP dispatch that forwards the message directly to my primary email inbox within seconds.

### Step 5: State Confirmation & Feedback
The backend returns an `HTTP 200 OK` status code. The frontend catches this response and updates the UI to display a clear success confirmation banner while resetting the input fields.

---

## 4. Verification & Testing Proof
- **End-to-End Test Run:** Dispatched live test payload `{"name": "Recruiter Test", "email": "test@flyrank.ai", "message": "Verification test for Week 6 FL submission"}`.
- **Delivery Confirmation:** Successfully received formatted email alert with correct timestamp, client headers, and sender details.
- **Resilience:** Gracefully handles invalid email formats and network disconnections with friendly error messages.
