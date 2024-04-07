#This module will perform checks on bolts
import math
import PySimpleGUI as Sg
#This function will calculate loads to each bolt given their position and overall loadings

def development_layout():
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
    return layout2


def bolt_actions(Bolts):
    #calculate bolt area
    bolt_area = int(Bolts['bolt_size'])**2 / 4 * math.pi
    #First calculate centroid of bolt group
    num_bolts = 0
    x_total = 0
    for i in range(int(Bolts['#rows'])):
        x_total += int(Bolts['x' + str(i+1)])*int(Bolts['row_'+str(i+1)+'_bolts'])
        num_bolts += int(Bolts['row_'+str(i+1)+'_bolts'])
    x_centroid = x_total / num_bolts
    print(x_centroid)
    y_total = 0
    for i in range(int(Bolts['#rows'])):
        y_total += int(Bolts['y' + str(i+1)])*int(Bolts['row_'+str(i+1)+'_bolts'])
    y_centroid = y_total / num_bolts
    print(y_centroid)
#Bolt pattern moments of inertia
    Icx = 0
    Icy = 0
    check_max_distance_x = 0
    check_max_distance_y = 0
    max_distance = 0
    for i in range(int(Bolts['#rows'])):
        Icy += (int(Bolts['x' + str(i+1)])-x_centroid)**2*bolt_area*int(Bolts['row_'+str(i+1)+'_bolts'])
        Icx += (int(Bolts['y' + str(i+1)])-y_centroid)**2*bolt_area*int(Bolts['row_'+str(i+1)+'_bolts'])
        check_max_distance_x = max(check_max_distance_x, abs(int(Bolts['x' + str(i+1)])) - x_centroid)
        check_max_distance_y = max(check_max_distance_y, abs(int(Bolts['y' + str(i + 1)])) - y_centroid)
        polar_distance = math.sqrt((abs(int(Bolts['x' + str(i+1)])) - x_centroid)**2 + (abs(int(Bolts['y' + str(i + 1)])) - y_centroid)**2)
        if polar_distance > max_distance:
            max_distance = polar_distance
            theta = math.atan((abs(int(Bolts['y' + str(i + 1)])) - y_centroid)/(abs(int(Bolts['x' + str(i+1)])) - x_centroid))


    #Calculate rxy to each bolt group



    Icp = Icy + Icx
    Pmxy = Bolts['Mz'] * max_distance / Icp * bolt_area
    Pmx = Pmxy * math.sin(theta)
    Pmy = Pmxy * math.cos(theta)

    Max_axial_force = round(int(Bolts['Axial'])/ num_bolts - int(Bolts['Mx'])*(check_max_distance_y)/Icx*bolt_area*1000,2)
    #Determine shear force in bolts
    Max_shear_force = round(math.sqrt((Bolts['Vx']/num_bolts + Pmx)**2 + (Bolts['Vy']/num_bolts + Pmy)**2),2)
    #Max_shear_force = round(float(Bolts['Shear'])/num_bolts)




    #determine bolt tensile capacity
    if Bolts['grade'] == '4.6/S':
        Ntf = round(bolt_area*400/1000*0.8)
    #determine shear capacity
        Vf = round(0.62*400*bolt_area*0.8/1000)
    return(Max_axial_force, Max_shear_force, Ntf,Vf)


#check adequacy of bolts being used
def Development_length(data):
    k2 = (132 - int(data['db']))/100
    k3 = min(max(1-0.15*(int(data['cd'])-int(data['db']))/int(data['db']),0.7),1)
    Lsy_tb = round(max((0.5*float(data['k1'])*k3*int(data['fsy'])*int(data['db']))/(k2*math.sqrt(int(data['fc']))),0.058*int(data['fsy'])*float(data['k1'])*int(data['db'])))
    return(Lsy_tb)

