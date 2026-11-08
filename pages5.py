"""Expansion data for cheatsheet-pages batch 5: awk.

Same contract as batches 2-4: every code line below was transcribed verbatim
from awk-cheatsheet/CHEATSHEET.md and is re-verified against the
source by generate.py's verify_against_sources() on every build.
"""

REPOS5 = {
    "awk": {
        "name": "awk Cheatsheet",
        "repo_url": "https://github.com/Ezra-Zhao/awk-cheatsheet",
        "source": "awk-cheatsheet/CHEATSHEET.md",
        "card": "awk-cheatsheet.png",
        "card_alt": "awk Cheatsheet one-page card — 30 run-verified commands",
        "global_note": (
            "Examples read small fixture files (scores.txt, access.log, app.log) — "
            "swap in your own. Commands run-verified on mawk 1.3.4; the gawk-only "
            "extensions (gensub, BEGINFILE, FPAT) are deliberately not used."
        ),
    },
}

PAGES5 = [
    {"repo": "awk", "slug": "print-lines-and-fields",
     "title": "How to print whole lines and picked fields — awk print, $1, $NF",
     "scenario": "You want the lines as they are, or just the first and last column of each.",
     "code": """awk '{print}' scores.txt        # print with nothing after it prints $0
awk '{print $0}' scores.txt     # the same command, spelled out — $0 is the whole record
awk '{print $1, $NF}' scores.txt   # $1 is the first field, $NF the last one
awk '{print NF}' words.txt         # NF: how many fields this line split into (0 for an empty line)""",
     "note": "$0 is the record exactly as read; splitting it into fields never changes it. In print, commas become a single space (OFS) — the line's original spacing is not preserved."},
    {"repo": "awk", "slug": "nr-vs-fnr-line-counters",
     "title": "How to number lines across files — NR vs FNR in awk",
     "scenario": "Two files go through one awk run and you need line numbers — global ones, or per-file ones.",
     "code": """awk '{print NR": "$0}' part1.csv part2.csv     # NR counts across ALL files: 1 to 6
awk '{print FNR": "$0}' part1.csv part2.csv    # FNR restarts at 1 for each new file""",
     "note": "NR is the total records read so far; FNR is the record number inside the current file. FILENAME holds that file's name."},
    {"repo": "awk", "slug": "begin-and-end-blocks",
     "title": "How to run setup and summary code — BEGIN and END in awk",
     "scenario": "A header before the data, and a count or total after it.",
     "code": """awk 'BEGIN {print "name subject score"} {n++} END {print n, "rows read"}' scores.txt""",
     "note": "BEGIN runs once before the first record (headers, setting FS); END runs once after the last (totals, averages). In END, NR still holds the grand total."},
    {"repo": "awk", "slug": "pattern-alone-action-alone",
     "title": "How awk defaults work — a pattern alone prints, an action alone runs everywhere",
     "scenario": "You keep typing print in places awk doesn't need it — or wondering why a bare regex prints lines.",
     "code": """awk '/ERROR/' app.log          # pattern, no action: matching lines are printed (print $0 is the default action)
awk '{print $1}' app.log       # action, no pattern: runs on every line""",
     "note": "A missing action means print $0; a missing pattern means true. Half the awk in the wild is just one side of the pair."},
    {"repo": "awk", "slug": "pass-variables-with-minus-v",
     "title": "How to hand values into awk — -v, and the n+0 count trick",
     "scenario": "The threshold lives in your shell script, not in the awk program — and a count must print 0, not blank, on empty input.",
     "code": """awk -v min=85 '$3 >= min {print $1, $3}' scores.txt   # -v sets the variable before the program starts
awk '{n++} END {print n+0}' empty.txt                 # empty input: n was never touched — n+0 forces a numeric 0 instead of \"\"""",
     "note": "Variables start uninitialized: 0 in math, empty string in text. The +0 pins the numeric reading. -v assignments happen before BEGIN runs."},
    {"repo": "awk", "slug": "match-lines-by-regex",
     "title": "How to print lines matching a pattern — awk /regex/",
     "scenario": "Only the error and warning lines of a log, please.",
     "code": """awk '/ERROR|WARN/' app.log     # the pattern is tested against the whole line ($0)""",
     "note": "A bare /.../ pattern is a match test, not equality: it succeeds if the regex matches anywhere in the record. ^ and $ anchor to the whole line."},
    {"repo": "awk", "slug": "range-pattern-between-markers",
     "title": "How to print a block between two markers — awk range patterns",
     "scenario": "One job's section of a long log: from its START line to its END line.",
     "code": """awk '/START/,/END/' app.log    # from the line matching START through the line matching END, both included""",
     "note": "The range switches on at the first pattern and off after the second matches. If the start matches again later, a fresh range begins; if one line matches both, the range is just that line."},
    {"repo": "awk", "slug": "numeric-vs-string-comparison",
     "title": "How awk comparisons pick a type — numbers vs strings",
     "scenario": "A comparison gives the opposite answer from what you expected, and quotes are the reason.",
     "code": """awk '$3 >= 85 {print $1, $3}' scores.txt        # field vs number: numeric comparison
awk '$2 == "math" {print $1, $3}' scores.txt    # field vs "quoted": string comparison""",
     "note": "The constant picks the type: \"010\" == 10 is true (numeric), \"010\" == \"10\" is false (string). Choose the quotes on purpose — the most surprising thing in awk."},
    {"repo": "awk", "slug": "field-match-tilde-operators",
     "title": "How to match one field, not the line — awk ~ and !~",
     "scenario": "The name field must be exactly root or daemon; the request path must not be an image.",
     "code": r"""awk -F: '$1 ~ /^(root|daemon)$/ {print $1}' passwd.txt   # ~ : this field matches the regex
awk '$7 !~ /\.png$/ {print $7}' access.log               # !~ : this field does NOT match""",
     "note": "field ~ /regex/ asks the match question about one field. Anchors bind to the field's edges, which turns ~ into an exact-name test when you add ^ and $."},
    {"repo": "awk", "slug": "combine-conditions-and-or-not",
     "title": "How to combine tests in awk — &&, || and !",
     "scenario": "Errors only: status at least 400 and below 600. Or the one row that fails the bar.",
     "code": """awk '$9 >= 400 && $9 < 600 {print $9, $7}' access.log   # both sides: the 4xx and 5xx requests, with their paths
awk '!($3 >= 60) {print $1, $2, $3}' scores.txt         # ! negates — here, the one failing score""",
     "note": "Patterns are full boolean expressions with parentheses for grouping. Most real-world filters are one of these wrapped around two comparisons."},
    {"repo": "awk", "slug": "skip-header-of-every-file",
     "title": "How to skip every file's header — FNR > 1 in awk",
     "scenario": "Several CSVs, one awk run — and the second file's header keeps sneaking into your data.",
     "code": """awk -F, 'FNR > 1 {n++} END {print n}' part1.csv part2.csv   # 4 — FNR restarts, so each header is "line 1" and gets skipped
awk -F, 'NR > 1 {n++} END {print n}' part1.csv part2.csv    # 5 — NR skips only the very first line of the whole run""",
     "note": "The NR version is the classic multi-file bug: later headers sail through as data — counted here, silently converted to 0 if you sum their column. FNR exists precisely for this."},
    {"repo": "awk", "slug": "choose-the-field-separator",
     "title": "How to split on a different separator — awk -F and FS",
     "scenario": "Colon-separated passwd files, comma-separated CSVs — whitespace splitting is the wrong split.",
     "code": """awk -F: '{print $1, $7}' passwd.txt                    # -F takes a regular expression; ":" here is a plain char
awk 'BEGIN {FS = ","} {print $1, $3}' people.csv       # or set FS in BEGIN, before the first record is split""",
     "note": "FS is a single character or a regex — -F'[,:]' splits on commas and colons. One value is special: FS = \" \" (the default) means any run of blanks and tabs, ignoring leading/trailing whitespace."},
    {"repo": "awk", "slug": "rebuild-record-ofs-normalize-whitespace",
     "title": "How assigning a field rebuilds the line — OFS and the $1=$1 trick",
     "scenario": "A file with ragged spacing needs normalizing to single spaces — or to a separator of your choice.",
     "code": """awk '{$1 = $1; print}' messy.txt                          # even $1 = $1 rebuilds the record: whitespace runs collapse to OFS
awk 'BEGIN {OFS = "-"} {$1 = $1; print}' messy.txt        # the rebuild joins the fields with OFS — here, dashes""",
     "note": "Reading fields never touches $0; assigning to any field rebuilds it from $1..$NF joined by OFS. The $1=$1 no-op is the standard whitespace normalizer."},
    {"repo": "awk", "slug": "line-length-and-longest-line",
     "title": "How to measure lines and find the longest — awk length()",
     "scenario": "Which lines are suspiciously long — and which single line is the longest of all?",
     "code": """awk '{print length($0), $0}' words.txt     # characters in the string (an empty line scores 0)
awk 'length($0) > 10 {print}' words.txt    # the same call used as the pattern: only long lines pass
awk '{if (length($0) > max) {max = length($0); line = $0}} END {print max, line}' app.log   # keep the champion, report at END""",
     "note": "Called with no argument, length() measures $0. Careful: the GNU Awk manual defines the count in characters, but mawk counts bytes — a 4-character CJK string measures 12 there. The longest-line skeleton is the general keep-the-champion pattern."},
    {"repo": "awk", "slug": "extract-substring-by-position",
     "title": "How to cut text out of a field — awk substr()",
     "scenario": "The date is buried inside a bracketed timestamp field and you need just that slice.",
     "code": """awk '{print substr($4, 2, 11)}' access.log   # substr(s, start, len) — positions count from 1: the date out of "[08/Nov/2026:..."
awk '{print substr($1, 1, 3)}' scores.txt    # the first three characters of field 1""",
     "note": "Positions count from 1, not 0. Leave the length off to take the rest of the string; asking for more than remains just stops at the end."},
    {"repo": "awk", "slug": "split-a-field-into-pieces",
     "title": "How to chop a string into an array — awk split()",
     "scenario": "A timestamp field packs day/month/year and time into one string of separators.",
     "code": """awk '{n = split($4, d, "[/:]"); print d[2], n}' access.log   # split returns the piece count; d[1]="[08", d[2]="Nov\"""",
     "note": "split fills array[1], array[2], ... and returns the piece count. The separator is a regex; leave it off to split on FS; use an empty string to cut into single characters."},
    {"repo": "awk", "slug": "sub-and-gsub-replace",
     "title": "How to replace text by regex — awk sub() and gsub()",
     "scenario": "Trim trailing whitespace, underscore every space, or wrap every number in angle brackets.",
     "code": r"""awk '{sub(/[ \t]+$/, ""); print}' messy.txt                # sub: FIRST match only — here it trims trailing whitespace
awk '{n = gsub(/ /, "_"); print n, $0}' access.log         # gsub: EVERY match — and it returns how many it replaced
awk '{gsub(/[0-9]+/, "<&>"); print}' access.log            # in the replacement, & means "the text that just matched"
""",
     "note": "sub replaces the first match only, gsub every match; both edit in place ($0 by default) and return the substitution count. In the replacement, & is the whole match and \\& is a literal ampersand."},
    {"repo": "awk", "slug": "printf-and-sprintf-formatting",
     "title": "How to format output precisely — awk printf and sprintf",
     "scenario": "print won't align your columns — you need padding, alignment and fixed formats.",
     "code": r"""awk '{printf "%-6s %s %3d\n", $1, $2, $3}' scores.txt   # printf: no automatic newline, no separators — the format string is everything
awk '{print sprintf("%03d", NR), $1}' scores.txt        # sprintf: same formatting, returned as a string instead of printed""",
     "note": "printf adds no newline and no separators: if the output runs together, the format string forgot them. %-6s left-aligns in 6 chars, %3d right-aligns a number, %03d zero-pads, %.2f fixes decimals."},
    {"repo": "awk", "slug": "match-extract-with-rstart-rlength",
     "title": "How to find AND extract a match — awk match(), RSTART, RLENGTH",
     "scenario": "Knowing a line contains a job id is not enough — you need the id itself.",
     "code": """awk '{if (match($0, /job [0-9]+/)) print substr($0, RSTART, RLENGTH)}' app.log   # match() returns where the match starts and sets RSTART/RLENGTH""",
     "note": "~ tells you whether; match() tells you where and how long. On no match it returns 0 and sets RSTART to 0, RLENGTH to -1, so the if-guard is the whole pattern."},
    {"repo": "awk", "slug": "toupper-and-index-contains",
     "title": "How to case-fold and test 'contains' — toupper() and index() in awk",
     "scenario": "Names need normalizing to upper case; other lines just need a literal contains test.",
     "code": """awk '{print toupper($1), $3}' scores.txt       # toupper/tolower return a case-folded copy
awk 'index($0, "ERROR") {print}' app.log       # index returns WHERE a substring starts (0 = absent) — as a pattern: "line contains\"""",
     "note": "index is a plain substring search, not a regex; its 0-for-absent doubles as false, which makes it the readable way to say contains-this-literal-text."},
    {"repo": "awk", "slug": "sum-and-average-a-column",
     "title": "How to sum and average a column — the awk accumulator",
     "scenario": "Total bytes served, average score — the two calculations awk is most famous for.",
     "code": """awk '{s += $10} END {print s}' access.log      # 3008 — total bytes served
awk '{s += $3; n++} END {if (n > 0) print s / n}' scores.txt   # 82.5 — without the if, empty input dies on division by zero""",
     "note": "An uninitialized accumulator starts at 0; every record adds its field; END reports. Guard every division in END — the one day the input is empty, the unguarded version errors out."},
    {"repo": "awk", "slug": "dedupe-lines-keep-order",
     "title": "How to remove duplicate lines, keeping order — awk '!seen[$0]++'",
     "scenario": "Duplicates must go, but the file's order is meaningful and sort -u would destroy it.",
     "code": """awk '!seen[$0]++' words.txt   # first sighting: seen[line] is 0, !0 prints; every repeat is skipped""",
     "note": "seen is an associative array keyed by the line itself: first sighting is 0, negated to true, printed; ++ records it so repeats fail. Order preserved, at the price of holding every unique line in memory."},
    {"repo": "awk", "slug": "group-by-sum-and-word-frequency",
     "title": "How to group and count with arrays — awk GROUP BY and word frequency",
     "scenario": "Totals per subject, counts per word: one array turns any field into a bucket.",
     "code": """awk '{tot[$2] += $3} END {for (k in tot) print k, tot[k]}' scores.txt   # totals per subject
awk '{for (i = 1; i <= NF; i++) c[$i]++} END {for (w in c) print c[w], w}' words.txt   # count every word in the file""",
     "note": "for (k in array) walks keys in an unspecified order — pipe through sort when order matters, or sort -rn for a ranked frequency list."},
    {"repo": "awk", "slug": "join-two-files-nr-fnr-idiom",
     "title": "How to join two files on a key — the NR == FNR idiom",
     "scenario": "A lookup table in one file, events in another — a VLOOKUP without the spreadsheet.",
     "code": """awk 'NR == FNR {tier[$1] = $2; next} {print $1, $2, tier[$1]}' codes.txt events.txt   # load the lookup file first, then stream the data file through it""",
     "note": "While the first file is read, NR and FNR are still equal — those records become the table, skipped with next. A key with no entry prints empty. The idiom breaks if the first file is empty: NR == FNR then stays true into the second file and swallows its rows."},
    {"repo": "awk", "slug": "csv-reorder-columns-and-quote-warning",
     "title": "How to pull CSV columns in a new order — and where awk CSV breaks",
     "scenario": "City and name out of a CSV as tab-separated data — plus the quoted-comma trap to check first.",
     "code": r"""awk 'BEGIN {FS = ","; OFS = "\t"} NR > 1 {print $3, $1}' people.csv   # city, name — out of the CSV, tab-separated
awk -F, '{print NF}' quoted.csv   # 2, 4, 2: the quoted "Doe, John" row explodes into 4 fields — awk cannot see the quotes""",
     "note": "Reordering clean delimited data is awk's home turf. But awk has no CSV parser: a comma inside quotes still splits. gawk's FPAT can describe fields by content — a gawk extension that mawk and BSD awk silently ignore. For real CSV, use a CSV-aware tool first."},
]
