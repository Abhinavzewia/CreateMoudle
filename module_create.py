import os

SEL = 'Selection'
M2O = 'Many2one'
O2M = 'One2many'
M2M = 'Many2many'
MAIN_MENU_ID = []
SUB_MENUS = []


def get_file(file):
    # path = os.getcwd()
    return open(os.path.join('static/data', "%s" % file), 'r')


class ModuleCreation:

    def __init__(self, model_name, model_details, module_name, location):
        self.basic_field_model = None
        self.xmlsave_security_blueprint_data = None
        self.inverse_model = None
        self.fields = None
        self.inherited_models_import = None
        self.main_py = None
        self.location = None
        self.model_name = model_name
        self.model_name_cap = " ".join(list(map(lambda x: x.capitalize(), self.model_name.split('.'))))
        self.module_name_cap = " ".join(list(map(lambda x: x.capitalize(), module_name.split('_'))))
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
        self.location = location

    def creating_basic_fields(self):
        for field in self.basic_fields:
            if field in self.model_details:
                self.field_list.extend([self.basic_field_model.replace('field_name1',
                                                                       f_name.lower()).replace('string_name',
                                                                                               " ".join(
                                                                                                   [na.capitalize() for
                                                                                                    na in
                                                                                                    f_name.split(
                                                                                                        '_')])).
                                       replace('field_type', field) for
                                        f_name in self.model_details[field]])
            print("\033[1;32m Creating basic field %s  \n" % field)
        self.fields = {field: typ for typ in self.model_details for field in self.model_details[typ]}

    def creating_many2one_fields(self):
        if M2O in self.model_details:
            self.field_list.extend([self.many2one_field_model.replace('field_name2',
                                                                      f_name.lower()).replace('string_name',
                                                                                              " ".join(
                                                                                                  [na.capitalize() for
                                                                                                   na in
                                                                                                   f_name.split('_')])).
                                   replace('model_name', self.model_details[M2O][f_name]).replace('field_type',
                                                                                                  M2O) for
                                    f_name in self.model_details[M2O]])
            [print("\033[1;32m Creating basic field %s  \n" % f_name) for
             f_name in self.model_details[M2O]]

    def creating_one2many_fields(self):
        def create_inverse_field(f_name):
            inverse_field_details = self.inverse_model.replace('model_name_comes_here', get_comodel(f_name)).replace(
                'class_name', "".join(
                    list(map(lambda x: x.capitalize(), get_comodel(f_name).split('.'))))).replace('field_name',
                                                                                                  inverse_name). \
                replace('model_name', self.model_name).replace('field_type', M2O).replace('string_name',
                                                                                          self.model_name_cap)
            self.inherited_models.append(inverse_field_details)

        if O2M in self.model_details:
            inverse_name = self.model_name.replace(".", "_") + "_id"

            def get_comodel(f_name):
                return self.model_details[O2M][f_name]

            self.field_list.extend([self.one2many_field_model.replace('field_name3',
                                                                      f_name.lower()).replace('string_name',
                                                                                              " ".join(
                                                                                                  [na.capitalize() for
                                                                                                   na in
                                                                                                   f_name.split('_')])).
                replace('comodel_name', get_comodel(f_name)).replace('inverse_name',
                                                                     inverse_name).replace(
                'field_type', O2M) for
                f_name in self.model_details[O2M]])
            [create_inverse_field(f) for f in self.model_details[O2M]]
            [print("\033[1;32m Creating basic field %s  \n" % f_name) for
             f_name in self.model_details[O2M]]

    def creating_many2many_fields(self):
        if M2M in self.model_details:
            self.field_list.extend([self.many2one_field_model.replace('field_name2',
                                                                      f_name.lower()).replace('string_name',
                                                                                              " ".join(
                                                                                                  [na.capitalize() for
                                                                                                   na
                                                                                                   in
                                                                                                   f_name.split('_')])).
                                   replace('model_name', self.model_details[M2M][f_name]).replace('field_type',
                                                                                                  M2M) for
                                    f_name in self.model_details[M2M]])
            [print("\033[1;32m Creating basic field %s  \n" % f_name) for
             f_name in self.model_details[M2M]]

    def create_selection_fields(self):
        def get_options(lis):
            return str([(n, n) for n in lis])

        if SEL in self.model_details:
            self.field_list.extend([self.basic_field_model.replace('field_name1',
                                                                   f_name.lower()).replace("string_name'",
                                                                                           " ".join(
                                                                                               [na.capitalize() for na
                                                                                                in
                                                                                                f_name.split(
                                                                                                    '_')]) + "', selection=" +
                                                                                           get_options(
                                                                                               self.model_details[SEL][
                                                                                                   f_name])).
                                   replace('field_type', SEL) for
                                    f_name in self.model_details[SEL]])
            [print("\033[1;32m Creating basic field %s  \n" % f_name) for
             f_name in self.model_details[SEL]]

    def create_model(self):
        py_blueprint = get_file('blue_print.txt')
        py_blueprint.seek(0)
        py_blueprint_data = py_blueprint.readlines()
        print("\033[1;32m Creating Model... \n")
        main_py = [n.replace('class_name',
                             "".join(list(map(lambda x: x.capitalize(), self.model_name.split('.'))))).replace(
            'model_name_comes_here', self.model_name).replace('model_description_here', self.model_name_cap)
                   for n in py_blueprint_data[:9]]
        inherit_py_blueprint = get_file('inherit_blue_print.txt')
        inherit_py_blueprint.seek(0)
        inherit_py_blueprint_data = inherit_py_blueprint.read()
        py_blueprint.close()
        inherit_py_blueprint.close()
        self.inverse_model = inherit_py_blueprint_data
        self.basic_field_model = py_blueprint_data[9]
        self.many2one_field_model = py_blueprint_data[10]
        self.one2many_field_model = py_blueprint_data[11]
        self.inherited_models_import = [py_blueprint_data[2]]
        print("\033[1;32m Creating Inherited Model... \n")
        self.main_py = main_py

    def create_files(self):
        self.main_py.extend(self.field_list)

    def get_xml_field_models(self):
        xml_blueprint = get_file('xml_structure.txt')
        xml_blueprint.seek(0)
        self.xml_blueprint_data = xml_blueprint.readlines()
        xml_blueprint.seek(0)
        self.save_xml_blueprint_data = xml_blueprint.read()
        self.tree_field_model = self.xml_blueprint_data[10]
        self.form_group1_field = self.xml_blueprint_data[23]
        self.form_group2_field = self.xml_blueprint_data[26]
        self.form_o2m_field = self.xml_blueprint_data[37]
        self.form_m2m_field = self.xml_blueprint_data[31]

    def create_list_view(self):
        self.tree_fields = [typ for typ in self.fields if self.fields[typ] in
                            ['Char', SEL, 'Date', M2O, 'Integer']]
        if self.tree_fields:
            self.xml_tree_fields.extend(
                [self.tree_field_model.replace('field_names', field) for field in self.tree_fields])
            [print("\033[1;32m Creating Tree View... \n") for typ in self.fields if self.fields[typ]]

    def create_form_view(self):
        self.form_fields1 = [typ for typ in self.fields if self.fields[typ] not in
                             [O2M, M2M]]
        self.o2m_fields = [typ for typ in self.fields if self.fields[typ] in
                           [O2M]]
        self.m2m_fields = [typ for typ in self.fields if self.fields[typ] in
                           [M2M]]
        [print("\033[1;32m Creating Form View... \n") for typ in self.fields if self.fields[typ]]

        if self.form_fields1:
            for i, fld in enumerate(self.form_fields1):
                if i % 2:
                    self.xml_form_group2_fields.extend([self.form_group2_field.replace('group_2_fields', fld)])
                else:
                    self.xml_form_group1_fields.extend([self.form_group1_field.replace('group_1_fields', fld)])
        if self.o2m_fields:
            self.xml_form_o2m_fields.extend(
                [self.form_o2m_field.replace('one2many_fields', fld) for fld in self.o2m_fields])
        if self.m2m_fields:
            self.xml_form_m2m_fields.extend(
                [self.form_m2m_field.replace('many2many_fields', fld) for fld in self.m2m_fields])

    def merging_xml_views(self):
        xml_data = self.save_xml_blueprint_data.replace("view_id", "_".join(self.model_name.split('.'))).replace(
            "view_name", self.model_name_cap).replace(
            "model_come_here", self.model_name).replace(self.tree_field_model, "".join(self.xml_tree_fields)).replace(
            "form_string_name", self.model_name_cap).replace(
            self.form_group1_field, "".join(self.xml_form_group1_fields)).replace(
            self.form_group2_field, "".join(self.xml_form_group2_fields)).replace(
            "action_name", self.model_name_cap).replace('action_id',
                                                        "_".join(self.model_name.split('.')))
        print("\033[1;32m Creating Merging Files... \n")
        if self.o2m_fields:
            xml_data = xml_data.replace(self.form_o2m_field, "".join(self.xml_form_o2m_fields))
        else:
            xml_data = xml_data.replace("".join(self.xml_blueprint_data[34:41]), "")
        if self.m2m_fields:
            xml_data = xml_data.replace(self.form_m2m_field, "".join(self.xml_form_m2m_fields))
        else:
            xml_data = xml_data.replace("".join(self.xml_blueprint_data[29:34]), "")
        self.xml_data = xml_data

    def get_xml_menu_models(self):
        print("\033[1;32m Creating Menues... \n")
        xml_menu_blueprint = get_file('xml_menu_structure.txt')
        xml_menu_blueprint.seek(0)
        self.xml_menu_blueprint_data = xml_menu_blueprint.readlines()
        xml_menu_blueprint.seek(0)
        self.save_xml_menu_blueprint_data = xml_menu_blueprint.read()
        xml_menu_blueprint.close()

    def creating_menu(self):
        if not MAIN_MENU_ID:
            MAIN_MENU_ID.extend(
                [self.xml_menu_blueprint_data[4].replace('Main_menu_name', self.module_name_cap).replace(
                    'main_menu_id', self.module_name)])
        SUB_MENUS.extend([self.xml_menu_blueprint_data[6].replace('submenu_name', self.model_name_cap).replace(
            'submenu_id', "_".join(self.model_name.split('.'))).replace('main_menu_id', self.module_name).replace(
            'menu_action', "_".join(self.model_name.split('.')) + "_action_window")])

    def get_security_file(self):
        xml_security_blueprint = get_file('security_xml.txt')
        xml_security_blueprint.seek(0)
        self.xmlsave_security_blueprint_data = xml_security_blueprint.read()
        xml_security_blueprint.close()
        csv_security_blueprint = get_file('security_csv.txt')
        csv_security_blueprint.seek(0)
        self.csv_security_blueprint_data = csv_security_blueprint.readlines()
        csv_security_blueprint.seek(0)
        self.csv_security_data = csv_security_blueprint.read()
        print("\033[1;32m Creating Security... \n")
        xml_security_blueprint.close()

    def creating_security(self):
        self.csv = self.csv_security_blueprint_data[1].replace(
            'model_name_here', self.model_name.replace(".", "_")).replace(
            "module_name_here", self.module_name).replace('group_name_here', self.module_name + "_permission")
