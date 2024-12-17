import sympy
import math

#This function calculate the unfactored moment capacity of a rectangular concrete section.
def moment(fc, b, d, Ast, fy):
    alpha_2 = max(0.67, 0.85 - 0.0015*fc)
    gamma = max(0.67, 0.97 - 0.0025*fc)
    dn = 0.85*max(d)
    Cc = alpha_2*fc*b*gamma*dn
    steel_strains = [0 for i in Ast]
    force_equilibrium = Cc - sum([Ast[i]*steel_strains[i]*200*10**3 for i in range(len(Ast))])
    while round(force_equilibrium) != 0:
        for i in range(len(Ast)):
            steel_strains[i] = min(max(-fy/(200*10**3),(dn - d[i])*0.003/(dn)),fy/(200*10**3))
        if force_equilibrium > 0:
            #increase dn
            dn *=0.99
        else:
            #decrease dn
            dn *=1.01
        Cc = alpha_2*fc*b*gamma*dn
        force_equilibrium = Cc + sum([Ast[i]*steel_strains[i]*200*10**3 for i in range(len(Ast))])

    if (dn - max(d))*0.003/dn > -fy/(200*10**3):
        print("steel not yielding")
    print(dn,"mm")
    Mu = Cc *(dn - 0.5*gamma*dn)*10**-6 + sum([abs(Ast[i]*steel_strains[i]*200*10**-3*(d[i] - dn)) for i in range(len(Ast))])
    return Mu 

def shear(fc,bv,d, D,Ast,Ec,M,V,N):
    dv = max(0.9*d, 0.72*D)
    dg = 20
    kdg = (32/(16+dg))
    ex = min((abs(M/dv)*10**6 + abs(V)*10**3 + 0.5*N*10**3)/(2*200*10**9*Ast*10**-6),3*10**-3)
    kv = (0.4/(1 + 1500*ex))*(1300/(1000 + kdg*dv))
    Vuc = kv * math.sqrt(fc) * bv * dv
    return Vuc*10**-3


fc = 32
b = 300
cover = 50
d = [45, 300-65]
Ast = [339, 339]
fy = 500
Ec = 30*10**9
print(moment(fc,b,d,Ast,fy))
print(shear(fc,b,d[1],d[1]+cover+6,Ast[0],Ec,18,36,0))