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
