import re

file_path = r'C:\Users\Shiro\Projects\Monomail\index.html'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update CSS for features-grid
old_css = """            .features-grid {
                display: grid;
                grid-template-columns: repeat(3, 1fr);
                gap: 16px;
            }
            .feat-card {
                background: var(--white);
                border-radius: var(--r-card);
                padding: 28px 26px;
                border: 1.5px solid var(--border);
                transition:
                    border-color 0.2s,
                    transform 0.2s;
            }
            .feat-card:hover {
                border-color: var(--black);
                transform: translateY(-3px);
            }
            .feat-icon {
                width: 48px;
                height: 48px;
                background: var(--black);
                border-radius: 16px;
                display: flex;
                align-items: center;
                justify-content: center;
                margin-bottom: 22px;
            }
            .feat-name {
                font-family: var(--font-d);
                font-size: 19px;
                font-weight: 700;
                letter-spacing: -0.3px;
                margin-bottom: 8px;
            }
            .feat-desc {
                font-size: 14px;
                color: var(--muted);
                line-height: 1.6;
            }"""

new_css = """            .features-grid {
                display: grid;
                grid-template-columns: repeat(4, 1fr);
                gap: 24px;
            }
            .feat-card {
                background: var(--white);
                border-radius: var(--r-card);
                padding: 32px;
                border: 1.5px solid var(--border);
                transition:
                    border-color 0.2s,
                    transform 0.2s,
                    box-shadow 0.2s;
                display: flex;
                flex-direction: column;
                justify-content: flex-start;
                align-items: flex-start;
            }
            .feat-card:hover {
                border-color: var(--black);
                transform: translateY(-4px);
                box-shadow: 0 12px 24px rgba(0,0,0,0.06);
            }
            .feat-span-2 {
                grid-column: span 2;
                flex-direction: row;
                align-items: flex-start;
            }
            .feat-span-2 .feat-icon {
                margin-bottom: 0;
                margin-right: 24px;
                width: 56px;
                height: 56px;
                flex-shrink: 0;
            }
            .feat-span-2 .feat-text-wrap {
                display: flex;
                flex-direction: column;
                justify-content: center;
                min-height: 56px;
            }
            .feat-icon {
                width: 48px;
                height: 48px;
                background: var(--black);
                border-radius: 16px;
                display: flex;
                align-items: center;
                justify-content: center;
                margin-bottom: 24px;
                flex-shrink: 0;
            }
            .feat-name {
                font-family: var(--font-d);
                font-size: 19px;
                font-weight: 700;
                letter-spacing: -0.3px;
                margin-bottom: 10px;
            }
            .feat-desc {
                font-size: 14px;
                color: var(--muted);
                line-height: 1.6;
            }"""

content = content.replace(old_css, new_css)

# 2. Update responsive media queries
old_mq = """                .features-grid {
                    grid-template-columns: 1fr;
                }"""
new_mq = """                .features-grid {
                    grid-template-columns: 1fr;
                }
                .feat-span-2 {
                    grid-column: span 1;
                    flex-direction: column;
                }
                .feat-span-2 .feat-icon {
                    margin-bottom: 24px;
                    margin-right: 0;
                    width: 48px;
                    height: 48px;
                }"""

# there are two places with this exact string, we want the one under 768px
content = content.replace(old_mq, new_mq)

# 3. Update the HTML
new_html = """                <div class="features-grid">
                    <!-- Row 1 -->
                    <div class="feat-card feat-span-2">
                        <div class="feat-icon">
                            <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
                                <ellipse cx="12" cy="5" rx="9" ry="3" />
                                <path d="M21 12c0 1.66-4 3-9 3s-9-1.34-9-3" />
                                <path d="M3 5v14c0 1.66 4 3 9 3s9-1.34 9-3V5" />
                            </svg>
                        </div>
                        <div class="feat-text-wrap">
                            <div class="feat-name">Offline-First</div>
                            <p class="feat-desc">Built on Room Database. Changes apply instantly and sync with Gmail in the background — works without a connection.</p>
                        </div>
                    </div>
                    <div class="feat-card">
                        <div class="feat-icon">
                            <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2.2" stroke-linecap="round">
                                <path d="M12 2a10 10 0 0110 10" />
                                <path d="M12 6v6l4 2" />
                                <polyline points="22,11 22,2 13,11" />
                            </svg>
                        </div>
                        <div class="feat-text-wrap">
                            <div class="feat-name">Background Sync</div>
                            <p class="feat-desc">WorkManager keeps your inbox up to date. Notifications and status changes happen flawlessly behind the scenes.</p>
                        </div>
                    </div>
                    <div class="feat-card">
                        <div class="feat-icon">
                            <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
                                <circle cx="11" cy="11" r="8" />
                                <path d="m21 21-4.35-4.35" />
                            </svg>
                        </div>
                        <div class="feat-text-wrap">
                            <div class="feat-name">Smart Search</div>
                            <p class="feat-desc">Fully integrated search that works offline and online, woven into navigation with a morphing SearchBar.</p>
                        </div>
                    </div>

                    <!-- Row 2 -->
                    <div class="feat-card">
                        <div class="feat-icon">
                            <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2.2" stroke-linecap="round">
                                <path d="M9 18l6-6-6-6" />
                            </svg>
                        </div>
                        <div class="feat-text-wrap">
                            <div class="feat-name">Swipe Gestures</div>
                            <p class="feat-desc">Swipe right to Archive / Unarchive. Swipe left to Star / Unstar. Fluid, native-feeling, and configurable.</p>
                        </div>
                    </div>
                    <div class="feat-card feat-span-2">
                        <div class="feat-icon">
                            <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2.2" stroke-linecap="round">
                                <path d="M3 6h18M3 12h18M3 18h18" />
                                <rect x="2" y="4" width="4" height="4" rx="1" />
                                <rect x="2" y="10" width="4" height="4" rx="1" />
                                <rect x="2" y="16" width="4" height="4" rx="1" />
                            </svg>
                        </div>
                        <div class="feat-text-wrap">
                            <div class="feat-name">Smart Grouping</div>
                            <p class="feat-desc">High-frequency senders are automatically collapsed into expandable folders with animated spring expand/collapse.</p>
                        </div>
                    </div>
                    <div class="feat-card">
                        <div class="feat-icon">
                            <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2.2" stroke-linecap="round">
                                <polyline points="9,14 4,9 9,4" />
                                <path d="M20 20v-7a4 4 0 00-4-4H4" />
                            </svg>
                        </div>
                        <div class="feat-text-wrap">
                            <div class="feat-name">Smart Undo</div>
                            <p class="feat-desc">Accidentally archived or deleted? A morphing toast gives you seconds to undo — without firing a network request.</p>
                        </div>
                    </div>

                    <!-- Row 3 -->
                    <div class="feat-card">
                        <div class="feat-icon">
                            <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2.2" stroke-linecap="round">
                                <rect x="3" y="3" width="18" height="18" rx="4" />
                                <path d="M3 9h18M9 21V9" />
                            </svg>
                        </div>
                        <div class="feat-text-wrap">
                            <div class="feat-name">Refined Settings</div>
                            <p class="feat-desc">Grouped card-based sections, M3 Modal Bottom Sheet pickers, and live font size preview before you apply changes.</p>
                        </div>
                    </div>
                    <div class="feat-card">
                        <div class="feat-icon">
                            <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2.2" stroke-linecap="round">
                                <rect x="1" y="4" width="22" height="16" rx="3" />
                                <path d="M1 10h22" />
                            </svg>
                        </div>
                        <div class="feat-text-wrap">
                            <div class="feat-name">Long Press</div>
                            <p class="feat-desc">Hold any email to Star, Archive, toggle Read/Unread, or Delete — in a clean contextual card with smooth animations.</p>
                        </div>
                    </div>
                    <div class="feat-card feat-span-2">
                        <div class="feat-icon">
                            <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2.2" stroke-linecap="round">
                                <path d="M12 20h9" />
                                <path d="M16.5 3.5a2.121 2.121 0 013 3L7 19l-4 1 1-4L16.5 3.5z" />
                            </svg>
                        </div>
                        <div class="feat-text-wrap">
                            <div class="feat-name">Compose &amp; Reply</div>
                            <p class="feat-desc">Distraction-free compose with attachment support, confirm-before-send, and configurable reply defaults.</p>
                        </div>
                    </div>

                    <!-- Row 4 -->
                    <div class="feat-card feat-span-2">
                        <div class="feat-icon">
                            <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
                                <path d="M17 21v-2a4 4 0 00-4-4H5a4 4 0 00-4 4v2" />
                                <circle cx="9" cy="7" r="4" />
                                <path d="M23 21v-2a4 4 0 00-3-3.87" />
                                <path d="M16 3.13a4 4 0 010 7.75" />
                            </svg>
                        </div>
                        <div class="feat-text-wrap">
                            <div class="feat-name">Multiple Accounts</div>
                            <p class="feat-desc">Add Gmail and Microsoft Outlook accounts and switch between them effortlessly. All your inboxes, one app.</p>
                        </div>
                    </div>
                    <div class="feat-card">
                        <div class="feat-icon">
                            <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
                                <rect x="2" y="3" width="20" height="14" rx="2" />
                                <path d="M8 21h8" />
                                <path d="M12 17v4" />
                                <path d="M2 10h20" />
                            </svg>
                        </div>
                        <div class="feat-text-wrap">
                            <div class="feat-name">Unified Inbox</div>
                            <p class="feat-desc">See all your accounts in one merged feed. One scroll, every email — no context switching.</p>
                        </div>
                    </div>
                    <div class="feat-card">
                        <div class="feat-icon">
                            <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
                                <polyline points="23,6 13.5,15.5 8.5,10.5 1,18" />
                                <polyline points="17,6 23,6 23,12" />
                            </svg>
                        </div>
                        <div class="feat-text-wrap">
                            <div class="feat-name">Coming Soon</div>
                            <p class="feat-desc">Labels, threads, rich text compose, and more — actively in development.</p>
                        </div>
                    </div>

                    <!-- Row 5 -->
                    <div class="feat-card feat-span-2">
                        <div class="feat-icon">
                            <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2.2" stroke-linecap="round">
                                <path d="M13 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V9z" />
                                <polyline points="13,2 13,9 20,9" />
                            </svg>
                        </div>
                        <div class="feat-text-wrap">
                            <div class="feat-name">GPL-3.0 Open Source</div>
                            <p class="feat-desc">Every line of Kotlin, every Composable — publicly readable on GitHub. Eight releases and counting. PRs welcome.</p>
                        </div>
                    </div>
                    <div class="feat-card feat-span-2">
                        <div class="feat-icon">
                            <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2.2" stroke-linecap="round">
                                <rect x="3" y="3" width="18" height="18" rx="3" />
                                <path d="M3 9h18M9 21V9" />
                            </svg>
                        </div>
                        <div class="feat-text-wrap">
                            <div class="feat-name">Pure Monochrome</div>
                            <p class="feat-desc">Black. White. Nothing in between. A Material 3 Expressive system stripped of all colour accents for ultimate focus.</p>
                        </div>
                    </div>
                </div>"""

import re
pattern = re.compile(r'<div class="features-grid">.*?</div>\s*</div>\s*</section>', re.DOTALL)

def replacer(match):
    return new_html + '\n            </div>\n        </section>'

content = pattern.sub(replacer, content)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Update complete")
