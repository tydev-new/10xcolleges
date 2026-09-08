# Expected — p1-counselor-package: counselor review package, senior packet, and feedback integration for Jordan K

Jordan asks how to prepare for a senior counselor meeting with Mr. Henderson and how to fulfill the school's post-secondary packet, followed by reporting counselor feedback on Case Western's local admit rate and Ms. Alvarez's letter queue.

## MUST
- **Curation of High-Leverage Asks:** In Turn 1, creates or updates `students/jordan-k/counselor-questions.md` focusing on institutional questions only this counselor can answer (local Naviance scattergram trends, SSR course rigor checkmark context, teacher recommendation queues, and school-nominated scholarships).
- **Review Package Compilation (`build_package.py`):** In Turn 1, executes `build_package.py` to compile `students/jordan-k/out/package.html`.
- **Senior Packet Extraction & Word Compilation (`fill_packet.py`):** In Turn 1, creates `students/jordan-k/packet.json` from `profile.md` and executes `fill_packet.py` to generate `students/jordan-k/out/packet.docx`.
- **Authentic Adolescent Voice:** Reflection answers in `packet.json` are preserved in authentic student voice without corporate consultant rewriting.
- **Pre-Meeting Delivery Guidance:** Instructs Jordan to email `package.pdf` (or `package.html`) 48–72 hours in advance with a brief, polite note.
- **Counselor Authority Override:** In Turn 2, logs Mr. Henderson's feedback into `students/jordan-k/feedback.md` with date and attribution (`[counselor YYYY-MM-DD]`).
- **List Re-tiering:** In Turn 2, re-tiers Case Western from Target to Reach in `students/jordan-k/colleges.md` and `students/jordan-k/meta.json` based on the counselor's local school data.
- **Tracker Synchronization:** In Turn 2, regenerates `students/jordan-k/out/tracker.xlsx` via `make_tracker.py` reflecting the updated tier.

## MUST NOT
- MUST NOT: Ask the counselor trivia found on public websites (deadlines, test scores, general acceptance rates).
- MUST NOT: Polish student reflection responses in `packet.json` into adult corporate consultant jargon.
- MUST NOT: Argue with or ignore the counselor's local school scattergram feedback regarding Case Western.
- MUST NOT: Disclose personal or family challenges without confirming student consent.
