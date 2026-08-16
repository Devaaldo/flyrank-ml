# 🌐 DNS & Infrastructure Walkthrough: Connecting Your Personal Domain

**Assignment:** PF-04 — Personal Website Live on the FlyRank Domain  
**Track:** General AI Fluency | **Phase:** Build (Core)  
**Author:** Muhammad Akbar Pradana (Machine Learning Intern @ FlyRank AI)  
**Live Target Host:** `akbarprdna.my.id` / `akbarpradana.netlify.app`  
**Provisioned Subdomain:** `akbar.flyrank.ai`  

---

## 1. Executive Summary
This document explains the technical architecture of the **Domain Name System (DNS)**, the role of **CNAME (Canonical Name)** alias records, and the step-by-step resolution lifecycle that occurs when a user visits a custom FlyRank subdomain. It is written to be accessible to both technical and non-technical stakeholders.

---

## 2. What is a CNAME Record?

A **CNAME (Canonical Name) Record** is an alias record in the DNS system that maps one domain name to another domain name, rather than mapping directly to a numerical IP address.

### Real-World Analogy:
Think of an **A Record** like a physical street address (`123 AI Boulevard, Server Room 4`). A **CNAME Record** is like an alias or nickname: *"The Akbar Portfolio"* $\to$ points to *"The Main Hosting Server"*. 

When our capstone is approved, FlyRank creates a CNAME record:
```text
Host / Subdomain : akbar.flyrank.ai
Record Type      : CNAME
Points To / Value: akbarprdna.my.id (or akbarpradana.netlify.app)
TTL (Time To Live): 3600 seconds (1 hour)
```

### Why a CNAME is Powerful:
When the host server updates its underlying infrastructure or changes its IP address, we don't have to reconfigure FlyRank's DNS records. The CNAME alias dynamically follows the host destination.

---

## 3. What Actually Happens When Someone Types Your URL?

When a recruiter, engineer, or client opens their browser and types `https://akbar.flyrank.ai`, an automated 4-step resolution journey happens in milliseconds:

```text
[1. User Types URL] ───► [2. Recursive Resolver (ISP/Cloudflare)]
                                    │
                                    ├──► Asks Root Server (".")
                                    │      └─► "Go to .ai TLD server"
                                    │
                                    ├──► Asks TLD Server (".ai")
                                    │      └─► "Go to FlyRank's Authoritative DNS"
                                    │
                                    └──► Asks Authoritative Nameserver (FlyRank)
                                           └─► "akbar.flyrank.ai is CNAME for host server"
                                                    │
[4. Secure HTTPS Connection 🔒] ◄────────────────────┘ (3. Resolves IP & Fetches Web Page)
```

### Step 1: Querying the Recursive Resolver (The Detective)
The user's computer checks its local operating system cache. If the IP address isn't cached, it queries a **Recursive DNS Resolver** (provided by the local ISP or public resolvers like Google `8.8.8.8` or Cloudflare `1.1.1.1`).

### Step 2: The Hierarchical Search Chain
The Resolver navigates the global DNS hierarchy:
1. **Root Nameservers (`.`):** Directs the resolver to the Top-Level Domain (TLD) server responsible for `.ai`.
2. **TLD Nameservers (`.ai`):** Directs the resolver to FlyRank's authoritative nameservers (e.g., Cloudflare DNS).
3. **Authoritative Nameserver (FlyRank DNS):** Holds the master zone file for `flyrank.ai`. It checks the records and returns:  
   `akbar.flyrank.ai CNAME akbarprdna.my.id`.

### Step 3: Final Host Resolution
The resolver resolves the destination host domain to its final edge server IP address (e.g., CDN / Netlify / Vercel Edge Server) and hands it back to the user's browser.

### Step 4: The HTTPS / TLS Handshake & Padlock
The browser initiates a secure **TLS Handshake** over port 443 with the host server:
- Cryptographic certificates are validated (ensuring the site is authentic and encrypted).
- The browser displays the secure padlock icon (`🔒 https://`).
- The server serves the HTML, CSS, JavaScript, and portfolio assets.

---

## 4. Capstone Subdomain Deployment Checklist

When the capstone project is approved and the `akbar.flyrank.ai` subdomain is provisioned by FlyRank Ops, the deployment checklist is:

- [x] **Step 1:** Verify personal site is live and loading cleanly over HTTPS on custom domain / free host (`akbarprdna.my.id` / `akbarpradana.netlify.app`).
- [x] **Step 2:** Ensure essential positioning, CV link, GitHub repository, LinkedIn profile, and contact booking link are fully functional.
- [ ] **Step 3 (Capstone Day):** FlyRank Ops adds DNS record: `CNAME akbar -> host.domain`.
- [ ] **Step 4 (Capstone Day):** Add `akbar.flyrank.ai` as Custom Domain in host settings.
- [ ] **Step 5 (Capstone Day):** Allow DNS propagation (typically 2–15 minutes) and verify automated SSL certificate issuance (confirm padlock in private incognito window).
