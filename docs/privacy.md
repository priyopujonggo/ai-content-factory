# Privacy Policy

**AI Content Factory**
Last updated: March 29, 2026

## 1. Introduction

This Privacy Policy explains how AI Content Factory ("we", "us", or "the Service") collects, uses, and protects information when you use our Service. We are committed to protecting your privacy and handling your data responsibly.

## 2. Information We Collect

### 2.1 Information You Provide
- **Account credentials** — OAuth tokens from connected social media platforms (TikTok, Instagram, YouTube, Twitter/X)
- **Content** — Video URLs and files you submit for processing
- **Preferences** — Settings and configurations you specify

### 2.2 Information Collected Automatically
- **Job data** — Processing logs, job status, and pipeline results
- **Clip metadata** — Timestamps, viral scores, and generated captions
- **Usage data** — API requests and error logs for debugging purposes

### 2.3 Information from Third-Party Platforms
When you connect a social media account, we receive:
- Basic profile information (username, account ID)
- OAuth access tokens required to post content on your behalf

## 3. How We Use Your Information

We use collected information to:
- Process video content and generate short-form clips
- Post content to your connected social media accounts on your behalf
- Store job history and results for your reference
- Improve the Service and debug issues

## 4. Data Storage

- All data is stored locally on your own infrastructure
- OAuth tokens are stored securely in your configured database
- Video files are stored temporarily during processing and saved to your configured storage
- We do not store your data on external servers beyond what is necessary for the Service to function

## 5. Third-Party Services

The Service integrates with the following third-party platforms:
- **TikTok** — [TikTok Privacy Policy](https://www.tiktok.com/legal/privacy-policy)
- **Instagram / Meta** — [Meta Privacy Policy](https://www.facebook.com/privacy/policy)
- **YouTube / Google** — [Google Privacy Policy](https://policies.google.com/privacy)
- **Twitter / X** — [X Privacy Policy](https://twitter.com/en/privacy)

We also use:
- **Groq API** — for AI transcript analysis (transcript data is sent to Groq's servers)
- **OpenAI Whisper** — runs locally on your machine, no data sent externally

## 6. Data Sharing

We do not sell, trade, or share your personal information with third parties except:
- As required to operate connected platform integrations
- As required by law or legal process
- With your explicit consent

## 7. OAuth Tokens and Platform Access

- We store OAuth tokens solely to enable automated posting on your behalf
- You can revoke access at any time by disconnecting the app from your social media account settings
- Revoking access will prevent the Service from posting to that platform

## 8. Data Retention

- Job history and clip metadata are retained until you delete them
- OAuth tokens are retained until you disconnect the platform or delete your data
- Temporary video files are deleted after processing is complete

## 9. Security

We implement reasonable security measures to protect your data including:
- Encrypted storage of OAuth tokens
- Secure database connections
- Environment variable-based secrets management

## 10. Your Rights

You have the right to:
- Access the data we hold about you
- Delete your data at any time
- Revoke platform access at any time
- Export your job history and clip data

## 11. Changes to This Policy

We may update this Privacy Policy from time to time. We will notify you of significant changes by updating the date at the top of this document.

## 12. Contact

For privacy-related questions or requests, please contact us through the repository's issue tracker.
