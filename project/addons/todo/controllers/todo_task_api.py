import json
import math
from urllib.parse import parse_qs
from odoo import http  # type: ignore
from odoo.http import request  # type: ignore


def valid_response(data, pagination_info, status):
    response_body = {
        "message": "Successful",
        "data": data,
    }
    if pagination_info:
        response_body["pagination_info"] = pagination_info
    return request.make_json_response(response_body, status=status)


def invalid_response(error, status):
    response_body = {"error": error}
    return request.make_json_response(response_body, status=status)


class TodoTaskApi(http.Controller):
    @http.route(
        "/v1/todo/task", auth="none", methods=["POST"], type="http", csrf=False
    )
    def post_task(self):
        args = request.httprequest.data.decode()
        vals = json.loads(args)
        if not vals.get("name"):
            return request.make_json_response(
                {
                    "status": "error",
                    "message": "name is required",
                },
                status=400,
            )
        try:
            task = request.env["todo.task"].sudo().create(vals)
            if task:
                return request.make_json_response(
                    {
                        "status": "success",
                        "message": "task created successfully",
                        "task_id": task.id,
                    },
                    status=200,
                )
        except Exception as error:
            return request.make_json_response(
                {
                    "status": "error",
                    "message": str(error),
                },
                status=400,
            )

    @http.route(
        "/v1/todo/task/<int:id>", method=["PUT"], auth="none", type="http", csrf=False
    )
    def update_task(self, id):
        try:
            task_id = request.env["todo.task"].sudo().search([("id", "=", id)])
            if not task_id:
                return request.make_json_response(
                    {
                        "status": "error",
                        "message": "Task not found",
                    },
                    status=404,
                )
            args = request.httprequest.data.decode()
            vals = json.loads(args)
            task_id.write(vals)
            return request.make_json_response(
                {
                    "status": "success",
                    "message": "Task updated successfully",
                },
                status=200,
            )
        except Exception as error:
            return request.make_json_response(
                {
                    "status": "error",
                    "message": str(error),
                },
                status=400,
            )

    @http.route(
        "/v1/todo/task/<int:id>", method=["GET"], auth="none", type="http", csrf=False
    )
    def get_task(self, id):
        try:
            task_id = request.env["todo.task"].sudo().search([("id", "=", id)])
            if not task_id:
                return request.make_json_response(
                    {
                        "status": "error",
                        "message": "Task not found",
                    },
                    status=404,
                )
            task = task_id.read()
            return request.make_json_response(
                {
                    "status": "success",
                    "message": "Task retrieved successfully",
                    "patient": task,
                },
                status=200,
            )
        except Exception as error:
            return request.make_json_response(
                {
                    "status": "error",
                    "message": str(error),
                },
                status=400,
            )

    @http.route(
        "/v1/todo/task/<int:id>",
        method=["DELETE"],
        auth="none",
        type="http",
        csrf=False,
    )
    def delete_task(self, id):
        try:
            task_id = request.env["todo.task"].sudo().search([("id", "=", id)])
            if not task_id:
                return request.make_json_response(
                    {
                        "status": "error",
                        "message": "Task not found",
                    },
                    status=404,
                )
            task_id.unlink()
            return request.make_json_response(
                {
                    "status": "success",
                    "message": "Task deleted successfully",
                },
                status=200,
            )
        except Exception as error:
            return request.make_json_response(
                {
                    "status": "error",
                    "message": str(error),
                },
                status=400,
            )

    @http.route(
        "/v1/todo/tasks", method=["GET"], auth="none", type="http", csrf=False
    )
    def get_tasks_list(self):
        try:
            params = parse_qs(request.httprequest.query_string.decode("utf-8"))
            task_domain = []
            page = offset = None
            limit = 4
            if params:
                if params.get("limit"):
                    limit = int(params["limit"][0])
                if params.get("page"):
                    page = int(params["page"][0])
            if page:
                offset = (page * limit) - limit
            if params.get("name"):
                task_domain.append(("name", "ilike", params["name"][0]))
            task_ids = (
                request.env["todo.task"]
                .sudo()
                .search(task_domain, offset=offset, limit=limit, order="id desc")
            )
            task_count = (
                request.env["hms.patient"].sudo().search_count(task_domain)
            )
            if not task_ids:
                return request.make_json_response(
                    {
                        "status": "error",
                        "message": "No Tasks found",
                    },
                    status=404,
                )
            return valid_response(
                [
                    {
                        "status": "success",
                        "id": task_id.id,
                        "first_name": task_id.name,

                    }
                    for task_id in task_ids
                ],
                pagination_info={
                    "page": page if page else 1,
                    "limit": limit,
                    "total": task_count,
                    "pages": math.ceil(task_count / limit) if limit else 1,
                },
                status=200,
            )
        except Exception as error:
            return request.make_json_response(
                {
                    "status": "error",
                    "message": str(error),
                },
                status=400,
            )

