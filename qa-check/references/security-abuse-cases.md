# Security scenarios a tester can run through the UI

Use this list to judge whether a story's scenarios cover the security angles its surface calls for, and to propose missing ones in `complete` mode. Only what a UI-first tester can do, derived from the story alone.

**When a scenario is expected.** Only when the story names the surface: a role or permission, a record with an owner or tenant, a login or session, a free-text or file input, personal data, or an action it describes as sensitive. If the story is silent about the surface, its absence is not a finding; never invent a role, a tenant model or a data classification. Quote labels, messages and redirect targets verbatim from the story; when it gives no message, describe the outcome (*"access denied"*) rather than inventing a string.

**Shape.** Ordinary scenarios in the story's own format: tagged with an ID, a type (`permission`, `negative` or `boundary`) and the criterion they validate; Given / When / Then at UI altitude.

| Scenario | Story signal | UI steps (shape) | Expected (shape) |
|---|---|---|---|
| Act as a blocked role | The story names roles that may or may not reach the screen or action | Sign in as an excluded role; look for the menu entry; paste the screen's address; attempt the action | Entry absent; direct address shows the story's access-denied message or redirect; no visible side effect |
| Open another user's record | Records belong to a user, team or tenant | As user A, open a record and note its address; as user B (other owner), paste it | Access denied or not found; B never sees A's data, in lists, search or exports |
| Listing limited to own data | The story adds lists, searches or filters over owned data | As a scoped user, open every new list, search and filter | Only own rows; totals and counters match own data |
| Hostile text in a form | The story has free-text fields | Paste markup, script tags, a very long string, quote characters and accented text into each field | Stored and shown as plain text, or rejected with the field's message; the record stays consistent |
| Over-limit values | The story states a maximum length, file size or allowed type | Exceed the limit; upload a disallowed type | The exact validation message; nothing saved |
| Ended session | The story involves login or a multi-step flow | Sign out in a second tab, then act in the first | Redirect to sign-in; the action does not complete; no partial write afterwards |
| Permission change takes effect | The story lets an admin grant or revoke permissions | Revoke a permission from a signed-in user, who then attempts the action | Denied on the next attempt (or after sign-in, if the story says so; quote it) |
| Double submit | The story has a create, submit, pay or send action | Double-click the action; go back and resubmit | Exactly one resulting record or event |
| Personal data exposure | The story shows, exports or notifies with personal data | Open each new screen, export or message as a role that should not see it | Personal data masked or absent as the story says; none in addresses |
| Audit trail visible | The story describes a sensitive action and names a history view | Perform the action; open the history view | One entry with actor, time and action; if no such view is named, an open question for the developer, not a scenario |

**Not scenarios** (open questions for the developer): token tampering, forged or missing headers, API-level invalid values, request forgery without a UI path, rate limiting, transport and header configuration, dependency vulnerabilities, anything a code scanner flagged, and any security requirement the tester cannot exercise through the UI.
