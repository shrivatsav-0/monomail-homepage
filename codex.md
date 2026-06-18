# Monomail — Codebase Documentation

> **Monomail** is an open-source, monochrome (black-and-white) email client for Android built with Jetpack Compose and Material 3 Expressive. It connects to **Gmail** and **Microsoft Outlook** via OAuth, follows an offline-first architecture with an encrypted Room database, and syncs in the background via WorkManager.

## Table of Contents

- [Tech Stack](#tech-stack)
- [Architecture Overview](#architecture-overview)
- [Project Structure](#project-structure)
- [Build Configuration](#build-configuration)
- [Authentication Layer](#authentication-layer)
- [Security Layer](#security-layer)
- [Data Layer](#data-layer)
  - [Domain Models](#domain-models)
  - [Remote API (Retrofit)](#remote-api-retrofit)
  - [Email Providers](#email-providers)
  - [Local Database (Room + SQLCipher)](#local-database-room--sqlcipher)
  - [Mapper](#mapper)
  - [Repository](#repository)
  - [Settings (DataStore)](#settings-datastore)
- [Background Workers](#background-workers)
- [Navigation](#navigation)
- [UI Layer](#ui-layer)
  - [Theme](#theme)
  - [Shared Components](#shared-components)
  - [Sign-In Screen](#sign-in-screen)
  - [Inbox Screen](#inbox-screen)
  - [Email Detail Screen](#email-detail-screen)
  - [Compose Screen](#compose-screen)
  - [Settings Screen](#settings-screen)
  - [Legal Screen](#legal-screen)
- [State Management Patterns](#state-management-patterns)
- [Animation Reference](#animation-reference)
- [Key Implementation Details](#key-implementation-details)
- [Data Flow](#data-flow)

---

## Tech Stack

| Category | Library / Tool | Version |
|---|---|---|
| **Language** | Kotlin | 2.2.10 |
| **UI** | Jetpack Compose (BOM) | 2026.02.01 |
| | Material 3 Expressive | 1.5.0-alpha21 |
| **Navigation** | Navigation Compose | 2.9.0 |
| **Database** | Room + SQLCipher | 2.7.1 / 4.6.1 |
| **Networking** | Retrofit 2 + OkHttp 4 | 2.11.0 / 4.12.0 |
| **Auth (Gmail)** | Credential Manager + GoogleAuthUtil | 1.5.0 |
| **Auth (Outlook)** | MSAL | 5.4.0 |
| **Background** | WorkManager | 2.10.1 |
| **Images** | Coil Compose | 2.7.0 |
| **Settings** | DataStore Preferences | 1.1.1 |
| **Encryption** | AndroidX Security Crypto | 1.1.0 |
| **Markdown** | Markwon | 4.6.2 |
| **Build** | Android Gradle Plugin | 9.2.1 |
| | KSP | 2.2.10-2.0.2 |
| **Target** | minSdk 26, targetSdk 35, compileSdk 37 | |

---

## Architecture Overview

The app follows an **MVVM + Repository** pattern without any DI framework — all dependencies are wired manually via the `Application` class acting as a service locator.

```
┌─────────────────┐     ┌──────────────────────┐     ┌────────────────┐
│   Compose UI     │────▶│    ViewModels        │────▶│  EmailRepository │
│  (Screens/Comps) │◀────│  (StateFlow)         │◀────│  (Data Hub)     │
└─────────────────┘     └──────────────────────┘     └───────┬────────┘
                                                             │
                        ┌────────────────────────────────────┼────────────────────┐
                        ▼                                    ▼                    ▼
               ┌──────────────┐                  ┌──────────────────┐   ┌────────────────┐
               │  Room +      │                  │  EmailProvider   │   │ SettingsDataStore│
               │  SQLCipher   │                  │  (Interface)     │   │ (DataStore)    │
               │  (Local)     │                  │  ┌────────────┐  │   └────────────────┘
               └──────────────┘                  │  │GmailProvdr│  │
                                                 │  ├──────────┤  │
                                                 │  │OutlookPrv│  │
                                                 │  └────────────┘  │
                                                 └──────────────────┘
                                                           │
                                                           ▼
                                                 ┌──────────────────┐
                                                 │  Retrofit + OkHttp│
                                                 │  (Gmail/Graph API)│
                                                 └──────────────────┘
```

**Read path:** UI observes `Flow` from Room via Repository. Room is the single source of truth.

**Write path (optimistic):** Repository mutates Room first, then enqueues a `SyncWorker` via WorkManager to propagate to the server. If the user is offline, the server change happens when connectivity returns.

**Refresh path:** `EmailRepository.refreshInbox()` fetches from the remote provider, maps to domain entities, and inserts into Room — which triggers reactive UI updates.

---

## Project Structure

```
com.shrivatsav.monomail/
├── MonoMailApp.kt                          # Application class (service locator)
├── MainActivity.kt                         # Single-activity entry point
│
├── auth/
│   ├── AccountManager.kt                   # Persistent account storage (encrypted DataStore)
│   ├── AuthManager.kt                      # Auth orchestrator (Google + MSAL)
│   ├── MicrosoftAuthManager.kt             # MSAL-based Outlook auth
│   └── UserProfile.kt                      # User account data class
│
├── security/
│   └── SecurityUtil.kt                     # AES/GCM encryption, DB passphrase
│
├── data/
│   ├── local/
│   │   ├── AppDatabase.kt                 # Room database (SQLCipher, version 4)
│   │   ├── Entities.kt                    # ThreadEntity, EmailEntity + mappers
│   │   ├── Converters.kt                  # List<String> <-> JSON
│   │   ├── ThreadDao.kt                   # Thread CRUD queries
│   │   └── EmailDao.kt                    # Email CRUD queries
│   │
│   ├── mapper/
│   │   └── EmailMapper.kt                # GmailMessage -> Email / EmailThread
│   │
│   ├── model/
│   │   ├── Email.kt                       # Domain model: Email + EmailAttachmentInfo
│   │   ├── EmailThread.kt                 # Domain model: EmailThread
│   │   └── EmailAttachment.kt             # Uri-based attachment for compose
│   │
│   ├── provider/
│   │   ├── EmailProvider.kt               # Interface + EmailFolder enum
│   │   ├── ProviderModels.kt              # ProviderThread, ProviderMessage, ...
│   │   ├── GmailProvider.kt               # Gmail API implementation
│   │   └── OutlookProvider.kt             # Microsoft Graph implementation
│   │
│   ├── remote/
│   │   ├── RetrofitClient.kt              # OkHttp/Retrofit setup + auth interceptor
│   │   ├── GmailApi.kt                    # Gmail v1 Retrofit interface
│   │   ├── GmailModels.kt                 # Gmail API DTOs
│   │   └── OutlookApi.kt                  # Microsoft Graph Retrofit interface + DTOs
│   │
│   ├── repository/
│   │   ├── EmailRepository.kt             # Central data orchestrator (optimistic writes)
│   │   └── ContactSuggestionProvider.kt   # In-memory contact index for autocomplete
│   │
│   ├── settings/
│   │   └── SettingsDataStore.kt           # User preferences via DataStore
│   │
│   └── worker/
│       └── SyncWorker.kt                  # One-shot sync for individual actions
│
├── worker/
│   └── EmailSyncWorker.kt                 # Periodic background sync + notifications
│
└── ui/
    ├── components/
    │   └── BlurredModalOverlay.kt         # Reusable animated modal overlay
    ├── navigation/
    │   └── NavGraph.kt                    # All routes + ViewModel wiring
    ├── screens/
    │   ├── auth/
    │   │   ├── SignInScreen.kt            # Sign-in UI (Google/MS provider selection)
    │   │   └── SignInViewModel.kt         # Sign-in state machine
    │   ├── inbox/
    │   │   ├── InboxScreen.kt             # Main inbox (~1850 lines)
    │   │   ├── InboxViewModel.kt          # Inbox state, polling, undo, pagination
    │   │   ├── InboxDisplayItem.kt        # Display item hierarchy + grouping logic
    │   │   └── EmailItem.kt              # Individual thread row composable
    │   ├── detail/
    │   │   ├── EmailDetailScreen.kt       # Thread/conversation view with WebView
    │   │   └── EmailDetailViewModel.kt    # Thread loading, star, archive
    │   ├── compose/
    │   │   ├── ComposeScreen.kt           # Email compose with attachments
    │   │   └── ComposeViewModel.kt        # Compose state, send, suggestions
    │   └── settings/
    │       ├── SettingsScreen.kt          # Full settings with sections
    │       ├── SettingsViewModel.kt       # Settings + GitHub update check
    │       └── LegalScreen.kt            # Markdown-rendered legal docs
    └── theme/
        ├── Color.kt                       # Monochrome color palette
        ├── FontFamilies.kt                # Google Sans Flex variable font
        ├── shape.kt                       # Rounded corner shapes
        ├── Theme.kt                       # MonoMailTheme composable
        └── Type.kt                        # Full Material 3 Typography
```

---

## Build Configuration

### App `build.gradle.kts` (key details)

```kotlin
android {
    namespace = "com.shrivatsav.monomail"
    compileSdk = 37
    defaultConfig {
        applicationId = "com.shrivatsav.monomail"
        minSdk = 26
        targetSdk = 35
        versionCode = 10
        versionName = "1.3.2"
    }
    buildFeatures { compose = true; buildConfig = true }
    composeCompiler { enableStrongSkippingMode = true }
}
```

**Key plugins:** `kotlin.compose`, `ksp` (for Room annotation processing).

**Signing:** Release builds signed with a project-specific keystore (`monomail-release.keystore`, gitignored). Keystore passwords in `keystore.properties` (gitignored).

**Minification:** R8 enabled for release builds (`isMinifyEnabled = true`). ProGuard rules in `app/proguard-rules.pro`.

**Known R8 issues & fixes (v1.3.2):**
- Gson serialization of `UserProfile` and data model classes requires explicit `-keep` rules for their fields; the broad `-keepclassmembers class com.shrivatsav.monomail.** { <fields>; }` covers most cases but explicit `-keep` for `data.remote.*`, `data.model.*`, `data.provider.*`, and `data.local.*` packages was added to prevent field renaming.
- All Gmail API DTOs (`GmailModels.kt`) have `@SerializedName` annotations so Gson deserialization works regardless of R8 obfuscation.

**Notable:** Secrets stored in `secrets.properties` (gitignored) for `GOOGLE_CLIENT_ID` build config field.

### AndroidManifest

- **Permissions:** `INTERNET`, `POST_NOTIFICATIONS`
- **Application:** `MonoMailApp`, backup disabled, transparent status/nav bar theme
- **Activities:** `MainActivity` (launcher, `adjustResize`), `BrowserTabActivity` (MSAL redirect)
- **Provider:** `FileProvider` for attachment cache access

---

## Authentication Layer

### UserProfile (`auth/UserProfile.kt`)

```kotlin
data class UserProfile(
    val id: String,           // e.g. "gmail_user@gmail.com" or "outlook_user@outlook.com"
    val displayName: String,
    val email: String,
    val photoUrl: String?,
    val accessToken: String,
    val provider: String,      // "gmail" or "outlook"
    val refreshToken: String   // currently empty
)
```

### AuthManager (`auth/AuthManager.kt`)

Orchestrates all sign-in flows.

**Google sign-in flow:**
1. Uses Android Credential Manager with `GetGoogleIdOption` to get Google ID token
2. Exchanges ID token for Gmail OAuth2 access token via `GoogleAuthUtil.getToken()`
3. Validates token by hitting `gmail.googleapis.com/gmail/v1/users/me/profile`
4. Creates `UserProfile(provider = "gmail")`, stores via `AccountManager.addAccount()`

**Microsoft sign-in flow:**
1. Delegates to `MicrosoftAuthManager` (MSAL library)
2. Acquires token with scopes: `User.Read`, `Mail.Read`, `Mail.ReadWrite`, `Mail.Send`
3. Creates `UserProfile(provider = "outlook")`

**Token management:** On 401 responses, the Retrofit interceptor calls a token refresher lambda that uses `GoogleAuthUtil.getToken()` (Gmail) or `MicrosoftAuthManager.getAccessTokenSilently()` (Outlook) to get a fresh token, then updates the stored profile.

**TYPE_NO_CREDENTIAL handling:** When Credential Manager throws `GetCredentialException.TYPE_NO_CREDENTIAL`, AuthManager returns a user-friendly error message suggesting the user add a Google account in Settings or register the app's SHA-1 fingerprint in Google Cloud Console.

### AccountManager (`auth/AccountManager.kt`)

Stores encrypted JSON list of accounts in DataStore. Provides reactive flows:
- `accountsFlow: Flow<List<UserProfile>>`
- `activeAccountFlow: Flow<UserProfile?>`

Supports up to 10 accounts. Account data encrypted via `SecurityUtil.encryptString()`/`decryptString()`.

### MicrosoftAuthManager (`auth/MicrosoftAuthManager.kt`)

Bridges MSAL's callback-based API into coroutines via `suspendCancellableCoroutine`. MSAL config in `res/raw/msal_config.json` (client ID `9f61613a-...`, multi-account mode).

---

## Security Layer

### SecurityUtil (`security/SecurityUtil.kt`)

- **Database passphrase:** 32-byte random Base64 string stored in `EncryptedSharedPreferences`, used to encrypt the SQLCipher Room database.
- **AES/GCM encryption:** `encryptString(data)`, `decryptString(encryptedBase64)` — uses Android KeyStore-backed AES-256 key with 12-byte random IV prepended.

---

## Data Layer

### Domain Models

| Class | File | Key Fields |
|-------|------|------------|
| `Email` | `data/model/Email.kt` | `id, threadId, subject, from, fromEmail, to, snippet, body, date, isRead, isStarred, labels, attachments` |
| `EmailThread` | `data/model/EmailThread.kt` | `threadId, subject, from, fromEmail, snippet, date, messageCount, isRead, isStarred, latestMessageId, participants` |
| `EmailAttachmentInfo` | `data/model/Email.kt` | `id, messageId, mimeType, name, size` |
| `EmailAttachment` | `data/model/EmailAttachment.kt` | `uri, name, size, mimeType` (for compose) |

### Remote API (Retrofit)

#### RetrofitClient (`data/remote/RetrofitClient.kt`)

Creates two Retrofit instances:
- **Gmail:** `https://gmail.googleapis.com/gmail/v1/`
- **Outlook:** `https://graph.microsoft.com/v1.0/`

Features an auth interceptor that:
1. Adds `Authorization: Bearer <token>` header
2. On 401, calls `tokenRefresher()`, retries request once

HTTP logging level is set to `HEADERS` (not `NONE`) in all builds for debugging; request/response bodies are not logged.

#### Gmail API (`data/remote/GmailApi.kt`)

Endpoints: `listMessages`, `getMessage`, `getAttachment`, `getProfile`, `batchModifyMessages`, `sendMessage`, `listThreads`, `getThread`, `modifyThread`, `trashThread`, `untrashThread`.

**GmailModels.kt** contains all Gmail API DTOs (`GmailMessage`, `MessagePart`, `ThreadListResponse`, `ThreadRef`, `GmailThread`, etc.). Every field has a `@SerializedName` annotation matching the JSON key to prevent R8 obfuscation from breaking Gson deserialization.

#### Outlook API (`data/remote/OutlookApi.kt`)

Endpoints: `listMessages`, `getMessage`, `getAttachments`, `getAttachment`, `updateMessage`, `moveMessage`, `deleteMessage`, `sendMail`. All DTOs in the same file.

### Email Providers

#### EmailProvider interface (`data/provider/EmailProvider.kt`)

```kotlin
interface EmailProvider {
    val providerName: String
    suspend fun listThreads(folder: EmailFolder, maxResults: Int, pageToken: String?, query: String?): ProviderThreadListResult
    suspend fun getThread(threadId: String): ProviderThread
    suspend fun getAttachmentBytes(messageId: String, attachmentId: String): ByteArray?
    suspend fun archiveThread(threadId: String)
    suspend fun unarchiveThread(threadId: String)
    suspend fun trashThread(threadId: String)
    suspend fun restoreThread(threadId: String)
    suspend fun toggleStar(threadId: String, starred: Boolean)
    suspend fun markRead(threadId: String, read: Boolean)
    suspend fun batchMarkRead(messageIds: List<String>)
    suspend fun sendEmail(from: String, to: String, subject: String, body: String, threadId: String?, attachments: List<EmailAttachment>)
}
```

#### GmailProvider (`data/provider/GmailProvider.kt`)

- Maps `EmailFolder` to Gmail label IDs. ARCHIVE = `-label:inbox -label:trash -label:sent`.
- Fetches threads in parallel via `coroutineScope { async { ... }.awaitAll() }`.
- `sendEmail()` builds raw RFC2822 MIME message manually (multipart/mixed for attachments), Base64URL-encodes, sends via Gmail API.
- Delegate to `EmailMapper` for DTO -> domain conversion.

#### OutlookProvider (`data/provider/OutlookProvider.kt`)

- Groups messages by `conversationId` to form threads.
- STARRED emulated via `"Yellow category"` string in `categories` field.
- `sendEmail()` enforces 3MB attachment limit.

### Local Database (Room + SQLCipher)

#### AppDatabase (`data/local/AppDatabase.kt`)

- Room database singleton encrypted with SQLCipher via `SupportOpenHelperFactory`.
- Passphrase from `SecurityUtil.getDatabasePassphrase()`.
- Version 4, migration 2→3 adds `accountId` columns.
- Tables: `threads`, `emails`.

#### Entities (`data/local/Entities.kt`)

**ThreadEntity** (`threads` table):
```kotlin
@PrimaryKey val threadId: String
val accountId: String
// ... subject, fromName, fromEmail, snippet, date, messageCount,
//     isRead, isStarred, latestMessageId, participants: List<String>,
//     inInbox, inSent, inArchived, inTrash: Boolean
```

**EmailEntity** (`emails` table):
```kotlin
@PrimaryKey val id: String
val accountId: String
// ... threadId, subject, fromName, fromEmail, toEmail, snippet, body,
//     date, isRead, isStarred, labels: List<String>,
//     attachmentsJson: String (JSON serialized),
//     inInbox, inSent, inArchived, inTrash: Boolean
```

Folder membership is tracked via boolean columns (`inInbox`, `inSent`, `inArchived`, `inTrash`) rather than tag/label tables.

#### ThreadDao (`data/local/ThreadDao.kt`)

Folder queries: `getInboxThreads`, `getAllInboxThreads`, `getSentThreads`, `getArchivedThreads`, `getStarredThreads`, `getTrashThreads`. All return `Flow<List<ThreadEntity>>`. Also provides `getLatestInboxThread(accountId)` for notification diffing. Mutation methods: `insertThreads`, `updateThreadStarred`, `archiveThread`, `unarchiveThread`, `updateThreadReadStatus`, `moveToTrash`, `restoreFromTrash`, `deleteThread`, `emptyTrash`, `clearForAccount`.

#### EmailDao (`data/local/EmailDao.kt`)

Folder queries mirror ThreadDao. Additional queries: `getEmailsForThread(threadId, accountId)` (ASC by date), `getEmailById`. Mutation methods mirror ThreadDao pattern.

#### Converters (`data/local/Converters.kt`)

`List<String>` ↔ JSON via Gson (for `participants` and `labels` fields).

### Mapper (`data/mapper/EmailMapper.kt`)

Object with extension functions converting Gmail API DTOs to domain models:
- `GmailMessage.toEmail()` — extracts Subject/From/To from MIME headers, parses `"Name <email>"` format, decodes HTML body with inline image CID injection, extracts attachments
- `GmailThread.toEmailThread()` — finds latest message, derives isRead/isStarred, collects participants
- `GmailThread.toEmailList()` — sorts messages by date, maps each to Email

### Repository (`data/repository/EmailRepository.kt`)

The central orchestrator implementing the optimistic UI pattern:

```kotlin
class EmailRepository(
    private val providerFactory: (UserProfile) -> EmailProvider,
    private val database: AppDatabase,
    private val context: Context,
    private val accountManager: AccountManager
)
```

**Key behaviors:**

| Method | Description |
|--------|-------------|
| `getInboxThreadsFlow(tab)` | Reactive thread list from Room (per folder) |
| `getAllInboxThreadsFlow()` | Unified inbox (all accounts) |
| `getThreadEmailsFlow(threadId)` | Reactive email list for a thread |
| `refreshInbox(tab, pageToken, query, accountId)` | Fetches from provider, persists to Room, returns next page token; catches and logs exceptions via `Log.e` |
| `refreshThread(threadId)` | Fetches single thread messages from provider |
| `clearLocalData()` | Calls `database.clearAllTables()` wrapped in `withContext(Dispatchers.IO)` to avoid main-thread violation |
| `toggleStar / archiveThread / deleteThread / ...` | **Optimistic update:** mutates Room first, then enqueues `SyncWorker` |

**Sync enqueue:** Every mutating method builds WorkManager `Data` with action constants and enqueues a `OneTimeWorkRequest<SyncWorker>` with `NetworkType.CONNECTED` constraint.

### Settings (DataStore)

#### SettingsDataStore (`data/settings/SettingsDataStore.kt`)

```kotlin
data class AppSettings(
    val themeMode: ThemeMode = ThemeMode.SYSTEM,
    val fontScale: FontScale = FontScale.DEFAULT,
    val showDividers: Boolean = false,
    val compactList: Boolean = false,
    val showSnippet: Boolean = true,
    val swipeLeftAction: SwipeAction = SwipeAction.STAR,
    val swipeRightAction: SwipeAction = SwipeAction.ARCHIVE,
    val confirmBeforeSending: Boolean = false,
    val defaultReply: DefaultReply = DefaultReply.REPLY,
    val emailNotifications: Boolean = true,
    val syncFrequency: SyncFrequency = SyncFrequency.MIN_15,
    val unifiedInboxEnabled: Boolean = false,
    val hasSeenDonationPrompt: Boolean = false,
    val smartGroupingEnabled: Boolean = true,
    val smartGroupingRecentOnly: Boolean = false,
    val organizeByThread: Boolean = true,
    val navScale: Float = 1f
)
```

Settings are stored in DataStore named `"app_settings"`. Each setting has its own key and setter method.

---

## Background Workers

### SyncWorker (`data/worker/SyncWorker.kt`)

One-shot `CoroutineWorker` for propagating local mutations to the server. Supports 8 action types: toggle star, mark thread read/unread, mark emails read, archive, unarchive, delete, restore. Can target a specific account (not just the active one).

### EmailSyncWorker (`worker/EmailSyncWorker.kt`)

Periodic `CoroutineWorker` (every 15 minutes with `NetworkType.CONNECTED`):

1. Iterates all accounts from `AccountManager`
2. For each account, calls `repository.refreshInbox(INBOX, accountId = accountId)`
3. If `refreshInbox` fails, logs the error via `Log.e` and continues to next account
4. Compares newest thread date with stored `lastKnownEmailId`
5. Shows Android notification for new emails (channel: `"monomail_notifications"`)

Scheduled from `MainActivity` via `PeriodicWorkRequestBuilder<EmailSyncWorker>(15, MINUTES)`.

---

## Navigation

### NavGraph (`ui/navigation/NavGraph.kt`)

**Routes (sealed class `Screen`):**

| Route | Pattern | Screen |
|-------|---------|--------|
| `sign_in` | `"sign_in"` | SignIn |
| `inbox` | `"inbox"` | Inbox |
| `thread_detail` | `"thread/{threadId}"` | EmailDetail |
| `compose` | `"compose?mode={mode}&to={to}&subject={subject}&threadId={threadId}&messageId={messageId}"` | Compose |
| `settings` | `"settings"` | Settings |
| `legal` | `"legal/{type}"` | Legal |

**Transitions:** All `tween(300)` — slide up for compose, slide left for thread/settings, fade for everything else. Pop transitions reverse the direction.

**Session restoration:** `LaunchedEffect(Unit)` calls `authManager.restoreSession()`. Start destination is `Inbox` if authenticated, `SignIn` otherwise.

**ViewModel factories:** Anonymous `ViewModelProvider.Factory` per screen — no DI framework. Dependencies wired from `MonoMailApp` application instance.

---

## UI Layer

### Theme

**MonoMailTheme** wraps content in `MaterialExpressiveTheme` with:
- **Colors:** Monochrome — white/light gray backgrounds in light mode, black/dark gray in dark mode
- **Typography:** Google Sans Flex variable font (weights 100-900, rounded variant)
- **Shapes:** Rounded corners (extraSmall=8dp to extraLarge=32dp)
- **Motion:** `MotionScheme.expressive()`

### Shared Components

#### BlurredModalOverlay (`ui/components/BlurredModalOverlay.kt`)

Reusable animated overlay for modals (donation prompt, trash confirmation, etc.):
- Outer `Box`: `AnimatedVisibility` with `fadeIn(tween(220))` / `fadeOut(tween(180))`
- Content `Box`: `.animateEnterExit` with `scaleIn(tween(200), FastOutSlowInEasing, 0.8f)` / `scaleOut(tween(200), 0.8f)`
- Background scrim clickable to dismiss; inner content swallows clicks

### Sign-In Screen

**SignInScreen** — Full-page entry with animated app logo (scale spring `MediumBouncy` + alpha spring `StiffnessLow`). "Continue with Email" button opens `ModalBottomSheet` with Google and Microsoft sign-in options. Privacy/ToS links at the bottom.

**SignInViewModel** — Manages sealed state: `Idle`, `Loading`, `Success(profile)`, `NeedsConsent(intent)`, `Error(message)`. Handles both Google (Credential Manager) and Microsoft (MSAL) flows.

### Inbox Screen

The largest screen (~1850 lines in `InboxScreen.kt`). Main composable is `InboxScreen()` which orchestrates:

| Section | Composables |
|---------|-------------|
| **Search bar** | `InboxSearchBar` — animated search field morphing to undo toast |
| **Thread list** | `LazyColumn` with `PullToRefreshBox`, items are `SwipeableEmailItem` wrappers |
| **Email row** | `EmailItem` — sender avatar (favicon via Coil), name, subject, snippet, timestamp |
| **Group header** | `GroupHeaderItem` — collapsible smart grouping header with rotating chevron |
| **Dock** | `AnimatedDockTab` × 4 (Inbox, Sent, Archive, Trash) with `updateTransition` for bg/content colors + label width/alpha. Computes inbox structure in `LaunchedEffect` with `Dispatchers.Default` to avoid jank. Sender name Regex cached as file-level `val`. |
| **FAB** | `AnimatedContent` morphing between compose icon (Inbox/Sent/Archived) and "Empty" label (Trash). Label calculated via `derivedStateOf` from current tab. |
| **Modals** | `BlurredModalOverlay` with `AnimatedContent` for profile card (fade+scale transition), switch account, add account |
| **Profile swipe** | `pointerInput` with `detectHorizontalDragGestures` on the avatar area; accumulates `totalDrag` across events (60px threshold). Swipe left/right cycles accounts without closing modal. |
| **Empty trash** | Trash confirmation modal with 5-second countdown timer. Auto-executes when timer hits 0. Cancel stops the timer. Batch undo pattern: hides all trash thread IDs immediately, shows "Trash emptied" + Undo, calls `repository.emptyTrash()` after 4s. |
| **Long-press** | Floating action overlay with star/read/archive/delete options |

**InboxViewModel** — Complex state machine combining:
- `InboxState`: `Loading`, `Success(threads, currentTab, isRefreshing, isLoadingMore, nextPageToken)`, `Error(message)`
- Built from `combine(currentTab, activeAccountId, unifiedInboxEnabled, organizeByThread).flatMapLatest { ... }`
- Foreground polling every 60s
- Undo support: optimistic hide with 4s delay, cancelable via `undoAction()`. Actions: `DELETE_THREAD`, `ARCHIVE_THREAD`, `EMPTY_TRASH`
- Pagination via `pageTokens: Map<String, String?>`
- Smart grouping via `InboxDisplayItem.computeInboxStructure()` (run on `Dispatchers.Default`)
- `ActionType` enum extended with `EMPTY_TRASH`; undo restores hidden thread IDs without server call; auto-delete fires after 4s

**InboxDisplayItem** — Sealed class hierarchy:
```
InboxDisplayItem
├── DateHeader(title)          // "Today", "Yesterday", "Mar 15"
├── GroupHeader(name, count, unreadCount, ...)  // Smart grouping
├── SingleThread(thread)
└── NestedThread(thread, groupName)
```

**Smart grouping logic:**
- Groups threads from same sender within 24h (recentOnly) or 3 days
- Minimum group size: 3 threads
- Groups always expanded if all unread

### Email Detail Screen

**EmailDetailScreen** — Thread/conversation view with:
- `TopAppBar`: back, star, overflow menu (mark unread, archive, trash)
- `LazyColumn` showing all emails in the thread
- Email body rendered in a `WebView` via `AndroidView` (HTML with sanitized quoted text removal)
- Attachments: images shown inline (downloaded, decoded, displayed), files in 2-column grid
- Conversation view: only latest message expanded, others collapsible via `AnimatedVisibility`
- Inline image CID injection replaces `cid:` references with base64 data URIs

**EmailDetailViewModel** — Combines `repository.getThreadEmailsFlow(threadId)` with loading/error state. Auto-marks thread as read on open. Exposes `isStarred: StateFlow<Boolean>` derived from email list.

### Compose Screen

**ComposeScreen** — Email composition with:
- To, Subject, Body fields (To disabled in REPLY mode)
- Contact autocomplete suggestions from `ContactSuggestionProvider` (debounced 200ms)
- Attachment support via system file picker (`GetMultipleContents`)
- Attachments shown in `LazyRow` with remove capability
- Original body shown at bottom when replying/forwarding
- Animated send button (spinner while sending)

**ComposeViewModel** — Handles modes: NEW, REPLY, FORWARD. Pre-fills To/Subject with "Re:" / "Fwd:" prefixes. Validates non-blank recipient and content before sending. Delegates to `repository.sendEmail()`.

### Settings Screen

**SettingsScreen** — Full settings with sections. Uses `SettingsToggleRow` composable with an `enabled` parameter. Unified inbox toggle is disabled (grayed out at 40% opacity) when `accountCount <= 1`, with subtitle "Add another account to enable".

| Section | Settings |
|---------|----------|
| Appearance | Theme (System/Light/Dark), Font Size (XS-XL), Nav Size (slider 0.6×–1.4×), Show Dividers, Compact List, Show Snippet |
| Behavior | Unified Inbox, Conversation View, Smart Grouping (with recent-only sub-option), Swipe Left/Right, Confirm Before Sending, Default Reply |
| Notifications | Email Notifications toggle, Sync Frequency (15min/30min/1hr/Manual) |
| Updates | Check for updates (GitHub releases API) |
| About | Version, Privacy Policy, Terms of Service, Open Source Licenses |

Animations: `animateColorAsState` for theme selector, `animateFloatAsState` for font/nav size previews, `AnimatedVisibility` with spring for smart grouping sub-option.

### Legal Screen

**LegalScreen** — Loads markdown from assets (`PRIVACY_POLICY.md` / `TERMS_OF_SERVICE.md`), renders with Markwon library in a `TextView` via `AndroidView`.

---

## State Management Patterns

| Pattern | Usage |
|---------|-------|
| `StateFlow` in ViewModels | All ViewModels expose `state: StateFlow<...>` |
| `MutableStateFlow` | Private `_state` backing field |
| `MutableSharedFlow` | One-shot events (e.g., `_uiError`) |
| `combine` + `flatMapLatest` | InboxViewModel combines tab, account, settings, repository flows |
| `stateIn(WhileSubscribed(5000))` | Cached reactive state with 5s timeout |
| `mutableStateOf` | Local UI state (search query, modals, expanded groups) |
| `derivedStateOf` | Computed values (filtered threads, pagination trigger) |
| `snapshotFlow` | Convert compose state to Flow for `LaunchedEffect` |
| `rememberSaveable` | Survive config changes (e.g., `expandedGroupsList`) |

---

## Animation Reference

| Location | Animation | Spec |
|----------|-----------|------|
| Navigation transitions | `slideIntoContainer + fadeIn` / reverse | `tween(300)` |
| BlurredModalOverlay outer | `AnimatedVisibility fade` | `tween(220)` / `tween(180)` |
| BlurredModalOverlay content | `scaleIn / scaleOut` | `tween(200, FastOutSlowInEasing)` |
| Dock tabs | `updateTransition` on 4 properties | `tween(200)` colors, `tween(220)` width, `tween(180)` alpha |
| Group header chevron | `animateFloatAsState rotation` | `tween(250)` |
| Swipe background color | `animateColorAsState` | `tween(200)` |
| Search bar color | `animateColorAsState` | `tween(300)` |
| Long-press overlay | `AnimatedVisibility scale` | `tween(300, FastOutSlowInEasing)` |
| FAB icon morph | `AnimatedContent scale + fade` | `tween(180/120)` |
| Modal content switch | `AnimatedContent scale + fade` | `tween(200, FastOutSlowInEasing)` |
| Profile account switch | `AnimatedContent fade + scale` | `fadeIn(tween(220)) + scaleIn(tween(220), 0.9f)` / `fadeOut(tween(150)) + scaleOut(tween(150), 0.9f)` |
| Trash countdown timer | `animateIntAsState` | `tween(1000, LinearEasing)` per tick |
| Email body expand | `expandVertically / shrinkVertically` | Default |
| Compose suggestions | `AnimatedVisibility expand + fade` | Default |
| Sign-in entry | `Animatable spring (scale + alpha)` | `MediumBouncy` / `StiffnessLow` |
| Settings cards | `animateContentSize spring` | `DampingRatioMediumBouncy` |
| Settings theme selector | `animateColorAsState` per button | `tween(250)` |
| Font/nav size preview | `animateFloatAsState spring` | `StiffnessMedium` |
| Smart grouping sub-option | `AnimatedVisibility spring expand` | `DampingRatioMediumBouncy` |
| LazyColumn items | `animateItem()` | Default |

---

## Key Implementation Details

### Optimistic UI + WorkManager Sync

The app uses a **local-first** approach:
1. User performs action (star, archive, delete)
2. Repository immediately updates Room database
3. UI reactively reflects the change via `Flow`
4. Repository enqueues `OneTimeWorkRequest<SyncWorker>` with the action and account ID
5. `SyncWorker` executes the same action on the remote API
6. If the sync fails and the user is offline, WorkManager retries with exponential backoff

### Multi-Account Support

- Account IDs are prefixed with provider: `gmail_user@gmail.com`, `outlook_user@outlook.com`
- All stored as encrypted JSON in DataStore via `AccountManager`
- Active account can be switched dynamically
- Room queries filter by `accountId`
- `SyncWorker` temporarily switches active account if the action targets a non-active account

### Smart Grouping

Groups threads from the same sender within a time window:
- Time window: 24h (recent only) or 3 days
- Minimum group size: 3 threads
- Groups smaller than the threshold remain as `SingleThread` items
- Groups displayed with expandable `GroupHeaderItem`
- Sender name parsing uses a cached `senderNameRegex` file-level `val` in `InboxDisplayItem.kt`

### Unified Inbox

When enabled, threads from all accounts are merged into a single list ordered by date. Uses `getAllInboxThreads()` DAO query instead of per-account queries.

### Email Body Rendering

- Bodies are decoded from Base64URL, HTML preferred over plain text
- Inline CID images are replaced with base64 data URIs
- Quoted text is stripped (blockquote, gmail_quote, gmail_extra, etc.)
- Rendered in a `WebView` with theme-aware colors, JS disabled, transparent background
- WebView height calculated from content, scrolled inside `LazyColumn`

### Attachment Handling

- **Download:** Bytes fetched from provider, saved to cache dir, launched via `ACTION_VIEW` with `FileProvider` URI
- **Compose:** System file picker via `GetMultipleContents`, metadata extracted via `ContentResolver`
- **Size limit:** Outlook provider enforces 3MB upload limit

### Notification Badging

`EmailSyncWorker` stores the latest email date per account via `AccountManager.setLastKnownEmailId()`. On each sync cycle, compares the newest inbox thread date against the stored value. If newer, shows a notification.

---

## Data Flow

### Sign-In Flow (Google)

```
User taps "Sign In with Google"
  → SignInScreen → SignInViewModel.signIn(context)
    → AuthManager.signIn(activityContext)
      → CredentialManager.getCredential(GetGoogleIdOption)  [gets ID token]
      → GoogleAuthUtil.getToken()  [gets Gmail OAuth2 access token]
      → Validates token via HTTP HEAD to gmail.googleapis.com
      → Creates UserProfile(provider = "gmail")
      → AccountManager.addAccount(profile)  [encrypted DataStore]
      → AuthManager switches active account
    → SignInViewModel emits SignInState.Success
  → NavGraph navigates to Inbox
```

### Inbox Loading Flow

```
InboxScreen renders
  → InboxViewModel collects state
    → combine(currentTab, activeAccountId, settings...).flatMapLatest
      → repository.getInboxThreadsFlow(tab)  [if organizeByThread]
        → ThreadDao.getInboxThreads(accountId)  [Flow from Room]
        → Maps ThreadEntity → EmailThread
    → combine with isRefreshing, isLoadingMore, pendingHideIds
    → Emits InboxState.Success(threads, ...)
  → InboxScreen renders LazyColumn
    → computeInboxStructure(threads)  [smart grouping on Dispatchers.Default]
    → flattenDisplayItems(structure, ...)  [date headers, group headers]
    → Renders each item with SwipeableEmailItem / GroupHeaderItem
```

### Action Flow (e.g., Archive)

```
User swipes left on thread
  → SwipeableEmailItem → viewModel.archiveThread(threadId)
    → repository.archiveThread(threadId)
      → ThreadDao.archiveThread(threadId, accountId)  [optimistic local update]
      → EmailDao.archiveThreadEmails(threadId, accountId)
      → WorkManager.enqueue(SyncWorker(ACTION_ARCHIVE, ...))
  → InboxViewModel updates pendingHideIds
    → UI hides the thread immediately
  → After 4s (or manual dismiss):
    → repository.archiveThread(threadId) actually fires
    → SyncWorker.doWork():
      → provider.archiveThread(threadId)
        → GmailProvider: api.modifyThread(id, removeLabelIds=["INBOX"])
```

### Periodic Sync Flow

```
EmailSyncWorker.doWork()
  → Get all accounts from AccountManager
  → For each account:
    → repository.refreshInbox(INBOX, accountId = accountId)
      → provider.listThreads(INBOX, ...)
        → GmailProvider: api.listThreads(labelIds=["INBOX"])
        → Parallel fetch each thread
        → Convert to ProviderThread → ProviderMessage
      → Map to ThreadEntity / EmailEntity
      → ThreadDao.insertThreads(...)
      → EmailDao.insertEmails(...)
    → Compare latest thread date against stored lastKnownEmailId
    → If newer → show Android notification
```
