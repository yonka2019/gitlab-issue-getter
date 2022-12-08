import gitlab
import datetime

FROM_DATE = (datetime.datetime.now() - datetime.timedelta(days=7))  # - 7 days from now
TO_DATE = (datetime.datetime.now() + datetime.timedelta(days=7))  # + 7 days from now

assignees = {
    "EyalSol": "איל",
    "yonka2019": "יונתן"
}

gl = gitlab.Gitlab(private_token='token')
issues = gl.issues.list(get_all=True)
project = gl.projects.get(project_id)

printed = False

print("-- TO-DO -- ")
for issue in project.issues.list(get_all=True, order_by='due_date'):
    if issue.due_date is not None:
        due_date = datetime.datetime.strptime(issue.due_date, '%Y-%m-%d')
        if FROM_DATE <= due_date <= TO_DATE:

            if (due_date <= datetime.datetime.now()) and not printed:  # print only one time
                print("-- DONE --")
                printed = True

            print(issue.title + " [" + due_date.strftime("%d.%m") + "] - " + assignees[issue.assignee["username"]] + " :אחראי ")

