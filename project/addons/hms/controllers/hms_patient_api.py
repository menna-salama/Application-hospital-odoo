import json
import math
from urllib.parse import parse_qs
from odoo import http # type: ignore
from odoo.http import request # type: ignore


def valid_response(data, pagination_info, status):
    response_body = {
        "message": "Successful",
        "data": data,
    }
    if pagination_info:
        response_body["pagination_info"] = pagination_info
    return request.make_json_response(response_body, status=status)

def invalid_response(error, status):
    response_body = {
        "error": error
    }
    return request.make_json_response(response_body, status=status)


class HmsPatientApi(http.Controller):
    @http.route('/v1/hms/patient', auth='none', methods=['POST'], type="http", csrf=False)
    def post_patient(self):
        args = request.httprequest.data.decode()
        vals = json.loads(args)
        if not vals.get("first_name") or not vals.get("last_name"):
            return request.make_json_response(
                {
                    "status": "error",
                    "message": "first_name and last_name are required",
                },
                status=400,
            )
        try:
            patient = request.env['hms.patient'].sudo().create(vals)
            if patient:
                return request.make_json_response(
                    {
                        "status": "success",
                        "message": "Patient created successfully",
                        "patient_id": patient.id,
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

    @http.route('/v1/hms/patient/<int:id>', method=["PUT"], auth='none', type="http", csrf=False)
    def update_patient(self, id):
        try:
            patient_id = request.env["hms.patient"].sudo().search([("id", "=", id)])
            if not patient_id:
                return request.make_json_response(
                    {
                        "status": "error",
                     "message": "Patient not found",
                    },
                    status=404,
                )
            args = request.httprequest.data.decode()
            vals = json.loads(args)
            patient_id.write(vals)
            return request.make_json_response(
                {
                    "status": "success",
                    "message": "Patient updated successfully",
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

    @http.route('/v1/hms/patient/<int:id>', method=["GET"], auth='none', type="http", csrf=False)
    def get_patient(self, id):
        try:
            patient_id = request.env["hms.patient"].sudo().search([("id", "=", id)])
            if not patient_id:
                return request.make_json_response(
                    {
                        "status": "error",
                     "message": "Patient not found",
                    },
                    status=404,
                )
            patient = patient_id.read()
            return request.make_json_response(
                {
                    "status": "success",
                    "message": "Patient retrieved successfully",
                    "patient": patient,
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

    @http.route('/v1/hms/patient/<int:id>', method=["DELETE"], auth='none', type="http", csrf=False)
    def delete_patient(self, id):
        try:
            patient_id = request.env["hms.patient"].sudo().search([("id", "=", id)])
            if not patient_id:
                return request.make_json_response(
                    {
                        "status": "error",
                        "message": "Patient not found",
                    },
                    status=404,
                )
            patient_id.unlink()
            return request.make_json_response(
                {
                    "status": "success",
                    "message": "Patient deleted successfully",
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

    @http.route('/v1/hms/patients', method=["GET"], auth='none', type="http", csrf=False)
    def get_patients_list(self):
        try:
            params = parse_qs(request.httprequest.query_string.decode('utf-8'))
            patient_domain = []
            page = offset = None
            limit = 4
            if params:
                if params.get('limit'):
                    limit = int(params["limit"][0])
                if params.get('page'):
                    page = int(params["page"][0])
            if page:
                offset = (page * limit) - limit
            if params.get("first_name"):
                patient_domain.append(("first_name", "ilike", params["first_name"][0]))
            patient_ids = (
                request.env["hms.patient"]
                .sudo()
                .search(patient_domain, offset=offset, limit=limit, order="id desc")
            )
            patient_count = request.env["hms.patient"].sudo().search_count(patient_domain)
            if not patient_ids:
                return request.make_json_response(
                    {
                        "status": "error",
                        "message": "No patients found",
                    },
                    status=404,
                )
            return valid_response(
                [
                    {
                        "status": "success",
                        "id": patient_id.id,
                        "first_name": patient_id.first_name,
                        "last_name": patient_id.last_name,
                        "age": patient_id.age,
                    }
                    for patient_id in patient_ids
                ],
                pagination_info={
                    "page": page if page else 1,
                    "limit": limit,
                    "total": patient_count,
                    "pages": math.ceil(patient_count / limit) if limit else 1,
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

    @http.route("/v1/hms/patient/sqlQuery", auth="none", methods=["POST"], type="http", csrf=False)
    def post_patient_by_sqlQuery(self):
        args = request.httprequest.data.decode()
        vals = json.loads(args)
        if not vals.get("first_name") or not vals.get("last_name"):
            return request.make_json_response(
                {
                    "status": "error",
                    "message": "first_name and last_name are required",
                },
                status=400,
            )
        try:
            # patient = request.env["hms.patient"].sudo().create(vals)
            cr = request.env.cr
            columns = ', '.join(vals.keys())
            values = ', '.join(['%s'] * len(vals))
            query = f""" INSERT INTO hms_patient ({columns}) VALUES ({values}) RETURNING id """
            cr.execute(query, tuple(vals.values()))
            patient = cr.fetchone()
            if patient:
                return request.make_json_response(
                    {
                        "status": "success",
                        "message": "Patient created successfully",
                        "patient_id": patient[0],
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
