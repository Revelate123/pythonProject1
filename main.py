# This is my steel calculator script

# This section of code will create the graphical user interface (GUI)

# load in steel functions which perform operations

# Choose sectiontype and size
import PySimpleGUI as Sg
import steel_functions as st
import Bolt_checks as bc
import math
import sys
import csv
sys.path.append("../")
from Timber.Timber import beam_moment, beam_shear, print_calcs, deflection_check
import Concrete
import Retaining_wall as Retaining_wall_script
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib
from resources import key_check

matplotlib.use('TkAgg')


def menu(variables):
    Sg.theme('GrayGrayGray')
    layout1 = [
        [Sg.Button('Steel Calculator', key='Steel_calculator')],
        [Sg.Button('Bolt group actions', key='Bolts')],
        [Sg.Button('Development Length', key='development')],
        [Sg.Button('Timber Calculator', key='Timber_calculator')],
        [Sg.Button('Concrete Beam Calculator', key='Concrete_calculator')],
        [Sg.Button('Retaining Wall Calculator', key='retaining_wall')],
        [Sg.Button('Soldier Pile Retaining wall', key='Soldier pile')],
        [Sg.Button('Laterally Loaded Pile', key='Laterally loaded pile')],
        [Sg.Button('Pad Footing Calculator', key='Pad_footing')],
        [Sg.Button('wind Calculator', key='Wind_calculator')]
    ]
    window1 = Sg.Window('Menu Select', layout1)

    while True:
        event, values1 = window1.read()
        if event == 'Steel_calculator':
            window1.close()
            steel_calculator()
            break
        elif event == 'Bolts':
            window1.close()
            bolts()
            break
        elif event == 'development':
            window1.close()
            development()
            break
        elif event == 'Timber_calculator':
            window1.close()
            Timber()
            break
        elif event == 'Concrete_calculator':
            window1.close()
            Concrete_Beam(concrete_beam)
            break
        elif event == 'Wind_calculator':
            window1.close()
            wind()
        elif event == 'retaining_wall':
            window1.close()
            retaining_wall()
        elif event == 'Soldier pile':
            window1.close()
            soldier_pile()
        elif event == 'Laterally loaded pile':
            window1.close()
            Lateral_pile()
        elif event == 'Pad_footing':
            window1.close()
            Pad_footing()
        elif event == Sg.WIN_CLOSED:
            break
    window1.close()


def variable_write(values, Name):
    # if values['Member Type'] == 'Beam':
    with open(Name + '.txt', 'w', newline='') as csv_file:
        data = [[str(i), values[i]] for i in values]
        print(data)
        writer = csv.writer(csv_file)
        writer.writerows(data)


def variable(Name):
    Dictionary = {}
    with open(str(Name) + '.txt') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            Dictionary[row[0]] = row[1]
    return Dictionary


def isfloat(num):
    try:
        float(num)
        return True
    except ValueError:
        return False


def Lateral_pile():
    layout = [
        [Sg.Column([
            [Sg.Text('Soil Parameters')],
            [Sg.Text('Friction angle:')],
            [Sg.Text('Density of soil:')],
            [Sg.Text('Cohesion:')],
            [Sg.Text('Angle of Backfill:')],
            [Sg.Text('Ka')],
            [Sg.Text('Kp')],
            [Sg.Text('Retained Height')],
            [Sg.Text('Pile Diameter')],
            [Sg.Text('Pile spacing')],
            [Sg.Text('Surcharge')],

            [Sg.Text('Height of sleeper:')],
            [Sg.Text('Depth to Water Table:')]

        ]), Sg.Column([
            [Sg.Text()],
            [Sg.Input(default_text=26, size=(5, 1), key='Friction_angle')],
            [Sg.Input(default_text=20, size=(5, 1), key='Density_soil')],
            [Sg.Input(default_text=5, size=(5, 1), key='cohesion')],
            [Sg.Input(default_text=15, size=(5, 1), key='beta')],
            [Sg.Input(default_text=0.4, size=(5, 1), key='Ka')],
            [Sg.Input(default_text=2.9, size=(5, 1), key='Kp')],
            [Sg.Input(default_text=1.5, size=(5, 1), key='H')],
            [Sg.Input(default_text=450, size=(5, 1), key='Dia')],
            [Sg.Input(default_text=2.25, size=(5, 1), key='Spacing')],
            [Sg.Input(default_text=5, size=(5, 1), key='surcharge')],

            [Sg.Input(default_text=400, size=(5, 1), key='SleeperH')],
            [Sg.Input(default_text=0, size=(5, 1), key='Water_table')]
        ]), Sg.Column([
            [Sg.Text()],
            [Sg.Text('Degrees')],
            [Sg.Text('KN/m3')],
            [Sg.Text('KPa')],
            [Sg.Text('Degrees')],
            [Sg.Checkbox(default=True, text='Override', key='Ka_over')],
            [Sg.Checkbox(default=True, text='Override', key='Kp_over')],

            [Sg.Text('m')],
            [Sg.Text('mm')],
            [Sg.Text('mm')],
            [Sg.Text('KPa')],

            [Sg.Text('mm')],
            [Sg.Text('m')],

        ]), Sg.Column(
            blank(5) + [[Sg.Text(key='Ka1')], [Sg.Text(key='Kp1')]] + blank(5) + [
                [Sg.Checkbox(default=True, text='Water Table', key='Water')]]
        )

        ],
        [Sg.Text('Results:')],
        [Sg.Column([
            [Sg.Text('d:')],
            [Sg.Text('D:')],
            [Sg.Text('Total Embedment, E:')],
            [Sg.Text('Soil Force, Pa:')],
            [Sg.Text('Surcharge Force, Pw:')],
            [Sg.Text('Max Moment:')],
            [Sg.Text('Effective pile width factor:')],

            [Sg.Text('Max moment on sleeper:')],
            [Sg.Text('Max shear on sleeper:')]
        ]), Sg.Column([
            [Sg.Text(key='d')],
            [Sg.Text(key='D')],
            [Sg.Text(key='E')],
            [Sg.Text(key='Pa')],
            [Sg.Text(key='Pw')],
            [Sg.Text(key='Mmax')],
            [Sg.Text(key='f')],

            [Sg.Text(key='M')],
            [Sg.Text(key='V')]
        ]), Sg.Column([
            [Sg.Text('m')],
            [Sg.Text('m')],
            [Sg.Text('m')],
            [Sg.Text('KN')],
            [Sg.Text('KN')],
            [Sg.Text('KNm')],
            [Sg.Text()],

            [Sg.Text('KNm')],
            [Sg.Text('KN')]
        ])],
        [Sg.Text()],
        [Sg.Button('Calculate', key='Calculate'), Sg.Button('Back', key='back')],
        [Sg.Button('Print calculations', key='print_calcs')],
        [Sg.Text('Type Job Name:'), Sg.Input(default_text='Soldier Pile', key='job_name')],
        [Sg.Text('Choose destination:'),
         Sg.Input(key='print_location', default_text=r'C:\Users\tduffett\PycharmProjects\pythonProject1'),
         Sg.FolderBrowse()],
        [Sg.Button('Back', key='back')],
    ]

    window = Sg.Window('Soldier Pile Retaining wall', layout)

    while True:
        event, values = window.read()
        if event == Sg.WIN_CLOSED:
            break
        elif event == 'Calculate':
            for i in values:
                if isfloat(values[i]) == True:
                    values[i] = float(values[i])
            if values['Ka_over'] == False:
                values['Ka'] = (math.cos(values['beta'] / 180 * math.pi) - math.sqrt(
                    math.cos(values['beta'] / 180 * math.pi) ** 2 - math.cos(
                        values['Friction_angle'] / 180 * math.pi) ** 2)) / (
                                       math.cos(values['beta'] / 180 * math.pi) + math.sqrt(
                                   math.cos(values['beta'] / 180 * math.pi) ** 2 - math.cos(
                                       values['Friction_angle'] / 180 * math.pi) ** 2))
                window['Ka1'].update(str(round(values['Ka'], 2)))
            if values['Kp_over'] == False:
                values['Kp'] = math.tan((45 + values['Friction_angle'] / 2) / 180 * math.pi) ** 2
                window['Kp1'].update(str(round(values['Kp'], 2)))
            Result = Retaining_wall_script.Soldier(values)
            for i in Result:
                window[i].update(str(round(Result[i], 3)))


def soldier_pile():
    layout = [
        [Sg.Column([
            [Sg.Text('Soil Parameters')],
            [Sg.Text('Friction angle:')],
            [Sg.Text('Density of soil:')],
            [Sg.Text('Cohesion:')],
            [Sg.Text('Angle of Backfill:')],
            [Sg.Text('Ka')],
            [Sg.Text('Kp')],
            [Sg.Text('Retained Height')],
            [Sg.Text('Pile Diameter')],
            [Sg.Text('Pile spacing')],
            [Sg.Text('Surcharge')],

            [Sg.Text('Height of sleeper:')],
            [Sg.Text('Depth to Water Table:')]

        ]), Sg.Column([
            [Sg.Text()],
            [Sg.Input(default_text=26, size=(5, 1), key='Friction_angle')],
            [Sg.Input(default_text=20, size=(5, 1), key='Density_soil')],
            [Sg.Input(default_text=5, size=(5, 1), key='cohesion')],
            [Sg.Input(default_text=15, size=(5, 1), key='beta')],
            [Sg.Input(default_text=0.4, size=(5, 1), key='Ka')],
            [Sg.Input(default_text=2.9, size=(5, 1), key='Kp')],
            [Sg.Input(default_text=1.5, size=(5, 1), key='H')],
            [Sg.Input(default_text=450, size=(5, 1), key='Dia')],
            [Sg.Input(default_text=2.25, size=(5, 1), key='Spacing')],
            [Sg.Input(default_text=5, size=(5, 1), key='surcharge')],

            [Sg.Input(default_text=400, size=(5, 1), key='SleeperH')],
            [Sg.Input(default_text=0, size=(5, 1), key='Water_table')]
        ]), Sg.Column([
            [Sg.Text()],
            [Sg.Text('Degrees')],
            [Sg.Text('KN/m3')],
            [Sg.Text('KPa')],
            [Sg.Text('Degrees')],
            [Sg.Checkbox(default=True, text='Override', key='Ka_over')],
            [Sg.Checkbox(default=True, text='Override', key='Kp_over')],

            [Sg.Text('m')],
            [Sg.Text('mm')],
            [Sg.Text('mm')],
            [Sg.Text('KPa')],

            [Sg.Text('mm')],
            [Sg.Text('m')],

        ]), Sg.Column(
            blank(5) + [[Sg.Text(key='Ka1')], [Sg.Text(key='Kp1')]] + blank(5) + [
                [Sg.Checkbox(default=True, text='Water Table', key='Water')]]
        )

        ],
        [Sg.Text('Results:')],
        [Sg.Column([
            [Sg.Text('d:')],
            [Sg.Text('D:')],
            [Sg.Text('Total Embedment, E:')],
            [Sg.Text('Soil Force, Pa:')],
            [Sg.Text('Surcharge Force, Pw:')],
            [Sg.Text('Max Moment:')],
            [Sg.Text('Effective pile width factor:')],

            [Sg.Text('Max moment on sleeper:')],
            [Sg.Text('Max shear on sleeper:')]
        ]), Sg.Column([
            [Sg.Text(key='d')],
            [Sg.Text(key='D')],
            [Sg.Text(key='E')],
            [Sg.Text(key='Pa')],
            [Sg.Text(key='Pw')],
            [Sg.Text(key='Mmax')],
            [Sg.Text(key='f')],

            [Sg.Text(key='M')],
            [Sg.Text(key='V')]
        ]), Sg.Column([
            [Sg.Text('m')],
            [Sg.Text('m')],
            [Sg.Text('m')],
            [Sg.Text('KN')],
            [Sg.Text('KN')],
            [Sg.Text('KNm')],
            [Sg.Text()],

            [Sg.Text('KNm')],
            [Sg.Text('KN')]
        ])],
        [Sg.Text()],
        [Sg.Button('Calculate', key='Calculate'), Sg.Button('Back', key='back')],
        [Sg.Button('Print calculations', key='print_calcs')],
        [Sg.Text('Type Job Name:'), Sg.Input(default_text='Soldier Pile', key='job_name')],
        [Sg.Text('Choose destination:'),
         Sg.Input(key='print_location', default_text=r'C:\Users\tduffett\PycharmProjects\pythonProject1'),
         Sg.FolderBrowse()],
        [Sg.Button('Back', key='back')],
    ]

    window = Sg.Window('Soldier Pile Retaining wall', layout)

    while True:
        event, values = window.read()
        if event == Sg.WIN_CLOSED:
            break
        elif event == 'Calculate':
            for i in values:
                if isfloat(values[i]):
                    values[i] = float(values[i])
            if not values['Ka_over']:
                values['Ka'] = (math.cos(values['beta'] / 180 * math.pi) - math.sqrt(
                    math.cos(values['beta'] / 180 * math.pi) ** 2 - math.cos(
                        values['Friction_angle'] / 180 * math.pi) ** 2)) / (
                                       math.cos(values['beta'] / 180 * math.pi) + math.sqrt(
                                   math.cos(values['beta'] / 180 * math.pi) ** 2 - math.cos(
                                       values['Friction_angle'] / 180 * math.pi) ** 2))
                window['Ka1'].update(str(round(values['Ka'], 2)))
            if not values['Kp_over']:
                values['Kp'] = math.tan((45 + values['Friction_angle'] / 2) / 180 * math.pi) ** 2
                window['Kp1'].update(str(round(values['Kp'], 2)))
            Result = Retaining_wall_script.Soldier(values)
            for i in Result:
                window[i].update(str(round(Result[i], 3)))
    return


def pad_footing_write(values):
    with open('Pf.txt', 'w', newline='') as csv_file:
        data = [

        ]

        writer = csv.writer(csv_file)
        writer.writerows(data)


def pad_footing_read():
    Pf = {}
    with open('Pf.txt') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            print(row)
            if row[0] == 'H':
                Pf['H'] = round(float(row[1]))
    return Pf


def blank(n):
    layout = [[]]
    for i in range(n):
        layout += [[Sg.Text('')]]
    return layout


def retaining_wall():
    # retaining_wall = Retaining_wall_read()
    Retaining_wall = variable('retaining_wall')
    list1 = ['Unrestrained', 'Minor', 'Moderate', 'Strong']
    if Retaining_wall['Masonry'] == 'False':
        Retaining_wall['Masonry'] = False
    layout = [
        [Sg.Column([
            [Sg.Text('Retaining Wall Calculator')],
            [Sg.Text('Pure Cantilever'),
             Sg.Checkbox('Masonry wall', key='Masonry', enable_events=True, default=Retaining_wall['Masonry'])],
            [Sg.Text('Dimensions:')],
            [Sg.Text('Wall Height, H:       ')],
            [Sg.Text('Footing Depth, D:     ')],
            [Sg.Text('Length of Toe, Ltoe:  ')],
            [Sg.Text('Length of Heel, Lheel:')],

            [Sg.Text('Soil Properties:')],
            [Sg.Text('Angle of internal friction, \u03A6')],
            [Sg.Text('Soil cohesion, c\'                ')],
            [Sg.Text('Density of soil, \u03B3')],
            [Sg.Text('Allowable bearing capacity:')],
            [Sg.Text('Passive Soil coefficient:')],
            [Sg.Text('Active Soil coefficient:')],
            [Sg.Text('Loads:')],
            [Sg.Text('Surcharge')],
            [Sg.Text('Additional Moment')],
            [Sg.Text('Additional Load ontop of Wall')],
            [Sg.Checkbox('Restrained at Top', default=key_check(Retaining_wall, 'Top_restraint'), key='Top_restraint',
                         enable_events=True)],
            [Sg.Text('Results:')],
            [Sg.Text('Bearing Pressure (SLS):')],
            [Sg.Text('Overturning (ULS):')],
            [Sg.Text('Sliding:')],
            [Sg.Text('Wall vertical steel:')],
            [Sg.Text('Wall horizontal steel:')],
            [Sg.Text('Toe reinforcement:')],
            [Sg.Text('Toe shrinkage steel:')],
            [Sg.Text('Heel reinforcement:')],
            [Sg.Text('Heel shrinkage steel:')]
        ]), Sg.Column([
            [Sg.Text('')],
            [Sg.Text('')],
            [Sg.Text('')],
            [Sg.Input(default_text=key_check(Retaining_wall, 'H'), size=(5, 1), key='H', enable_events=True)],
            [Sg.Input(default_text=key_check(Retaining_wall, 'D'), size=(5, 1), key='D', enable_events=True)],
            [Sg.Input(default_text=key_check(Retaining_wall, 'Ltoe'), size=(5, 1), key='Ltoe', enable_events=True)],
            [Sg.Input(default_text=key_check(Retaining_wall, 'Lheel'), size=(5, 1), key='Lheel', enable_events=True)],
            [Sg.Text('')],
            [Sg.Input(default_text=key_check(Retaining_wall, 'Internal_friction'), size=(5, 1), key='Internal_friction',
                      enable_events=True)],
            [Sg.Input(default_text=key_check(Retaining_wall, 'c'), size=(5, 1), key='c', enable_events=True)],
            [Sg.Input(default_text=key_check(Retaining_wall, 'Soil_density'), size=(5, 1), key='Soil_density',
                      enable_events=True)],
            [Sg.Input(default_text=key_check(Retaining_wall, 'Allowable_bearing'), size=(5, 1), key='Allowable_bearing',
                      enable_events=True)],
            [Sg.Input(default_text=key_check(Retaining_wall, 'Kp'), size=(5, 1), key='Kp', enable_events=True)],
            [Sg.Input(default_text=key_check(Retaining_wall, 'Ka'), size=(5, 1), key='Ka', enable_events=True)],
            [Sg.Text('')],
            [Sg.Input(default_text=key_check(Retaining_wall, 'Surcharge'), size=(5, 1), key='Surcharge',
                      enable_events=True)],
            [Sg.Input(default_text=key_check(Retaining_wall, 'Additional_moment'), size=(5, 1), key='Additional_moment',
                      enable_events=True)],
            [Sg.Input(default_text=key_check(Retaining_wall, 'Additional_load'), size=(5, 1), key='Additional_load',
                      enable_events=True)],
            [Sg.Input(default_text=key_check(Retaining_wall, 'Restraint_height'), size=(5, 1), key='Restraint_height',
                      enable_events=True)],
            [Sg.Text('')],

            [Sg.Text('', key='bearing_check')],
            [Sg.Text('', key='overturning_check')],
            [Sg.Text('', key='sliding_check')],
            [Sg.Text('', key='wall_vertical_steel')],
            [Sg.Text('', key='wall_horizontal_steel')],
            [Sg.Text('', key='toe_horizontal_steel')],
            [Sg.Text('', key='toe_OoP')],
            [Sg.Text('', key='heel_horizontal_steel')],
            [Sg.Text('', key='heel_OoP')]
        ]), Sg.Column([
            [Sg.Text('')],
            [Sg.Text('')],
            [Sg.Text('')],
            [Sg.Text('mm')],
            [Sg.Text('mm')],
            [Sg.Text('mm')],
            [Sg.Text('mm')],
            [Sg.Text('')],
            [Sg.Text('Degrees')],
            [Sg.Text('KPa')],
            [Sg.Text('KN/m3')],
            [Sg.Text('KPa')],
            [Sg.Checkbox(text='Override', key='Kp_over')],
            [Sg.Checkbox(text='Override', key='Ka_over')],
            [Sg.Text('')],
            [Sg.Text('KPa')],
            [Sg.Text('KNm')],
            [Sg.Text('KN')],
            [Sg.Text('Restraint Height mm')],
            [Sg.Text('')],
            [Sg.Text('KPa')],
            [Sg.Text('KNm')],
            [Sg.Text('KN')],
            [Sg.Text('mm2/m')],
            [Sg.Text('mm2/m')],
            [Sg.Text('mm2/m')],
            [Sg.Text('mm2/m')],
            [Sg.Text('mm2/m')],
            [Sg.Text('mm2/m')],
        ]), Sg.Column(blank(12) + [
            [Sg.Text(key='Kp1')],
            [Sg.Text(key='Ka1')]
        ] + blank(6) + [

                          [Sg.Text('OK/NG', key='bearing_OK/NG')],
                          [Sg.Text('OK/NG', key='overturning_OK/NG')],
                          [Sg.Text('OK/NG', key='sliding_OK/NG')],
                          [Sg.Text('minimum')],
                          [Sg.Text('minimum')],
                          [Sg.Text('')],
                          [Sg.Text('')],
                          [Sg.Text('')],
                          [Sg.Text('')]
                      ]), Sg.Column(blank(2) + [
            [Sg.Text('Wall thickness, tw:')],
            [Sg.Text('Shear Key Depth:')],
            [Sg.Text('Shear Key Width:')],
            [Sg.Text('Shear Key Distance from Toe:')],
            [Sg.Text('Angle of Backfill soil:')],
            [Sg.Text('Overburden Soil:')]
        ] + blank(1) + [
                                        [Sg.Text('Concrete Properties')],
                                        [Sg.Text('f\'c')],
                                        [Sg.Text('Concrete Density')],
                                        [Sg.Text('Wall cover')],
                                        [Sg.Text('Footing cover:')],
                                        [Sg.Text('Degree of Crack control')],
                                        [Sg.Text('')],
                                        [Sg.Text('Masonry Properties')],
                                        [Sg.Text('fuc')],
                                        [Sg.Text('Bedding thickness:')],
                                        [Sg.Text('Masonry Block Size:')],
                                        [Sg.Text('Masonry Material:')],
                                        [Sg.Text('Depth from extreme comp. to steel, d:')]

                                    ] + blank(7)), Sg.Column(blank(2) + [
            [Sg.Input(default_text=key_check(Retaining_wall, 'tw'), size=(5, 1), key='tw', enable_events=True)],
            [Sg.Input(default_text=key_check(Retaining_wall, 'SD'), size=(5, 1), key='SD', enable_events=True)],
            [Sg.Input(default_text=key_check(Retaining_wall, 'SW'), size=(5, 1), key='SW', enable_events=True)],
            [Sg.Input(default_text=key_check(Retaining_wall, 'SKD'), size=(5, 1), key='SKD', enable_events=True)],
            [Sg.Input(default_text=key_check(Retaining_wall, 'beta'), size=(5, 1), key='beta', enable_events=True)],
            [Sg.Input(default_text=key_check(Retaining_wall, 'Overburden'), size=(5, 1), key='Overburden',
                      enable_events=True)]
        ] + blank(2) + [

                                                                 [Sg.Input(default_text=key_check(Retaining_wall, 'fc'),
                                                                           size=(5, 1), key='fc', enable_events=True)],
                                                                 [Sg.Input(default_text=key_check(Retaining_wall, 'DC'),
                                                                           size=(5, 1), key='DC', enable_events=True)],
                                                                 [Sg.Input(default_text=key_check(Retaining_wall,
                                                                                                  'wall_cover'),
                                                                           size=(5, 1), key='wall_cover',
                                                                           enable_events=True)],
                                                                 [Sg.Input(default_text=key_check(Retaining_wall,
                                                                                                  'footing_cover'),
                                                                           size=(5, 1), key='footing_cover',
                                                                           enable_events=True)],
                                                                 [Sg.Combo(list1, default_value=list1[0],
                                                                           size=(12, 1), key='crack',
                                                                           enable_events=True)],
                                                                 [Sg.Text('')],
                                                                 [Sg.Text('')],
                                                                 [Sg.Input(
                                                                     default_text=key_check(Retaining_wall, 'fuc'),
                                                                     size=(5, 1), key='fuc', enable_events=True)],
                                                                 [Sg.Input(default_text=key_check(Retaining_wall, 'BT'),
                                                                           size=(5, 1), key='BT', enable_events=True)],
                                                                 [Sg.Combo(['10 series', '15 series', '20 series',
                                                                            '25 series', '30 series'],
                                                                           default_value='20 series',
                                                                           size=(12, 1), key='Masonry_size',
                                                                           enable_events=True)],
                                                                 [Sg.Combo(['Clay', 'Concrete'], default_value='Clay',
                                                                           size=(12, 1), key='Masonry_type',
                                                                           enable_events=True)],
                                                                 [Sg.Input(default_text=120, size=(5, 1), key='d',
                                                                           enable_events=True)]
                                                             ] + blank(7)), Sg.Column(blank(2) + [
            [Sg.Text('mm')],
            [Sg.Text('mm')],
            [Sg.Text('mm')],
            [Sg.Text('mm')],
            [Sg.Text('Degrees')],
            [Sg.Text('mm')]

        ] + blank(2) + [
                                                                                          [Sg.Text('MPa')],
                                                                                          [Sg.Text('KN/m3')],
                                                                                          [Sg.Text('mm')],
                                                                                          [Sg.Text('mm')]
                                                                                      ] + blank(14)),
            Sg.Column(blank(27))],
        [Sg.Button('Calculate', key='Calculate'), Sg.Button('Back', key='back')],
        [Sg.Button('Print calculations', key='print_calcs')],
        [Sg.Text('Type Job Name:'), Sg.Input(default_text='Retaining Walls', key='job_name')],
        [Sg.Text('Choose destination:'),
         Sg.Input(key='print_location', default_text=r'C:\Users\tduffett\PycharmProjects\pythonProject1'),
         Sg.FolderBrowse()],
        [Sg.Button('Back', key='back')],

    ]
    window = Sg.Window('Retaining Wall Calculator', layout, resizable=True).finalize()
    window.Maximize()

    while True:
        event, values = window.read()
        for i in values:
            if event == i:
                variable_write(values, 'retaining_wall')
        if event == Sg.WIN_CLOSED:
            break
        elif event == 'Calculate':
            for i in values:
                if isfloat(values[i]):
                    values[i] = float(values[i])
            if not values['Ka_over']:
                values['Ka'] = (math.cos(values['beta'] / 180 * math.pi) - math.sqrt(
                    math.cos(values['beta'] / 180 * math.pi) ** 2 - math.cos(
                        values['Internal_friction'] / 180 * math.pi) ** 2)) / (
                                       math.cos(values['beta'] / 180 * math.pi) + math.sqrt(
                                   math.cos(values['beta'] / 180 * math.pi) ** 2 - math.cos(
                                       values['Internal_friction'] / 180 * math.pi) ** 2))
                window['Ka1'].update(str(round(values['Ka'], 2)))
            if not values['Kp_over']:
                values['Kp'] = math.tan((45 + values['Internal_friction'] / 2) / 180 * math.pi) ** 2
                window['Kp1'].update(str(round(values['Kp'], 2)))

            h = math.tan(float(values['beta']) / 180 * math.pi) * float(values['Lheel'])
            Dimensions = {'SW': float(values['SW']), 'SD': float(values['SD']), 'SKD': float(values['SKD']),
                          'footing_cover': float(values['footing_cover']), 'H': float(values['H']),
                          'D': float(values['D']), 'tw': float(values['tw']), 'Ltoe': float(values['Ltoe']),
                          'Lheel': float(values['Lheel']), 'h': h, 'wall_cover': float(values['wall_cover'])}
            Results = Retaining_wall_script.bearing(Dimensions, float(values['Allowable_bearing']), float(values['DC']),
                                                    float(values['Soil_density']), float(values['Surcharge']),
                                                    float(values['Additional_moment']), float(values['Ka']),
                                                    float(values['Internal_friction']), float(values['c']),
                                                    float(values['Kp']), values, values['Top_restraint'],
                                                    values['Restraint_height'])
            if values['Masonry'] == False:
                Results2 = Retaining_wall_script.concrete_wall(Dimensions, float(values['Allowable_bearing']),
                                                               float(values['DC']), float(values['Soil_density']),
                                                               float(values['Surcharge']),
                                                               float(values['Additional_moment']), float(values['Ka']),
                                                               float(values['Internal_friction']), float(values['c']),
                                                               float(values['fc']), values['crack'], values)
                window['wall_vertical_steel'].update(str(round(Results2[0])))
                window['wall_horizontal_steel'].update(str(round(Results2[1])))
            else:
                Masonry = {'Masonry_size': values['Masonry_size'], 'BT': float(values['BT']),
                           'Masonry_type': values['Masonry_type'], 'd': values['d']}
                Results2 = Retaining_wall_script.masonry_wall(float(values['d']), 500, float(values['fuc']), Masonry,
                                                              Dimensions, float(values['Ka']),
                                                              float(values['Surcharge']), float(values['Soil_density']),
                                                              values)

                if isinstance(Results2[0], str):
                    window['wall_vertical_steel'].update(Results2[0])
                    window['wall_horizontal_steel'].update(Results2[1])
                else:
                    window['wall_vertical_steel'].update(str(round(Results2[0])))
                    window['wall_horizontal_steel'].update(str(round(Results2[1])))
            Results3 = Retaining_wall_script.concrete_heel(Dimensions, float(values['Allowable_bearing']),
                                                           float(values['DC']), float(values['Soil_density']),
                                                           float(values['Surcharge']),
                                                           float(values['Additional_moment']), float(values['Ka']),
                                                           float(values['Internal_friction']), float(values['c']),
                                                           float(values['fc']), values['crack'], values)
            Results4 = Retaining_wall_script.concrete_toe(Dimensions, float(values['Soil_density']),
                                                          float(values['Surcharge']),
                                                          float(values['Additional_moment']), float(values['Ka']),
                                                          float(values['Internal_friction']), float(values['c']),
                                                          float(values['fc']), values['crack'], Results['qmax_ULS'],
                                                          Results['a_ULS'], values)
            if isinstance(Results['qmax'], str):
                window['bearing_check'].update(Results['qmax'])
            else:
                window['bearing_check'].update(str(round(Results['qmax'])))
                if Results['qmax'] <= float(values['Allowable_bearing']):
                    window['bearing_OK/NG'].update('OK', text_color='green')
                else:
                    window['bearing_OK/NG'].update('NG', text_color='red')
            window['sliding_check'].update(str(round(Results['F'], 1)))

            window['heel_horizontal_steel'].update(str(round(Results3[0])))
            window['heel_OoP'].update(str(round(Results3[1])))
            window['toe_horizontal_steel'].update(str(round(Results4[0])))
            window['toe_OoP'].update(str(round(Results4[1])))
            Results1 = Retaining_wall_script.overturning(Dimensions, float(values['Allowable_bearing']),
                                                         float(values['DC']), float(values['Soil_density']),
                                                         float(values['Surcharge']), float(values['Additional_moment']),
                                                         float(values['Ka']), values, values['Top_restraint'],
                                                         values['Restraint_height'])

            window['overturning_check'].update(str(round(Results1)))
            if Results1 <= 0:
                window['overturning_OK/NG'].update('NG', text_color='red')
            else:
                window['overturning_OK/NG'].update('OK', text_color='green')
            if Results['F'] <= 0:
                window['sliding_OK/NG'].update('NG', text_color='red')
            else:
                window['sliding_OK/NG'].update('OK', text_color='green')
        elif event == 'back':
            window.close()
            menu(variables)


def wind():
    layout = [
        [Sg.Text('Base wind pressure calculator')],
        [Sg.Text('Input')],
        [Sg.Button('Back', key='back')]
    ]
    window = Sg.Window('wind Calcualtor', layout)

    while True:
        event, values = window.read()
        if event == Sg.WIN_CLOSED:
            break
        elif event == 'back':
            window.close()
            menu(variables)

def Concrete_Beam(concrete_beam):
    layout1 = Concrete.concrete_beam_layout(concrete_beam)
    window = Sg.Window('Concrete Beam', layout1)
    while True:
        event, values = window.read()
        for i in values:
            if event == i:
                variable_write(values, 'concrete_beam')
        if event == Sg.WIN_CLOSED:
            break
        elif event == 'Calculate':
            concrete_beam['number of rows of reinforcement'] = int(concrete_beam['number of rows of reinforcement'])
            y = [0 for x in range(concrete_beam['number of rows of reinforcement'])]
            Ast = [0 for x in range(concrete_beam['number of rows of reinforcement'])]
            fy = [0 for x in range(concrete_beam['number of rows of reinforcement'])]
            values['stirrups'] = [float(values['stirrups']), float(values['stirrup2']), float(values['stirrup3'])]
            for x in range(concrete_beam['number of rows of reinforcement']):
                y[x] = float(values['y' + str(x + 1)])
                Ast[x] = float(values['Ast' + str(x + 1)])
                fy[x] = float(values['fy' + str(x + 1)])
            print(y, 'main x')
            try:
                depth = int(values['depth'])
            except:
                depth = int(values['breadth'])
            result = Concrete.beam_moment(int(values['breadth']), depth, int(values['cover']), y, Ast,
                                          float(values['Moment']), float(values['Shear']), float(values['Axial']),
                                          values['stirrups'], float(values['fc']), fy, values['Shape'])
            for x in range(concrete_beam['number of rows of reinforcement']):
                y[x] = float(values['y' + str(x + 1)])
                Ast[x] = float(values['Ast' + str(x + 1)])
            print(y, 'main y')
            result1 = Concrete.beam_shear(int(values['breadth']), depth, int(values['cover']), y, Ast,
                                          float(values['Moment']), float(values['Shear']), float(values['Axial']),
                                          values['stirrups'], float(values['fc']), fy, values['Shape'])
            result2 = Concrete.service_moments(int(values['breadth']), depth, int(values['cover']), y, Ast,
                                               float(values['Moment']), float(values['Shear']), float(values['Axial']),
                                               values['stirrups'], float(values['fc']), fy, values)
            window['M'].update(str(round(result['Mn'] * 0.65, 2)) + '   KNm')
            window['Vuc'].update(str(round(result1['Vuc'] / 1000 * 0.6, 2)) + '   KN')
            window['Vus'].update(str(round(result1['Vus'] / 1000 * 0.6, 2)) + '   KN')
            window['Vu'].update(str(round((result1['Vus'] + result1['Vuc']) / 1000 * 0.6, 2)) + '   KN')
            window['Icr'].update(str("{:.3e}".format(result2['Icr'])) + ' mm^4')
            window['Mcr.t'].update(str(round(result2['Mcr.t'], 1)) + ' KNm')
            window['steel_stress'].update(str(round(result2['steel_stress'])) + ' MPa')
            window['Mu,min'].update(str(round(result['Mu_min'] * 0.65, 1)) + ' KNm')
            window['Ec'].update(str(round(result2['Ec'])) + ' GPa')
            window['Ig'].update(str("{:.3e}".format(result2['Ig'])) + ' mm4')
            window['dn'].update(str(round(result2['dn'])) + ' mm')
            window['Ief'].update(str("{:.3e}".format(result2['Ief'])) + ' mm4')
            if result['Failure mode'] == 'Tensile failure':
                window['Failure_mode'].update(result['Failure mode'], text_color='green')
            else:
                window['Failure_mode'].update(result['Failure mode'], text_color='red')
            if float(values['Moment']) < result['Mn'] * 0.65 and result['Mn'] > result['Mu_min']:
                window['M_check'].update('OK', text_color='green')
            else:
                window['M_check'].update('NG', text_color='red')
            if float(values['Shear']) > (result1['Vus'] + result1['Vuc']) * 0.6:
                window['Vu_check'].update('NG', text_color='red')
            else:
                window['Vu_check'].update('OK', text_color='green')
        elif event == 'number of rows of reinforcement':
            for i in range(int(concrete_beam['number of rows of reinforcement']),
                           int(values['number of rows of reinforcement'])):
                values['y' + str(i + 1)] = 100
                values['Ast' + str(i + 1)] = 0
                values['fy' + str(i + 1)] = 500
            variable_write(values, 'concrete_beam')
            concrete_beam = variable('concrete_beam')
            window.close()
            Concrete_Beam(concrete_beam)
        elif event == 'back':
            window.close()
            menu(variables)


# breadth,depth,cover,rows,fc,y,Ast,stirrups


def Timber():
    layout = [[Sg.Column([[Sg.Text('Timber Calculator')],
                          [Sg.Input(key='b', size=(5, 1), default_text='45'), Sg.Text('Breadth')],
                          [Sg.Input(key='d', size=(5, 1), default_text='240'), Sg.Text('Depth')],
                          [Sg.Combo(['MGP 10', 'MGP 12', 'MGP 15', 'meySPAN 13', 'F17', 'F27'], key='grade',
                                    default_value='MGP 10', size=(15, 1)), Sg.Text('Grade')],
                          [Sg.Combo(['Seasoned', 'Unseasoned'], default_value='Seasoned', key='Seasoned'),
                           Sg.Text('Seasoned')],
                          [Sg.Combo(['5 seconds', '5 minutes', '5 hours', '5 days', '5 months', '50+ years'],
                                    default_value='5 months', key='load_duration'), Sg.Text('Load Duration')],
                          [Sg.Combo(['Yes', 'No'], key='nailed', size=(5, 1), default_value='Yes'),
                           Sg.Text('Are members nailed together?')],
                          [Sg.Combo([1, 2, 3, 4, 5, 6, 7, 8, 9], default_value=1, key='ncom'),
                           Sg.Text('Number of Members joined')],
                          [Sg.Combo([1, 2, 3, 4, 5, 6, 7, 8, 9], key='nmem', default_value=1),
                           Sg.Text('Number of parallel member groups separated by spacing s')],
                          [Sg.Input(key='s', size=(5, 1), default_text='1'),
                           Sg.Text('Spacing, s in mm, if not applicable ignore')],
                          [Sg.Input(key='Length', size=(5, 1), default_text='1000'), Sg.Text('Length in mm'),
                           Sg.Input(key='segment length', size=(5, 1)), Sg.Text('Segment Length')],
                          [Sg.Button('Calculate', key='Calculate')],
                          [Sg.Text(key='Md')],
                          [Sg.Text(key='Vd')],
                          [Sg.Text('Filename:')],
                          [Sg.Input(default_text='TimberBeam', key='name')],
                          [Sg.Text('Comments:')],
                          [Sg.Input(key='comments', default_text='')],
                          [Sg.Text('Choose destination:'), Sg.Input(key='print_location',
                                                                    default_text=r'C:\Users\tduffett\PycharmProjects\pythonProject1'),
                           Sg.FolderBrowse()],
                          [Sg.Button('Print Calcs', key='print'),
                           Sg.Checkbox('Include Design Actions', default=True, key='Design Actions')],
                          [Sg.Button('Back', key='back')]]), Sg.VSeparator(),
               Sg.Column([[Sg.Text('Simply Supported:\nDisplacement Calculator\nDemand Calculator')],
                          [Sg.Input(key='G_UDL', size=(5, 1), default_text='0'), Sg.Text('G UDL'),
                           Sg.Input(key='Q_UDL', size=(5, 1), default_text='0'), Sg.Text('Q UDL')],
                          [Sg.Input(key='G_PL', size=(5, 1), default_text='0'), Sg.Text('G PL'),
                           Sg.Input(key='Q_PL', size=(5, 1), default_text='0'), Sg.Text('Q PL')],
                          [Sg.Input(key='distance', size=(5, 1), default_text='0'),
                           Sg.Text('Point load distance from support')],
                          [Sg.Button('Calculate', key='deflection')],
                          [Sg.Column([
                              [Sg.Text(key='deflection results')]
                          ]), Sg.VSeparator(), Sg.Text(key='moment results'), Sg.VSeparator(),
                              Sg.Text(key='shear results')]]
                         )]]
    window = Sg.Window('Timber', layout)

    while True:
        event, values = window.read()
        if event == 'Calculate':
            if values['Seasoned'] == 'Seasoned':
                seasoned = True
            else:
                seasoned = False
            if values['nailed'] == 'Yes':
                nailed = True
            elif values['nailed'] == 'No':
                nailed = False
            Md = beam_moment(float(values['b']), float(values['d']), values['load_duration'], seasoned,
                             int(values['ncom']), int(values['nmem']), int(values['s']), int(values['Length']),
                             values['grade'], nailed)
            Vd = beam_shear(float(values['b']), float(values['d']), values['load_duration'], seasoned,
                            int(values['ncom']),
                            int(values['nmem']), int(values['s']), int(values['Length']), values['grade'])
            window['Md'].update('PhiMd = ' + str(round(Md[0] / 1000, 1)) + ' KNm')
            window['Vd'].update('PhiVd = ' + str(round(Vd[0] / 1000, 1)) + ' KN')
        elif event == Sg.WIN_CLOSED:
            break
        elif event == 'print':
            if values['Seasoned'] == 'Seasoned':
                seasoned = True
            else:
                seasoned = False
            if values['nailed'] == 'Yes':
                nailed = True
            elif values['nailed'] == 'No':
                nailed = False
            Md = beam_moment(float(values['b']), float(values['d']), values['load_duration'], seasoned,
                             int(values['ncom']), int(values['nmem']), int(values['s']), int(values['Length']),
                             values['grade'], nailed)
            Vd = beam_shear(float(values['b']), float(values['d']), values['load_duration'], seasoned,
                            int(values['ncom']),
                            int(values['nmem']), int(values['s']), int(values['Length']), values['grade'])
            d = deflection_check(float(values['b']), float(values['d']), int(values['ncom']), values['grade'],
                                 float(values['G_UDL']), float(values['Q_UDL']), float(values['G_PL']),
                                 float(values['Q_PL']), float(values['Length']))
            print_calcs(values['name'], values['Design Actions'], d[2] + d[4], d[3] + d[5], Md[0], Md[1], Md[2], Md[3],
                        Md[4], Md[5], Md[6], Md[7], Vd[1], Vd[2], Md[8], Vd[0], values['print_location'],
                        values['comments'], d[0], d[1], float(values['Length']))
        elif event == 'deflection':
            d = deflection_check(float(values['b']), float(values['d']), int(values['ncom']), values['grade'],
                                 float(values['G_UDL']), float(values['Q_UDL']), float(values['G_PL']),
                                 float(values['Q_PL']), float(values['Length']))
            window['deflection results'].update(
                'UDL Deflection: ' + str(round(d[0], 2)) + ' mm\nPoint Load Deflection: ' + str(round(d[1], 2)) +
                ' mm\nTotal Deflection: ' + str(round(d[0] + d[1], 2)) + ' mm')
            window['moment results'].update('UDL Moment:' + str(round(d[2], 2)) + ' KNm\nPL Moment: ' + str(
                round(d[4], 2)) + ' KNm\nTotal Moment :' +
                                            str(round(d[2] + d[4], 2)) + ' KNm')
            window['shear results'].update('UDL Shear: ' +
                                           str(round(d[3], 2)) + ' KN\nPL Shear :' + str(
                round(d[5], 2)) + ' KN\nTotal Shear :' + str(round(d[3] + d[5], 2)) + ' KN')
        elif event == 'back':
            window.close()
            menu(variables)
        elif event == Sg.WIN_CLOSED:
            break


def steel_calculator():
    wb = st.import_steel_data()
    SectionSize = st.steel_data('Universal_Beam',wb)
    window = Sg.Window("Steel Calculator", st.steel_gui(SectionSize), resizable=True)

    while True:
        event, values = window.read()
        if event == 'calculate':
            section_properties = st.calculate(values)
            print(section_properties)
            for i in window.AllKeysDict:
                if i in section_properties:
                    window[i].update(str(round(section_properties[i], 1)))

        elif event == 'SectionType':
            SectionSize = st.steel_data(values[event],wb)
            window['SectionSize'].update(value=SectionSize[0], values=SectionSize)

        elif event == 'restraint':
            if values['restraint'] == 'FU' or values['restraint'] == 'PU':
                window['ends_with_restraint'].update(values=['Any'], value='Any')
            elif values['restraint'] == 'FF' or values['restraint'] == 'FP' or values['restraint'] == 'PP':
                window['ends_with_restraint'].update(values=['None', 'One', 'Both'], value='None')
            elif values['restraint'] == 'FL' or values['restraint'] == 'PL' or values['restraint'] == 'LL':
                window['ends_with_restraint'].update(values=['None'], value='None')
        elif event == 'back':
            window.close()
            menu(variables)
        elif event == 'b2' or event == Sg.WIN_CLOSED:
            break
    window.close()


def bolts():
    layout = [[Sg.Text('Number of rows')],
              [Sg.Input(key='#rows', enable_events=True, size=(5, 1)), Sg.Button('OK', key='rows')],
              [Sg.Button('Back', key='back')]
              ]
    window = Sg.Window("Bolt Calculator", layout)

    while True:
        event, values = window.read()
        if event == 'rows':

            left_column = [[Sg.Text('x')]] + [[Sg.Input(size=(5, 1), key='x' + str(i), default_text='0')] for i in
                                              range(int(values['#rows']))]

            right_column = [[Sg.Text('y')]] + [[Sg.Input(size=(5, 1), key='y' + str(i)),
                                                Sg.Input(key='Bolts in row' + str(i), size=(2, 1), default_text='1'),
                                                Sg.Text('row' + str(i + 1))] for i in range(int(values['#rows']))]

            layout = [
                [Sg.Text('Number of rows')],
                [Sg.Input(default_text=values['#rows'], key='#rows', enable_events=True, size=(5, 1)),
                 Sg.Button('OK', key='rows')],
                [Sg.Text('Bolt Size'), Sg.Input(default_text='20', key='bolt_size', size=(5, 1)), Sg.Text('Bolt grade'),
                 Sg.Combo(['4.6/S'], default_value='4.6/S', key='grade')],
                [Sg.Column(left_column, vertical_alignment='top'), Sg.VSeparator(),
                 Sg.Column(right_column, vertical_alignment='top')],
                [Sg.Input(default_text='0', key='Moment', size=(5, 1)), Sg.Text('Moment')],
                [Sg.Input(default_text='0', key='Shear', size=(5, 1)), Sg.Text('Shear')],
                [Sg.Input(default_text='0', key='Axial', size=(5, 1)), Sg.Text('Axial (Tension Negative)')],
                [Sg.Button('Calculate', key='Calculate'), Sg.Button('Back', key='back')],
                [Sg.Text('', key='result')],
                [Sg.Text('', key='result2')],
                [Sg.Text('', key='result3'), Sg.Text('', key='result33')],
                [Sg.Text('', key='result4'), Sg.Text('', key='result44')]
            ]
            window2 = Sg.Window('Bolt Calculator', layout)
            window.close()
            window = window2
        elif event == Sg.WIN_CLOSED:
            break
        elif event == 'Calculate':
            bolts = {}
            bolts['Size'] = values['bolt_size']
            bolts['Moment'] = values['Moment']
            bolts['Shear'] = values['Shear']
            bolts['Axial'] = values['Axial']
            bolts['rows'] = values['#rows']
            bolts['grade'] = values['grade']
            for i in range(int(values['#rows'])):
                bolts['x' + str(i + 1)] = values['x' + str(i)]
                bolts['y' + str(i + 1)] = values['y' + str(i)]
                bolts['row_' + str(i + 1) + '_bolts'] = values['Bolts in row' + str(i)]
            result = bc.bolt_actions(bolts)
            window['result'].update(str(result[0]) + ' kN Axial Force on bolt')
            window['result2'].update(str(result[1]) + ' kN Shear Force on bolt')
            window['result3'].update(str(result[2]) + ' kN Bolt tensile capacity')
            window['result4'].update(str(result[3]) + ' kN Bolt shear capacity')
            if abs(result[0]) > result[2]:
                window['result33'].update('FAIL')

            elif abs(result[0]) < result[2]:
                window['result33'].update('PASS')

            if result[1] > result[3]:
                window['result44'].update('FAIL')

            elif result[1] < result[3]:
                window['result44'].update('PASS')

        elif event == 'back':
            window.close()
            menu(variables)
    window.close()


def development():
    right = [
        [Sg.Text('fsy characteristic yield strength of reinforcement, determined in accordance with Clause 3.2.1')],
        [Sg.Text('f \'c characteristic compressive (cylinder) strength of concrete at 28 days')],
        [Sg.Text('Bar diameter in mm')],
        [Sg.Text(
            'k1 a coefficient that accounts for the bond properties of the bonded reinforcement (see Clause 8.6.2.3)')],
        [Sg.Text('cd a dimension (in mm) corresponding to the smaller of the concrete'
                 ' cover to a bar developing stress and half the clear distance to the next'
                 ' parallel bar developing stress, as shown in Figure 13.1.2.2')]
    ]
    left = [
        [Sg.Input(size=(5, 2), key='fsy', default_text='400')],
        [Sg.Input(size=(5, 1), key='fc', default_text='20')],
        [Sg.Input(size=(5, 1), key='db', default_text='30')],
        [Sg.Input(size=(5, 1), key='k1', default_text=1)],
        [Sg.Input(size=(5, 3), key='cd', default_text='30')]
    ]
    layout2 = [
        [Sg.Text('Enter properties')],
        [Sg.Column(left, vertical_alignment='top'), Sg.VSeparator(), Sg.Column(right, vertical_alignment='top')],
        [Sg.Button('Calculate', key='calculate')],
        [Sg.Text('Minimum Development Length (AS3600:2018 Clause 13.1.2.2):')],
        [Sg.Text('', key='result')],
        [Sg.Text('Bar stress developed over length:'), Sg.Input(default_text='500', size=(5, 1), key='L'),
         Sg.Button('Calculate', key='calc2')],
        [Sg.Text('', key='result1')],
        [Sg.Button('Back', key='back')]
    ]
    window = Sg.Window('Development Length Calculator', layout2, resizable=True)

    while True:
        event, values = window.read()
        if event == Sg.WIN_CLOSED:
            break
        elif event == 'calculate':
            bar_properties = {}
            bar_properties['fsy'] = values['fsy']
            bar_properties['fc'] = values['fc']
            bar_properties['k1'] = values['k1']
            bar_properties['db'] = values['db']
            bar_properties['cd'] = values['cd']
            development_length = bc.Development_length(bar_properties)
            window['result'].update(str(development_length) + ' mm')
        elif event == 'calc2':
            bar_properties = {}
            bar_properties['fsy'] = values['fsy']
            bar_properties['fc'] = values['fc']
            bar_properties['k1'] = values['k1']
            bar_properties['db'] = values['db']
            bar_properties['cd'] = values['cd']
            development_length = bc.Development_length(bar_properties)
            window['result'].update(str(development_length) + ' mm')
            window['result1'].update(
                str(min(round(int(values['L']) / development_length * int(values['fsy'])), int(values['fsy']))) +
                ' MPa or ' +
                str(round(
                    0.8 * min(int(values['L']) / development_length * int(values['fsy']), int(values['fsy'])) * int(
                        values['db']) ** 2 / 4 * math.pi / 1000)) + ' KN')
        elif event == 'back':
            window.close()
            menu(variables)
    window.close()


steel = 1


def draw_figure(canvas, figure):
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
    return figure_canvas_agg


concrete_beam = variable('concrete_beam')
variables = {'concrete': concrete_beam, 'steel': steel}

if __name__ == "__main__":
    menu(variables)
