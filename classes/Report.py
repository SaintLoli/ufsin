import openpyxl
from classes.DB_helper import DBHelper
from classes.TABLENAMES import TABLES

database = DBHelper(filepath="../DB/UFSIN_DB.db")

class Report:
    def __init__(self, template_name):
        if template_name == "items_on_warehouses":
            self.workbook = openpyxl.load_workbook("../templates/items_on_warehouses.xlsx")
            self.fill_items_on_warehouses()

        else:
            self.workbook = openpyxl.load_workbook("../templates/empty_template.xlsx")

    def fill_items_on_warehouses(self):
        sheet = self.workbook.active
        row, column = 2, 1
        cell = sheet.cell(row, column)

        for warehouse in database.get_warehouses():
            cell.value = f"{warehouse[0]}\n{warehouse[1]}"

            row += 1
            column += 1
            cell = sheet.cell(row, column)

            all_warehouse_items = database.get_item_name_by_warehouse(warehouse[0])
            for GROUP_NAME in TABLES.keys():
                typed_warehouse_items = [i for i in all_warehouse_items if i[0] == GROUP_NAME]
                other_typed_items = [i for i in all_warehouse_items if i[0] == "other"]

                if typed_warehouse_items:
                    if GROUP_NAME != 'other':
                        cell.value = TABLES[GROUP_NAME]

                        row += 1
                        column += 1
                        cell = sheet.cell(row, column)

                        for item in typed_warehouse_items:
                            cell.value = database.get_item_name_by_type(item[1], item[0])

                            column += 1
                            cell = sheet.cell(row, column)

                            cell.value = item[2]
                            row += 1
                            column -= 1
                            cell = sheet.cell(row, column)

                        column -= 1
                        cell = sheet.cell(row, column)
                    else:
                        for spec_type in database.get_other_types():
                            if spec_type[0] in set(database.get_item_type_by_id(i[1])[0] for i in other_typed_items):
                                cell.value = spec_type[0]

                                row += 1
                                column += 1
                                cell = sheet.cell(row, column)

                                for spec_item in typed_warehouse_items:

                                    if spec_type[0] == database.get_item_type_by_id(spec_item[1])[0]:
                                        cell.value = database.get_item_name_by_type(spec_item[1], spec_item[0])

                                        column += 1
                                        cell = sheet.cell(row, column)

                                        cell.value = spec_item[2]
                                        row += 1
                                        column -= 1
                                        cell = sheet.cell(row, column)

                                column -= 1
                                cell = sheet.cell(row, column)

            column -= 1
            cell = sheet.cell(row, column)

        sheet.column_dimensions["A"] = 45
        sheet.column_dimensions["B"] = 25
        sheet.column_dimensions["C"] = 25
        sheet.column_dimensions["D"] = 10

        self.workbook.save('new_example.xlsx')


if __name__ == "__main__":
    report = Report("items_on_warehouses")