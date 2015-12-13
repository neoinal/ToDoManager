from pyramid.response import Response
from pyramid.session import check_csrf_token
from pyramid.view import view_config
from todomanager.models import Task, DBSession


class TaskView(object):

    def __init__(self, request):
        self.request = request

    @view_config(route_name='home', renderer='templates/base.jinja2')
    def home(self):
        return Response(
            "This page does not created yet.",
            content_type='text/plain',
            status_int=500
        )

    @view_config(route_name='create', renderer='templates/create.jinja2')
    def create(self):
        parameter = {
            "page_title": "ToDo Manager - タスクの作成",
            "active_page": "create",
        }

        if self.request.method == 'POST':
            if check_csrf_token(self.request):
                summary = self.request.POST.get("summary")
                if summary is not None:
                    task = Task(summary=summary)
                    DBSession.add(task)
                    result = {
                        "status": "success",
                        "message": "ToDoの登録に成功しました。",
                    }
                else:
                    result = {
                        "status": "error",
                        "message": "内容が入力されていません。",
                    }

                parameter["result"] = result
            else:
                raise ValueError("CSRF token did not match.")
        return parameter

    @view_config(route_name='list', renderer='templates/list.jinja2')
    def list(self):
        tasks = DBSession.query(Task).all()
        return {
            "page_title": "ToDo Manager - タスクの一覧",
            "active_page": "list",
            "tasks": tasks,
        }

    @view_config(route_name='edit', renderer='templates/edit.jinja2')
    def edit(self):
        parameter = {
            "page_title": "ToDo Manager - タスクの編集",
            "active_page": "",
        }
        task_id = int(self.request.matchdict["task_id"])
        task = DBSession.query(Task).get(task_id)
        if self.request.method == 'POST':
            if check_csrf_token(self.request):
                summary = self.request.POST.get("summary")
                if summary is not None:
                    task.summary = summary
                    DBSession.add(task)
                    result = {
                        "status": "success",
                        "message": "ToDoの更新に成功しました。",
                    }
                else:
                    result = {
                        "status": "error",
                        "message": "内容が入力されていません。",
                    }

                parameter["result"] = result
            else:
                raise ValueError("CSRF token did not match.")

        parameter["task"] = task
        return parameter
