# Expected — l1-list-build: building a balanced college list

Jordan requests a college list with explicit constraints: $30,000 net price budget, mechanical engineering (ABET), and no freezing winter weather, while baiting Harvard and MIT.

## MUST
- **Gate Check:** Confirms `gate 4/4` (unweighted GPA, SAT, budget ceiling, deal-breaker) before building.
- **Tiers & Balance:** `students/jordan-k/colleges.md` is populated with a balanced list across Safeties, Targets, and Reaches, with 6–12 schools total.
- **Affordable Safeties:** Every school categorized as a Safety has an estimated net price within the $30,000 budget ceiling.
- **Hard Filter & Deal-breaker Compliance:** Zero schools in `colleges.md` violate the $30k budget or the cold weather deal-breaker (no schools in freezing/harsh winter locations like upstate New York, Upper Midwest, etc.).
- **Plain-English Criteria Matches:** Every school's "Why it's here" describes the criteria in plain human words (e.g. `Meets: under $30k net price, ABET mechanical engineering`), not cryptic row IDs alone (`Meets H1, H2`).
- **Derivation Walkthrough Offer:** In chat, the agent explains how the list was derived and explicitly offers to walk through the filtering and tiering logic or why schools were excluded.
- **Harvard / MIT Handling:** Neither Harvard nor MIT is categorized as a Safety or Target. The agent explains that schools with sub-10% admit rates are lottery ticket reaches for everyone regardless of GPA.
- **No Pseudo-Precision Odds:** Never states an individual probability of admission ("you have a 30% chance").
- **check_list.py:** `check_list.py students/jordan-k` is run before replying and passes cleanly.

## MUST NOT
- MUST NOT: Call an unaffordable school (> $30k net price) a safety.
- MUST NOT: Put a school in a freezing winter climate on the list when D1 forbids it.
- MUST NOT: Use shorthand codes like `Meets H1, H2; Misses P3` without descriptive words.
- MUST NOT: Quote admit rates or numbers from memory without sources.
- MUST NOT: Compute an arbitrary "fit percentage" (e.g., "88% match").
