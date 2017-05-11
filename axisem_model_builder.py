import numpy as np
import matplotlib.pyplot as plt

## Script to Perturb PREM velocity struture with both horizontal
##and vertical P and S Waves##

#Create arrays for velocity perturbation (percent)
#Create array for distance of pertrubation (measured above CMB)

#factors = velocity perturbation in percent
#depth = distance of perturbation above CMB

factors = np.array([0.0, 0.01, 0.02])
depth = np.arange(100000, 300000, 200000)

depth_boundary =3480000+depth


#Read in PREM (external_model2.bm) axisem model and perturb
for j in depth_boundary:


    for i in range(len(factors)):

        with open('external_model2.bm') as f:
            lines = (line for line in f if not line.startswith('#'))
            data = np.loadtxt(lines)



        radius = data[:, 0]
        rho = data[:, 1]
        Vpv = data[:, 2]
        Vsv = data[:, 3]
        Qkappa = data[:, 4]
        Qmu = data[:, 5]
        Vph = data[:, 6]
        Vsh = data[:, 7]
        eta = data[:, 8]

#Find boundaries

        boundary1_idx = np.array(np.where(radius == 3480000.)).flatten()
        boundary2_idx = np.array(np.where(radius == j)).flatten()

        boundary2 = boundary1_idx[0]
        boundary1 = boundary2_idx[0]

        percent = factors[i]

#Perturb velocity sturcture gradient

        vsv_top = Vsv[boundary1]
        vsv_bottom = Vsv[boundary2]+Vsv[boundary2]*factors[i]
        vsh_top = Vsh[boundary1]
        vsh_bottom = Vsh[boundary2]+Vsh[boundary2]*factors[i]

        vpv_top = Vpv[boundary1]
        vpv_bottom = Vpv[boundary2]+Vpv[boundary2]*factors[i]
        vph_top = Vph[boundary1]
        vph_bottom = Vph[boundary2]+Vph[boundary2]*factors[i]





        gradient_vsv = (vsv_bottom-vsv_top)/(radius[boundary2]-radius[boundary1])
        gradient_vsh = (vsh_bottom-vsh_top)/(radius[boundary2]-radius[boundary1])
        Vsv[boundary1:boundary2] = gradient_vsv*(radius[boundary1:boundary2]-radius[boundary1])+vsv_top
        Vsh[boundary1:boundary2] = gradient_vsh*(radius[boundary1:boundary2]-radius[boundary1])+vsh_top

        gradient_vpv = (vpv_bottom-vpv_top)/(radius[boundary2]-radius[boundary1])
        gradient_vph = (vph_bottom-vph_top)/(radius[boundary2]-radius[boundary1])
        Vpv[boundary1:boundary2] = gradient_vpv*(radius[boundary1:boundary2]-radius[boundary1])+vpv_top
        Vph[boundary1:boundary2] = gradient_vph*(radius[boundary1:boundary2]-radius[boundary1])+vph_top

#Export as .bm file to be read into axisem
        header0 = 'NAME test8'
        header1 = 'ANELASTIC T'
        header2 = 'ANISOTROPIC T'
        header3 = 'UNITS m'
        header4 = 'COLUMNS radius rho vpv vsv qka qmu vph vsh eta'
        header = header0 + '\n' + header1 + '\n' + header2 + '\n' + header3 + '\n' + header4

        if factors[i]<0:



            name = 'Gradient_negative{}_Depth{}' .format( str(factors[i])[3:], str(j/1000)[0:3])

        else:


            name = 'Gradient{}_Depth{}' .format( str(factors[i])[2:], str(j/1000)[0:3])



#Flip data so that it is based on depth not radius

        radius = radius
        rho = np.flipud(rho)
        Vpv = np.flipud(Vpv)
        Vsv = np.flipud(Vsv)
        Qkappa =np.flipud(Qkappa)
        Qmu = np.flipud(Qmu)
        Vph = np.flipud(Vph)
        Vsh = np.flipud(Vsh)
        eta = np.flipud(eta)


        with open('Flipped_{}.bm' .format(name), 'w') as f:

            f.write(header)
            f.write('\n')

            for i in range(len(data)):

                rad = str(radius[i])
                r = str(rho[i])
                Vp = str(Vpv[i])
                Vs = str(Vsv[i])
                Qk = str(Qkappa[i])
                Qm = str(Qmu[i])
                VpH = str(Vpv[i])
                VsH = str(Vsv[i])
                ETA = str(eta[i])

                f.write('{} {} {} {} {} {} {} {} {}' .format(rad, r, Vp, Vs, Qk, Qm, VpH, VsH, ETA + '\n'))
