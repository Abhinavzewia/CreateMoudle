SEL = 'Selection'
M2O = 'Many2one'
O2M = 'One2many'
M2M = 'Many2many'
MAIN_MENU_ID = []
SUB_MENUS = []

def basic_module_details():
    basic_module_details.module_name = module_name = input("Enter the module name: ")
    dependencies = input("Enter the dependencies: ")
    return module_name



def get_location():
    'location validation needed'
    location = input("Enter The Location In Which The Module  To Be Created: ")
    return location


def collecting_model_name():
    model = input("enter the MODEL Name: ")
    return model


def get_no_of_model():
    while True:
        try:
            no_of_models = int(input("Enter the Number of models in %s module: " % basic_module_details.module_name))
        except:
            print('Invalid Entry')
            continue
        break
    return no_of_models


def get_field_count(name, model):
    while True:
        try:
            cnt = int(input("Enter the no:of %s fields in %s model: " % (name, model)))
        except:
            print('Invalid Entry')
            continue
        break
    return cnt


def get_field_name(field, no, model):
    f_name = input("Enter the name of %s field %s in %s model: " % (field, no, model))
    return f_name


def opt_cnt(sel_name):
    while True:
        try:
            opt_cnt = int(input("Enter the no:of Options for %s : " % sel_name))
        except:
            print('Invalid Entry')
            continue
        break
    return opt_cnt


def get_options(sel_name, opt_cnt):
    opt_name = input("Enter the %s Option for %s Selection Field : " % (sel_name.upper(), opt_cnt))
    return opt_name


def get_comodel_name(field_name):
    comodel = input("Enter the comodel name of %s : " % field_name.upper())
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


class ModuleCreation:

    def __init__(self, model_name, model_details, module_name):
        self.main_py = None
        self.location = None
        self.model_name = model_name
        self.model_details = model_details
        self.module_name = module_name
        self.basic_fields = ['Boolean', 'Char', 'Integer', 'Float', 'Text', 'Date']
        self.field_list = []
        self.inherited_models = []
        self.xml_tree_fields = []
        self.xml_form_group1_fields = []
        self.xml_form_group2_fields = []
        self.xml_form_o2m_fields = []
        self.xml_form_m2m_fields = []

    def creating_directories(self):
        self.location = get_location()
        self.main_py_location = ""

    def creating_basic_fields(self):
        for field in self.basic_fields:
            if field in self.model_details:
                self.field_list.extend([self.basic_field_model.replace('field_name1',
                                                           f_name.lower()).replace('string_name',
                                                                                   " ".join([na.capitalize() for na in
                                                                                             f_name.split('_')])).
                                       replace('field_type', field) for
                                       f_name in self.model_details[field]])
        self.fields = {field: type for type in self.model_details for field in self.model_details[type]}

    def creating_many2one_fields(self):
        if M2O in self.model_details:
            self.field_list.extend([self.many2one_field_model.replace('field_name2',
                                                                  f_name.lower()).replace('string_name',
                                                                                          " ".join(
                                                                                              [na.capitalize() for na in
                                                                                               f_name.split('_')])).
                                   replace('model_name', self.model_details[M2O][f_name]).replace('field_type',
                                                                                                      M2O)for
                                   f_name in self.model_details[M2O]])

    def creating_one2many_fields(self):
        def create_inverse_field(f_name):
            inverse_field_details = self.inverse_model.replace('model_name_comes_here', get_comodel(f_name)).replace('class_name', "".join(
                list(map(lambda x: x.capitalize(), get_comodel(f_name).split('.'))))).replace('field_name',
                                                                                              inverse_name).\
                replace('model_name', self.model_name).replace('field_type', M2O).replace('string_name',
                                                                                          " ".join(
                                                                                              [na.capitalize() for na in
                                                                                               self.model_name.split('.')]))
            self.inherited_models.append(inverse_field_details)
        if O2M in self.model_details:
            inverse_name = self.model_name.replace(".", "_") + "_id"
            def get_comodel(f_name):
                return self.model_details[O2M][f_name]
            self.field_list.extend([self.one2many_field_model.replace('field_name3',
                                                                  f_name.lower()).replace('string_name',
                                                                                          " ".join(
                                                                                              [na.capitalize() for na in
                                                                                               f_name.split('_')])).
                                   replace('comodel_name', get_comodel(f_name)).replace('inverse_name',
                                   inverse_name).replace('field_type', O2M) for
                                   f_name in self.model_details[O2M]])
            [create_inverse_field(f) for f in self.model_details[O2M]]

    def creating_many2many_fields(self):
        if M2M in self.model_details:
            self.field_list.extend([self.many2one_field_model.replace('field_name2',
                                                                     f_name.lower()).replace('string_name',
                                                                                             " ".join(
                                                                                                 [na.capitalize() for na
                                                                                                  in
                                                                                                  f_name.split('_')])).
                                   replace('model_name', self.model_details['field'][f_name]).replace('field_type',
                                                                                                      M2M) for
                                   f_name in self.model_details['field']])

    def create_selection_fields(self):
        def get_options(lis):
            return str([(n, n) for n in lis])
        if SEL in self.model_details:
            self.field_list.extend([self.basic_field_model.replace('field_name1',
                                                           f_name.lower()).replace("string_name'",
                                                                                   " ".join([na.capitalize() for na in
                                                                                             f_name.split('_')]) + "', " +
                                                                                   get_options(self.model_details[SEL][f_name])).
                                       replace('field_type', SEL) for
                                       f_name in self.model_details[SEL]])

    def create_model(self):
        py_blueprint = open('blue_print.txt', 'r')
        py_blueprint.seek(0)
        py_blueprint_data = py_blueprint.readlines()
        main_py = [n.replace('class_name',
                             "".join(list(map(lambda x: x.capitalize(), self.model_name.split('.'))))).replace(
            'model_name_comes_here', self.model_name).replace('model_description_here',
                                                              " ".join(list(map(lambda x: x.capitalize(),
                                                                                self.model_name.split('.')))))
                   for n in py_blueprint_data[:9]]
        inherit_py_blueprint = open('inherit_blue_print.txt', 'r')
        inherit_py_blueprint.seek(0)
        inherit_py_blueprint_data = inherit_py_blueprint.read()
        py_blueprint.close()
        inherit_py_blueprint.close()
        self.inverse_model = inherit_py_blueprint_data
        self.basic_field_model = py_blueprint_data[9]
        self.many2one_field_model = py_blueprint_data[10]
        self.one2many_field_model = py_blueprint_data[11]
        self.inherited_models_import = [py_blueprint_data[2]]
        self.main_py = main_py

    def create_files(self):
        self.main_py.extend(self.field_list)
        self.inherited_models_import.extend(self.inherited_models)


    def get_xml_field_models(self):
        xml_blueprint = open('xml_structure.txt', 'r')
        xml_blueprint.seek(0)
        self.xml_blueprint_data = xml_blueprint.readlines()
        xml_blueprint.seek(0)
        self.save_xml_blueprint_data = xml_blueprint.read()
        self.tree_field_model = self.xml_blueprint_data[10]
        self.form_group1_field = self.xml_blueprint_data[22]
        self.form_group2_field = self.xml_blueprint_data[25]
        self.form_o2m_field = self.xml_blueprint_data[36]
        self.form_m2m_field = self.xml_blueprint_data[30]

    def create_list_view(self):
        self.tree_fields = [field  for type in self.field_list for field in type if self.field_list[type] in
                       ['Char', SEL, 'Date', M2O, 'Integer']]
        if self.tree_fields:
            self.xml_tree_fields.extend([self.tree_field_model.replace('field_names', field) for field in self.tree_fields])

    def create_form_view(self):
        self.form_fields1 = [field  for type in self.field_list for field in type if self.field_list[type] not in
                       [O2M, M2M]]
        self.o2m_fields = [field  for type in self.field_list for field in type if self.field_list[type] in
                       [O2M]]
        self.m2m_fields = [field  for type in self.field_list for field in type if self.field_list[type] in
                       [M2M]]
        if self.form_fields1:
            for i, fld in enumerate(self.form_fields1):
                if i % 2:
                    self.xml_form_group1_fields.extend([self.form_group1_field.replace('group_1_fields', fld)])
                else:
                    self.xml_form_group2_fields.extend([self.form_group2_field.replace('group_2_fields', fld)])
        if self.o2m_fields:
            self.xml_form_o2m_fields.extend([self.form_o2m_field.replace('one2many_fields', fld) for fld in self.o2m_fields])
        if self.m2m_fields:
            self.xml_form_m2m_fields.extend([self.form_m2m_field.replace('many2many_fields', fld) for fld in self.m2m_fields])

    def merging_xml_views(self):
        xml_data = self.save_xml_blueprint_data.replace("view_id", "_".join(self.model_name.split('.'))).replace(
            "view_name", " ".join(list(map(lambda x: x.capitalize(), self.model_name.split('.'))))).replace(
            "model_come_here", self.model_name).replace(self.tree_field_model, self.xml_tree_fields).replace(
            "form_string_name", " ".join(list(map(lambda x: x.capitalize(), self.model_name.split('.'))))).replace(
            self.form_group1_field, self.xml_form_group1_fields).replace(
            self.form_group2_field, self.xml_form_group2_fields).replace(
            "action_name", " ".join(list(map(lambda x: x.capitalize(), self.model_name.split('.'))))).replace('action_id',
            "_".join(self.model_name.split('.')))
        if self.o2m_fields:
            xml_data = xml_data.replace(self.form_o2m_field, self.xml_form_o2m_fields)
        else:
            xml_data = xml_data.replace("".join(self.xml_blueprint_data[28:33]), "")
        if self.m2m_fields:
            xml_data = xml_data.replace(self.form_m2m_field, self.xml_form_m2m_fields)
        else:
            xml_data = xml_data.replace("".join(self.xml_blueprint_data[33:40]), "")
        self.xml_data = xml_data

    def get_xml_menu_models(self):
        xml_menu_blueprint = open('xml_menu_structure.txt', 'r')
        xml_menu_blueprint.seek(0)
        self.xml_menu_blueprint_data = xml_menu_blueprint.readlines()
        xml_menu_blueprint.seek(0)
        self.save_xml_menu_blueprint_data = xml_menu_blueprint.read()


    def creating_menu(self):
        if not MAIN_MENU_ID:
            MAIN_MENU_ID.extend([self.xml_menu_blueprint_data[4].replace('Main_menu_name', self.module_name).replace(
                'main_menu_id', self.module_name)])
        SUB_MENUS.extend([self.xml_menu_blueprint_data[6].replace('submenu_name', " ".join(
            list(map(lambda x: x.capitalize(), self.model_name.split('.'))))).replace(
                'submenu_id', "_".join(self.model_name.split('.'))).replace('main_menu_id', self.module_name).replace(
            'menu_action', "_".join(self.model_name.split('.')) + "_action_window")])







# module_name = basic_module_details()
# module_details = collecting_details()
# print(module_details)
dit = {'model.modle': {'Boolean': ['Boolfield1'], 'Char': ['char_field1'], 'Selection': {'sel_field1': ['opt1', 'opt2']}, 'Many2one': {'a': 'test.model'}, 'One2many': {'O2M': 'o.m'}}}

for key, value in dit.items():
    obj = ModuleCreation(key, value, 'test_module')
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
    # print(obj.field_list)
    print(obj.inherited_models_import)
    print(obj.main_py)
    print(obj.xml_data)