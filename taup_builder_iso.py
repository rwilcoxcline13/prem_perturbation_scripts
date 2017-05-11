import numpy as np
import matplotlib.pyplot as plt

#Create arrays for velocity perturbation (percent)
#Create array for distance of pertrubation (measured above CMB)
factors = [0]
depth = np.array([0])

depth_boundary =3480000+depth


#Read in PREM axisem model and perturb
for j in depth_boundary:


    for i in range(len(factors)):

        with open('prem.bm') as f:
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


        if factors[i]<0:



            name = 'gradient_negative{}_depth{}' .format( str(factors[i])[3:], str(j/1000)[0:3])

        else:


            name = 'gradient{}_depth{}' .format( str(factors[i])[2:], str(j/1000)[0:3])

        name = 'PREM_032517'

        print(name)

        radius = np.abs(radius -6371000)
        rho = rho
        Vpv = Vpv
        Vsv = Vsv
        Qkappa = Qkappa
        Qmu = Qmu



#Write as .tvel to be read into TauP
        with open('{}.tvel' .format(name), 'w') as f:

            f.write('\n')
            f.write('\n')

            for i in range(len(data)):

                rad = str(radius[i]/1000)
                density = str(rho[i]/1000)
                Vp = str(Vpv[i]/1000)
                Vs = str(Vsv[i]/1000)


                f.write('{} {} {} {}' .format(rad, Vp, Vs, density + '\n'))
