# This is my steel calculator script

# This section of code will create the graphical user interface (GUI)

# load in steel functions which perform operations

# Choose sectiontype and size
import PySimpleGUI as Sg
import steel_functions as st
import Bolt_checks as bc
import math
import sys

sys.path.append("../")
from Timber.Timber import beam_moment, beam_shear, print_calcs, deflection_check
import Concrete
import Retaining_wall as Retaining_wall_script
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib
from resources import key_check, variable_write, isfloat, variable, blank

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
        elif event == Sg.WIN_CLOSED:
            break
    window1.close()

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


def retaining_wall():
    window = Sg.Window('Retaining Wall Calculator', Retaining_wall_script.retaining_wall_layout(), resizable=True).finalize()
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


def Concrete_Beam(concrete_beam):
    window = Sg.Window('Concrete Beam', Concrete.concrete_beam_layout(concrete_beam))
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
            depth = int(values['depth'])
            result = Concrete.beam_moment(int(values['breadth']), depth, int(values['cover']), y, Ast,
                                          float(values['Moment']), float(values['Shear']), float(values['Axial']),
                                          values['stirrups'], float(values['fc']), fy, values['Shape'])

            result1 = Concrete.beam_shear(int(values['breadth']), depth, int(values['cover']), y, Ast,
                                          float(values['Moment']), float(values['Shear']), float(values['Axial']),
                                          values['stirrups'], float(values['fc']), fy, values['Shape'])
            result2 = Concrete.service_moments(int(values['breadth']), depth, int(values['cover']), y, Ast,
                                               float(values['Moment']), float(values['Shear']), float(values['Axial']),
                                               values['stirrups'], float(values['fc']), fy, values)
            window['M'].update(str(round(result['M'] * 0.65, 2)) + '   KNm')
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
            if float(values['Moment']) < result['M'] * 0.65 and result['M'] > result['Mu_min']:
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
    window = Sg.Window('Development Length Calculator', bc.development_layout(), resizable=True)

    while True:
        event, values = window.read()
        if event == Sg.WIN_CLOSED:
            break
        elif event == 'calculate':
            development_length = bc.Development_length({i: values[i] for i in ['fsy','fc','k1','db','cd']})
            window['result'].update(str(development_length) + ' mm')
        elif event == 'calc2':
            development_length = bc.Development_length({i: values[i] for i in ['fsy','fc','k1','db','cd']})
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

concrete_beam = variable('concrete_beam')
variables = {'concrete': concrete_beam, 'steel': 1}

if __name__ == "__main__":
    menu(variables)
