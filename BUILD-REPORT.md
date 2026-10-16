# BUILD REPORT — cheatsheet-pages 首批构建（2026-10-16）

## 产出概览

| 项 | 数量 |
|---|---|
| 内容页 | **75 页**（git 25 / sql 25 / kubectl 25） |
| 首页 index.html | 1（站名 + 3 仓入口 + 75 页按仓分组目录） |
| sitemap.xml | 76 条 URL（首页 + 75 页，前缀占位 `https://ezra-zhao.github.io/cheatsheet-pages/`） |
| robots.txt | 1（Allow all + Sitemap 行） |
| 图卡图片 | 3 张（images/git|sql|kubectl-cheatsheet.png，从 goals/.../files/cards/ 复制） |
| 生成脚本 | `generate.py`（可复跑：改数据后 `python3 generate.py` 重新生成全部页面） |

目录：`~/workspace/github-repos/cheatsheet-pages/`（未 push、未建仓，本地构建完成待上线）。

## 页面模型

「一个命令 × 一个使用场景 = 一页」：搜索问句式 `<title>` + 一句场景说明 + 代码块 + 「Good to know」说明段（仅当仓里有对应说明文字时才写，无则省略）+ 本仓图卡（嵌图并回链仓）+ 页脚双回链（完整速查表仓 + 作者主页 github.com/Ezra-Zhao）。SQL 页另带样本表说明（取自仓内 Test data 段），kubectl 页另带占位符说明（取自仓首段）。英文页面、深色样式、单文件内联 CSS、无任何外部资源引用。

## 质量门结果

1. **逐字校验（全量，机器执行）**：生成脚本内置校验——75 页共 **184 行代码逐行与三仓 CHEATSHEET.md 比对**（空白对齐归一化后比对，即命令 token 序列完全一致），全部命中源文件，校验通过构建才放行；任何一行对不上构建即失败。
2. **抽查 6 页（每仓 2 页，实际打开 HTML 核对）**：
   - git/undo-last-commit-reset-soft-mixed-hard.html ✅ 三种 reset 与源文件一致，⚠️ 标记正常
   - git/recover-lost-commit-reflog.html ✅ `<sha>` 正确转义为 `&lt;sha&gt;`，图卡路径有效
   - sql/having-vs-where.html ✅ HAVING 说明与源文件注释一致，`>` 转义正确
   - sql/upsert-on-conflict.html ✅ 长方言注释行与源文件逐字一致，→ 符号无乱码
   - kubectl/logs-previous-crashed-container.html ✅ `-p` 命令与源一致，占位符说明在位
   - kubectl/debug-ephemeral-container.html ✅ debug 两条命令与源一致，说明段源自仓内文字
3. **结构校验（脚本执行）**：index.html 75 条页面链接全部指向真实文件（0 缺失）；75 页逐页检查图片引用存在、作者回链与首页回链在位、无乱码替换符、无 script/link 外部资源标签——**0 问题**。

## 页面清单（75）

### git/（25）
amend-last-commit · bisect-find-bad-commit · check-remote-url · cherry-pick · config-user-name-email · create-switch-branch · default-branch-main · delete-branch-local-and-remote · discard-file-changes · fetch-prune · list-branches · log-oneline-graph · pull-with-rebase · push-set-upstream · rebase-continue-abort · rebase-onto-main · recover-lost-commit-reflog · revert-pushed-commit · squash-commits-interactive-rebase · stage-hunks-add-p · stash-changes · stash-list-pop-apply · status-short · undo-last-commit-reset-soft-mixed-hard · unstage-file

### sql/（25）
case-when-conditional-aggregation · count-sum-avg · create-index · create-table · cte-with · delete-rows-where · exists-check · filter-rows-where · find-rows-with-no-match · group-by · having-vs-where · in-and-between · inner-join · insert-row · join-three-tables-aggregate · left-join · like-pattern-matching · rank-window-function · select-distinct · self-join · subquery-above-average · top-n-rows-limit · transactions-begin-commit · update-rows-where · upsert-on-conflict

### kubectl/（25）
apply-manifest · check-current-cluster · cp-copy-files · create-deployment · debug-ephemeral-container · delete-pod-deployment · describe-pod · exec-shell · get-contexts · get-events-sorted · get-pods-all-namespaces · get-resources-by-label · list-create-namespaces · logs-follow-tail · logs-pod · logs-previous-crashed-container · port-forward · rollout-history-undo · rollout-restart · rollout-status · scale-deployment · set-default-namespace · set-image · switch-context · top-usage

## 待办（上线时）

- 建仓后把 sitemap/robots 的 URL 前缀从占位 `ezra-zhao.github.io/cheatsheet-pages/` 换成真实 Pages 地址（如有变动），重跑 `generate.py` 即可。
- 选题说明：任务示例中的「SQL find duplicate rows」仓里没有逐字对应的语句（仓内无 GROUP BY…HAVING COUNT 查重条目），按「不许新编」红线未做该页，改选仓内真实条目补足 25 页。

---

# 扩仓记录（2026-10-16）：3 仓 → 12 仓，75 页 → 300 页

新增 9 仓 × 25 页 = **225 页**，与首批同模板、同质量门：

| 仓 | 页数 | 内容来源 |
|---|---|---|
| ffmpeg | 25 | ffmpeg-cheatsheet/CHEATSHEET.md（28 代码块） |
| docker | 25 | docker-cheatsheet/CHEATSHEET.md（30 代码块） |
| curl | 25 | curl-cheatsheet/CHEATSHEET.md（29 代码块） |
| jq | 25 | jq-cheatsheet/CHEATSHEET.md（31 代码块） |
| regex | 25 | regex-cheatsheet/CHEATSHEET.md（31 代码块） |
| ssh | 25 | ssh-cheatsheet/CHEATSHEET.md（31 代码块） |
| terminal | 25 | terminal-superpowers-cheatsheet/CHEATSHEET.md（15 块，工具页+组合页） |
| adobe | 25 | adobe-free-alternatives-cheatsheet/CHEATSHEET.md + README.md（对照条目页） |
| desubscribe | 25 | desubscribe-cheatsheet/README.md + CHEATSHEET.md（对照条目页，价格数字逐字） |

## 实现方式

- 数据文件 `pages2.py`（REPOS2 + PAGES2）：代码字符串先由抽取脚本从各仓 CHEATSHEET.md 的围栏代码块按段落编号提取原文，再按「一个命令/条目 × 一个场景」组页；不经过手工转写。
- `generate.py` 改动：① 构建时合并 pages2 数据；② 校验器支持多源文件（`sources`）与 fragment 模式（adobe 仓内容为表格条目，逐行须作为源文件归一化文本的子串命中）；③ 首页标题/描述改为 12 仓口径，目录按 12 仓分组列全 300 页；④ 写页前自动建目录。
- 9 张图卡复制进 `images/`（文件名与各仓 card 字段一致）。

## 质量门结果（本次）

1. **逐字校验（全量，机器执行）**：300 页共 **793 行代码**逐行（adobe 为 fragment 子串）与 12 仓源文件比对，全部命中，构建放行。
2. **抽查 18 页（每新仓 2 页，脚本随机抽样 + 实际打开核对）**：18/18 图片路径有效、渲染代码与页面规格逐字一致、无乱码替换符；另通读 4 页（desubscribe 五年成本、adobe Linux 安装、ssh 用户限制+改端口、regex 前瞻）确认中文原文行、说明段、回链齐全。
3. **结构校验**：index.html 300 条页面链接 0 缺失；sitemap.xml 301 个 URL（首页 + 300 页）全部对应真实文件。

## 页面清单（新增 225，slug）

- ffmpeg（25）：audio-extract-volume-and-loudnorm · burn-subtitles-into-video · concat-join-videos · convert-webm-to-mp4 · correct-mp4-flagged-as-rotated · extract-audio-to-mp3 · extract-thumbnail-at-timestamp · images-to-video-slideshow · inspect-media-file-ffprobe · loop-video-or-stream · make-screen-recording · make-timelapse-from-video · merge-video-and-audio · optimize-video-for-web · reduce-video-file-size · remove-audio-track · replace-audio-track · resize-video-720p · rotate-video-90-degrees · speed-up-or-slow-down-video · split-video-by-time · stabilize-shaky-video · trim-video-no-reencode · video-to-animated-webp · video-to-gif-with-palette
- docker（25）：build-image-from-dockerfile · build-multi-platform-images · clean-up-unused-space · common-flags-worth-knowing · compose-logs-shell-stop-down · compose-up-down · connect-two-services-with-networking · copy-files-with-docker-cp · debug-a-crashed-container · edit-file-in-running-container · export-and-import-images · inspect-container-details · inspect-container-logs · inspect-images-and-volumes · override-entrypoint-for-debugging · publish-ports · remove-containers-images-volumes · rename-tag-and-push-images · run-an-image · run-detached-and-follow-logs · run-one-off-commands · set-environment-variables · share-a-directory-with-a-container · start-stop-restart-containers · system-prune-cleanup
- curl（25）：basic-auth · bearer-token-auth · cookies-and-sessions · custom-headers · custom-user-agent · delete-resource · head-request-headers-only · limit-download-speed · measure-timing-and-status-code · patch-partial-update · post-form-data-urlencode · post-json · put-replace-resource · resume-interrupted-download · retry-failed-downloads · route-through-proxy · save-response-to-file · show-response-headers · silent-mode-show-errors · simple-get-request · skip-tls-verification-debug · trace-ascii-full-dump · upload-file-multipart · verbose-mode · which-http-version
- jq（25）：build-new-objects · chain-filters-with-pipes · compact-output-one-per-line · deduplicate-with-unique · drill-into-nested-objects · extract-one-field · group-by-and-count · index-and-stream-arrays · keys-has-del · map-add-computed-field · map-pluck-one-field · map-reshape-objects · max-min-by-field · pretty-print-json · raw-output-no-quotes · real-world-api-and-logs · regex-match-with-test · select-by-number · select-by-string-match · select-with-boolean-logic · shell-variables-and-slurp · sort-by-field · strings-and-type-conversion · sum-with-add · count-with-length
- regex（25）：alternation-or · anchors-start-and-end · backreferences · capturing-groups · catastrophic-backtracking · character-classes-and-negation · date-yyyy-mm-dd-pattern · dot-any-character · dont-parse-html-with-regex · email-pattern · greedy-vs-lazy · html-tag-pattern · international-phone-pattern · ipv4-address-strict · lookahead-assertions · lookbehind-assertions · named-capturing-groups · non-capturing-groups · quantifier-exact-counts · quantifiers-star-plus-question · replacement-backreferences · shorthand-classes-digit-word-space · trim-whitespace-pattern · url-pattern · word-boundary
- ssh（25）：background-tunnel-fn · change-passphrase-and-permissions · config-global-defaults-host-star · config-host-alias · config-wildcard-hosts · connect-basics-and-ports · create-ed25519-key · debug-failed-login-verbose · disable-root-login · dynamic-forward-socks-proxy · escape-sequences-frozen-session · fix-too-many-authentication-failures · install-key-with-copy-id · jump-host-proxyjump · keepalive-idle-sessions · keys-only-no-password-auth · local-forward-port · login-with-specific-key · proxyjump-in-config · remote-forward-port · restrict-users-and-change-port · rsync-over-ssh · scp-copy-files · sftp-interactive-shell · ssh-agent-passphrase-once
- terminal（25）：bat-cat-with-highlighting · btop-resource-monitor · cmux-terminal-for-ai-agents · eza-modern-ls · fd-friendlier-find · find-and-search-fd-ripgrep · fzf-fuzzy-finder · git-workflow-lazygit-starship · lazygit-terminal-ui · learn-commands-tldr-fzf · monitor-with-btop-in-tmux · navigate-faster-zoxide-fzf · new-in-2026-cmux-yoinks · remote-sessions-tmux-zoxide · replace-classic-unix-tools · ripgrep-grep-rebuilt-in-rust · starship-prompt · starter-pack-one-command · tldr-man-pages-you-will-read · tmux-terminal-multiplexer · tmux-vs-zellij · view-files-eza-bat · yoinks-download-videos · zellij-modern-multiplexer · zoxide-smarter-cd
- adobe（25）：after-effects-alternatives-compared · artcraft-suite-seven-apps · audacity-alternative-to-audition · blender-alternative-to-after-effects · darktable-alternative-to-lightroom · davinci-resolve-alternative-to-premiere · designcraft-alternative-to-indesign · effectcraft-alternative-to-after-effects · filmcraft-alternative-to-premiere · gimp-alternative-to-photoshop · illustrator-alternatives-compared · indesign-alternatives-compared · inkscape-alternative-to-illustrator · install-alternatives-on-linux · kdenlive-alternative-to-premiere · lightcraft-alternative-to-lightroom · lightroom-alternatives-compared · mature-free-creative-suite · penpot-alternative-to-figma-xd · photocraft-alternative-to-photoshop · photoshop-alternatives-compared · premiere-alternatives-compared · printcraft-alternative-to-acrobat · scribus-alternative-to-indesign · vectorcraft-alternative-to-illustrator
- desubscribe（25）：are-these-prices-current · biggest-savings-first · cheapest-swaps-to-start · files-and-photos-stack · five-year-cost-of-subscriptions · free-tiers-honest-note · meetings-and-design-stack · notes-stack-appflowy-joplin · passwords-and-data-stack · replace-airtable-with-nocodb · replace-dropbox-with-nextcloud · replace-evernote-with-joplin · replace-figma-with-penpot · replace-google-one-with-immich · replace-notion-with-appflowy · replace-slack-with-mattermost · replace-trello-with-wekan · replace-zoom-with-jitsi · replace-1password-with-vaultwarden · run-all-ten-replacements · team-chat-and-boards-stack · team-savings-4470 · total-savings-1260-a-year · wekan-full-install-with-mongodb · what-you-need-to-self-host
