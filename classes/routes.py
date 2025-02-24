from flask import Flask, render_template, request, redirect, url_for, jsonify
from classes.PCInfo import *
from classes.Filler import *

app = Flask(__name__, template_folder="../layout", static_folder="../static")
database = DBHelper()

'''Информация о пользователе'''
USER_ID = ''

'''Девайсы на момент заполнения'''
USER_DEVICES = JSON_FORM.copy()

@app.route('/')
def redirect_to_panel():
    global USER_ID

    USER_ID = database.get_user_id_by_pc_name(get_pc_name())

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



@app.route("/admin_home",methods=['GET', 'POST'])
def admin_panel():
    fill_devices(USER_ID)
    USER_ROLE = (database.get_user_role(USER_ID))
    if(USER_ROLE==1):

        fill_organizations(USER_ROLE, database.get_organization_name(USER_ID))

        return render_template("organization.html", organization=ORGANIZATIONS)
    if (USER_ROLE == 2):
        fill_organizations(USER_ROLE, database.get_organization_name(USER_ID))
        return render_template("organization.html"
                               , organization=ORGANIZATIONS)
    else:
        return render_template("admin_home.html",
            devices=DEVICES)


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
        fill_report_warehouse(request.form["start_date"],
                              request.form["end_date"])

        return render_template("otchet_ready.html", wrhs_items=ITEMSONSKLAD, name=request.form["report_name"])

    return render_template("otchet.html")



@app.route("/admin_home/<name>/departments")
def departments(name):
    name = name
    fill_departments(name)
    return render_template("departments.html",
                           departments=DEPARTMENTS)

@app.route("/admin_home/<office>/staff")
def department_staff(office):
    office = office
    organization = database.get_organization_name(USER_ID)
    fill_department_staff(organization, office)
    return render_template("staff.html",
                           users=STAFF)


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