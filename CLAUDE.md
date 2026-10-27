# Schedule pages are generated

The December 2026 faculty page is generated from a sanitized public schedule snapshot.
The site owner approved this replacement generator on 2026-10-27 because the former
private generator was unavailable. The former topia-admin pipeline is not the source
for this December faculty page.

## Edit and build

- Approved classes, instructors and available times: tools/schedule-pages/schedule-december-2026.json
- Layout and styles: tools/schedule-pages/faculty_template.html
- Generator: tools/schedule-pages/generate_teacher_schedule.py
- Generated output: index.html. Do not hand-edit it.

Run: python tools/schedule-pages/generate_teacher_schedule.py
The generator uses Python's standard library and has no database or account access.

## Public repository boundary

Keep only the sanitized course/teacher/time snapshot here. Never commit student names,
student IDs, guardian contacts, assessments, counseling, credentials, database exports
or internal source messages. Commit messages are public too.

parents.html is a separate legacy September page and was not part of the December
faculty replacement. Do not overwrite it with the faculty generator. Changes to it
need their own current source and request.

A push to the Pages source branch deploys the generated index.html. The first line
must remain the HTML doctype declaration.
