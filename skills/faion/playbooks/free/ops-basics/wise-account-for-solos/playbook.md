---
name: wise-account-for-solos
description: Open a Wise personal multi-currency account, complete KYC, get USD/EUR/GBP routing details, and receive your first ACH payment from a US client.
tier: free
group: ops-basics
status: active
owner: ruslan
last_verified: 2026-05-02
version: 1.0.0
---

## Goal

After this playbook you will have a verified Wise personal account with a USD account number and routing number (ABA), a EUR IBAN, and a GBP sort code — ready to share with a US client so they can pay you via ACH bank transfer. Currency conversion on the receiving end costs ~0.5%.

## Prerequisites

- A valid passport or national ID (for KYC identity verification).
- A proof-of-address document dated within the last 3 months — utility bill, bank statement, or official letter.
- A mobile phone capable of receiving SMS (for 2FA setup).
- A personal email address you control.
- You are not a US resident (Wise personal accounts with ACH receiving work for non-US residents getting paid by US clients).

## Steps

1. Open https://wise.com/register in your browser and click **Sign up with email**.
2. Enter your email address and a strong password (≥12 chars, mix of letters, numbers, symbols), then click **Create account**.
3. Check your inbox for the verification email from `no-reply@wise.com` and click **Verify email**.
4. On the "Tell us about yourself" screen, select **Personal** account type (not Business).
5. Enter your legal name exactly as it appears on your passport, your date of birth, and your country of residence. Click **Continue**.
6. On the "Add your address" screen, enter your full residential address. Wise uses this to assign the correct currency accounts and for KYC. Click **Continue**.
7. On the identity verification screen, select **Passport** as document type. Click **Take a photo** on mobile (or **Upload a file** on desktop) and upload a clear image of the photo page. The name and document number must be fully visible.
8. Upload the proof-of-address document when prompted (utility bill PDF or a bank statement). File must be ≤8 MB and show your name and address.
9. Wise will display "We're verifying your identity" — this takes between 2 minutes and 24 hours. You will receive an email at the address you registered once approved.
10. After approval, log in and navigate to **Home** → **Open a balance**. Select **USD** from the currency list and click **Open balance**. Repeat for **EUR** and **GBP**.
11. Click on the **USD balance** tile. Under "Account details", click **Show account details**. You will see:
    - **Account holder name**: your legal name
    - **ACH routing number** (9 digits, e.g. `026073150` for Wise's US partner bank)
    - **Account number** (10 digits)
    - **Account type**: Checking
12. Copy both numbers. Open your email client and draft a message to your US client with exactly these details:

    ```
    Bank name: Community Federal Savings Bank (Wise's US partner)
    Account holder: <Your Legal Name>
    Account type: Checking
    Routing number (ABA): <9-digit routing number from Wise>
    Account number: <10-digit account number from Wise>
    ```

13. Ask the client to initiate an ACH Credit transfer. ACH transfers typically settle in 1–3 business days.
14. Once the USD funds arrive in your Wise USD balance, go to **Send** → **Convert** and convert to your local currency. Wise charges ~0.5% conversion fee (shown before you confirm).

## Verify

Log in at https://wise.com, navigate to **USD balance** → **Account details**, and confirm that both the routing number and account number fields are populated with numeric values (not placeholder dashes). If they are present, your account is ready to receive ACH transfers.

## Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| "We need more information" after uploading passport | Photo too dark or name partially cut off | Re-upload with the full passport spread flat under good light; crop to show only the photo page |
| "Address document not accepted" | Document older than 3 months or shown as screenshot | Use a PDF export from your bank's online portal dated within 90 days; screenshots are rejected |
| USD account details show only dashes after opening the balance | Wise KYC is still pending (can take up to 24 hours) | Wait for the approval email; account numbers are assigned only after full KYC clearance |
| ACH transfer from client bounced | Client used wrong account type field | Confirm with the client that they selected ACH Credit (push), not ACH Debit; also verify they entered Checking, not Savings |
| Conversion fee higher than 0.5% | You converted at the weekend | Wise charges a small weekend markup (up to 1%) when interbank markets are closed; convert on a weekday during business hours for the lowest rate |

## Next

- Open a Wise Business account if you invoice under a company name — it supports batch payments and accounting integrations.
- Set up a Stripe account to accept card payments from clients who cannot do ACH.
- Track your incoming payments in a simple spreadsheet: date, client name, USD amount received, conversion rate, local-currency amount deposited.

## References

- [knowledge/free/dev/devtools-developer/github-repo-bootstrap](../../../knowledge/free/dev/devtools-developer/github-repo-bootstrap) — the bootstrap pattern of structured account setup steps (create → verify → configure → share credentials) applied here to financial infrastructure instead of code infrastructure.
