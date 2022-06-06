import os
import module_create
import shutil

DATATYPE = {'Char': 'char_name', 'Selection': 'selection_name', 'Many2one': 'm2o_name', 'Date': 'date_name',
            'Boolean': 'bool_name', 'Integer': 'int_name', 'Text': 'text_name', 'Float': 'float_name',
            'One2many': 'o2m_name', 'Many2many': 'm2m_name'}
SEL = 'Selection'
M2O = 'Many2one'
O2M = 'One2many'
M2M = 'Many2many'


def basic_module_details():
    module_name = input("\033[1;37m \nEnter the module name: ").lower().strip()
    if module_name.find("_") == -1:
        module_name = module_name.replace(" ", "_")
    basic_module_details.module_name = module_name
    dependencies = input("\033[1;37m \nEnter the dependencies: ")
    return module_name, dependencies


def get_location():
    while True:
        location = input("\033[1;37m \nEnter The Location In Which The Module  To Be Created: ")
        if os.path.exists(location):
            return location
        print('\033[1;31m \nGiven Path Does Not Exist \nTry Again!')


def collecting_model_name():
    while True:
        model = input("\033[1;37m \nEnter the MODEL Name: ").lower().strip()
        if model.find(".") == -1:
            if model.find("_") != -1:
                return model.replace("_", ".")
            if model.find(" ") != -1:
                return model.replace(" ", ".")
            print("\031[1;31m \n\nInvalid Entry\nTry Again")
            continue
        return model


def get_no_of_model():
    while True:
        try:
            no_of_models = int(
                input("\033[1;37m \nEnter the Number of models in %s module: " % basic_module_details.module_name))
        except:
            print('\033[1;31m \nInvalid Entry\nTry Again')
            continue
        return no_of_models


def get_field_count(name, model):
    while True:
        try:
            cnt = int(input("\033[1;37m \nEnter the no:of %s fields in %s model: " % (name, model)))
        except:
            print('\033[1;31m \nInvalid Entry\nTry Again')
            continue
        return cnt


def get_field_name(field, no, model):
    while True:
        f_name = input(
            "\033[1;37m \nEnter the name of %s field %s in %s model: " % (field, no + 1, model)).lower().strip()
        if f_name.find(" ") != -1:
            print("\031[1;31m \n\nInvalid Entry\nTry Again")
            continue
        if f_name.find(".") != -1:
            print("\031[1;31m \n\nInvalid Entry\nTry Again")
            continue
        return f_name


def opt_cnt(sel_name):
    while True:
        try:
            opt_cnt = int(input("\033[1;37m \nEnter the no:of Options for %s : " % sel_name))
        except:
            print('\033[1;31m \nInvalid Entry\nTry Again')
            continue
        return opt_cnt


def get_options(sel_name, opt_cnt):
    opt_name = input("\033[1;37m \nEnter the %s Option for %s Selection Field : " % (sel_name.upper(), opt_cnt + 1))
    return opt_name


def get_comodel_name(field_name):
    while True:
        comodel = input("\033[1;37m \nEnter the comodel name %s : " % field_name.upper()).lower().strip()
        if comodel.find(".") == -1:
            if comodel.find("_") != -1:
                return comodel.replace("_", ".")
            if comodel.find(" ") != -1:
                return comodel.replace(" ", ".")
            print("\033[1;31m \nInvalid Entry\nTry Again")
            continue
        return comodel


def get_basic_fields(det, field_name, model):
    field_cnt = get_field_count(field_name, model)
    if field_cnt:
        fields = det[field_name] = []
        for n in range(field_cnt):
            fields.append(get_field_name(field_name, n, model))


def get_selection_fields(det, model):
    field_count = get_field_count(SEL, model)
    if field_count:
        sel_field = det[SEL] = {}
        for sel in range(field_count):
            opt_lis = sel_field[get_field_name(SEL, sel, model)] = []
            for opt in range(opt_cnt(list(sel_field)[sel])):
                opt_lis.append(get_options(list(sel_field)[sel], opt))


def get_many2one2many_fields(det, field_name, model):
    field_count = get_field_count(field_name, model)
    if field_count:
        m2o_field = det[field_name] = {}
        for n in range(field_count):
            field_na = get_field_name(field_name, n, model)
            m2o_field[field_na] = get_comodel_name(field_na)


def collecting_details():
    main_details = {}
    for model in range(get_no_of_model()):
        model_name = collecting_model_name()
        mod_det = main_details[model_name] = {}
        get_basic_fields(mod_det, 'Boolean', model_name)
        get_basic_fields(mod_det, 'Char', model_name)
        get_basic_fields(mod_det, 'Integer', model_name)
        get_basic_fields(mod_det, 'Float', model_name)
        get_basic_fields(mod_det, 'Text', model_name)
        get_basic_fields(mod_det, 'Date', model_name)
        get_selection_fields(mod_det, model_name)
        get_many2one2many_fields(mod_det, M2O, model_name)
        get_many2one2many_fields(mod_det, O2M, model_name)
        get_many2one2many_fields(mod_det, M2M, model_name)
    return main_details


def get_file(file):
    # path = os.getcwd()
    return open(os.path.join('static/data', "%s" % file), 'r')


def create_dir(module_path, dir_name):
    os.makedirs(os.path.join(module_path, dir_name))


def creating_py_xml(py, xml, model_name, module_name, location):
    module_path = os.path.join(location, module_name)
    if not os.path.exists(os.path.join(module_path, 'models')):
        create_dir(module_path, 'models')
    if not os.path.exists(os.path.join(module_path, 'view')):
        create_dir(module_path, 'view')
    if not os.path.exists(os.path.join(module_path, 'security')):
        create_dir(module_path, 'security')
    model = "_".join(model_name.split("."))
    py_file = open(os.path.join(module_path, 'models/%s.py' % model), "w")
    py_file.write("".join(py))
    xml_file = open(os.path.join(module_path, 'view/%s.xml' % model), "w")
    xml_file.write("".join(xml))
    xml_menu_file = open(os.path.join(module_path, 'view/menu.xml'), "w")
    xml_menu_file.write("".join(xml))
    py_file.close()
    xml_file.close()
    return model, module_path


def create_init(file_lis, path):
    py_file = open(os.path.join(path, 'models/__init__.py'), "w")
    py_file.write("from . import inherited_file, " + ", ".join(file_lis))
    py_file.close()


def create_manifest(file_lis, path, module_name_cap, dependencies):
    manifest_model_file = get_file('manifest.txt')
    manifest_model_file.seek(0)
    manifest_model = manifest_model_file.read()
    manifest = manifest_model.replace('module_name_here', module_name_cap).replace(
        'depends_file_name',
        ", ".join(["'%s'" % dep.strip() for dep in dependencies.split(",") if dep.strip() != 'base'])).replace(
        'file_name', ",\n".join(["'view/%s.xml'" % n.strip() for n in file_lis])
    )
    manifest_file = open(os.path.join(path, '__manifest__.py'), "w")
    manifest_file.write(manifest)
    manifest_file.close()
    print("\033[1;32m Creating Manifest... \n")
    init = open(os.path.join(path, '__init__.py'), "w")
    init.write("from . import models")
    init.close()


def create_inherit_file(path, inherit_list):
    inherit_file = open(os.path.join(path, 'models/inherited_file.py'), "w")
    inherit_file.write("".join(inherit_list))
    inherit_file.close()


def creating_security(module_name, module_name_cap, path, seq_read, csv_model, csv, xml):
    seq_file_csv = open(os.path.join(path, 'security/ir.model.access.csv'), "w")
    seq_file_csv.write(seq_read.replace(csv_model, "\n".join(csv)))
    seq_file_csv.close()
    seq_file_xml = open(os.path.join(path, 'security/access.xml'), "w")
    seq_file_xml.write(xml.replace('group_name_here', module_name + "_permission").replace(
        'module_name_here', module_name).replace('module_name_cap', module_name_cap))
    seq_file_xml.close()


def create_menu_files(path, main_menu, sub_menu, menu_read):
    menu_file = open(os.path.join(path, 'view/menu.xml'), "w")
    menu_file.write(menu_read.replace(main_menu, "".join(module_create.MAIN_MENU_ID)).replace(sub_menu, "".join(
        module_create.SUB_MENUS)))
    menu_file.close()
#
#
# dit = {'test.model.one': {'Boolean': ['bool1', 'bool2'], 'Char': ['char1', 'char2'], 'Integer': ['int'],
#                           'Float': ['float'], 'Text': ['txt'], 'Date': ['date'],
#                           'Selection': {'selection1': ['a', 'b', 'c'], 'selection2': ['1', '2']},
#                           'Many2one': {'many2one': 'co.model1'},
#                           'One2many': {'one2many1': 'co.model1', 'one2many2': 'co.model2'},
#                           'Many2many': {'teestt': 'co.model1'}},
#        'test.model.two': {'Boolean': ['bool2'], 'Char': ['char2'], 'Integer': ['int2'], 'Float': ['float2'],
#                           'Text': ['text2'], 'Date': ['date2'], 'Selection': {'selection2': ['x', 'y']},
#                           'Many2one': {'many2one': 'co.model2'},
#                           'One2many': {'one2many2': 'co.model5', 'one2many4': 'co.model5'}}}


def delete_dir(file_path):
    shutil.rmtree(file_path)
    print("\033[1;31m Deleting Directory... \n")


def making_structure(details, dependencies, module_name, location):
    try:
        return run_main(details, dependencies, module_name, location)
    except:
        delete_dir(os.path.join(location, module_name))
        return False


def start_function():
    module_name, dependencies = basic_module_details()
    location = get_location()
    module_details = collecting_details()
    run_main(module_details, dependencies, module_name, location)
    print("\033[1;32m MODULE CREATED SUCCESSFULLY \n")
    print("\033[1;32m MODULE PATH >>  %s\n" % os.path.join(location, module_name))


def run_main(details, dependencies, module_name, location):
    inherit_py = []
    file_names = []
    csv_list = []
    for key, value in details.items():
        obj = module_create.ModuleCreation(key, value, module_name, location)
        obj.create_model()
        obj.creating_basic_fields()
        obj.creating_many2one_fields()
        obj.create_selection_fields()
        obj.creating_one2many_fields()
        obj.creating_many2many_fields()
        obj.create_files()
        obj.get_xml_field_models()
        obj.create_list_view()
        obj.create_form_view()
        obj.merging_xml_views()
        obj.get_xml_menu_models()
        obj.creating_menu()
        obj.get_security_file()
        obj.creating_security()
        main_menu = obj.xml_menu_blueprint_data[4]
        submenu = obj.xml_menu_blueprint_data[6]
        menu_read = obj.save_xml_menu_blueprint_data
        inherit_py.extend(obj.inherited_models)
        module_name_cap = obj.module_name_cap
        inherited_models_import = obj.inherited_models_import
        inherited_models_import.extend(inherit_py)
        model, module_path = creating_py_xml(obj.main_py, obj.xml_data, obj.model_name, obj.module_name, location)
        file_names.append(model)
        csv_list.append(obj.csv)
        seq_read = obj.csv_security_data
        csv_model = obj.csv_security_blueprint_data[1]
        xml = obj.xmlsave_security_blueprint_data
    create_inherit_file(module_path, inherited_models_import)
    create_menu_files(module_path, main_menu, submenu, menu_read)
    creating_security(module_name, module_name_cap, module_path, seq_read, csv_model, csv_list, xml)
    create_init(file_names, module_path)
    create_manifest(file_names, module_path, module_name_cap, dependencies)
    return os.path.join(location, module_name)


if __name__ == '__main__':
    dit = {'test.model.one': {'Boolean': ['bool1', 'bool2'], 'Char': ['char1', 'char2'], 'Integer': ['int'],
                              'Float': ['float'], 'Text': ['txt'], 'Date': ['date'],
                              'Selection': {'selection1': ['a', 'b', 'c'], 'selection2': ['1', '2']},
                              'Many2one': {'many2one': 'co.model1'},
                              'One2many': {'one2many1': 'co.model1', 'one2many2': 'co.model2'},
                              'Many2many': {'tesst': 'co.model1'}},
           'test.model.two': {'Boolean': ['bool2'], 'Char': ['char2'], 'Integer': ['int2'], 'Float': ['float2'],
                              'Text': ['text2'], 'Date': ['date2'], 'Selection': {'selection2': ['x', 'y']},
                              'Many2one': {'many2one': 'co.model2'},
                              'One2many': {'one2many2': 'co.model5', 'one2many4': 'co.model5'}}}

    run_main(dit, 'dependencies', 'module_name', '/home/abhi/')


def update_value(con, data, fields, typ):
    if isinstance(con, dict):
        if typ == SEL:
            [con[get_name(data[fields])]] = [[get_name(x) for x in data[n].split(',')] for n in data if
                                             fields.replace('selection_name', 'option_name') == n]
        if typ == M2O:
            con[get_name(data[fields])] = get_name(data[fields.replace('m2o_name', 'm2o_comodel_name')])
        if typ == M2M:
            con[get_name(data[fields])] = get_name(data[fields.replace('m2m_name', 'm2m_comodel_name')])
        if typ == O2M:
            con[get_name(data[fields])] = get_name(data[fields.replace('o2m_name', 'o2m_comodel_name')])
    else:
        con.append(data[fields].strip())


def get_name(model):
    return model.strip().lower()


def arrange_data(MODEL_DETIALS, module):
    FINALRESULT = {}
    for data in MODEL_DETIALS:
        model = FINALRESULT[get_name(data['model_name'])] = {}
        for k, v in DATATYPE.items():
            for fields in data:
                if fields.find(v) != -1 or fields == v:
                    if not model.get(k) and k not in [SEL, M2M, M2O, O2M]:
                        model[k] = []
                    elif not model.get(k) and k in [SEL, M2M, M2O, O2M]:
                        model[k] = {}
                    update_value(model[k], data, fields, k)
    location = module['location']
    if not os.path.exists(location):
        location = os.path.join("/home", os.listdir('/home')[0])
    try:
        res = making_structure(FINALRESULT, module['depends'], module['module_name'], location)
    except:
        return False
    return res
