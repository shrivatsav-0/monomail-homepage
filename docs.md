# MonoMail — User Guide

> **MonoMail** is an open-source, monochrome email client for Android. No colour accents, no noise — just email. Supports Gmail, Outlook, and any IMAP/SMTP provider.

---

## Table of Contents

1. [What is MonoMail?](#what-is-monomail)
2. [Getting Started](#getting-started)
3. [Your Inbox](#your-inbox)
4. [Reading Emails](#reading-emails)
5. [Composing & Sending](#composing--sending)
6. [Multi-Account](#multi-account)
7. [Search](#search)
8. [Notifications](#notifications)
9. [Attachments](#attachments)
10. [PGP Encryption](#pgp-encryption)
11. [Settings](#settings)
12. [Troubleshooting](#troubleshooting)

---

## What is MonoMail?

MonoMail is a **black-and-white email client** built for focus. Everything is greyscale — no coloured dots, no notification badges, no visual clutter. It supports:

- **Gmail** and **Outlook** via one-tap sign-in
- **Any IMAP/SMTP provider** via manual setup
- Up to **10 accounts** at once
- A **Unified Inbox** that combines all accounts into one feed

**Requirements:** Android 8.0 or later.

**Download:** [GitHub Releases](https://github.com/shrivatsav-0/monomail/releases/latest) or [Google Play Store](https://play.google.com/store/apps/details?id=me.millosaurs.monomail).

---

## Getting Started

### Installing

1. Download the `.apk` from [GitHub Releases](https://github.com/shrivatsav-0/monomail/releases/latest).
2. Open the file. If prompted, enable **"Install unknown apps"** for your browser or file manager.

There are two versions:

| Version | Google Sign-In | Outlook | IMAP/SMTP |
|---|---|---|---|
| **Play Store** | Works | Works | Works |
| **GitHub APK** | Disabled (OAuth pending) | Works | Works |

### First Launch

1. Open MonoMail and swipe through the welcome screen.
2. Tap **Get Started**.
3. Pick your sign-in method:
   - **Google** — uses the Google account on your device.
   - **Microsoft** — opens a browser to sign in with your Microsoft account.
   - **Other (IMAP/SMTP)** — manual server configuration (see [IMAP Setup](#imap-setup)).
4. Grant notification permission when asked (Android 13+).
5. Your inbox loads and syncs automatically.

### Adding More Accounts

- Tap your **avatar** (top-left) → **Add Account**
- Or go to **Settings → Accounts → Add Account**

---

## Your Inbox

### Layout

- **Search bar** (top) — tap to search. Shows a calendar icon when you have scheduled messages.
- **Email list** — scrollable list of threads. Pull down to refresh.
- **Dock bar** (bottom) — navigation tabs in a pill-shaped container.

### Tabs

| Tab | What's in it |
|---|---|
| **Unified** | All accounts combined (enable in Settings → Navigation) |
| **Inbox** | Primary inbox for the active account |
| **Sent** | Messages you've sent |
| **Archived** | Archived threads |
| **Starred** | Starred or flagged threads |
| **Trash** | Deleted threads |
| **Snoozed** | Temporarily hidden threads |
| **Spam** | Spam folder |

### Swiping

Swipe left or right on any thread. Default actions:

| Swipe | Action |
|---|---|
| **Left** | Mark Read/Unread |
| **Right** | Archive |

Customise these in **Settings → Inbox → Swipe Left/Right Action**. Options: Archive, Star, Delete, Mark Read/Unread.

Swipe backgrounds are colour-coded so you know what you're about to do:

- Archive = yellow
- Star = amber
- Delete = red
- Mark Read/Unread = blue-grey

### Long Press

- **Long-press a thread** — contextual actions appear (4 buttons).
- **Long-press an avatar** — enter **bulk select mode** to act on multiple threads at once.

### Bulk Select Mode

- Toggle individual threads with tap.
- **Tap an item body** to select a range from the last toggled item.
- Use **Select All / Deselect All** in the top bar.
- A floating action bar appears with: Archive, Delete, Mark Read, Mark Unread, Star.

### Undo

After archiving, deleting, snoozing, or sending, an **Undo bar** appears at the bottom with a countdown timer. Tap **Undo** to reverse the action. If you don't tap, the action commits when the timer expires.

### Smart Grouping

When enabled (Settings → Inbox), threads from the same sender are auto-collapsed into expandable groups. Group headers show the sender name, message count, and unread badge.

### Scroll Position

Each tab remembers where you left off — switching tabs or going back keeps your scroll position.

---

## Reading Emails

### Conversation View vs Message Chain

Toggle in **Settings → Inbox → Conversation View**.

| Mode | Behaviour |
|---|---|
| **Conversation View** (default) | Only the latest message is expanded. Tap older messages to expand them. |
| **Message Chain** | All messages in the thread are expanded inline as one scrollable list. |

### What You See

Each message shows:

- Sender name and email (with avatar or initial)
- Date (relative: "just now", "5m ago", etc.)
- Blue dot = unread
- To/Cc/Bcc (Cc/Bcc hidden by default — tap "To:" to expand)
- HTML body rendered safely (JavaScript disabled)
- Attachments shown inline

### Thread Actions

| Action | Where |
|---|---|
| Star / Unstar | Top bar star icon |
| Mark read/unread | Overflow menu (three dots) |
| Archive | Overflow menu |
| Delete | Overflow menu |
| Reply | Button at bottom |
| Forward | Button at bottom |

### Quoted Text

If an email has quoted text (e.g., from a reply chain), a **"Show quoted text"** toggle appears below the body. Tap to expand.

### Remote Images

By default, external images in emails are blocked. A **"Show"** banner appears at the top of the email if you want to load them. Toggle this globally in **Settings → Reading → Load Remote Images**.

---

## Composing & Sending

### Opening the Composer

| Action | What happens |
|---|---|
| Tap the **compose button** (bottom-right in inbox) | New email |
| Tap **Reply** in a thread | Reply to sender (or Reply All) |
| Tap **Forward** in a thread | Forward the thread |

### Compose Screen

- **To** — type an email address. Suggestions appear as you type (from your sent/received history).
- **Subject** — optional but recommended.
- **Body** — rich text editor with a formatting toolbar:
  - **Bold** / *Italic* / Underline
  - Bulleted list / Numbered list
  - Block quote
- **Cc/Bcc** — tap to expand.
- **From** — appears if you have multiple send-as addresses configured in Gmail/Outlook.

### Attachments

- Tap the **paperclip icon** in the bottom bar.
- Pick a file from your device.
- Preview cards appear above the toolbar. Tap **X** on any to remove it.

### Schedule Send

1. Tap the **clock icon** in the bottom bar.
2. Pick a date and time.
3. The email is saved and sent automatically at that time.
4. View or cancel scheduled messages: tap the **calendar icon** in the inbox search bar.

### Undo Send

After sending, an undo bar appears with a countdown (default 10 seconds). Tap **Undo** to cancel. Configure the window in **Settings → Compose → Undo Send** (5s, 10s, 20s, or 30s).

### Confirm Before Sending

Enable in **Settings → Compose → Confirm Before Sending**. A dialog pops up before every send.

### Templates

Save frequently-used email bodies as templates. Manage them in **Settings → Compose → Templates**. Tap a template in the compose screen to fill the subject and body (only if they're currently blank).

---

## Multi-Account

### Adding Accounts

Up to 10 accounts. Mix Gmail, Outlook, and IMAP freely.

### Switching Accounts

Three ways:

1. **Tap your avatar** (top-left) → tap an account in the list.
2. **Swipe horizontally** on the avatar to cycle through accounts.
3. **Profile card** — tap your avatar, then tap an account name.

### Unified Inbox

Enable in **Settings → Navigation → Unified Inbox** (requires 2+ accounts). Adds a **Unified** tab that combines all accounts into one feed.

---

## Search

- Tap the **search bar** at the top of the inbox.
- Type to search instantly — results come from your local email cache.
- If nothing is found locally, tap **"Search server for older emails"** to search on the server.

---

## Notifications

### Sync Behaviour

| State | How often it syncs |
|---|---|
| **App visible** | Every ~2 minutes |
| **App backgrounded** | At your configured interval (Settings → Notifications → Sync Frequency) |
| **Just closed** | One quick sync after 1 minute |

**Default sync interval:** 15 minutes. Options: 15 min, 30 min, 1 hour, Manual.

### Push Notifications (Play Store Build Only)

The Play Store build receives push notifications via Firebase Cloud Messaging. The GitHub APK uses polling only (no push).

### Notification Actions

From the notification shade, you can:

- **Reply** — reply directly without opening the app.
- **Archive** — archive the thread.
- **Undo** — after archiving, a follow-up notification lets you undo.

### Per-Account Settings

Each account gets its own notification channel on Android 8+. Configure sound and vibration per account in your device's notification settings.

---

## Attachments

### Viewing

- **Images** — inline thumbnails (tap to open full-screen with pinch-to-zoom).
- **PDFs** — tap to open in the built-in PDF viewer.
- **Videos** — tap to play with built-in video player.
- **Other files** — tap to open with an external app.

### Sending

Tap the **paperclip icon** in the compose screen → pick a file → it's attached.

---

## PGP Encryption

PGP (Pretty Good Privacy) encrypts your emails so only the intended recipient can read them.

### Setting Up PGP

1. Go to **Settings → PGP Keys**.
2. **Generate** a new key pair, or **Import** an existing one.
3. Optionally protect your key with a passphrase.

### Encrypting an Email

1. Import or generate a PGP key pair.
2. Import the recipient's **public key**.
3. In the compose screen, tap the **lock icon** to enable encryption.
4. Optionally tap the **pen icon** to also sign the message.
5. Send normally.

### Receiving Encrypted Email

- Encrypted emails are detected and decrypted automatically if you have the private key.
- A **green lock badge** appears if decryption succeeded.
- A **signature badge** shows whether the sender's signature is valid.

### Exporting Your Public Key

1. Go to **Settings → PGP Keys**.
2. Tap **Export** next to your key.
3. The key is shown — tap **Copy** to share it with your contacts.

---

## Settings

Settings is organised into categories. Tap **your avatar → Settings** to access.

### Appearance

| Setting | What it does | Default |
|---|---|---|
| Theme | Light, Dark, or System | System |
| Font Size | Extra Small to Extra Large | Default |
| Show Dividers | Lines between inbox items | Off |
| Compact List | Reduced spacing in inbox | Off |
| Show Snippet Preview | Preview text below sender name | On |
| Load Remote Images | Block external images in emails | On (blocked) |
| Render Markdown | Show markdown formatting in plain text emails | Off |

### Inbox

| Setting | What it does | Default |
|---|---|---|
| Conversation View | Collapsible threads (off = expanded chain) | On |
| Smart Grouping | Auto-group threads by sender | On |
| Group Recent Only | Group within 24h (on) or 3 days (off) | On |
| Swipe Left Action | Archive / Star / Delete / Mark Read/Unread | Mark Read/Unread |
| Swipe Right Action | Archive / Star / Delete / Mark Read/Unread | Archive |

### Compose

| Setting | What it does | Default |
|---|---|---|
| Default Reply | Reply or Reply All | Reply |
| Confirm Before Sending | Dialog before send | Off |
| Undo Send | Show undo bar after sending | On |
| Undo Send Window | Countdown: 5s, 10s, 20s, or 30s | 10s |
| Templates | Manage saved email bodies | — |

### Navigation

| Setting | What it does | Default |
|---|---|---|
| Unified Inbox | Combine all accounts in one tab | Off |
| Nav Size | Scale dock bar icons (0.6x–1.4x) | 1.0x |
| Dock Bar Editor | Reorder, add, or remove tabs | Inbox, Sent, Archived |

### Notifications

| Setting | What it does | Default |
|---|---|---|
| Email Notifications | Master toggle | On |
| Sync Frequency | Background polling interval | 15 min |

### Accounts

- View all signed-in accounts.
- Re-authenticate when tokens expire.
- Add or remove accounts.
- Sign out individually or all at once.

---

## Troubleshooting

### "This app is blocked" on Google sign-in

The Gmail API is limited to 100 test users during OAuth verification. Solutions:

1. Build from source with your own Google Cloud project.
2. Use Outlook or IMAP/SMTP instead.

### "No Google account found"

Make sure you have a Google account added on your device: **Settings → Accounts → Add account → Google**. Then restart MonoMail.

### Microsoft sign-in fails

- Ensure you have a Microsoft account.
- Make sure you have a web browser installed (MSAL opens a browser for auth).
- Try restarting the sign-in flow.

### Notifications aren't working

1. Check **Settings → Notifications → Email Notifications** is on.
2. On Android 13+, check **POST_NOTIFICATIONS** permission is granted.
3. If using the GitHub APK, push is disabled — you need polling (set Sync Frequency to 15 min or 30 min, not Manual).

### Can't connect to IMAP/SMTP

1. Double-check host and port numbers.
2. Check SSL/TLS settings:
   - IMAP: usually port 993 (SSL) or 143 (STARTTLS)
   - SMTP: usually port 465 (SSL) or 587 (STARTTLS)
3. Use the **connection test** before saving.
4. For Gmail with 2FA, you need an **app password** (not your regular password).

### Where are scheduled messages?

Tap the **calendar icon** in the inbox search bar.

### Why does the GitHub APK differ from the Play Store version?

The GitHub APK excludes the developer's Google OAuth credentials (for security) and has no push notifications. Outlook and IMAP work identically in both.

### App feels slow

- Disable **Smart Grouping** (Settings → Inbox).
- Use fewer accounts (performance warning appears at 4+ accounts).

---

## Support

- **Website:** [monomail.millosaurs.me](https://monomail.millosaurs.me)
- **GitHub:** [github.com/shrivatsav-0/monomail](https://github.com/shrivatsav-0/monomail)
- **Discord:** [discord.gg/monomail](https://discord.gg/monomail)
- **Report issues:** [GitHub Issues](https://github.com/shrivatsav-0/monomail/issues)

### Donate

- **Ko-fi:** [ko-fi.com/N4N2W53M5](https://ko-fi.com/N4N2W53M5)
- **UPI / Crypto:** Available in-app under Support.
