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

