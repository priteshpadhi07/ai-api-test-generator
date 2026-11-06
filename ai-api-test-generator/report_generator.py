
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.utils import get_column_letter


def generate_excel_report(
    results,
    filename="AI_API_Test_Report.xlsx"
):

    workbook = Workbook()
    sheet = workbook.active
    sheet.title = "API Test Results"

    headers = [
        "Test ID",
        "Description",
        "HTTP Method",
        "Endpoint",
        "Expected Status",
        "Actual Status",
        "Result",
        "Response Time (sec)",
        "Error Message"
    ]

    sheet.append(headers)

    for result in results:

        sheet.append([
            result["test_id"],
            result["description"],
            result["method"],
            result["endpoint"],
            result["expected_status"],
            result["actual_status"],
            result["result"],
            result["response_time"],
            result["error_message"]
        ])

    # Header formatting
    for cell in sheet[1]:

        cell.font = Font(
            bold=True,
            color="FFFFFF"
        )

        cell.fill = PatternFill(
            start_color="1F4E78",
            end_color="1F4E78",
            fill_type="solid"
        )

        cell.alignment = Alignment(
            horizontal="center",
            vertical="center",
            wrap_text=True
        )

    # Result formatting
    for row in range(2, sheet.max_row + 1):

        status_cell = sheet.cell(
            row=row,
            column=7
        )

        if status_cell.value == "PASS":
            color = "C6EFCE"

        elif status_cell.value == "FAIL":
            color = "FFC7CE"

        else:
            color = "FFEB9C"

        status_cell.fill = PatternFill(
            start_color=color,
            end_color=color,
            fill_type="solid"
        )

    # Column widths
    widths = [15, 45, 18, 30, 20, 20, 15, 22, 50]

    for index, width in enumerate(widths, start=1):

        sheet.column_dimensions[
            get_column_letter(index)
        ].width = width

    # Wrap text
    for row in sheet.iter_rows():

        for cell in row:
            cell.alignment = Alignment(
                vertical="top",
                wrap_text=True
            )

    sheet.freeze_panes = "A2"
    sheet.auto_filter.ref = sheet.dimensions

    workbook.save(filename)

    print(f"\nExcel report generated: {filename}")
