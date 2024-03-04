# This script will perform calculations pertaining to the design of a retaining wall.
# Initially, these calculations will conservatively only account for freestanding retaining walls.
# Further functionality may be added in the future.

# Checks to be performed on a retaining wall are:
# 1. Check bearing pressures using SLS loads and allowable bearing pressures
# 2. Check for overturning about the toe
# 3. Check for sliding failure
# 4. Determine Steel requirements within wall
import math
import Concrete
import sympy
import PySimpleGUI as Sg
from resources import key_check, variable_write, isfloat, variable, blank

def retaining_wall_layout():
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
    return layout

def bearing(Dimensions, allowable_end_pressure, density_concrete, density_soil, surcharge, Additional_moment, Ka,
            Internal_friction, c, Kp, values, Top_restraint, Restraint_height):
    PA1 = 0.5 * Ka * density_soil * (Dimensions['H'] + Dimensions['D'] + Dimensions['h']) ** 2 * 10 ** -6

    PA2 = Ka * surcharge * (Dimensions['H'] + Dimensions['D'] + Dimensions['h']) * 10 ** -3

    values['Additional_load'] = float(values['Additional_load'])

    values['Overburden'] = float(values['Overburden'])

    N = density_concrete * Dimensions['H'] * Dimensions['tw'] * 10 ** -6 + (Dimensions['Ltoe']
                                                                            + Dimensions['Lheel']) * Dimensions[
            'D'] * density_concrete * 10 ** -6 \
        + Dimensions['Lheel'] * Dimensions['H'] * density_soil * 10 ** -6 + surcharge * Dimensions['Lheel'] * 10 ** -3 \
        + Dimensions['SW'] * Dimensions['SD'] * density_concrete * 10 ** -6 + values['Additional_load'] + values[
            'Overburden'] * density_soil * (Dimensions['Ltoe'] - Dimensions['tw']) * 10 ** -6

    centroid_N = (density_concrete * Dimensions['H'] * Dimensions['tw'] * 10 ** -6 * (
            Dimensions['Ltoe'] - Dimensions['tw'] / 2) + (Dimensions['Ltoe']
                                                          + Dimensions['Lheel']) * Dimensions[
                      'D'] * density_concrete * 10 ** -6 * (Dimensions['Ltoe'] + Dimensions['Lheel']) / 2
                  + Dimensions['Lheel'] * Dimensions['H'] * density_soil * 10 ** -6 * (
                          Dimensions['Ltoe'] + 0.5 * Dimensions['Lheel']) + surcharge * Dimensions[
                      'Lheel'] * 10 ** -3 * (Dimensions['Ltoe'] + 0.5 * Dimensions['Lheel'])
                  + Dimensions['SW'] * Dimensions['SD'] * density_concrete * 10 ** -6 * (Dimensions['SKD'] / 2)
                  + values['Additional_load'] * (Dimensions['Ltoe'] - Dimensions['tw'] / 2) + values[
                      'Overburden'] * density_soil * (Dimensions['Ltoe'] - Dimensions['tw']) ** 2 / 2 * 10 ** -6) / N

    Moment = PA1 * (Dimensions['H'] + Dimensions['D'] + Dimensions['h']) / 3 * 10 ** -3 + PA2 * (
            Dimensions['H'] + Dimensions['D'] + Dimensions['h']) / 2 * 10 ** -3 + Additional_moment

    x = Moment / N

    a = 3 * (centroid_N * 10 ** -3 - x)

    if a < (Dimensions['Ltoe'] + Dimensions['Lheel']) * 10 ** -3 and x < centroid_N * 10 ** -3:
        qmax = 2 * N / a
    elif a > (Dimensions['Ltoe'] + Dimensions['Lheel']) * 10 ** -3:
        M = -N * (centroid_N - Dimensions['Ltoe'] / 2 - Dimensions['Lheel'] / 2) * 10 ** -3 \
            + Moment
        qmax = N / ((Dimensions['Ltoe'] + Dimensions['Lheel']) * 10 ** -3) + 6 * M / (
                (Dimensions['Ltoe'] + Dimensions['Lheel']) * 10 ** -3) ** 2
        a = (Dimensions['Ltoe'] + Dimensions['Lheel']) * 10 ** -3
    elif x > centroid_N * 10 ** -3:
        qmax = 'INCREASE LENGTH'
    Moment = 1.25 * PA1 * (Dimensions['H'] + Dimensions['D'] + Dimensions['h']) / 3 * 10 ** -3 + 1.5 * PA2 * (
            Dimensions['H'] + Dimensions['D'] + Dimensions['h']) / 2 * 10 ** -3 + Additional_moment
    x_ULS = Moment / N
    a_ULS = 3 * (centroid_N * 10 ** -3 - x_ULS)
    if a_ULS < (Dimensions['Ltoe'] + Dimensions['Lheel']) * 10 ** -3 and x_ULS < centroid_N * 10 ** -3:
        qmax_ULS = 2 * N / a_ULS
    elif a_ULS > (Dimensions['Ltoe'] + Dimensions['Lheel']) * 10 ** -3:
        M1 = -N * (centroid_N - Dimensions['Ltoe'] / 2 - Dimensions['Lheel'] / 2) * 10 ** -3 \
             + Moment
        qmax_ULS = N / ((Dimensions['Ltoe'] + Dimensions['Lheel']) * 10 ** -3) + 6 * M1 / (
                (Dimensions['Ltoe'] + Dimensions['Lheel']) * 10 ** -3) ** 2
        a_ULS = (Dimensions['Ltoe'] + Dimensions['Lheel']) * 10 ** -3
    elif x_ULS > centroid_N * 10 ** -3:
        qmax_ULS = 10
        a_ULS = 10000

    print('Auls', a_ULS, PA1, PA2, qmax_ULS)

    F = 0.9 * (N * math.tan(
        0.75 * Internal_friction / 180 * math.pi) + c * a_ULS) - 1.25 * PA1 - 1.5 * PA2 + 0.9 * 0.5 * Kp * (
                Dimensions['D'] + Dimensions['SD'] + values['Overburden']) ** 2 * density_soil * 10 ** -6
    results = {'qmax': qmax, 'F': F, 'a_ULS': a_ULS, 'qmax_ULS': qmax_ULS, 'PA1': PA1, 'PA2': PA2, 'N': N,
               'N_centroid': centroid_N, 'a': a}
    return results


def overturning(Dimensions, allowable_end_pressure, density_concrete, density_soil, surcharge, Additional_moment, Ka,
                values, Top_restraint, Restraint_height):
    PA1 = 0.5 * Ka * density_soil * (Dimensions['H'] + Dimensions['D'] + Dimensions['h']) ** 2 * 10 ** -6
    PA2 = Ka * surcharge * (Dimensions['H'] + Dimensions['D'] + Dimensions['h']) * 10 ** -3
    Moment = 1.25 * PA1 * (Dimensions['H'] + Dimensions['D'] + Dimensions['h']) / 3 * 10 ** -3 + 1.5 * PA2 * (
            Dimensions['H'] + Dimensions['D'] + Dimensions['h']) / 2 * 10 ** -3 + Additional_moment
    M = (density_concrete * Dimensions['H'] * Dimensions['tw'] * (Dimensions['Ltoe'] - Dimensions['tw'] / 2) * 10 ** -9 \
         + (Dimensions['Ltoe'] + Dimensions['Lheel']) * Dimensions['D'] * density_concrete * ( \
                     Dimensions['Ltoe'] + Dimensions['Lheel']) / 2 * 10 ** -9 \
         + Dimensions['Lheel'] * Dimensions['H'] * density_soil * ( \
                     Dimensions['Ltoe'] + Dimensions['Lheel'] / 2) * 10 ** -9 + Dimensions['SW'] * Dimensions[
             'SD'] * density_concrete * (Dimensions['SKD'] + Dimensions['SW'] / 2) * 10 ** -9 \
         + surcharge * Dimensions['Lheel'] * (Dimensions['Ltoe'] + Dimensions['Lheel'] / 2) * 0.4 * 10 ** -6 \
         + values['Additional_load'] * (Dimensions['Ltoe'] - Dimensions['tw'] / 2) * 10 ** -3 \
         + Dimensions['Lheel'] * Dimensions['h'] * 0.5 * density_soil * (
                 Dimensions['Ltoe'] + Dimensions['Lheel'] * 2 / 3) * 10 ** -9) * 0.9 \
        - Moment
    return M


def concrete_wall(Dimensions, allowable_end_pressure, density_concrete, density_soil, surcharge, Additional_moment, Ka,
                  Internal_friction, c, fc, crack, values):
    PA1 = 0.5 * Ka * density_soil * (Dimensions['H'] + Dimensions['D'] + Dimensions['h']) ** 2 * 10 ** -6
    PA2 = Ka * surcharge * (Dimensions['H'] + Dimensions['D'] + Dimensions['h']) * 10 ** -3
    M = 1.5 * (PA1 * Dimensions['H'] / 3 * 10 ** -3) + PA2 * Dimensions['H'] / 2 * 10 ** -3
    d = Dimensions['tw'] - Dimensions['wall_cover'] - 10
    p = 2.5 * M / d ** 2
    pmin = 0.2 * (Dimensions['tw'] / d) ** 2 * (0.6 * math.sqrt(fc) / 500)
    p = max(p, pmin)
    print(p, 'p', M, d)
    results = {'Mn': 0, 'Mu_min': 0}
    Ast = [p * 1000 * d]
    while results['Mn'] * 0.65 < M or results['Mu_min'] > results['Mn']:
        results = Concrete.beam_moment(1000, Dimensions['tw'], Dimensions['wall_cover'],
                                       [Dimensions['tw'] - Dimensions['wall_cover']], Ast, M, 0, 0, [0, 0, 0], fc,
                                       [500])
        print(results, 'ast')
        Ast[0] = Ast[0] + 10
    print(results, 'ast')

    if crack == 'Moderate':
        Ast1 = 0.0035 * Dimensions['tw'] * 1000
    elif crack == 'Minor':
        Ast1 = 0.00175 * Dimensions['tw'] * 1000
    elif crack == 'Strong':
        Ast1 = 0.006 * Dimensions['tw'] * 1000
    elif crack == 'Unrestrained':
        Ast1 = 0.00175 * Dimensions['tw'] * 1000
    Ast[0] = max(0.75 * Ast1, Ast[0])
    results = [Ast[0], Ast1]
    return results


def concrete_heel(Dimensions, allowable_end_pressure, density_concrete, density_soil, surcharge, Additional_moment, Ka,
                  Internal_friction, c, fc, crack, values):
    PA1 = 0.5 * Ka * density_soil * (Dimensions['H'] + Dimensions['D'] + Dimensions['h']) ** 2 * 10 ** -6
    PA2 = Ka * surcharge * (Dimensions['H'] + Dimensions['D'] + Dimensions['h']) * 10 ** -3
    M = 1.5 * (PA1 * Dimensions['H'] / 3 * 10 ** -3) + PA2 * Dimensions['H'] / 2 * 10 ** -3
    d = Dimensions['D'] - Dimensions['footing_cover'] - 10
    p = 2.5 * M / d ** 2
    pmin = 0.2 * (Dimensions['D'] / d) ** 2 * (0.6 * math.sqrt(fc) / 500)
    p = max(p, pmin)

    results = {'M': 0, 'Mu_min': 0}
    Ast = [p * 1000 * d]
    while results['M'] * 0.65 < M or results['Mu_min'] > results['M']:
        results = Concrete.beam_moment(1000, Dimensions['D'], Dimensions['footing_cover'],
                                       [Dimensions['D'] - Dimensions['footing_cover']], Ast, M, 0, 0, [0, 0, 0], fc,
                                       [500], 'Rectangle')

        Ast[0] = Ast[0] + 10

    if crack == 'Moderate':
        Ast1 = 0.0035 * Dimensions['tw'] * 1000
    elif crack == 'Minor':
        Ast1 = 0.00175 * Dimensions['tw'] * 1000
    elif crack == 'Strong':
        Ast1 = 0.006 * Dimensions['tw'] * 1000
    elif crack == 'Unrestrained':
        Ast1 = 0.00175 * Dimensions['tw'] * 1000
    Ast[0] = max(0.75 * Ast1, Ast[0])
    results = [Ast[0], Ast1]
    return results


def concrete_toe(Dimensions, density_soil, surcharge, Additional_moment, Ka, Internal_friction, c, fc, crack, qmax_ULS,
                 a_ULS, values):
    if a_ULS * 1000 < Dimensions['Ltoe']:
        M = a_ULS * qmax_ULS * 0.5 * (Dimensions['Ltoe'] * 10 ** -3 - a_ULS / 3)

    else:
        x = (a_ULS - Dimensions['Ltoe'] * 10 ** -3) / a_ULS * qmax_ULS
        M = x * Dimensions['Ltoe'] ** 2 * 10 ** -6 + (qmax_ULS - x) * Dimensions['Ltoe'] ** 2 * 10 ** -6 / 3
        print(M, 'toeM', a_ULS, qmax_ULS)
    d = Dimensions['D'] - Dimensions['footing_cover'] - 10
    p = 2.5 * M / d ** 2
    pmin = 0.2 * (Dimensions['D'] / d) ** 2 * (0.6 * math.sqrt(fc) / 500)
    p = max(p, pmin)

    results = {'M': 0, 'Mu_min': 0}
    Ast = [p * 1000 * d]
    while results['M'] * 0.65 < M or results['Mu_min'] > results['M']:
        results = Concrete.beam_moment(1000, Dimensions['D'], Dimensions['footing_cover'],
                                       [Dimensions['D'] - Dimensions['footing_cover']], Ast, M, 0, 0, [0, 0, 0], fc,
                                       [500], 'Rectangle')

        Ast[0] = Ast[0] + 10

    if crack == 'Moderate':
        Ast1 = 0.0035 * Dimensions['tw'] * 1000
    elif crack == 'Minor':
        Ast1 = 0.00175 * Dimensions['tw'] * 1000
    elif crack == 'Strong':
        Ast1 = 0.006 * Dimensions['tw'] * 1000
    elif crack == 'Unrestrained':
        Ast1 = 0.00175 * Dimensions['tw'] * 1000
    Ast[0] = max(0.75 * Ast1, Ast[0])
    results = [Ast[0], Ast1]
    return results


def masonry_properties(Masonry):
    if Masonry['Masonry_size'] == '10 series':
        Masonry['H'] = 190
        Masonry['W'] = 90
        Masonry['L'] = 390
    elif Masonry['Masonry_size'] == '15 series':
        Masonry['H'] = 190
        Masonry['W'] = 140
        Masonry['L'] = 390
    elif Masonry['Masonry_size'] == '20 series':
        Masonry['H'] = 190
        Masonry['W'] = 190
        Masonry['L'] = 390
    elif Masonry['Masonry_size'] == '25 series':
        Masonry['H'] = 190
        Masonry['W'] = 240
        Masonry['L'] = 390
    elif Masonry['Masonry_size'] == '30 series':
        Masonry['H'] = 190
        Masonry['W'] = 290
        Masonry['L'] = 390
    return Masonry


def masonry_wall(d, fsy, fuc, Masonry, Dimensions, Ka, surcharge, density_soil, values):
    Masonry = masonry_properties(Masonry)
    Kh = min(1.3 * (Masonry['H'] / 19 * Masonry['BT']) ** 0.29, 1.3)
    Km = 1.4  # for clay
    fm = Kh * Km * math.sqrt(fuc)
    PA1 = 0.5 * Ka * density_soil * (Dimensions['H'] + Dimensions['h']) ** 2 * 10 ** -6
    PA2 = Ka * surcharge * (Dimensions['H'] + Dimensions['h']) * 10 ** -3
    M = 1.5 * (PA1 * Dimensions['H'] / 3 * 10 ** -3) + PA2 * Dimensions['H'] / 2 * 10 ** -3 + values[
        'Additional_moment']
    print(M, 'M', PA1, PA2, fm, Kh, Km)
    Ast = 10
    b = 1000
    Md = 0
    Area = (Masonry['W'] - 36 * 2) ** 3 * (Masonry['L'] - 36 * 3) / 12 * 10 ** -12
    y = Masonry['W'] / 2 * 10 ** -3
    Mcv = 0 * Area / y * 10 ** 3
    while Md < M or Md < 1.2 * Mcv:
        Asd = min(0.29 * 1.3 * fm * b * d / fsy, Ast)
        Md = 0.75 * fsy * Asd * d * (1 - (0.6 * fsy * Asd) / (1.3 * fm * b * d)) * 10 ** -6
        if Asd < Ast:
            Ast = 'Increase Block size'
            break
        Ast = Ast + 10

    results = [Ast, Ast]
    return results


def soldier_layout():
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
    return layout


def Soldier(values):
    #Determine the effective pile width
    f = min(2.5, 0.08 * values['Friction_angle'])

    #Determine the active pressure on pile
    Pa = values['Ka'] * values['Density_soil'] * values['H'] ** 2 / 2 * values['Spacing'] * 1.25
    Z = 2 * values['cohesion'] / (
            values['Density_soil'] * math.sqrt(values['Ka']))
    if values['cohesion'] > 0:
        Pa = (values['Density_soil'] * values['H'] * values['Ka'] - 2 * values['cohesion'] * math.tan(
            (45 - values['Friction_angle'] / 2) / 180 * math.pi)) * (values['H'] - Z) / 2 * values['Spacing'] * 1.25
    Pw = values['Ka'] * values['surcharge'] * values['H'] * values['Spacing'] * 1.5
    if values['Water'] == False:
        values['Water_table'] = values['H']

    Pwater = 10 * (values['H'] - values['Water_table']) ** 2 / 2

    x = sympy.symbols('x')
    eq1 = sympy.Eq(x * 2 * values['cohesion'] * math.tan((45 + values['Friction_angle'] / 2) / 180 * math.pi) * values[
        'Dia'] * f * 10 ** -3 + x ** 2 * values['Kp'] * values['Density_soil'] * values[
                       'Dia'] * f * 10 ** -3 * 0.5 - x * 10 * (values['H'] - values['Water_table']),
                   Pa + Pw + Pwater)
    dn = sympy.solve(eq1)
    d = dn[1]
    print(dn)
    # d = math.sqrt((2*(Pa + Pw))/(values['Density_soil'] * values['Kp'] * values['Dia']*10**-3 * f))
    print(d)
    Mmax = abs(d * 2 * values['cohesion'] * math.tan((45 + values['Friction_angle'] / 2) / 180 * math.pi) * values[
        'Dia'] * f * 10 ** -3 * d / 2 + d * values['Kp'] * values['Density_soil'] * d / 2 * values[
                   'Dia'] * f * 10 ** -3 * d / 3 - Pa * ((values['H'] - Z) / 3 + d) - Pw * (
                       values['H'] / 2 + d) - Pwater * ((values['H'] - values['Water_table']) / 3 + d))
    # Mmax = (Pw*(0.5*values['H'] + 0.67*d) + Pa*(0.33*values['H'] + 0.67*d))

    D = math.sqrt(Mmax / (0.67 * 0.25 * (
            values['Density_soil'] * d * values['Kp'] + 2 *
            values['cohesion'] * math.tan((45 + values['Friction_angle'] / 2) / 180 * math.pi)) * values[
                              'Dia'] * 10 ** -3 * f))
    # D = math.sqrt((Mmax) / (values['Kp'] * values['Density_soil'] * values['Dia'] * 10 ** -3 * f * 0.25 * 0.67 * d))
    E = d + D
    print('Total Embedment depth: ', E, ' m', Pa, Pw, D, d)

    # Determine loads on sleepers
    P = (values['Density_soil'] * values['H'] * values['Ka'] - 2 * values['cohesion'] * math.tan(
        (45 - values['Friction_angle'] / 2) / 180 * math.pi)) * values['SleeperH'] * 10 ** -3
    M = P * values['Spacing'] ** 2 / 8
    V = P * values['Spacing'] / 2
    return {'Pa': Pa, 'Pw': Pw, 'd': d, 'D': D, 'E': E, 'Mmax': Mmax, 'f': f, 'M': M, 'V': V}
