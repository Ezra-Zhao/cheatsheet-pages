"""Expansion data for cheatsheet-pages batch 6: grep.

Same contract as batches 2-5: every code line below was transcribed verbatim
from grep-cheatsheet/CHEATSHEET.md and is re-verified against the
source by generate.py's verify_against_sources() on every build.
"""

REPOS6 = {
    "grep": {
        "name": "grep Cheatsheet",
        "repo_url": "https://github.com/Ezra-Zhao/grep-cheatsheet",
        "source": "grep-cheatsheet/CHEATSHEET.md",
        "card": "grep-cheatsheet.png",
        "card_alt": "grep Cheatsheet one-page card — 30 run-verified commands",
        "global_note": (
            "Examples run against a small fixture tree (proj/ with logs, "
            "sources, a binary file and symlinks) — swap in your own paths. "
            "Commands run-verified on GNU grep 3.11; BSD grep differences "
            "are noted in the sheet."
        ),
    },
}

PAGES6 = [
    {"repo": "grep", "slug": "search-lines-matching-pattern",
     "title": "How to print the lines that match a pattern — plain grep",
     "scenario": "A log file, and you want only the lines that mention the failure.",
     "code": """grep 'ERROR' proj/app.log    # prints the 2 lines that contain ERROR""",
     "note": "The pattern is a regular expression tested against each line. Case matters: a lowercase error line is not printed. A match sets exit status 0, no match 1."},
    {"repo": "grep", "slug": "ignore-case-search",
     "title": "How to search case-insensitively — grep -i",
     "scenario": "The same word shows up as Error, ERROR and error across your logs.",
     "code": """grep -i 'error' proj/server.log   # 2 lines: "Error mixed case failure" and "ERROR disk full"
grep -i 'error' proj/app.log      # 3 lines: the two ERROR lines plus the lowercase "error" line""",
     "note": "-i folds case in both the pattern and the text. Log files never agree on capitalization, so this is the default reflex for incident hunting."},
    {"repo": "grep", "slug": "invert-match-exclude-lines",
     "title": "How to show everything EXCEPT matching lines — grep -v",
     "scenario": "The log is 95% routine INFO lines. You want the other 5%.",
     "code": """grep -v 'INFO' proj/app.log    # 4 lines: everything that is NOT an INFO line""",
     "note": "-v selects the lines that do not match. It is the whole command for 'the log with the noise removed'."},
    {"repo": "grep", "slug": "count-matching-lines",
     "title": "How to count matching lines — grep -c, and its exit-code trap",
     "scenario": "How many errors per file — and your script then misreads the answer.",
     "code": """grep -c 'ERROR' proj/app.log proj/server.log   # proj/app.log:2  proj/server.log:1 — one count per file
grep -c 'ZZZ' proj/app.log                     # prints 0 — and still exits 1, because no line was selected""",
     "note": "-c counts lines that match, not occurrences — a line with three matches still counts once. And a printed 0 still comes with exit status 1."},
    {"repo": "grep", "slug": "show-line-numbers",
     "title": "How to get line numbers for matches — grep -n",
     "scenario": "You found the bad lines and need to point an editor (or a ticket) at them.",
     "code": """grep -n 'ERROR' proj/app.log    # 3:…failed to open config   6:…timeout after 30s""",
     "note": "Each match is prefixed with its 1-based line number in its file. With several files the form becomes file:line:content."},
    {"repo": "grep", "slug": "list-files-with-or-without-matches",
     "title": "How to list files that match — and files that don't — grep -l and -L",
     "scenario": "Fifty files; first question is just: which ones even mention this?",
     "code": """grep -l 'ERROR' proj/app.log proj/server.log proj/notes.txt   # proj/app.log, proj/server.log
grep -L 'ERROR' proj/app.log proj/server.log proj/notes.txt   # proj/notes.txt — the one WITHOUT any match""",
     "note": "-l stops at each file's first match and prints only the name; -L is the exact complement. The building block of grep -l … | xargs pipelines."},
    {"repo": "grep", "slug": "recursive-search-directory-tree",
     "title": "How to search a whole directory tree — grep -r",
     "scenario": "The string is somewhere in this project. You don't know which file.",
     "code": """grep -r 'ERROR' proj    # every match under proj/, each prefixed with its file name""",
     "note": "Recursion prefixes every line with its path. Two verified behaviors: symlinks found inside the tree are skipped, and a matching binary file is reported as a one-line notice on stderr, not printed. With no path, grep -r searches the working directory."},
    {"repo": "grep", "slug": "recursive-follow-symlinks",
     "title": "How to make recursion follow symlinks — grep -R vs -r",
     "scenario": "Your recursive search silently missed files that live behind symlinks.",
     "code": """grep -R 'ERROR' proj     # now proj/link.log:… and proj/extlink/deep.log:… appear too
grep 'ERROR' proj/link.log   # a symlink named ON the command line is followed even by plain grep""",
     "note": "-R follows symlinks wherever it meets them; -r follows only the ones named on the command line. With -R the same file can arrive by two paths and appear twice."},
    {"repo": "grep", "slug": "include-exclude-file-filters",
     "title": "How to aim a recursive search — --include, --exclude, --exclude-dir",
     "scenario": "Only the logs. Or everything except that vendor directory.",
     "code": """grep -r --include='*.log' 'ERROR' proj     # only *.log files: the .c/.py sources are never opened
grep -r --exclude-dir='sub' 'ERROR' proj   # the whole sub/ subtree is pruned from the search""",
     "note": "The globs match each file's base name during recursion. --include whitelists, --exclude blacklists files, --exclude-dir prunes directories before grep descends into them."},
    {"repo": "grep", "slug": "extended-regex-vs-basic",
     "title": "How extended regex differs from basic — grep -E and the backslash trap",
     "scenario": "Your alternation matched nothing — because in basic regex, | is a literal character.",
     "code": """grep -E 'ERROR|WARN' proj/app.log     # 3 lines — alternation with a bare |
grep 'ERROR\\|WARN' proj/app.log       # the SAME search in default BRE: the | needs a backslash""",
     "note": "Default BRE treats | + ? ( ) { } as literals and the backslash forms as operators. -E flips that. Pick one dialect per command — mixing them is grep's most common silent failure."},
    {"repo": "grep", "slug": "fixed-string-literal-search",
     "title": "How to search for a literal string — grep -F",
     "scenario": "The text you want is full of regex punctuation: a function call, a path, a version string.",
     "code": """grep -F 'error.' proj/notes.txt    # no match (exit 1): no line contains a literal "error."
grep 'error.' proj/notes.txt       # 3 lines: the . is a wildcard and matches _, s, space, …
grep -F 'log_error(' proj/src/main.c   # finds it — parentheses need no escaping under -F""",
     "note": "-F (the old fgrep) matches character for character and runs no regex engine at all, which also makes it the fastest flavor."},
    {"repo": "grep", "slug": "whole-word-match",
     "title": "How to match whole words only — grep -w",
     "scenario": "You want error, not errors, error_codes or terror.",
     "code": """grep -w 'error' proj/notes.txt    # 1 line: "error handling notes\"""",
     "note": "A word is bounded by non-word characters — anything but letters, digits and underscore, which is why error_codes does not count as containing the word error."},
    {"repo": "grep", "slug": "whole-line-match",
     "title": "How to match an entire line exactly — grep -x",
     "scenario": "A config check: the line must be exactly this, byte for byte.",
     "code": """grep -x 'deep INFO calm' proj/sub/deep.log   # matches: the line is exactly this
grep -x 'deep INFO' proj/sub/deep.log        # no match (exit 1): a line prefix is not the line""",
     "note": "-x anchors the pattern at both ends, as if wrapped in ^…$. The right tool for exact-line lookups in config files."},
    {"repo": "grep", "slug": "multiple-patterns",
     "title": "How to search for several patterns at once — grep -e",
     "scenario": "Errors or warnings — either one is worth printing.",
     "code": """grep -e 'ERROR' -e 'WARN' proj/app.log   # 3 lines: a line matching EITHER pattern is printed""",
     "note": "Each -e adds an alternative; a line matching any of them is selected once. -e is also the escape hatch for patterns that begin with a dash."},
    {"repo": "grep", "slug": "patterns-from-file",
     "title": "How to read patterns from a file — grep -f",
     "scenario": "The watchlist of strings lives in a file — maybe one another program maintains.",
     "code": """grep -f proj/patterns.txt proj/app.log   # patterns.txt holds ERROR and timeout: 2 lines match""",
     "note": "One pattern per line; a line matches if it matches any of them. Beware: an empty pattern line matches every line, so a stray blank line turns the search into print-everything."},
    {"repo": "grep", "slug": "anchors-start-end-of-line",
     "title": "How to anchor a match to the start or end of a line — ^ and $",
     "scenario": "The level is at the start of the line; the verdict is at the end.",
     "code": """grep 'complete$' proj/app.log    # 1 line: "…INFO shutdown complete" — the line ENDS with the word
grep '^INFO' proj/server.log     # 1 line: "INFO boot ok" — the line STARTS with it""",
     "note": "Anchors pin the pattern to a position instead of letting it float anywhere in the line. Log formats put the level first and the verdict last — exactly what ^LEVEL and word$ exploit."},
    {"repo": "grep", "slug": "context-lines-after-match",
     "title": "How to show lines after each match — grep -A",
     "scenario": "The error line is not the whole story; what the program did next is.",
     "code": """grep -A 1 'ERROR' proj/app.log    # each ERROR line plus the line that follows it""",
     "note": "Groups separated by non-matching lines are divided by a -- separator line in the output."},
    {"repo": "grep", "slug": "context-lines-before-match",
     "title": "How to show lines before each match — grep -B",
     "scenario": "What led into the failure matters more than the failure line itself.",
     "code": """grep -B 1 'ERROR' proj/app.log    # the run-up: WARN disk at 81% before one, the lowercase failure before the other""",
     "note": "The mirror image of -A. When the context groups do not touch, grep prints a -- separator between them."},
    {"repo": "grep", "slug": "context-both-sides-merged-groups",
     "title": "How to show context on both sides — grep -C, and why groups merge",
     "scenario": "You used -C and the -- group separator you expected never appeared.",
     "code": """grep -C 1 'ERROR' proj/app.log    # 6 lines, NO '--' separator — see why below""",
     "note": "Context groups that touch are merged: here the groups cover lines 2-4 and 5-7, which are adjacent, so grep prints one continuous block. A missing -- means the matches were close together, not that there was one match."},
    {"repo": "grep", "slug": "color-highlight-matches",
     "title": "How to highlight matches in color — grep --color",
     "scenario": "Matches should light up in the terminal — or in a pager that renders escapes.",
     "code": """grep --color=always 'ERROR' proj/app.log | less -R   # the match is wrapped in ANSI color escapes
grep --color=auto 'ERROR' proj/app.log               # color only when output is a terminal""",
     "note": "--color=auto is why grep colors matches interactively but not in pipes. Force it with always when the consumer renders escapes. Colors are tunable via GREP_COLORS."},
    {"repo": "grep", "slug": "only-matching-part-extract",
     "title": "How to print only the matching part — grep -o as an extractor",
     "scenario": "You don't want the lines. You want the timestamps — or a count of occurrences.",
     "code": """grep -oE '[0-9]{2}:[0-9]{2}:[0-9]{2}' proj/app.log   # 08:00:01, 08:01:14, … — 7 timestamps, one per line
grep -o 'ERROR' proj/app.log | wc -l                 # 2 — count OCCURRENCES, not lines (contrast with -c)""",
     "note": "Each match is printed on its own line, which makes the output directly countable and sortable. With -E (or -P) this is the standard way to pull fields out of unstructured logs."},
    {"repo": "grep", "slug": "filename-prefix-control",
     "title": "How to force or suppress the filename prefix — grep -H and -h",
     "scenario": "A script parses file:line output from a single file — or the filenames are pure noise.",
     "code": """grep -H 'ERROR' proj/app.log                    # proj/app.log:… — filename even for a single file
grep -h 'ERROR' proj/app.log proj/server.log    # 3 matching lines, no filenames at all""",
     "note": "By default the prefix appears only with several files or recursion. -H forces it, -h suppresses it. With -n the forms combine: file:line:content."},
    {"repo": "grep", "slug": "quiet-mode-exit-codes",
     "title": "How grep exit codes work — grep -q and the 0/1/2 contract",
     "scenario": "Your script branches on whether the pattern exists in a huge file.",
     "code": """grep -q 'ERROR' proj/app.log; echo $?      # 0 — a line was selected
grep -q 'ZZZ' proj/app.log; echo $?        # 1 — no line was selected
grep -q 'ERROR' proj/missing.txt; echo $?  # 2 — an error occurred (file not found)""",
     "note": "0 = match, 1 = no match, 2 = error. -q prints nothing and quits at the first match, so it never reads past the answer — the only sane choice for if grep -q checks over big files."},
    {"repo": "grep", "slug": "silence-error-messages",
     "title": "How to silence grep's error messages — grep -s (status unchanged)",
     "scenario": "A wildcard search legitimately hits gaps, and the error noise buries the results.",
     "code": """grep 'ERROR' proj/missing.txt      # stderr: "grep: proj/missing.txt: No such file or directory", exit 2
grep -s 'ERROR' proj/missing.txt   # nothing printed anywhere — and the exit status is STILL 2""",
     "note": "-s suppresses messages about nonexistent or unreadable files. It quiets the message, not the outcome: a script checking $? still sees the error."},
    {"repo": "grep", "slug": "stop-after-n-matches",
     "title": "How to stop after the first few matches — grep -m",
     "scenario": "A multi-gigabyte log, and you only need to know it happens — plus the first example.",
     "code": """grep -m 1 'INFO' proj/app.log    # only the first INFO line; grep stops reading there""",
     "note": "-m caps the matches per file and closes the input early. Combined with -r, the cap applies to each file separately."},
]
