#!/usr/bin/env python3
"""
cheatsheet-pages generator — one command x one scenario = one page.

Source of truth: ~/workspace/github-repos/<repo>/CHEATSHEET.md
Every code line in PAGES below was transcribed verbatim from those files.
Before writing anything, this script verifies each code line against the
source file (whitespace-normalized line comparison). If a line is not
found in the source, the build FAILS — no invented commands get in.

Rerun:  python3 generate.py
Output: index.html, git|sql|kubectl/*.html, sitemap.xml, robots.txt
"""
import html
import os
import sys

BASE = os.path.dirname(os.path.abspath(__file__))
SRC_DIR = os.path.expanduser("~/workspace/github-repos")
SITE_URL = "https://ezra-zhao.github.io/cheatsheet-pages/"
AUTHOR_URL = "https://github.com/Ezra-Zhao"
SITE_NAME = "Cheatsheet Pages"

REPOS = {
    "git": {
        "name": "Git Cheatsheet",
        "repo_url": "https://github.com/Ezra-Zhao/git-cheatsheet",
        "source": "git-cheatsheet/CHEATSHEET.md",
        "card": "git-cheatsheet.png",
        "card_alt": "Git Cheatsheet one-page card — 30 daily and rescue commands",
        "global_note": None,
    },
    "sql": {
        "name": "SQL Cheatsheet",
        "repo_url": "https://github.com/Ezra-Zhao/sql-cheatsheet",
        "source": "sql-cheatsheet/CHEATSHEET.md",
        "card": "sql-cheatsheet.png",
        "card_alt": "SQL Cheatsheet one-page card — queries that actually work",
        "global_note": (
            "Every example runs against the cheatsheet's sample tables — "
            "departments(id, name), employees(id, name, dept_id, salary, manager_id, hired_on) "
            "and orders(id, emp_id, amount, ordered_on) — and was executed and verified "
            "against SQLite, so you can paste it in and get the same result."
        ),
    },
    "kubectl": {
        "name": "kubectl Cheatsheet",
        "repo_url": "https://github.com/Ezra-Zhao/kubectl-cheatsheet",
        "source": "kubectl-cheatsheet/CHEATSHEET.md",
        "card": "kubectl-cheatsheet.png",
        "card_alt": "kubectl Cheatsheet one-page card — commands that actually work",
        "global_note": (
            "Placeholders follow the cheatsheet: web is a deployment/pod name and "
            "app.yaml is your manifest. Most commands act on the current namespace — "
            "add -n &lt;ns&gt; to target another one."
        ),
    },
}

CSS = """
:root{color-scheme:dark}
*{box-sizing:border-box}
body{margin:0;background:#0d1117;color:#e6edf3;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,'Helvetica Neue',Arial,sans-serif;line-height:1.6}
main{max-width:780px;margin:0 auto;padding:24px 16px 56px}
a{color:#58a6ff;text-decoration:none}
a:hover{text-decoration:underline}
.crumb{font-size:.85rem;color:#8b949e;margin-bottom:8px}
h1{font-size:1.5rem;line-height:1.3;margin:.2em 0 .35em;color:#f0f6fc}
h2{font-size:1.08rem;margin:1.7em 0 .45em;color:#f0f6fc}
.scenario{color:#c9d4e0;font-size:1.02rem;margin:.2em 0 1em}
pre{background:#161b22;border:1px solid #30363d;border-radius:8px;padding:14px 16px;overflow-x:auto;margin:0 0 1em}
code{font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,'Liberation Mono',monospace;font-size:.9rem}
pre code{white-space:pre;color:#e6edf3}
.note{background:#101c14;border:1px solid #1f4429;border-left:4px solid #3fb950;border-radius:6px;padding:10px 14px;margin:0 0 1.2em;color:#c9e8d1}
.note p{margin:.2em 0}
.ctx{background:#161b22;border:1px solid #30363d;border-radius:6px;padding:10px 14px;margin:0 0 1.2em;color:#9fb2c3;font-size:.92rem}
.ctx p{margin:.2em 0}
.card{margin:1.6em 0}
.card img{width:100%;max-width:430px;height:auto;border:1px solid #30363d;border-radius:10px;display:block}
.card figcaption{font-size:.85rem;color:#8b949e;margin-top:6px}
footer{border-top:1px solid #30363d;margin-top:2.2em;padding-top:1em;font-size:.92rem;color:#8b949e}
footer p{margin:.35em 0}
ul.pages{list-style:none;padding:0;margin:.4em 0 1.4em}
ul.pages li{padding:.34em 0;border-bottom:1px solid #21262d}
ul.pages li:last-child{border-bottom:none}
.intro{color:#c9d4e0}
"""

PAGES = [
    # ================= GIT (25) =================
    {"repo": "git", "slug": "config-user-name-email",
     "title": "How to set your Git username and email — git config",
     "scenario": "You just installed Git on a new machine and your first commit is refused or stamped with the wrong name.",
     "code": """git config --global user.name "Your Name"     # your display name
git config --global user.email "you@example.com"  # your email""",
     "note": "Every commit you make is stamped with this name and email. Do this once per machine."},
    {"repo": "git", "slug": "default-branch-main",
     "title": "How to make main the default branch for new Git repos",
     "scenario": "You want every repository you create from now on to start with a main branch instead of master.",
     "code": """git config --global init.defaultBranch main   # default branch for new repos""",
     "note": "New repos (and git init) will use main instead of master."},
    {"repo": "git", "slug": "status-short",
     "title": "How to see what has changed in Git, compactly — git status -sb",
     "scenario": "You want a compact overview of your branch, staged files and untracked files before you commit.",
     "code": """git status -sb   # -s = short, -b = show branch + ahead/behind""",
     "note": "Compact status: branch, staged (M), unstaged, untracked."},
    {"repo": "git", "slug": "stage-hunks-add-p",
     "title": "How to stage only part of a file in Git — git add -p",
     "scenario": "A file contains two separate changes and you only want to commit one of them.",
     "code": """git add -p        # walk through each hunk: y = stage, n = skip, s = split""",
     "note": "Pick exactly which hunks go into the commit — no more committing a file you did not mean to include."},
    {"repo": "git", "slug": "amend-last-commit",
     "title": "How to fix the last Git commit — git commit --amend",
     "scenario": "You just committed and immediately spot a typo in the message or a file you forgot to include.",
     "code": """git commit -m "Add login validation"   # normal commit
git commit --amend --no-edit           # fold new staged changes into the last commit""",
     "note": "--amend rewrites the most recent commit instead of adding a new one. Warning: don't amend commits already pushed."},
    {"repo": "git", "slug": "log-oneline-graph",
     "title": "How to view Git history as a graph — git log --oneline --graph",
     "scenario": "You need to understand how branches diverged without reading pages of log output.",
     "code": """git log --oneline --graph --all -20   # last 20 commits, all branches""",
     "note": "One line per commit, with branch lines drawn — the fastest way to understand a repo."},
    {"repo": "git", "slug": "unstage-file",
     "title": "How to unstage a file in Git and keep your edits — git restore --staged",
     "scenario": "You staged a file by accident and want it out of the next commit without losing the edits.",
     "code": """git restore --staged <file>   # unstage, keep edits""",
     "note": "Removes the file from the staging area; your working-tree changes stay."},
    {"repo": "git", "slug": "discard-file-changes",
     "title": "How to discard local changes in a file — git restore (permanent)",
     "scenario": "Your edits in one file turned out to be a dead end and you want the committed version back.",
     "code": """git restore <file>            # ⚠️ permanently discards unstaged changes in <file>""",
     "note": "Throws away unstaged edits in one file. There is no undo for this."},
    {"repo": "git", "slug": "undo-last-commit-reset-soft-mixed-hard",
     "title": "How to undo the last commit in Git — git reset --soft vs --mixed vs --hard",
     "scenario": "You committed too early, or to the wrong branch, and want the last commit undone.",
     "code": """git reset --soft HEAD~1    # undo last commit, keep changes staged
git reset --mixed HEAD~1   # undo last commit, unstage, keep edits (default)
git reset --hard HEAD~1   # ⚠️ undo last commit AND delete all changes""",
     "note": "--soft keeps everything staged, --mixed unstages but keeps edits, --hard deletes everything."},
    {"repo": "git", "slug": "revert-pushed-commit",
     "title": "How to undo a pushed commit safely — git revert",
     "scenario": "A commit that is already pushed and shared turns out to be wrong and must be undone safely.",
     "code": """git revert <commit-sha>   # safe undo; use this instead of reset on pushed work""",
     "note": "Creates a new commit that undoes an old one — safe for shared branches, unlike reset."},
    {"repo": "git", "slug": "list-branches",
     "title": "How to list all branches in Git, local and remote — git branch -a / -vv",
     "scenario": "You lost track of which branches exist locally and which ones track a remote.",
     "code": """git branch -a    # all local + remote branches
git branch -vv   # verbose: upstream + last commit per branch""",
     "note": "See all branches and which one you are on; -vv also shows upstream tracking."},
    {"repo": "git", "slug": "create-switch-branch",
     "title": "How to create and switch to a new branch in Git — checkout -b / switch -c",
     "scenario": "You are starting a new feature and want it isolated on its own branch.",
     "code": """git checkout -b feature/login   # classic
git switch -c feature/login     # modern equivalent""",
     "note": "One command to branch off and start working; switch -c is the modern spelling."},
    {"repo": "git", "slug": "delete-branch-local-and-remote",
     "title": "How to delete a Git branch locally and on the remote",
     "scenario": "A feature is merged and its branches are cluttering your local and remote lists.",
     "code": """git branch -d feature/login          # safe delete (fails if unmerged)
git branch -D feature/login          # ⚠️ force delete, even if unmerged
git push -d origin feature/login     # delete the branch on the remote too""",
     "note": "-d refuses if unmerged (safe); -D forces. Remote delete needs a push."},
    {"repo": "git", "slug": "rebase-onto-main",
     "title": "How to rebase your branch onto the latest main in Git",
     "scenario": "Your feature branch fell behind main and you want your commits replayed on top of the latest code.",
     "code": """git fetch origin             # get the latest main first
git rebase origin/main       # replay your commits on top of it""",
     "note": "The golden rule of rebase: never rebase commits that others have already pulled. Rewriting shared history breaks your teammates' repos — rebase your own private branches freely; use revert or merge for shared ones."},
    {"repo": "git", "slug": "squash-commits-interactive-rebase",
     "title": "How to squash or reword recent commits — git rebase -i",
     "scenario": "Your last few commits are a mess of fixups and you want them cleaned up before opening a pull request.",
     "code": """git rebase -i HEAD~3   # opens an editor: pick / squash / reword / drop""",
     "note": "Squash, reorder, reword, or drop your last few commits before sharing. Same golden rule as any rebase: only rewrite commits nobody else has pulled."},
    {"repo": "git", "slug": "rebase-continue-abort",
     "title": "How to finish or cancel a Git rebase — --continue / --abort",
     "scenario": "A rebase stopped on a conflict and you need to push through it — or bail out completely.",
     "code": """git rebase --continue   # after resolving conflicts and staging them
git rebase --abort      # cancel everything, back to pre-rebase state""",
     "note": "Resolve conflicts, stage them, then continue — or abort to return to where you started."},
    {"repo": "git", "slug": "stash-changes",
     "title": "How to stash unfinished work in Git — git stash push",
     "scenario": "Urgent work lands while you are mid-change and your working tree is full of unfinished edits.",
     "code": """git stash push -m "WIP: half-done login form"   # stash with a message""",
     "note": "Shelve your changes (tracked files) with a message, work on something else, come back later."},
    {"repo": "git", "slug": "stash-list-pop-apply",
     "title": "How to list, restore and drop Git stashes — pop vs apply",
     "scenario": "You stashed work earlier and now need to find it, restore it, or throw it away.",
     "code": """git stash list                 # see all stashes
git stash pop                  # restore newest stash and delete it
git stash apply stash@{1}      # restore a specific stash, keep it stored
git stash drop stash@{0}       # delete a stash you no longer need""",
     "note": "pop restores and deletes the stash; apply restores but keeps it."},
    {"repo": "git", "slug": "check-remote-url",
     "title": "How to check which URL a Git remote points to — git remote -v",
     "scenario": "Push or pull is failing and you first want to confirm the remote URLs are what you think they are.",
     "code": """git remote -v   # list remotes with fetch/push URLs""",
     "note": "Check which URLs origin (and others) point to — first step when push/pull misbehaves."},
    {"repo": "git", "slug": "fetch-prune",
     "title": "How to clean up stale remote branches in Git — git fetch --prune",
     "scenario": "Teammates deleted branches on the remote but your local list still shows them.",
     "code": """git fetch --prune   # update remote refs, clean up deleted branches""",
     "note": "Download remote changes without merging; --prune removes local tracking of deleted remote branches."},
    {"repo": "git", "slug": "pull-with-rebase",
     "title": "How to pull with rebase instead of merge — git pull --rebase",
     "scenario": "You want incoming changes integrated without a merge commit bubble in your history.",
     "code": """git pull --rebase   # fetch + rebase instead of fetch + merge""",
     "note": "Updates your branch by replaying your commits on top of incoming changes — no merge bubbles."},
    {"repo": "git", "slug": "push-set-upstream",
     "title": "How to push a branch and set its upstream — git push -u",
     "scenario": "You are pushing a branch for the first time and want future pushes to need no arguments.",
     "code": """git push -u origin feature/login              # first push: publish + set upstream
git branch --set-upstream-to=origin/main main  # re-point an existing branch's upstream""",
     "note": "-u links your branch to the remote so future git push / git pull need no arguments."},
    {"repo": "git", "slug": "recover-lost-commit-reflog",
     "title": "How to recover a lost commit in Git — git reflog",
     "scenario": "A reset or a deleted branch made a commit disappear — and you need it back.",
     "code": """git reflog                        # find the SHA of the "lost" commit
git checkout <sha>                # inspect it safely (detached HEAD)
git branch rescue <sha>           # or: put it on a new branch to keep it""",
     "note": "Almost nothing is truly lost: reflog records every move of HEAD for ~90 days."},
    {"repo": "git", "slug": "cherry-pick",
     "title": "How to copy one commit onto your branch — git cherry-pick",
     "scenario": "One commit on another branch is exactly what you need, without merging the whole branch.",
     "code": """git cherry-pick <commit-sha>   # apply that commit here""",
     "note": "Copy one specific commit (by SHA) from anywhere onto your current branch."},
    {"repo": "git", "slug": "bisect-find-bad-commit",
     "title": "How to find the commit that broke your code — git bisect",
     "scenario": "Something broke somewhere between the last release and now, and reading every commit would take days.",
     "code": """git bisect start
git bisect bad                    # current HEAD is broken
git bisect good v1.2.0            # v1.2.0 was fine
# git checks out commits; test each, then: git bisect good|bad
git bisect reset                  # done: back to where you started""",
     "note": "Bisect binary-searches history between a known-good and a known-bad commit."},
    # ================= SQL (25) =================
    {"repo": "sql", "slug": "filter-rows-where",
     "title": "How to filter rows in SQL — WHERE",
     "scenario": "You need only the rows that meet a condition — here, employees earning more than 80000, best paid first.",
     "code": """SELECT name, salary FROM employees WHERE salary > 80000 ORDER BY salary DESC;
-- Alice 120000 / Bob 95000 / Carol 88000""",
     "note": None},
    {"repo": "sql", "slug": "top-n-rows-limit",
     "title": "How to get the top N rows in SQL — ORDER BY ... LIMIT",
     "scenario": "You want a leaderboard: just the three highest salaries in the table.",
     "code": """SELECT name, salary FROM employees ORDER BY salary DESC LIMIT 3;
-- Top 3 salaries: Alice / Bob / Carol
-- LIMIT works in MySQL / PostgreSQL / SQLite; SQL Server uses TOP 3, the SQL:2008 spelling FETCH FIRST 3 ROWS ONLY works in Oracle and PostgreSQL 10+""",
     "note": None},
    {"repo": "sql", "slug": "select-distinct",
     "title": "How to remove duplicate values from a result — SELECT DISTINCT",
     "scenario": "A column repeats the same values across rows and you want each value once.",
     "code": """SELECT DISTINCT dept_id FROM employees;
-- 1 / 2 / 3 / NULL (Grace has no department; NULL counts as a value here)""",
     "note": None},
    {"repo": "sql", "slug": "like-pattern-matching",
     "title": "How to match text patterns in SQL — LIKE % and _",
     "scenario": "You need names starting with a given letter, or any text pattern, without loading the whole table.",
     "code": """SELECT name FROM employees WHERE name LIKE 'A%';
-- Alice. % matches any run of characters, _ matches exactly one
-- Dialect: LIKE is case-insensitive for ASCII in SQLite / MySQL, but case-sensitive in PostgreSQL.
--          PostgreSQL also has ILIKE for case-insensitive matching (PG only; MySQL / SQLite don't have it)""",
     "note": None},
    {"repo": "sql", "slug": "in-and-between",
     "title": "How to filter by a set or a range in SQL — IN / BETWEEN",
     "scenario": "You want rows belonging to a short list of departments with salaries inside a range.",
     "code": """SELECT name, salary FROM employees
WHERE dept_id IN (1, 2) AND salary BETWEEN 70000 AND 100000
ORDER BY salary DESC;
-- Bob 95000 / Carol 88000 / David 72000 (BETWEEN includes both endpoints)""",
     "note": None},
    {"repo": "sql", "slug": "count-sum-avg",
     "title": "How to count, sum and average in SQL — COUNT / SUM / AVG",
     "scenario": "You need headcount, total payroll and average salary in a single result row.",
     "code": """SELECT COUNT(*) AS headcount, SUM(salary) AS total_payroll, AVG(salary) AS avg_salary FROM employees;
-- 7 people / total 557000 / average 79571.43""",
     "note": None},
    {"repo": "sql", "slug": "group-by",
     "title": "How to compute per-group statistics in SQL — GROUP BY",
     "scenario": "Totals for the whole table are not enough — you need the numbers per department.",
     "code": """SELECT dept_id, COUNT(*) AS n, AVG(salary) AS avg_salary FROM employees GROUP BY dept_id;
-- dept 1: 3 people, avg 101000; dept 2: 2, 70000; dept 3: 1, 54000; NULL group: 1, 60000""",
     "note": None},
    {"repo": "sql", "slug": "having-vs-where",
     "title": "HAVING vs WHERE in SQL — filtering groups, not rows",
     "scenario": "You want to keep only the groups whose aggregate passes a threshold, such as departments averaging over 60000.",
     "code": """SELECT dept_id, AVG(salary) AS avg_salary FROM employees GROUP BY dept_id HAVING AVG(salary) > 60000;
-- Only dept 1 (101000) and dept 2 (70000) survive
-- WHERE filters rows before grouping; HAVING filters groups after. Don't mix them up""",
     "note": None},
    {"repo": "sql", "slug": "case-when-conditional-aggregation",
     "title": "How to count with conditions in SQL — CASE WHEN inside aggregates",
     "scenario": "You want several differently-defined metrics — total staff and high earners — from one pass over the table.",
     "code": """SELECT COUNT(*) AS total,
       SUM(CASE WHEN salary >= 90000 THEN 1 ELSE 0 END) AS high_earners
FROM employees;
-- total 7 / high earners 2 (Alice, Bob). Several metrics with different rules in one pass""",
     "note": None},
    {"repo": "sql", "slug": "inner-join",
     "title": "INNER JOIN in SQL — only rows that match in both tables",
     "scenario": "You want each employee shown with their department name, and only employees who have one.",
     "code": """SELECT e.name, d.name AS dept FROM employees e JOIN departments d ON e.dept_id = d.id;
-- 6 rows: Grace has no department and drops out""",
     "note": None},
    {"repo": "sql", "slug": "left-join",
     "title": "LEFT JOIN in SQL — keep every row of the left table",
     "scenario": "You need the full roster, including people with no department assigned.",
     "code": """SELECT e.name, d.name AS dept FROM employees e LEFT JOIN departments d ON e.dept_id = d.id;
-- 7 rows: Grace is there with dept = NULL. Full roster → LEFT JOIN; only matched → INNER JOIN""",
     "note": None},
    {"repo": "sql", "slug": "find-rows-with-no-match",
     "title": "How to find rows with no match in SQL — LEFT JOIN ... IS NULL",
     "scenario": "You are hunting rows that should have related records but do not — employees who never placed an order.",
     "code": """SELECT e.name FROM employees e LEFT JOIN orders o ON o.emp_id = e.id WHERE o.id IS NULL;
-- Carol / Frank / Grace: employees who never ordered. The classic orphan-finder""",
     "note": "The classic orphan-finder: keep every left-table row, then keep only the ones where the joined table's key came back NULL."},
    {"repo": "sql", "slug": "self-join",
     "title": "How to join a table to itself in SQL — self join for org charts",
     "scenario": "The hierarchy lives in one table: each employee row points at their manager in the same table.",
     "code": """SELECT e.name AS employee, m.name AS manager
FROM employees e LEFT JOIN employees m ON e.manager_id = m.id;
-- Bob→Alice, Carol→Alice, Eve→David; people without a manager get NULL
-- Org charts, threaded comments, any hierarchy stored in one table works this way""",
     "note": None},
    {"repo": "sql", "slug": "join-three-tables-aggregate",
     "title": "How to join three tables and aggregate in SQL — orders per department",
     "scenario": "The answer spans three tables: order counts and revenue grouped by department.",
     "code": """SELECT d.name AS dept, COUNT(o.id) AS order_count, SUM(o.amount) AS revenue
FROM departments d
JOIN employees e ON e.dept_id = d.id
JOIN orders o ON o.emp_id = e.id
GROUP BY d.id, d.name;
-- Engineering: 3 orders, 2370.50; Sales: 4 orders, 1650.74; HR has no orders and doesn't appear (INNER JOIN)""",
     "note": None},
    {"repo": "sql", "slug": "subquery-above-average",
     "title": "How to compare rows against an overall average in SQL — scalar subquery",
     "scenario": "You want everyone paid more than the company-wide average salary.",
     "code": """SELECT name, salary FROM employees WHERE salary > (SELECT AVG(salary) FROM employees);
-- Alice / Bob / Carol: everyone paid above the company average (79571.43)""",
     "note": None},
    {"repo": "sql", "slug": "exists-check",
     "title": "How to check that a related row exists in SQL — EXISTS",
     "scenario": "You only care whether a matching row exists at all — departments with at least one employee earning over 100k.",
     "code": """SELECT d.name FROM departments d
WHERE EXISTS (SELECT 1 FROM employees e WHERE e.dept_id = d.id AND e.salary > 100000);
-- Engineering: departments with at least one employee earning over 100k.
-- EXISTS only cares whether a row exists — a common pick for large tables""",
     "note": None},
    {"repo": "sql", "slug": "cte-with",
     "title": "How to name an intermediate result in SQL — WITH (CTE)",
     "scenario": "A query needs an intermediate result — each department's average salary — before the real question can be asked.",
     "code": """WITH dept_avg AS (
  SELECT dept_id, AVG(salary) AS avg_salary FROM employees GROUP BY dept_id
)
SELECT e.name, e.salary FROM employees e
JOIN dept_avg a ON e.dept_id = a.dept_id
WHERE e.salary > a.avg_salary;
-- Alice (above dept avg 101000) / David (above 70000): paid more than their own department's average
-- CTEs make complex queries read top-to-bottom instead of inside-out; MySQL 8.0+ / PostgreSQL / SQLite 3.8.8+ support them""",
     "note": None},
    {"repo": "sql", "slug": "rank-window-function",
     "title": "How to rank rows inside groups in SQL — RANK() OVER (PARTITION BY ...)",
     "scenario": "You want a ranking inside each group, such as salary rank per department, without collapsing the rows.",
     "code": """SELECT name, dept_id, salary,
       RANK() OVER (PARTITION BY dept_id ORDER BY salary DESC) AS rnk
FROM employees;
-- In dept 1: Alice 1, Bob 2, Carol 3; in dept 2: David 1, Eve 2
-- GROUP BY collapses rows; window functions keep every row and attach a rank — that's the key difference
-- Dialect: MySQL 8.0+ / PostgreSQL / SQLite 3.25+. Older MySQL can't do this""",
     "note": None},
    {"repo": "sql", "slug": "insert-row",
     "title": "How to insert a row in SQL — INSERT INTO ... VALUES",
     "scenario": "You are adding one new employee row and want the columns spelled out explicitly.",
     "code": """INSERT INTO employees (id, name, dept_id, salary, manager_id, hired_on)
VALUES (8, 'Henry', 2, 71000, 4, '2024-06-01');
-- Always name the columns; multi-row inserts chain more (...) groups after VALUES""",
     "note": None},
    {"repo": "sql", "slug": "update-rows-where",
     "title": "How to update rows in SQL — UPDATE ... WHERE (and the mistake that updates the whole table)",
     "scenario": "One employee got a raise and exactly one row must change.",
     "code": """UPDATE employees SET salary = salary + 5000 WHERE name = 'Eve';
-- Eve: 68000 → 73000, exactly 1 row affected
-- ⚠️ Forget the WHERE and you update the whole table. Run a SELECT with the same condition first to count the rows""",
     "note": None},
    {"repo": "sql", "slug": "delete-rows-where",
     "title": "How to delete rows in SQL — DELETE ... WHERE",
     "scenario": "Orders below 100 should be removed from the table.",
     "code": """DELETE FROM orders WHERE amount < 100;
-- Removes 1 row (the 89.99 order). Without WHERE it empties the table
-- Business data is usually soft-deleted instead (a deleted_at flag), not hard-DELETEd""",
     "note": None},
    {"repo": "sql", "slug": "transactions-begin-commit",
     "title": "How SQL transactions work — BEGIN / COMMIT / ROLLBACK",
     "scenario": "Several changes belong together: either all of them land, or none of them does.",
     "code": """BEGIN;
UPDATE employees SET dept_id = 2 WHERE name = 'Frank';
COMMIT;
-- Frank moves from HR to Sales. If any step fails, ROLLBACK undoes everything as if it never happened
-- Money transfers and stock deductions must run inside a transaction. In MySQL, START TRANSACTION is the same as BEGIN""",
     "note": None},
    {"repo": "sql", "slug": "upsert-on-conflict",
     "title": "How to upsert in SQL — INSERT ... ON CONFLICT DO UPDATE",
     "scenario": "A row may or may not exist yet — insert it if missing, update it if present, in one statement.",
     "code": """INSERT INTO departments (id, name) VALUES (3, 'People')
ON CONFLICT(id) DO UPDATE SET name = excluded.name;
-- id=3 already exists → the department is renamed HR → People; if it didn't exist, it would be inserted
-- This is the SQLite / PostgreSQL spelling. MySQL: ON DUPLICATE KEY UPDATE name = VALUES(name) — but VALUES() is deprecated since MySQL 8.0.20; modern spelling uses a row alias: ... VALUES (3, 'People') AS new ON DUPLICATE KEY UPDATE name = new.name""",
     "note": None},
    {"repo": "sql", "slug": "create-table",
     "title": "How to create a table in SQL — CREATE TABLE with keys and foreign keys",
     "scenario": "You are defining a new table with a primary key, required columns and a foreign key to another table.",
     "code": """CREATE TABLE projects (
  id INTEGER PRIMARY KEY,
  title TEXT NOT NULL,
  lead_id INTEGER REFERENCES employees(id)
);
-- Primary keys, NOT NULL and foreign keys belong in the schema, not in application code
-- SQLite note: foreign keys are parsed but NOT enforced unless you run PRAGMA foreign_keys = ON""",
     "note": "Dialect: INTEGER PRIMARY KEY is SQLite's auto-incrementing row id; MySQL writes INT AUTO_INCREMENT PRIMARY KEY; PostgreSQL writes INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY (or the older SERIAL)."},
    {"repo": "sql", "slug": "create-index",
     "title": "How to speed up frequent lookups in SQL — CREATE INDEX",
     "scenario": "Queries filtering on dept_id are scanning the whole employees table and getting slow.",
     "code": """CREATE INDEX idx_employees_dept ON employees(dept_id);
-- After this, WHERE dept_id = ? uses the index instead of scanning the whole table
-- Verify: EXPLAIN QUERY PLAN in SQLite, EXPLAIN in MySQL / PostgreSQL
-- Every index slows writes down, so index the columns you actually filter on — not everything""",
     "note": None},
    # ================= KUBECTL (25) =================
    {"repo": "kubectl", "slug": "check-current-cluster",
     "title": "How to check which cluster kubectl is talking to — kubectl cluster-info",
     "scenario": "Before changing anything, you want proof of which cluster your commands will hit.",
     "code": """kubectl cluster-info          # control plane address + core service endpoints""",
     "note": None},
    {"repo": "kubectl", "slug": "get-pods-all-namespaces",
     "title": "How to list every pod in every namespace — kubectl get pods -A",
     "scenario": "A pod is misbehaving somewhere but you do not know its namespace.",
     "code": """kubectl get pods -A           # -A = --all-namespaces; drop it for the current ns only
kubectl get pods -o wide      # also: pod IP and which node it runs on
kubectl get pods -w           # -w = watch: stream changes live (Ctrl+C to stop)""",
     "note": None},
    {"repo": "kubectl", "slug": "describe-pod",
     "title": "How to find out why a pod is pending or crashing — kubectl describe",
     "scenario": "A pod is stuck Pending or keeps crashing and you need the events that explain why.",
     "code": """kubectl describe pod web-6d9f7c5b4-x2abc   # why pending/crashing? read the Events at the bottom
kubectl describe node node-1               # capacity, allocatable, taints, conditions""",
     "note": "describe shows full detail plus the Events section at the bottom — troubleshooting station #1."},
    {"repo": "kubectl", "slug": "get-events-sorted",
     "title": "How to see cluster events in order — kubectl get events --sort-by",
     "scenario": "You want the cluster's own story in time order — scheduling failures, pull errors, OOM kills.",
     "code": """kubectl get events --sort-by=.lastTimestamp        # OOMKilled, FailedScheduling, pull errors live here
kubectl get events -n prod --sort-by=.lastTimestamp""",
     "note": None},
    {"repo": "kubectl", "slug": "top-usage",
     "title": "How to check live CPU and memory usage — kubectl top",
     "scenario": "You suspect a pod or node is running out of CPU or memory and want live numbers.",
     "code": """kubectl top pods              # per-pod usage (needs the metrics-server installed)
kubectl top nodes             # per-node usage""",
     "note": None},
    {"repo": "kubectl", "slug": "apply-manifest",
     "title": "How to deploy or update from a manifest — kubectl apply -f",
     "scenario": "You have a manifest file and want the cluster to match what it declares.",
     "code": """kubectl apply -f app.yaml     # create or update whatever the file declares
kubectl apply -f ./k8s/       # a whole directory of manifests""",
     "note": None},
    {"repo": "kubectl", "slug": "create-deployment",
     "title": "How to create a deployment in one line — kubectl create deployment",
     "scenario": "You need a simple deployment running right now, without writing YAML first.",
     "code": """kubectl create deployment web --image=nginx:1.27 --replicas=3
kubectl expose deployment web --type=LoadBalancer --port=80   # give it a Service right away""",
     "note": None},
    {"repo": "kubectl", "slug": "scale-deployment",
     "title": "How to change a deployment's replica count — kubectl scale",
     "scenario": "Traffic spiked — or you want a deployment paused — by changing its replica count.",
     "code": """kubectl scale deployment web --replicas=5
kubectl scale deployment web --replicas=0    # "stop" it without deleting anything""",
     "note": None},
    {"repo": "kubectl", "slug": "set-image",
     "title": "How to update a deployment's image — kubectl set image",
     "scenario": "A new image version is ready and the deployment should roll over to it.",
     "code": """kubectl set image deployment/web web=nginx:1.28   # syntax: container-name=new-image""",
     "note": "Bumping the image triggers a rolling update."},
    {"repo": "kubectl", "slug": "rollout-restart",
     "title": "How to restart all pods of a deployment — kubectl rollout restart",
     "scenario": "Pods need a fresh start — for example to pick up a reloaded ConfigMap — with no config change.",
     "code": """kubectl rollout restart deployment/web   # fresh pods pick up reloaded ConfigMaps/Secrets""",
     "note": "Restart all pods without changing the configuration."},
    {"repo": "kubectl", "slug": "rollout-status",
     "title": "How to watch a rollout until it finishes — kubectl rollout status",
     "scenario": "You kicked off an update and want to block until it has fully finished, for example in CI.",
     "code": """kubectl rollout status deployment/web    # blocks until done — safe to use in CI scripts""",
     "note": None},
    {"repo": "kubectl", "slug": "rollout-history-undo",
     "title": "How to roll back a deployment — kubectl rollout history / undo",
     "scenario": "The new release is broken and you need the previous revision back, fast.",
     "code": """kubectl rollout history deployment/web        # list revisions
kubectl rollout undo deployment/web           # back to the previous revision
kubectl rollout undo deployment/web --to-revision=2""",
     "note": None},
    {"repo": "kubectl", "slug": "logs-pod",
     "title": "How to read a pod's logs — kubectl logs",
     "scenario": "The application misbehaves and its stdout is the first place to look.",
     "code": """kubectl logs web-6d9f7c5b4-x2abc            # stdout/stderr of the (single) container
kubectl logs web-6d9f7c5b4-x2abc -c api     # multi-container pod? pick one with -c""",
     "note": None},
    {"repo": "kubectl", "slug": "logs-follow-tail",
     "title": "How to follow pod logs live — kubectl logs -f --tail",
     "scenario": "You want the last hundred lines of log and then watch new lines as they happen.",
     "code": """kubectl logs -f --tail=100 web-6d9f7c5b4-x2abc   # last 100 lines, then stream
kubectl logs -f -l app=web                       # follow by label, across replicas""",
     "note": None},
    {"repo": "kubectl", "slug": "logs-previous-crashed-container",
     "title": "How to get logs from a crashed container — kubectl logs -p (CrashLoopBackOff)",
     "scenario": "The container keeps restarting (CrashLoopBackOff) and the current logs only show the new instance starting up.",
     "code": """kubectl logs -p web-6d9f7c5b4-x2abc   # CrashLoopBackOff? this is where the real error is""",
     "note": "This reads the logs of the previous, crashed container instance — where the real error usually is."},
    {"repo": "kubectl", "slug": "exec-shell",
     "title": "How to open a shell inside a running container — kubectl exec -it",
     "scenario": "You need to look around inside the running container — files, environment, processes.",
     "code": """kubectl exec -it web-6d9f7c5b4-x2abc -- sh    # sh exists almost everywhere; try bash too
kubectl exec web-6d9f7c5b4-x2abc -- env       # or run a single command, no shell""",
     "note": None},
    {"repo": "kubectl", "slug": "cp-copy-files",
     "title": "How to copy files in and out of a container — kubectl cp",
     "scenario": "A file inside the container — a dump or a log — needs to come out, or a config needs to go in.",
     "code": """kubectl cp web-6d9f7c5b4-x2abc:/tmp/dump.log ./   # container -> local
kubectl cp ./config.yaml web-6d9f7c5b4-x2abc:/etc/app/   # needs tar inside the container""",
     "note": None},
    {"repo": "kubectl", "slug": "get-resources-by-label",
     "title": "How to query resources by label — kubectl get pods -l",
     "scenario": "You want just the resources belonging to one app, selected by label, or several resource types at once.",
     "code": """kubectl get pods,svc,deploy                 # comma-separated types in one call
kubectl get pods -l app=web                 # filter by label selector
kubectl get all                             # common resources in the current ns (not literally everything)""",
     "note": None},
    {"repo": "kubectl", "slug": "delete-pod-deployment",
     "title": "How to delete pods and deployments — kubectl delete",
     "scenario": "You want a pod restarted by its controller, or a deployment removed entirely.",
     "code": """kubectl delete pod web-6d9f7c5b4-x2abc   # the controller recreates it — that's the point (self-healing)
kubectl delete deployment web            # delete the deployment itself (and its pods)
kubectl delete -f app.yaml               # delete everything a manifest created""",
     "note": "Deleting a pod is safe by design: its controller recreates it (self-healing). Deleting the deployment removes the deployment itself and its pods."},
    {"repo": "kubectl", "slug": "port-forward",
     "title": "How to access a cluster service from your laptop — kubectl port-forward",
     "scenario": "A service is not exposed publicly but you need it in your local browser.",
     "code": """kubectl port-forward svc/web 8080:80     # now open http://localhost:8080
kubectl port-forward pod/web-6d9f7c5b4-x2abc 8080:80""",
     "note": "Map a cluster service to your laptop, then open it locally."},
    {"repo": "kubectl", "slug": "get-contexts",
     "title": "How to list the clusters you can reach — kubectl config get-contexts",
     "scenario": "You work with several clusters and want to see which ones you can reach and which is active.",
     "code": """kubectl config get-contexts        # the * marks the current one
kubectl config current-context     # just print the current context name""",
     "note": None},
    {"repo": "kubectl", "slug": "switch-context",
     "title": "How to switch Kubernetes clusters — kubectl config use-context",
     "scenario": "You need to run commands against a different cluster than the current one.",
     "code": """kubectl config use-context prod-cluster   # ⚠️ double-check before running prod commands""",
     "note": "Double-check the context before running production commands."},
    {"repo": "kubectl", "slug": "list-create-namespaces",
     "title": "How to list and create namespaces — kubectl get ns / create namespace",
     "scenario": "You want to see the namespaces in the cluster, or create a fresh one for a new environment.",
     "code": """kubectl get ns                     # list namespaces (ns = the short name)
kubectl create namespace dev       # make a new one""",
     "note": None},
    {"repo": "kubectl", "slug": "set-default-namespace",
     "title": "How to set a default namespace and stop typing -n — kubectl config set-context",
     "scenario": "You type -n dev on every single command and want your default namespace pinned instead.",
     "code": """kubectl config set-context --current --namespace=dev   # stop typing -n dev on every command""",
     "note": None},
    {"repo": "kubectl", "slug": "debug-ephemeral-container",
     "title": "How to debug a running pod without restarting it — kubectl debug",
     "scenario": "A slim container has no shell or tools, and restarting it would destroy the evidence.",
     "code": """kubectl debug -it web-6d9f7c5b4-x2abc --image=busybox:1.36 --target=web
# 1.25+ clusters: ephemeral containers are stable — debug without restarting the pod
kubectl debug node/node-1 --image=busybox:1.36   # node-level debugging shell""",
     "note": "kubectl debug attaches an ephemeral debug container to a running pod — on 1.25+ clusters ephemeral containers are stable, so you debug without restarting the pod."},
]


def norm(s):
    return " ".join(s.split())


def verify_against_sources():
    """Every code line must exist in the repo's CHEATSHEET.md (whitespace-normalized)."""
    errors = []
    for key, repo in REPOS.items():
        path = os.path.join(SRC_DIR, repo["source"])
        with open(path, encoding="utf-8") as f:
            src_lines = {norm(line) for line in f}
        for p in PAGES:
            if p["repo"] != key:
                continue
            for line in p["code"].split("\n"):
                if line.strip() and norm(line) not in src_lines:
                    errors.append(f"{key}/{p['slug']}: line not in source: {line!r}")
    return errors


def esc(s):
    return html.escape(s, quote=True)


def render_page(p):
    repo = REPOS[p["repo"]]
    title = esc(p["title"])
    parts = []
    parts.append("<!DOCTYPE html>")
    parts.append('<html lang="en">')
    parts.append("<head>")
    parts.append('<meta charset="utf-8">')
    parts.append('<meta name="viewport" content="width=device-width, initial-scale=1">')
    parts.append(f"<title>{title}</title>")
    parts.append(f'<meta name="description" content="{esc(p["scenario"])}">')
    parts.append(f"<style>{CSS}</style>")
    parts.append("</head>")
    parts.append("<body>")
    parts.append("<main>")
    parts.append(f'<p class="crumb"><a href="../index.html">{SITE_NAME}</a> / '
                 f'<a href="{repo["repo_url"]}">{esc(repo["name"])}</a></p>')
    parts.append(f"<h1>{title}</h1>")
    parts.append(f'<p class="scenario">{esc(p["scenario"])}</p>')
    if repo["global_note"]:
        parts.append(f'<div class="ctx"><p>{repo["global_note"]}</p></div>')
    parts.append(f"<pre><code>{esc(p['code'])}</code></pre>")
    if p["note"]:
        parts.append("<h2>Good to know</h2>")
        parts.append(f'<div class="note"><p>{esc(p["note"])}</p></div>')
    parts.append(f'<figure class="card"><a href="{repo["repo_url"]}">'
                 f'<img src="../images/{repo["card"]}" alt="{esc(repo["card_alt"])}" loading="lazy"></a>'
                 f'<figcaption>The full one-page card — {esc(repo["name"])}. '
                 f'<a href="{repo["repo_url"]}">Get the complete cheatsheet on GitHub</a></figcaption></figure>')
    parts.append("<footer>")
    parts.append(f'<p>Full cheatsheet: <a href="{repo["repo_url"]}">{esc(repo["name"])} on GitHub</a> '
                 f'— every command on this page comes from it, tested and verified.</p>')
    parts.append(f'<p>More cheatsheets and tools by the author: <a href="{AUTHOR_URL}">github.com/Ezra-Zhao</a></p>')
    parts.append(f'<p><a href="../index.html">&larr; All command pages</a></p>')
    parts.append("</footer>")
    parts.append("</main>")
    parts.append("</body>")
    parts.append("</html>")
    return "\n".join(parts) + "\n"


def render_index():
    parts = []
    parts.append("<!DOCTYPE html>")
    parts.append('<html lang="en">')
    parts.append("<head>")
    parts.append('<meta charset="utf-8">')
    parts.append('<meta name="viewport" content="width=device-width, initial-scale=1">')
    parts.append(f"<title>{SITE_NAME} — Git, SQL &amp; kubectl, one question per page</title>")
    parts.append('<meta name="description" content="One command, one real-world scenario, one page. '
                 'Searchable command pages for Git, SQL and kubectl, drawn from tested open-source cheatsheets.">')
    parts.append(f"<style>{CSS}</style>")
    parts.append("</head>")
    parts.append("<body>")
    parts.append("<main>")
    parts.append(f"<h1>{SITE_NAME}</h1>")
    parts.append('<p class="intro">One command, one real-world scenario, one page. '
                 'Every page answers a single question developers actually search for, '
                 'with a command copied from a tested, open-source cheatsheet — '
                 'no invented flags, no untested syntax.</p>')
    for key, repo in REPOS.items():
        repo_pages = [p for p in PAGES if p["repo"] == key]
        parts.append(f'<h2>{esc(repo["name"])} — {len(repo_pages)} pages</h2>')
        parts.append(f'<p class="intro">Full cheatsheet: <a href="{repo["repo_url"]}">{repo["repo_url"]}</a></p>')
        parts.append('<ul class="pages">')
        for p in repo_pages:
            parts.append(f'<li><a href="{key}/{p["slug"]}.html">{esc(p["title"])}</a></li>')
        parts.append("</ul>")
    parts.append("<footer>")
    parts.append(f'<p>All cheatsheets by <a href="{AUTHOR_URL}">Ezra-Zhao on GitHub</a> — '
                 'free, MIT-licensed, in English with Chinese / Spanish / Portuguese editions.</p>')
    parts.append("</footer>")
    parts.append("</main>")
    parts.append("</body>")
    parts.append("</html>")
    return "\n".join(parts) + "\n"


def render_sitemap():
    urls = [SITE_URL]
    for p in PAGES:
        urls.append(f"{SITE_URL}{p['repo']}/{p['slug']}.html")
    out = ['<?xml version="1.0" encoding="UTF-8"?>',
           '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for u in urls:
        out.append(f"<url><loc>{u}</loc></url>")
    out.append("</urlset>")
    return "\n".join(out) + "\n"


def main():
    errors = verify_against_sources()
    if errors:
        print("VERIFICATION FAILED — these code lines are not in the source cheatsheets:")
        for e in errors:
            print(" -", e)
        sys.exit(1)
    total_lines = sum(len([l for l in p["code"].split("\n") if l.strip()]) for p in PAGES)
    print(f"verification OK: {total_lines} code lines across {len(PAGES)} pages all found in source files")

    for p in PAGES:
        path = os.path.join(BASE, p["repo"], p["slug"] + ".html")
        with open(path, "w", encoding="utf-8") as f:
            f.write(render_page(p))
    with open(os.path.join(BASE, "index.html"), "w", encoding="utf-8") as f:
        f.write(render_index())
    with open(os.path.join(BASE, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write(render_sitemap())
    with open(os.path.join(BASE, "robots.txt"), "w", encoding="utf-8") as f:
        f.write(f"User-agent: *\nAllow: /\n\nSitemap: {SITE_URL}sitemap.xml\n")

    for key in REPOS:
        n = len([p for p in PAGES if p["repo"] == key])
        print(f"{key}: {n} pages")
    print(f"total: {len(PAGES)} pages + index.html + sitemap.xml + robots.txt")


if __name__ == "__main__":
    main()
