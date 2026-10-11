# AI Learning Log

## Fellow: Bartholomew Akor (Engineer A)

**AI assistance disclosure:** AI (Claude) wrote first drafts of `tickets.py`, `storage.py`, their tests and
the `main.py` menu. I read the code, ran the tests, spotted missing features, and merged it with my partner's work.

### 1. Git branch names and `git switch -c`
- **Problem:** `git switch -c test/3- priority-validation` failed with `fatal: invalid reference: priority-validation`.
  I had put a space in the branch name and did not realise a space ends an argument.
- **AI guidance:** The space split my input into two arguments, so Git treated `priority-validation` as the starting
  point, which does not exist.
- **Experiment and result (run by the AI, reviewed by me):** `git switch -c "test/3-" priority-validation` gave the same
  error; `git switch -c test/3-priority-validation` printed `Switched to a new branch`.
- **Decision:** Accepted. Use hyphens and no spaces: `<type>/<issue-number>-<description>`.
- **I can now explain:** Git splits commands on spaces, and the second argument of `git switch -c` is the starting point.

### 2. Merging `main` into my feature branch
- **Problem:** After `git pull origin main`, my partner's work was on `main` but not on my branch. Git also opened
  nano during `git merge main`.
- **AI guidance:** Keep my `tickets.py` (main had an empty placeholder), keep my partner's `main.py` and add my handlers,
  remove conflict markers, and in nano save with Ctrl+O then Enter and exit with Ctrl+X.
- **Result:** `python -m unittest discover -s tests` on the full project, run by the AI: `Ran 43 tests ... OK`.
- **Decision:** Accepted.
- **I can now explain:** A merge brings `main` into my branch. Conflicts mean both sides changed the same lines, so I
  combine them by hand, rerun the tests, then commit and push.

### 3. Checking AI output against the requirements (critical evaluation)
- **Problem:** The AI's first `main.py` had only create, list and view, with saving commented out, and `storage.py`
  had never been written. I noticed this by comparing the project with the guide's seven features ("i didnt see JSON
  persistence"; the menu lacked assign, change status, work queue and report).
- **Decision:** Rejected that `main.py`. The updated one wires options 4 to 7, loads and saves `data/tickets.json`, and
  exits on corrupt JSON without overwriting it.
- **Result (demo route run by the AI):** create tickets, reject an invalid one, reject starting an unassigned ticket,
  assign and progress, show queue and report, restart and reload (next ID T003), corrupt the JSON (clear error, file
  untouched). The 43 tests pass.
- **I can now explain:** AI output can look finished and still miss requirements, so I check it against the written list.
- **Files:** `main.py`, `campusflow/storage.py`, `tests/test_storage.py`

### 4. Python packages and `__init__.py`
- **Problem:** I typed `--init--.py` and did not know what the file should contain.
- **AI guidance:** The file can be empty, the name has two underscores each side, and without it imports can fail with
  `ModuleNotFoundError`.
- **Experiment and result (run by the AI, reviewed by me):** With `campusflow/__init__.py` removed, all 43 tests still
  passed and `from campusflow.tickets import create_ticket` still worked on Python 3.12 (namespace packages, PEP 420).
- **Decision:** Corrected the AI's claim: the file is not strictly required in modern Python. I keep the empty files
  because the guide's layout includes them and they make the package explicit.
- **I can now explain:** `__init__.py` marks a regular package; modern Python can import without it, but it is the clearer convention.

### Final reflection
1. **Feature I implemented and how I know it works:** Ticket creation, validation and the priority engine in `tickets.py`,
   and JSON persistence in `storage.py`. Tests cover the four priority rules and boundaries, invalid input, ID uniqueness
   after reload and corrupt JSON, and the app was run through create, restart and reload.
2. **What AI taught me:** A space splits shell arguments; `git merge main` brings my partner's work into my branch;
   `__init__.py` is a convention in modern Python, not a hard requirement.
3. **Verified, changed or rejected a suggestion:** I rejected the first `main.py` for missing five of seven features
    and tested the `__init__.py` claim and found it overstated (#4). I also found two issues in my partner's code during review (#5).
4. **What I learned reviewing my partner's PR:** Two modules can share a helper name with different error behaviour, so imports must be explicit, and wording like "open, unresolved" needs one agreed meaning and a test.
5. **What I would improve in another hour:** Re-validate every ticket field when loading the JSON, and add ticket
   editing and filtering.

---

## Fellow: Godwin Ngbede (Engineer B)

**AI assistance disclosure:** AI (Claude) wrote the first drafts of `workflow.py`, `reports.py`, `test_workflow.py` and
`test_reports.py`. I write them in my repository folder, worked on a feature branch, and they were merged into `main`.

### 1. Feature branches, staging and one push (Git)
- **Problem:** I needed to put my files on GitHub without touching `main` or Engineer A's files.
- **What I asked:** What Engineer A's part was, whether my file arrangement was correct (I sent a screenshot of my
  Explorer), and whether all my files can be pushed together.
- **AI guidance:** Use one branch per engineer. Stage named folders (`git add campusflow/ tests/`) instead of `git add .`
  and check `git status`. My layout was correct and `U` means untracked. Git pushes commits, not individual files, so
  make a couple of incremental commits and push once. Never push to `main`; open a PR for review.
- **What I did and result:** `git pull origin main` printed "Already up to date", and `git switch -c feat/4-status-workflow`
  printed "Switched to a new branch 'feat/4-status-workflow'". The AI had suggested the number 2; I used 4, and the AI
  confirmed the number only needs to match the Issue.
- **Decision:** Accepted, using my own Issue number.
- **I can now explain:** `git add` stages, `git commit` saves locally, `git push` sends commits to GitHub, and a feature
  branch keeps `main` clean until a reviewed PR.

### 2. Preparing for the audit by running every function
- **Problem:** I had an audit and needed to understand the whole project, both engineers' code, from start to end.
- **What I asked:** Explain the project, run each file's functions, and classify the patterns used.
- **AI output:** A study guide covering the overview, every file for Engineers A and B, a diagram of how the files connect,
  real outputs, a table of 25 coding patterns (such as first-match-wins priority rules and the transition table), and
  likely audit questions; plus `audit_demo.py`, which reruns every function and prints the results.
- **Result:** The AI ran all four test files: 43 tests pass in total (my 18: 15 in `test_workflow.py` and 3 in `test_reports.py`).
- **Decision:** Accepted as a study aid. It describes the code but does not replace being able to explain it in the audit.
- **I can now explain:** My modules: `ALLOWED_TRANSITIONS` limits status moves, `change_status` also blocks starting an
  unassigned ticket, `get_work_queue` sorts by priority and then numeric ID (`_id_number`), and `build_report` counts by
  status and priority.

### 3. AI claims corrected and an open queue question (critical evaluation)
- **Problem:** AI statements about the project had to be checked against the code.
- **What was wrong:** The AI first said Engineer A's ticket tests number 21. When it ran all four test files it corrected
  this to 19 (43 in total, all passing). The AI found this itself, not me. Separately, its guide lists as a limitation that
  the work queue includes `in_progress` tickets, although the guide says "open, unresolved".
- **How it was checked:** By running the tests, and by running the queue: an `in_progress` ticket stays in it and leaves
  once resolved.
- **Decision:** I use the corrected test count. The queue behaviour stays as it is, with the assumption documented in
  the `get_work_queue` docstring, until the team agrees on one meaning.
- **I can now explain:** The queue shows every ticket that is not resolved. If the team decides it should show only `open`
  tickets, the filter changes to `== "open"` and the test is updated.

### Final reflection
1. **Feature I implemented and how I know it works:** Assignment, status workflow, work queue and reports in `workflow.py`
   and `reports.py`. The 15 workflow tests and 3 report tests pass, and the whole project passes 43 tests.
2. **What AI taught me:** Feature branches, staging named folders, making incremental commits and pushing once, and what
   `U` and `git status` mean.
3. **Verified, changed or rejected a suggestion:** I used branch number 4 instead of the suggested 2, and the AI corrected
   its own test count from 21 to 19 after running the tests.
4. **What I learned reviewing my partner's PR:** taught me the importance of teamwork, code quality, and testing in software development. I learned to read another person's code carefully, compare it with the project requirements, and check whether the tests cover both valid and invalid cases.
5. **What I would improve in another hour:** Decide whether the work queue should include in-progress tickets and test that
   choice, and name the helper functions so they do not clash with `tickets.find_ticket`.