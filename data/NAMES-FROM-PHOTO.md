# Names read from the name-card photograph

**These are unverified.** They were read off handwritten cards in
`assets/source/graduands-name-cards.jpg` at limited resolution. Several are
partly obscured or ambiguous, and a graduation roll is exactly the wrong place
for a guessed spelling. Use this as a prompt for whoever holds the register,
not as data.

Note also what the cards actually appear to be: most carry a small annotation in
the top-right corner reading `1st`, `2nd` or `3rd` with a class, and at least one
card has an office written underneath the name. So this photograph looks like a
**position or prefect announcement**, not necessarily the graduating set. Confirm
before reusing the picture as a graduation photograph.

## Read with reasonable confidence

| Read as | Confidence | Note |
|---|---|---|
| ADAMSON Abdullahi Olajuwon | good | front row, clear card |
| GINA Idris | good | short card, clear |
| JAMIU Abdul Manan | good | second word may be "Mannan" |
| HASSAN-MURITALA Ikhlas | good | hyphenated surname on the card |
| JABAAR Abdulbasit Amobi | good | front centre |
| OJEWUMI Fawaz Babatunde | good | front right |
| RASAQ Aisha Omobolanle | good | may be "Rasaq" or "Rasaki" |
| SANNI Fareedat | good | a second given name follows, unread |
| DURODOLA Amarat | fair | may be "Duroosola" |
| MAKINDE Thoirah Omotara | fair | office written beneath, unread |
| OJEWUMI Hameedah | fair | a third name follows, unread |
| IBRAHIM Fatimah | fair | back row right |

## Read poorly — do not use without checking

| Read as | Problem |
|---|---|
| AROOF Maryam Morenikeji | surname may be SAROF / TAROF / AROOF |
| SHOBA Aisha Ib—— | second given name illegible |
| IBRAHIM Fah—— | given name illegible; a second IBRAHIM on the card |
| AMU—— O—— | card mostly hidden behind another student |
| ——hameed ——tunde | card cropped at the frame edge |
| ——EZ A—— | card cropped at the frame edge |

## What to do

1. Get the official roll from the register.
2. Paste it into `data/graduands.json` under `sections[].names`.
3. Set `"verified": true` in that file once a member of staff has checked
   every spelling.
4. Re-run `python3 build/build.py`. The DRAFT banner disappears and both
   documents pick up the real names.
