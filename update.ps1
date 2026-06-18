$path = "C:\Users\Shiro\Projects\Monomail\index.html"
$content = Get-Content $path -Raw -Encoding utf8

$new_html = @"
                <div class="features-grid">
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
                    <div class="feat-card">
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
                            <p class="feat-desc">High-frequency senders are collapsed into expandable folders with spring expand animations.</p>
                        </div>
                    </div>

                    <!-- Row 2 -->
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
                    <div class="feat-card">
                        <div class="feat-icon">
                            <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2.2" stroke-linecap="round">
                                <path d="M9 18l6-6-6-6" />
                            </svg>
                        </div>
                        <div class="feat-text-wrap">
                            <div class="feat-name">Swipe Gestures</div>
                            <p class="feat-desc">Swipe right to Archive / Unarchive. Swipe left to Star / Unstar. Fluid and native-feeling.</p>
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

                    <!-- Row 3 -->
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
                </div>

                <h3 class="minor-title">And so much more</h3>
                <div class="features-list">
                    <div class="feat-list-item">
                        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"></polyline></svg>
                        Background Sync
                    </div>
                    <div class="feat-list-item">
                        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"></polyline></svg>
                        Smart Undo Toasts
                    </div>
                    <div class="feat-list-item">
                        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"></polyline></svg>
                        Refined Settings
                    </div>
                    <div class="feat-list-item">
                        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"></polyline></svg>
                        Long Press Context Menu
                    </div>
                    <div class="feat-list-item">
                        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"></polyline></svg>
                        GPL-3.0 Open Source
                    </div>
                    <div class="feat-list-item">
                        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"></polyline></svg>
                        More features coming soon
                    </div>
                </div>
"@

$content = [System.Text.RegularExpressions.Regex]::Replace($content, "(?s)<div class=`"features-grid`">.*?</div>\s*</div>\s*</section>", "$new_html`n            </div>`n        </section>")

$css_to_add = @"
            .minor-title {
                font-family: var(--font-d);
                font-size: 20px;
                font-weight: 700;
                margin-top: 56px;
                margin-bottom: 24px;
                text-align: left;
                letter-spacing: -0.2px;
            }
            .features-list {
                display: grid;
                grid-template-columns: repeat(3, 1fr);
                gap: 16px;
                text-align: left;
            }
            .feat-list-item {
                display: flex;
                align-items: center;
                gap: 14px;
                font-size: 15px;
                color: var(--black);
                font-weight: 500;
                background: rgba(0,0,0,0.04);
                padding: 16px 20px;
                border-radius: 12px;
            }
            .feat-list-item svg {
                flex-shrink: 0;
            }
"@

$content = $content.Replace("/* ── RESPONSIVE ── */", "$css_to_add`r`n`r`n            /* ── RESPONSIVE ── */")

$mq_find = @"
                .features-grid {
                    grid-template-columns: 1fr;
                }
"@

$mq_to_add = @"
                .features-list {
                    grid-template-columns: 1fr;
                }
"@

if ($content.Contains($mq_find)) {
    $content = $content.Replace($mq_find, "$mq_find$mq_to_add")
} else {
    $mq_find2 = "                .features-grid {`n                    grid-template-columns: 1fr;`n                }"
    $mq_to_add2 = "                .features-list {`n                    grid-template-columns: 1fr;`n                }`n"
    $content = $content.Replace($mq_find2, "$mq_find2`n$mq_to_add2")
}


Set-Content -Path $path -Value $content -Encoding utf8
Write-Host "Updated"
