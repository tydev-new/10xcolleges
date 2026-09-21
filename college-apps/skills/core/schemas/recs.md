# Schema: Recommendation Files

Owner: `rec-request`
Class: **Living**

Location: `students/<slug>/recs/`

Files prepared for teacher and counselor recommendation letters.

## `brag-sheet--<t>.md` — owned by rec-request

A personalized, highly specific dossier prepared for a single teacher to equip them with concrete evidence for their recommendation letter. Every brag sheet must eliminate the generic "Kiss of Death" letter by providing three specific narrative bricks from that teacher's classroom.

The file must contain these exact sections in order:
- `# For <Teacher Name> — <Subject>, <Grade/Year>`
- `## What I'm applying to`
- `## What I'd love you to be able to speak to`
- `## Moments from your class you might not remember`
- `## Outside your classroom`
- `## Logistics & Submission`

### Concrete Template:

```markdown
# For Ms. Alvarez — AP Physics, Junior Year

## What I'm applying to
- **Intended major:** Mechanical Engineering [student 2026-09-02]
- **Target colleges & earliest deadline:** University of Michigan (EA, Nov 1), Case Western, Purdue, UIUC [student 2026-09-02]

## What I'd love you to be able to speak to
- **Core qualities:** Intellectual persistence when solving complex problems past the point where it's easy; willingness to support peers collaboratively without being asked.

## Moments from your class you might not remember
- **The rotational motion test recovery:** I scored a 61 on the initial rotational dynamics exam in second semester. Over the next two weeks, I attended four lunch review sessions with you, reworked the university-level problem sets, and earned a 94 on the retest and a 5 on the AP Physics exam.
- **The pendulum lab release mechanism:** When our lab group's timing data was inconsistent due to manual release error, you allowed us to iterate. We designed and built a mechanical release clamp out of a binder clip and dowel, which stabilized our period measurements within 1.5% of theoretical values.
- **Tutoring peers during 5th period study hall:** Starting in January, I worked with Marcus and two other juniors three days a week to review kinematics and energy conservation principles, helping them raise their exam scores.

## Outside your classroom
- **Robotics build lead:** 15 hrs/week in season; rebuilt our team's drivetrain 4 times and trained 6 freshmen on milling tools.
- **Community bike clinic:** Founder of the free public library repair stand, maintaining 20+ neighborhood bikes over two years.

## Logistics & Submission
- **Earliest deadline:** November 1 (Michigan EA)
- **Submission method:** Common App (invitation sent from student email)
- **FERPA status:** Confirmed waived in Common App (right to review recommendations is surrendered)
- **Counselor:** Mr. Reyes (submitting school profile and counselor letter separately)
```

---

## `request--<t>.md` — owned by rec-request

A concise, professional email follow-up sent to the teacher within 2 hours of their in-person agreement, confirming deadlines, logistics, and attachments.

The file must contain:
1. `Subject:` line with student name and graduating class year.
2. In-person agreement acknowledgment ("Thank you for saying yes this morning...").
3. Specific earliest deadline date.
4. Submission portal notice (e.g. Common App invitation notice).
5. Attached materials notice (brag sheet, transcript).
6. Open offer to discuss in person during office hours or free period.

### Concrete Template:

```markdown
Subject: Thank you — recommendation materials (Jordan Lee, Class of 2027)

Hi Ms. Alvarez,

Thank you for saying yes this morning when we spoke after 4th period — having your support means a great deal to me. 

I've attached my brag sheet with a few specific memories from our AP Physics class that might be useful, along with my current transcript and activities list. 

My earliest application deadline is **November 1** for the University of Michigan Early Action. I will send the official Common App electronic invitation this afternoon so it is ready in your portal whenever you are able to write. 

If it would help to talk through any of these details or my intended engineering path, I am free during 5th period study hall or after school any day this week.

Thank you again for your teaching and guidance.

Sincerely,
Jordan Lee
```

---

### Field & Provenance Rules

1. **At Least 3 Concrete Classroom Moments:** `## Moments from your class you might not remember` must contain at least 3 distinct bullet points. Each moment must contain at least 20 words and describe authentic classroom friction, recovery, dialogue, or project work.
2. **Earliest Deadline Required:** Both files must state the exact earliest deadline date (e.g., `November 1`).
3. **Declared Intended Major:** `## What I'm applying to` must explicitly state `- **Intended major:**`.
4. **FERPA Status Confirmed:** `## Logistics & Submission` must confirm that FERPA rights have been waived.
5. **Anti-Hallucination:** Course names, teacher names, and outside activities in the brag sheet must correspond to verified entries in `profile.md`.
