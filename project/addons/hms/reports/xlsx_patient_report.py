from odoo import http # type: ignore
from odoo.http import request, Response # type: ignore
import json
import io
import xlsxwriter # type: ignore
from datetime import datetime


class XlsxPatientReport(http.Controller):

    def _prepare_workbook_style(self, workbook):
        return {
            "header": workbook.add_format(
                {
                    "bold": True,
                    "bg_color": "#2F75B5",
                    "color": "white",
                    "border": 1,
                    "align": "center",
                    "valign": "vcenter",
                }
            ),
            "cell": workbook.add_format(
                {"border": 1, "align": "center", "valign": "vcenter"}
            ),
            "date": workbook.add_format(
                {
                    "border": 1,
                    "align": "center",
                    "valign": "vcenter",
                    "num_format": "yyyy-mm-dd",
                }
            ),
        }

    def _get_report_headers(self):

        return [
            "First Name",
            "Last Name",
            "Email",
            "Age",
            "Birth Date",
            "Blood Type",
            "Department",
            "State",
            "PCR",
            "CR Ratio",
        ]

    def _get_patient_data(self, patient):

        return [
            patient.first_name,
            patient.last_name,
            patient.email,
            patient.age,
            patient.birth_date,
            dict(patient._fields["blood_type"].selection).get(patient.blood_type, ""),
            patient.department_id.name,
            dict(patient._fields["states"].selection).get(patient.states, ""),
            "Yes" if patient.pcr else "No",
            patient.cr_ratio or "",
        ]

    @http.route(
        "/api/hms/patient/report",
        type="http",
        auth="user",
        methods=["GET"],
        csrf=False,
    )
    def generate_excel_report(self, **kw):
        try:

            patient_ids = kw.get('ids', '').split(',')
            patient_ids = [int(id) for id in patient_ids if id.isdigit()]

            if not patient_ids:
                return request.make_json_response(
                {"error": "No patients selected"},
                status=400
                )


            patients = request.env["hms.patient"].sudo().browse(patient_ids)
            if not patients:
                return request.make_json_response(
                    {"error": "No patients found"}, status=404
                )


            output = io.BytesIO()
            workbook = xlsxwriter.Workbook(output, {"in_memory": True})
            worksheet = workbook.add_worksheet("Patients Report")


            styles = self._prepare_workbook_style(workbook)
            headers = self._get_report_headers()


            worksheet.set_column(0, len(headers) - 1, 15)


            for col, header in enumerate(headers):
                worksheet.write(0, col, header, styles["header"])


            for row, patient in enumerate(patients, 1):
                patient_data = self._get_patient_data(patient)
                for col, value in enumerate(patient_data):

                    if col == 4 and value:  # Birth Date column
                        worksheet.write(row, col, value, styles["date"])
                    else:
                        worksheet.write(row, col, value, styles["cell"])


            workbook.close()
            output.seek(0)


            filename = (
                f'patients_report_{datetime.now().strftime("%Y%m%d_%H%M%S")}.xlsx'
            )

            
            return request.make_response(
                output.getvalue(),
                headers=[
                    (
                        "Content-Type",
                        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    ),
                    ("Content-Disposition", f"attachment; filename={filename}"),
                    ("Cache-Control", "no-cache"),
                ],
            )

        except Exception as e:
            return request.make_json_response({"error": str(e)}, status=500)
