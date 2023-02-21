

    with doc.create(Section('Members subject to bending' + standard + 'Section 5', numbering=False)):
        doc.create(Subsection('Design for bending moment' + standard + 'Cl 5.1', numbering=False))
        doc.append('A member bent about the section major principal x-axis which is analysed by the elastic method (see\n'
                   'AS4100:2020 Clause 4.4) shall satisfy:\n\n')
        doc.append(NoEscape('$M_{x}^{*} \leq \phi M_{sx}$'))
        doc.append(',  and  ')
        doc.append(NoEscape('$M_{x}^{*} \leq \phi M_{bx}$'))
        doc.append('\n\nwhere\n\n\t')
        doc.append(NoEscape(
            r'$M_{x}^{*}$\hspace{11mm}=' + tab_width + 'design bending moment about the x-axis determined in accordance with Clause 4.4'))
        doc.append('\n')
        doc.append(NoEscape(r'$\phi$\hspace{14mm}=' +
                            tab_width +
                            'capacity factor (see Table 3.4)'))
        doc.append('\n')
        doc.append(NoEscape(r'$M_{sx}$' + tab_width + '=' +
                            tab_width +
                            r'nominal section moment capacity, as specified in Clause 5.2, for bending about the x-axis'))
        doc.append('\n')
        doc.append(NoEscape(r'$M_{bx}$' + tab_width + '=' +
                            tab_width +
                            r'nominal member moment capacity, as specified in Clause 5.3 or 5.6, for bending about the'))
        doc.append('\n')
        doc.append(NoEscape(r'\hspace*{28mm} x-axis'))

    with doc.create(Section('Section moment capacity for bending about a principal axis' + standard + 'Cl5.2',
                            numbering=False)):
        doc.append(Subsection('General' + standard + 'Cl 5.2.1', numbering=False))
        doc.append('The nominal section moment capacity (')
        doc.append(NoEscape('$M_{s}$'))
        doc.append(') shall be calculated as follows:\n\n')
        doc.append(NoEscape(r'$M_{s} = f_{y}Z_{e}$'))
        doc.append('\n\nwhere the effective section modulus (')
        doc.append(NoEscape('$Z_{e}$'))
        doc.append(') shall be as specified in Clauses 5.2.3, 5.2.4, or 5.2.5.')
        doc.append(Subsection('Section slenderness' + standard + 'Cl 5.2.2', numbering=False))
        doc.append('For a section with flat compression plate elements, the section slenderness (')
        doc.append(NoEscape(
            r'$\lambda_{e}$) shall be taken as the value of the plate element slenderness ($\lambda_{e}$) for the '))
        doc.append(NoEscape(r'element of the cross-section which has the greatest values of '
                            r'$\lambda_{e}/\lambda_{ey}$.'))
        doc.append('For a ' + SectionSize + ' the section is ' + compact + ' therefore, the effective section modulus ')
        doc.append(NoEscape(r'$Z_{e}$ is given by '))
        if compact == 'compact':
            doc.append('Clause 5.2.3.')
            doc.append(Subsection('Compact sections' + standard + 'Cl 5.2.3', numbering=False))
            doc.append(NoEscape(
                'For sections which satisfy $\lambda_{s} \leq \lambda_{sp}$, the effective section modulus ($Z_{e}$) shall be the lesser of $S$ or $1.5Z$, '))
            doc.append(NoEscape(
                'where $S$ and $Z$ are the plastic and elastic section moduli respectively, determined in accordance with Clause 5.2.6'))
            doc.append('\n\n')
            doc.append(NoEscape('$Z_{ex} = $'))
            doc.append(Zex)
            doc.append(NoEscape(' mm^{2}'))
        else:
            doc.append('To be added')

        doc.append(Subsection(NoEscape('Section moment capacity $\phi M_{sx}'), numbering=False))
        doc.append(NoEscape('$\phi M_{sx}  =  '))
        doc.append(str(round(PhiMsx, 2)) + ' KNm')
        doc.append(Subsection('Member capacity of segments without full lateral restraint' + standard + 'Cl 5.6',
                              numbering=False))
        doc.append(Subsection('Open Sections with equal flanges' + standard + 'Cl 5.6.1', numbering=False))
        doc.append('For open sections with equal flanges the following shall apply:\n')
        doc.append('(a) Segments of constant cross-section - The nominal member moment capacity (')
        doc.append(NoEscape('$M_{b}$) shall be calculated as follows:\n'))
        doc.append('\n')
        doc.append(NoEscape(r'$M_{b} = \alpha_{m}\alpha_{s}M_{s} \leq M_{s}'))
        doc.append('\n\nwhere\n\n\t')
        doc.append(NoEscape(
            r'$\alpha_{m}$\hspace{11mm}=' + tab_width + 'moment modifcation factor'))
        doc.append('\n')
        doc.append(NoEscape(r'$\alpha_{s}$\hspace{11mm}=' +
                            tab_width +
                            'slenderness reduction factor'))
        doc.append('\n')
        doc.append(NoEscape(r'$M_{s}$' + tab_width + '=' +
                            tab_width +
                            r'nominal section moment capacity determined in accordance with Clause 5.2 for the gross section'))

        doc.append(Subsection(NoEscape(r'Determination of $\alpha_{m}$  and  $\alpha_{s}$'), numbering=False))
        doc.append(NoEscape(r'$\alpha_{m} = $' + str(alpha_m) + '\n'))
        doc.append('\n')
        doc.append('\n')
        doc.append(NoEscape(
            r'$\alpha_{s} = 0.6\left[\sqrt{\left[\left(\frac{M_{sx}}{M_{oa}}\right)^{2}+3\right]}-\left(\frac{M_{sx}}{M_{oa}}\right)\right]$'))
        doc.append('\n')
        doc.append('\n')
        doc.append('\n')
        doc.append(NoEscape(
            r'$M_{oa} = \sqrt{\left[\left(\frac{\pi^{2} E I_{y}}{L_{e}^{2}}\right)\left[GJ + \left(\frac{\pi^{2} E I_{w}}{L_{e}^{2}}\right)\right]\right]}$'))
        doc.append('\n')
        doc.append('\n')
        doc.append('\n')
        doc.append(NoEscape(r'$M_{oa} = ' + str(round(Moa, 3))))
        doc.append('\n')
        doc.append('\n')
        doc.append(NoEscape(r'$\alpha_{s} = $' + str(round(alpha_s, 3))))
        doc.append(Subsection(NoEscape('Member moment capacity $\phi M_{bx}$'), numbering=False))
        doc.append(NoEscape(r'$M_{b} = \alpha_{m}\alpha_{s}M_{s} = $ ' + str(round(PhiMbx, 2)) + ' KNm'))

    with doc.create(Section('Shear capacity of webs' + standard + 'Cl 5.11', numbering=False)):
        doc.append(Subsection('Shear capacity' + standard + 'Cl 5.11.1', numbering=False))
        doc.append(NoEscape('A web subject to a design force ($V^{*}$) shall satisfy:\n'))
        doc.append('\n')
        doc.append(NoEscape('$V^{*} \leq \phi V_{v}'))
        doc.append('\n\nwhere\n\n\t')
        doc.append(NoEscape(
            r'$\phi$\hspace{11mm}=' + tab_width + 'capacity factor (see Table 3.4)'))
        doc.append('\n')
        doc.append(NoEscape(r'$V_{v}$\hspace{10mm}=' +
                            tab_width +
                            'nominal shear capacity of the web determined from either Clause 5.11.2 or Clause 5.11.3'))
        doc.append(
            '\n\n\nNote: The shear capacity of the section may be limited by the shear capacity of the flange-to-web connection which should be checked.')
        doc.append(
            Subsection('Approximately uniform shear stress distribution' + standard + 'Cl 5.11.2', numbering=False))
        doc.append(NoEscape(
            'The nominal shear capacity ($V_{v}$) of a web where the shear stress distribution is approximately uniform shall be taken as:'))
        doc.append('\n\n')
        doc.append(NoEscape('$V_{v} = V_{u}$'))
        doc.append('\n\n')
        doc.append(NoEscape(
            'Where $V_{u}$ is the nominal shear capacity of a web with a uniform shear stress distribution given as follows:'))
        doc.append('\n\n')
        doc.append(
            NoEscape('(a)\hspace{10mm}When the maximum web panel depth to thickness ratio $d_{p}/t_{w}$ satisfies:'))
        doc.append('\n\n')
        doc.append(NoEscape(r'$\frac{d_{p}}{t_{w}} \leq \frac{82}{\sqrt{\left(\frac{f_{y}}{250}\right)}}$'))
        doc.append('\n\nthe nominal shear capacity of the web (')
        doc.append(NoEscape('$V_{u}$) shall be taken as:'))
        doc.append('\n\n')
        doc.append(NoEscape('$V_{u} = V_{w}$'))
        doc.append('\n\nwhere the nominal shear yield capacity of the web (')
        doc.append(NoEscape('$V_{u}$) is specified in Clause 5.11.4.'))
        doc.append('\n\n')
        doc.append(
            NoEscape('(b)\hspace{10mm}When the maximum web panel depth to thickness ratio $d_{p}/t_{w}$ satisfies:'))
        doc.append('\n\n')
        doc.append(NoEscape(r'$\frac{d_{p}}{t_{w}} > \frac{82}{\sqrt{\left(\frac{f_{y}}{250}\right)}}$'))
        doc.append('\n\nthe nominal shear capacity of the web (')
        doc.append(NoEscape('$V_{u}$) shall be taken as:'))
        doc.append('\n\n')
        doc.append(NoEscape('$V_{u} = V_{b}$'))
        doc.append('\n\nwhere the nominal shear buckling capacity of the web (')
        doc.append(NoEscape('$V_{b}$) is specified in Clause 5.11.5.'))