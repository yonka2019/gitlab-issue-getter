import gitlab
import datetime

# GitLab Constants
PRIVATE_TOKEN = ''
PROJECT_ID = 0
ASSIGNEES = {
    "EyalSol": "איל",
    "yonka2019": "יונתן"
}

# Project Constants
LAST_LESSON_DAYS = 7  # [LAST LESSON] {->} CLOSEST LESSON -> NEXT LESSON    ({days number})
NEXT_LESSON_DAYS = 7  # LAST LESSON -> CLOSEST LESSON {->} [NEXT LESSON]    ({days number})
LESSON_DAY = 3  # 0 - Monday, 1 - Thursday ..


def main():
    closest_lesson_date = next_weekday(datetime.datetime.now(), LESSON_DAY)  # (, 0 - monday) ; closest thursday (lesson day)

    last_lesson_date = (closest_lesson_date - datetime.timedelta(days=LAST_LESSON_DAYS))  # - 7 days from the closest lesson day
    next_lesson_date = (closest_lesson_date + datetime.timedelta(days=NEXT_LESSON_DAYS))  # + 7 days from the closest lesson day

    print_lessons(last_lesson_date, closest_lesson_date, next_lesson_date)

    gl = gitlab.Gitlab(private_token=PRIVATE_TOKEN)
    project = gl.projects.get(PROJECT_ID)

    printed = False

    print("-- TO-DO -- ")
    for issue in project.issues.list(get_all=True, order_by='due_date'):
        if issue.due_date is not None:
            due_date = datetime.datetime.strptime(issue.due_date, '%Y-%m-%d')

            if last_lesson_date <= due_date <= next_lesson_date:
                if (due_date <= closest_lesson_date) and not printed:  # print only one time
                    print("\n-- DONE --")
                    printed = True

                try:
                    print_issue(issue, due_date)
                except:
                    print("### (ERROR) [Title] OR [Assignee] OR [Time estimate] is not configured ###")


def print_lessons(last_lesson, closest_lesson, next_lesson):

    print(f"\nLAST LESSON  "
          f"CLOSEST LESSON   "
          f"NEXT LESSON")

    print(f"{last_lesson.date().strftime('%d-%m-%Y')} -> "  # LAST LESSON
          f"[{closest_lesson.date().strftime('%d-%m-%Y')}] -> "  # CLOSEST LESSON (OR CURRENT)
          f"{next_lesson.date().strftime('%d-%m-%Y')}\n")  # NEXT LESSON


def print_issue(issue, due_date):

    if "Bug" in issue.labels:  # check if BUG label setted
        print("[BUG]", end=" ")

    print(issue.title +
          " [" + due_date.strftime("%d.%m") + "] - " + ASSIGNEES[issue.assignee["username"]] + " :אחראי " + "(" +
          issue.time_stats()["human_time_estimate"] + ")")


def next_weekday(date, day):
    """
    Returns the date of the next given weekday after
    the given date. For example, the date of next Monday.

    NB: if it IS the day we're looking for, this returns 0. (nothing change)
    consider then doing onDay(foo, day + 1).
    """
    days = (day - date.weekday() + 7) % 7
    return date + datetime.timedelta(days=days)


if __name__ == '__main__':
    main()
