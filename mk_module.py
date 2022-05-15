def basic_module_details():
    basic_module_details.module_name = module_name = input("Enter the module name: ")
    dependencies = input("Enter the dependencies: ")


def get_no_of_model():
    no_of_models = input("Enter the Number of models in %s module: " % basic_module_details.module_name)
    return int(no_of_models)


def get_field_count(name, model):
    cnt = int(input("Enter the no:of %s fields in %s model: " % name, model))
    return cnt


def get_field_name(field, no, model):
    f_name = input("Enter the name of %s field %s in %s model: " % field, no, model)
    return f_name


def opt_cnt(sel_name):
    opt_cnt = int(input("Enter the no:of Options for %s : " % sel_name))
    return opt_cnt


def get_options(sel_name, opt_cnt):
    opt_name = input("Enter the %s Option for %s Selection Field : " % sel_name.upper(), opt_cnt)
    return opt_name


def get_comodel_name(field_name):
    comodel = input("Enter the comodel name of %s : " % field_name.upper())
    return comodel


def get_basic_fields(det, field_name, model):
    field_cnt = get_field_count(field_name, model)
    if field_cnt:
        fields = det[field_name] = []
        for n in bool_num:
            fields.append(get_field_name(field_name, n, model))


def get_selection_fields(det, model):
    field_count = get_field_count('Selection')
    if field_count:
        sel_field = det['char'] = {}
        for sel in field_count:
            opt_lis = sel_field[get_field_name('Selection', sel)] = []
            for opt in opt_cnt(sel_field.keys()[sel]):
                opt_lis.append(get_options(sel_field.keys()[sel], opt))


def get_many2one2many_fields(det, field_name, model):
    field_count = get_field_count(field_name, model)
    if field_count:
        m2o_field = det[field_name] = {}
        for n in field_count:
            m2o_field[get_field_name(field_name, n, model)] = get_comodel_name(get_field_name(field_name, n, model))


def get_location():
    'location validation needed'
    location = input("Enter The Location In Which The Module  To Be Created: ")
    return location


def collecting_model_name():
    model = input("enter the MODEL Name: ")
    return model


def collecting_details():
    main_details = {}
    for model in get_no_of_model():
        model_name = collecting_model_name()
        mod_det = main_details[model_name] = {}
        get_basic_fields(mod_det, 'Boolean', model_name)
        get_basic_fields(mod_det, 'Char', model_name)
        get_basic_fields(mod_det, 'Integer', model_name)
        get_basic_fields(mod_det, 'Float', model_name)
        get_basic_fields(mod_det, 'Text', model_name)
        get_basic_fields(mod_det, 'Date', model_name)
        get_selection_fields(mod_det, model_name)
        get_many2one2many_fields(mod_det, 'Many2one', model_name)
        get_many2one2many_fields(mod_det, 'One2many', model_name)
        get_many2one2many_fields(mod_det, 'Many2many', model_name)


class ModuleCreation:

    def __init__(self, model_name, model_details):
        self.main_py = None
        self.location = None
        self.model_name = model_name
        self.model_details = model_details

    def creating_directories(self):
        self.location = get_location()
        self.main_py_location = ""

    def creating_fields(self):
        if details['Boolean']:


    def create_model(self):
        py_blueprint = file('blue_print.txt', 'r')
        py_blueprint_data = py_blueprint.readlines()
        main_py = [n.replace('class_name',
                             "".join(list(map(lambda x: x.capitalize(), self.model_name.split('.'))))).replace(
            'model_name_comes_here', self.model_name).replace('model_description_here',
                                                              " ".join(list(map(lambda x: x.capitalize(),
                                                                                self.model_name.split('.')))))
                   for n in py_blueprint_data[:9]]
        self.main_py = main_py


obj = ModuleCreation()
