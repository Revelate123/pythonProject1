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

# Edge pads
M_sls = [88, 49]  # in KNm
N_sls = [35, 29]  # in KN
V_sls = [21.5, 7]  # in KN
M_uls = [125, 18.5, 76]  # in KNm
N_uls = [30, -5, 32]  # in KN
V_uls = [28, 2, 12]  # in KN

SLS = {'M': M_sls, 'N': N_sls, 'V': V_sls}

ULS = {'M': M_uls, 'N': N_uls, 'V': V_uls}
Dimensions = {'D': 0.6, 'W': 1}  # in metres
allowable_end_pressure = 150  # in KPa
density_concrete = 25  # in KN/m3
overburden = 0.2 * 18  # KPa from soil above (depth x unit weight)
Friction_angle = 24  # in degrees
cohesion = 5  # in KPa


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
    print(Moment, 'Moment_U')

    print(qmax, 'qmax', a, N)

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
               'N_centroid': centroid_N, 'a': a, 'qmax': qmax}
    return results


def overturning(Dimensions, allowable_end_pressure, density_concrete, density_soil, surcharge, Additional_moment, Ka,
                values, Top_restraint, Restraint_height):
    PA1 = 0.5 * Ka * density_soil * (Dimensions['H'] + Dimensions['D'] + Dimensions['h']) ** 2 * 10 ** -6
    PA2 = Ka * surcharge * (Dimensions['H'] + Dimensions['D'] + Dimensions['h']) * 10 ** -3

    if Top_restraint == True:
        M_unrestrained = PA1 * (Dimensions['H'] + Dimensions['D'] + Dimensions['h']) / 3 * 10 ** -3 + PA2 * (
                Dimensions['H'] + Dimensions['D'] + Dimensions['h']) / 2 * 10 ** -3 + Additional_moment
        x1 = (Dimensions['H'] * 10 ** -3) / (2 ** 0.25)
        thetaB = (Restraint_height / Dimensions['H']) * (Dimensions['H'] * 10 ** -3 - x1) * (
                1.25 * Ka * density_soil * Dimensions['H'] * 10 ** -3) * (Dimensions['H'] * 10 ** -3) ** 3 / 24
        thetaA = (Restraint_height * 10 ** -3) ** 3 / 3
        thetaB2 = 1.5 * Ka * surcharge * (Dimensions['H'] * 10 ** -3) ** 4 / 8 * Restraint_height / (Dimensions['H'])
        M_restrained = (1.25 * Ka * density_soil * Dimensions['H'] * 10 ** -3) * (Dimensions[
                                                                                      'H'] * 10 ** -3) ** 2 / 6 - thetaB / thetaA * Restraint_height * 10 ** -3 + 1.5 * Ka * surcharge * (
                               Dimensions[
                                   'H'] * 10 ** -3) ** 2 / 2 - thetaB2 / thetaA * Restraint_height * 10 ** -3 + Additional_moment

        Moment = M_restrained
        print(M_restrained, 'Moment_R', thetaB, thetaA, x1, thetaB2)
    else:
        Moment = 1.25 * PA1 * (Dimensions['H'] + Dimensions['D'] + Dimensions['h']) / 3 * 10 ** -3 + 1.5 * PA2 * (
                Dimensions['H'] + Dimensions['D'] + Dimensions['h']) / 2 * 10 ** -3 + Additional_moment
        print(Moment, 'Moment_U')

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
    # - PA1 * (Dimensions['H'] + Dimensions['D'] + Dimensions['h']) / 3 * 10 ** -3 * 1.25\
    # - PA2 * (Dimensions['H'] + Dimensions['D'] + Dimensions['h']) / 2 * 10 ** -3 * 1.5\
    # - Additional_moment
    print(M, 'M', PA1, PA2, Dimensions['h'])
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

    results = {'Mn': 0, 'Mu_min': 0}
    Ast = [p * 1000 * d]
    while results['Mn'] * 0.65 < M or results['Mu_min'] > results['Mn']:
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

    results = {'Mn': 0, 'Mu_min': 0}
    Ast = [p * 1000 * d]
    while results['Mn'] * 0.65 < M or results['Mu_min'] > results['Mn']:
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
    # d = Masonry['W']/2

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


x = 450
values = {'Friction_angle': 26, 'Density_soil': 20, 'H': 1.5, 'surcharge': 5, 'Dia': x, 'Ka': 0.4, 'Kp': 2.9,
          'Spacing': 5 * x / 1000, 'cohesion': 0, 'bf': 150, 'fc': 20, 'SleeperH': 0.4, 'Water': True, 'Water_table': 0}
# Soldier(values)
