from flask import Flask, render_template, request, redirect, url_for, jsonify, send_file
from classes.PCInfo import *
from classes.Filler import *
from classes.Report import Report

app = Flask(__name__, template_folder="../layout", static_folder="../static")
database = DBHelper()

'''Информация о пользователе'''
USER_ID = ''
USER_ROLE = ''
USER_ORGANIZATION = ''
'''Девайсы на момент заполнения'''
USER_DEVICES = JSON_FORM.copy()



@app.route('/')
def redirect_to_panel():
    global USER_ID, USER_ROLE, USER_ORGANIZATION

    USER_ID = database.get_user_id_by_pc_name(get_pc_name())
    USER_ROLE = database.get_user_role(USER_ID)
    USER_ORGANIZATION = database.get_user_organization_by_id(USER_ID)
    if not USER_ID:
        database.add_pc_name(get_pc_name())
        USER_ID = (database.get_user_id_by_pc_name(get_pc_name()))



        return redirect(url_for("pc_register"))

    return redirect(url_for('admin_panel'))


@app.route('/pc_register', methods=['GET', 'POST'])
def pc_register():
    PC = PCInfo()
    if request.method == "POST":
        if request.form:
            USER_DEVICES['cpu'] = request.form.get('cpu')
            USER_DEVICES['motherboard'] = request.form.get('motherboard')
            USER_DEVICES['gpu'] = request.form.get('gpu')
            USER_DEVICES['ram'] = request.form.get('ram')
            USER_DEVICES['year'] = request.form.get('year')
            USER_DEVICES['s_number'] = request.form.get('s_number')

            i = 1
            while True:
                device_type = request.form.get(f'device_type_{i}')
                device_name = request.form.get(f'device_name_{i}')
                device_s_number = request.form.get(f'device_s_number_{i}')
                device_year = request.form.get(f'device_year_{i}')

                if not device_type:
                    break

                else:
                    USER_DEVICES['devices'].append(DEVICE_TEMPLATE.copy())
                    USER_DEVICES['devices'][-1]['type'] = device_type
                    USER_DEVICES['devices'][-1]['name'] = device_name
                    USER_DEVICES['devices'][-1]['s_number'] = device_s_number
                    USER_DEVICES['devices'][-1]['year'] = device_year

                i += 1

            return jsonify({'status': 'success', 'message': 'Data received successfully'})

    return render_template("check.html", devices=TABLES, cpu=PC.processor,
                                         motherboard=PC.motherboard,
                                         gpu=PC.video_card)


@app.route('/add_devices', methods=["POST"])
def add_devices():
    database.add_computer_info(user_id=USER_ID,
                               cpu=USER_DEVICES["cpu"],
                               motherboard=USER_DEVICES["motherboard"],
                               gpu=USER_DEVICES["gpu"],
                               ram=USER_DEVICES["ram"],
                               year=USER_DEVICES["year"],
                               s_number=USER_DEVICES["s_number"])
    for device in USER_DEVICES['devices']:
        database.add_item(device['type'], device['name'], USER_ID)
    return redirect(url_for("admin_panel"))


#
# @app.route("/admin_home",methods=['GET', 'POST'])
# def admin_panel():
#     fill_devices(USER_ID)
#     if(USER_ROLE==1):
#
#         fill_organizations(USER_ROLE, database.get_organization_name(USER_ID))
#
#         return render_template("organization.html", organization=ORGANIZATIONS)
#     if (USER_ROLE == 2):
#         fill_organizations(USER_ROLE, database.get_organization_name(USER_ID))
#         return render_template("organization.html"
#                                , organization=ORGANIZATIONS)
#     else:
#         return render_template("admin_home.html",
#             devices=DEVICES)
@app.route("/admin_home", methods=['GET', 'POST'])
def admin_panel():
    fill_devices(USER_ID)
    if request.method == 'POST':
        if 'deleteId' in request.form:

            print(request.form['deleteId'])
            database.delete_organization(database.get_organization_id_by_name(request.form['deleteId']))
            return '', 204
        else:

            name = request.form['name']
            address = request.form['address']
            priority = request.form['priority']

            if 'id' in request.form and request.form['id']:
                org_id = database.get_organization_id_by_name(request.form['name'])
                database.update_organization(org_id, name, address, priority)
            else:
                database.add_organization(name, address, priority)
            return redirect(url_for('admin_panel'))

    if USER_ROLE == 1 or USER_ROLE == 2:
        fill_organizations(USER_ROLE, database.get_organization_name(USER_ID))
        return render_template("organization.html", organization=ORGANIZATIONS)
    else:
        return render_template("admin_home.html", devices=DEVICES)

@app.route("/admin_home")
def staff():
    fill_users()
    return render_template("staff.html", users=USERS)


@app.route("/admin_home/sklad")
def sklad():
    fill_warehouses()
    return render_template("sklad.html", warehouses=WAREHOUSES)


@app.route("/admin_home/otchet", methods=["GET", "POST"])
def otchet():
    if request.method == "POST":
        if request.form.get("format") == "html":
            fill_report_warehouse(request.form["start_date"],
                                  request.form["end_date"])

            return render_template("otchet_ready.html", wrhs_items=ITEMSONSKLAD, name=request.form["report_name"])

        elif request.form.get("format") == "excel":
            report = Report(request.form.get("report_type"), database=database, template_path="templates/")
            file_stream = report.get_bytes_stream()

            # Отправляем файл клиенту
            return send_file(
                file_stream,
                mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                as_attachment=True,
                download_name='{}.xlsx'.format(request.form.get("report_name").replace("/", "_").replace("\\", "_"))
            )

    return render_template("otchet.html")



# @app.route("/admin_home/<name>/departments")
# def departments(name):
#     if (USER_ROLE <= 2):
#         if(USER_ORGANIZATION == name or USER_ORGANIZATION == 'main'):
#             name = name
#             fill_departments(name)
#             return render_template("departments.html",
#                                 departments=DEPARTMENTS)


@app.route("/admin_home/<name>/departments", methods=['GET', 'POST'])
def departments(name):
    global org
    org = name
    if int(USER_ROLE) <= 2:
        if USER_ORGANIZATION == name or USER_ORGANIZATION == 'main':

            if request.method == 'POST':
                if 'deleteId' in request.form:

                    delete_name = request.form['deleteId']
                    print(delete_name)
                    delete_id = database.get_office_id_by_name(delete_name)
                    database.delete_department(delete_id)
                    return '', 204
                else:

                    key = request.form['key']
                    dep_name = request.form['name']
                    supervisor = request.form['supervisor']
                    address = request.form['address']
                    phone = request.form['phone']

                    if 'id' in request.form and request.form['id']:
                        dep_id = database.get_office_id_by_name(request.form['name'])
                        database.update_department(dep_id, key, dep_name, supervisor, address, phone)
                    else:
                        database.add_department(key, dep_name, supervisor, address, phone, name)
                    return redirect(url_for('departments', name=name))

            fill_departments(name)


            return render_template("departments.html", departments=DEPARTMENTS, name=name)
    return "Доступ запрещен", 403






@app.route("/admin_home/<office>/staff", methods=['GET', 'POST'])
def department_staff(office):
    if not (USER_ROLE <= 2 and (database.get_department_organization_by_department_name(office) == USER_ORGANIZATION or USER_ORGANIZATION == 'main')):
        return "Доступ запрещен", 403

    organization = database.get_organization_name(USER_ID)
    fill_department_staff(organization, office)
    ofiices = database.get_departments_of_organization(org)
    print(org)

    if request.method == "POST":

        if 'employeeName' in request.form and 'employeeId' not in request.form:
            name = request.form.get('employeeName')
            access_level = request.form.get('accessLevel')
            organization = request.form.get('organization')
            department = request.form.get('department')
            telephone = request.form.get('telephone')


            if name and access_level and organization and department :
                database.add_person(
                    name,
                    access_level,
                    organization,
                    department,
                    telephone

                )
                fill_department_staff(organization, office)


                return redirect(url_for('department_staff', office=office))

        #
        elif 'employeeId' in request.form:
            print(request.form)
            id_person = request.form.get('employeeId')

            person_name = ""


            for user in STAFF:
                if str(user.id) == id_person:
                    print(user.name)
                    person_name = user.name

            employee_id = database.get_user_id_by_name(person_name)
            name = person_name
            employeeName = request.form.get('employeeName')
            access_level = request.form.get('accessLevel')
            organization = request.form.get('organization')
            department = request.form.get('department')
            telephone = request.form.get('telephone')


            print(employeeName, employee_id, access_level, organization, department)

            department = database.get_office_by_name_of_ofiice(department)

            if employee_id and name and access_level and organization and department :

                database.change_person(employeeName, access_level, organization, department, telephone, employee_id)


                fill_department_staff(organization, office)
                return redirect(url_for('department_staff', office=office))


        elif 'deleteId' in request.form:
            employee_id = request.form.get('deleteId')


            for user in STAFF:
                if str(user.id) == employee_id:
                    employee_id = user.name
                    break

            print(employee_id)
            if employee_id:
                database.cur.execute("DELETE FROM user WHERE fio =? ", ( employee_id,))
                database.con.commit()
                fill_department_staff(organization, office)
                return '', 200


    return render_template("staff.html", users=STAFF, department_name=office,  ofiices=ofiices)

@app.route("/admin_home/staff/<name>", methods=['GET', 'POST'])
def user_devices(name):
    name = name
    this_user_id = database.get_user_id_by_name(name)

    if request.method == "POST":
        print(request.form)
        deviceId = request.form.get("deviceId")
        deviceName = request.form.get("deviceName")
        deviceType = request.form.get("deviceType")
        deviceCustomType = request.form.get("customType")
        deviceSNumber = request.form.get("deviceSNumber")
        deviceYear = request.form.get("deviceYear")

        deleteId = request.form.get("deleteId")
        deleteType = request.form.get("deleteType")
        if deleteType == "undefined":
            deleteType = "other"

        if not deviceId and not deleteId:
            database.add_device(deviceType, database.get_user_id_by_name(name), deviceName, custom_type=deviceCustomType)

        if deviceId:
            for device in DEVICES:
                print(device.id, " device ", deviceId)
                print(device.type, " deviceType ", deviceType)
                if str(device.id) == str(deviceId) and device.type == TABLES[deviceType]:
                    database.edit_device(deviceType, deviceName, device.global_id, custom_type=deviceCustomType)
                elif str(device.id) == str(deviceId) and device.type != TABLES[deviceType]:
                    database.add_device(deviceType, database.get_user_id_by_name(name), deviceName,
                                        custom_type=deviceCustomType)
                    database.delete_device(REVERSE_TABLES[device.type], device.global_id)

        if deleteId:
            for device in DEVICES:
                print(device.id, " device ", deleteId, device.global_id)
                print(device.type, " deviceType ", TABLES[deleteType])
                if str(device.id) == str(deleteId) and device.type == TABLES[deleteType]:
                    database.delete_device(deleteType, device.global_id)

                    return '', 200




        return redirect(url_for("user_devices", name=name, devices=DEVICES, USER_ROLE=USER_ROLE))



    if USER_ROLE <= 2 and (database.get_user_organization_by_id(this_user_id) == USER_ORGANIZATION or USER_ORGANIZATION == 'main'):
        fill_devices(this_user_id)

    return render_template("admin_home.html",
                    devices=DEVICES, USER_ROLE=USER_ROLE, name=name)


# @app.route("/admin_home/departments")
# def departments():
#     fill_departments()
#     return render_template("departments.html",
#                            departments=DEPARTMENTS)

# @app.route("/check_data", methods=["GET", "POST"])
# def check_data():
#     PC = PCInfo()
#     if request.method == "POST":
#         database.add_computer_info(user_id=USER_ID,
#                                    cpu=request.form["cpu"],
#                                    motherboard=request.form["motherboard"],
#                                    gpu=request.form["gpu"],
#                                    ram=request.form["ram"],
#                                    year=request.form["year"],
#                                    s_number=request.form["s_number"])
#
#
#     return render_template("check_old.html", cpu=PC.processor,
#                                          motherboard=PC.motherboard,
#                                          gpu=PC.video_card)



if __name__ == '__main__':
    app.run(debug=True)
    """ыдопыдвлп"""