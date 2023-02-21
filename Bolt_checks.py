#This module will perform checks on bolts
import math
#This function will calculate loads to each bolt given their position and overall loadings

def bolt_actions(Bolts):
    #calculate bolt area
    bolt_area = int(Bolts['Size'])**2 / 4 * math.pi
    #First calculate centroid of bolt group
    tally = 0
    x_total = 0
    for i in range(int(Bolts['rows'])):
        x_total += int(Bolts['x' + str(i+1)])*int(Bolts['row_'+str(i+1)+'_bolts'])
        tally += int(Bolts['row_'+str(i+1)+'_bolts'])
    x_centroid = x_total / tally
    print(x_centroid)
    y_total = 0
    for i in range(int(Bolts['rows'])):
        y_total += int(Bolts['y' + str(i+1)])*int(Bolts['row_'+str(i+1)+'_bolts'])
    y_centroid = y_total / tally
    print(y_centroid)
#Bolt pattern moments of inertia
    Icx = 0
    Icy = 0
    check_max_distance_x = 0
    check_max_distance_y = 0
    for i in range(int(Bolts['rows'])):
        Icy += (int(Bolts['x' + str(i+1)])-x_centroid)**2*bolt_area*int(Bolts['row_'+str(i+1)+'_bolts'])
        Icx += (int(Bolts['y' + str(i+1)])-y_centroid)**2*bolt_area*int(Bolts['row_'+str(i+1)+'_bolts'])
        check_max_distance_x = max(check_max_distance_x, abs(int(Bolts['x' + str(i+1)])) - x_centroid)
        check_max_distance_y = max(check_max_distance_y, abs(int(Bolts['y' + str(i + 1)])) - y_centroid)
    Icp = Icy + Icx
    Max_axial_force = round(int(Bolts['Axial'])/ tally - int(Bolts['Moment'])*(check_max_distance_y)/Icx*bolt_area*1000,2)
    #Determine shear force in bolts
    Max_shear_force = round(float(Bolts['Shear'])/tally)
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



