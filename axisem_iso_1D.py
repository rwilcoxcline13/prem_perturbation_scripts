import numpy as np

#Create arrays for velocity perturbation (percent)
#Create array for distance of pertrubation (measured above CMB)
factors = np.array([0.02])
depth = np.arange(100000, 800000, 50000)

depth_boundary =3480000+depth


#Read in PREM axisem model and perturb
for j in depth_boundary:


    for i in range(len(factors)):

        with open('PREM_real.bm') as f:
            lines = (line for line in f if not line.startswith('#'))
            data = np.loadtxt(lines)



        radius = data[:, 0]
        rho = data[:, 1]
        Vpv = data[:, 2]
        Vsv = data[:, 3]
        Qkappa = data[:, 4]
        Qmu = data[:, 5]


        boundary1_idx = np.array(np.where(radius == 3480000.)).flatten()
        boundary2_idx = np.array(np.where(radius == j)).flatten()

        boundary2 = boundary1_idx[0]
        boundary1 = boundary2_idx[0]

        percent = factors[i]

        vsv_top = Vsv[boundary1]
        vsv_bottom = Vsv[boundary2]+Vsv[boundary2]*factors[i]


        vpv_top = Vpv[boundary1]
        vpv_bottom = Vpv[boundary2]+Vpv[boundary2]*factors[i]






        gradient_vsv = (vsv_bottom-vsv_top)/(radius[boundary2]-radius[boundary1])
        Vsv[boundary1:boundary2] = gradient_vsv*(radius[boundary1:boundary2]-radius[boundary1])+vsv_top

        gradient_vpv = (vpv_bottom-vpv_top)/(radius[boundary2]-radius[boundary1])
        Vpv[boundary1:boundary2] = gradient_vpv*(radius[boundary1:boundary2]-radius[boundary1])+vpv_top

#Export as .bm file to be read into axisem
        header0 = 'NAME test8'
        header1 = 'ANELASTIC T'
        header2 = 'ANISOTROPIC F'
        header3 = 'UNITS m'
        header4 = 'COLUMNS radius rho vpv vsv qka qmu'
        header = header0 + '\n' + header1 + '\n' + header2 + '\n' + header3 + '\n' + header4

        if factors[i]<0:



            name = 'Gradient_negative{}_Depth{}' .format( str(factors[i])[3:], str(j/1000)[0:3])

        else:


            name = 'Gradient{}_Depth{}' .format( str(factors[i])[2:], str(j/1000)[0:3])



        radius = radius
        rho = rho
        Vpv = Vpv
        Vsv = Vsv
        Qkappa =Qkappa
        Qmu = Qmu


        print(name)


        with open('{}.bm' .format(name), 'w') as f:

            f.write(header)
            f.write('\n')

            for i in range(len(data)):

                rad = str(radius[i])
                r = str(rho[i])
                Vp = str(Vpv[i])
                Vs = str(Vsv[i])
                Qk = str(Qkappa[i])
                Qm = str(Qmu[i])

                f.write('{} {} {} {} {} {}' .format(rad, r, Vp, Vs, Qk, Qm + '\n'))
