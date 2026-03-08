from __future__ import annotations

from .session import TutorSession


def _show_current(session: TutorSession) -> None:
    print(session.current_lesson_note())
    print("```python")
    print(session.current_lesson_code().rstrip())
    print("```")


def main() -> int:
    session = TutorSession.from_workspace()

    if not session.courses:
        print("No courses found in ./courses or ./my-courses")
        return 1

    print("Available courses:")
    for idx, course in enumerate(session.courses, start=1):
        print(f"{idx}. {course.id} ({len(course.lessons)} lessons)")

    raw = input("Select course by number: ").strip()
    try:
        selection = int(raw) - 1
        course = session.select_course(selection)
    except (ValueError, IndexError):
        print("Invalid selection")
        return 1

    print(f"\nStarting course: {course.id}\n")
    _show_current(session)

    while True:
        action = input("\nEnter [n]ext lesson or [q]uit: ").strip().lower()
        if action == "q":
            print("Session ended.")
            return 0
        if action == "n":
            if session.next_lesson():
                print()
                _show_current(session)
                continue
            print("You are at the last lesson.")
            continue
        print("Unknown command. Use 'n' or 'q'.")


if __name__ == "__main__":
    raise SystemExit(main())
