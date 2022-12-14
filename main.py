import gitlab
import datetime


def main():
    lesson_date = next_weekday(datetime.datetime.now(), 3)  # 0 - monday

    from_date = (lesson_date - datetime.timedelta(days=7))  # - 7 days from now
    to_date = (lesson_date + datetime.timedelta(days=7))  # + 7 days from now

    print(f"\n[i] FROM DATE: {from_date.date()} -> [{lesson_date.date()}] -> {to_date.date()}\n")

    assignees = {
        "EyalSol": "איל",
        "yonka2019": "יונתן"
    }

    gl = gitlab.Gitlab(private_token='glpat-MsKuF3VDgXm3NXbcSrtn')
    project = gl.projects.get(39312664)

    printed = False

    print("-- TO-DO -- ")
    for issue in project.issues.list(get_all=True, order_by='due_date'):
        if issue.due_date is not None:
            due_date = datetime.datetime.strptime(issue.due_date, '%Y-%m-%d')

            if from_date <= due_date <= to_date:
                if (due_date <= lesson_date) and not printed:  # print only one time
                    print("-- DONE --")
                    printed = True

                print(issue.title + " [" + due_date.strftime("%d.%m") + "] - " + assignees[issue.assignee["username"]] + " :אחראי ")


def next_weekday(date, day):
    """
    Returns the date of the next given weekday after
    the given date. For example, the date of next Monday.

    NB: if it IS the day we're looking for, this returns 0.
    consider then doing onDay(foo, day + 1).
    """
    days = (day - date.weekday() + 7) % 7
    return date + datetime.timedelta(days=days)

if __name__ == '__main__':
    main()
