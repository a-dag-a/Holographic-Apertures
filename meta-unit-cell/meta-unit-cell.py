import meep as mp
import numpy as np
import matplotlib.pyplot as plt
from scipy.constants import c
import pdb

a = 1e-6
# Atom-specific paramaters
# |<------------ srr_sq_outer ------------->|
#  ___________________________________  ______
# |///////////////////////////////////|     |
# |///////////////////////////////////|     |
# |///////////////////////////////////|     |
# |///////// _______________ /////////|     |
# |<d_track>|               |/////////|     |
# |/////////|               |/////////|     |
# |/////////|               |/////////|   srr_sq_outer
# |/////////|               |/////////|     |
# |/////////|               |/////////|     |
# |/////////|               |/////////|     |
# |/////////|_____     _____|/////////|     |
# |///////////////|   |///////////////|     |
# |///////////////|   |///////////////|     |
# |///////////////|   |///////////////|     |
# |_______________|   |_______________|_____|____
#                 |<->|
#                 srr_gap

def main(args):
    # resolution = args.resolution
    no_sim = args.no_sim
    print(f'no_sim flag is {no_sim}')    
    

    # Parse the frequency range for the input pulse
    # a = 1e-6
    # realLife2mp_freq = lambda f: f/(c/a)
    # src_fcen = realLife2mp_freq(args.fcen)
    # src_df = realLife2mp_freq(args.df)

    # GEOMETRY
    # Main geometric parameters =======
    space_factor = 140/5 # multplicative factor for 5 um -> 140 um ring edge length
    d_padding = 10#*(140/5) # NOT SCALING
    d_pml = 2#*(140/5) # NOT SCALING

    srr_sq_outer = 5*space_factor
    srr_track = 1*space_factor
    srr_gap = 0*srr_track/2

    srr_sq_inner = srr_sq_outer-2*srr_track
    # resolution = 10/space_factor
    resolution = 0.5
    src_fcen = 3/space_factor
    src_df = 1.5/space_factor
    run_time = 30*space_factor

    # =================================
    cell_a = srr_sq_outer+srr_track
    cell = mp.Vector3(cell_a,cell_a,2*d_padding+2*d_pml)
    geometry = [
        mp.Block(size=mp.Vector3(srr_sq_outer,srr_sq_outer,0),center=mp.Vector3(0,0,0),material=mp.metal),
        mp.Block(size=mp.Vector3(srr_sq_inner,srr_sq_inner,0),center=mp.Vector3(0,0,0),material=mp.air),
        # mp.Block(size=mp.Vector3(srr_gap,srr_track,0),center=mp.Vector3(0,-srr_sq_outer/2+srr_track/2,0),material=mp.air),
        # mp.Block(size=mp.Vector3(srr_track,2*srr_gap,0),center=mp.Vector3(-srr_sq_outer/2+srr_track/2,0,0),material=mp.air)
    ]
    if(srr_gap!=0):
        geometry.append(mp.Block(size=mp.Vector3(srr_track,2*srr_gap,0),center=mp.Vector3(-srr_sq_outer/2+srr_track/2,0,0),material=mp.air))

    # SOURCES
    
    sources = [
        mp.Source(
            src=mp.GaussianSource(src_fcen,src_df),
            component=mp.Ex,
            center=mp.Vector3(0,0,-d_padding),
            size=mp.Vector3(cell_a,cell_a,0)
        )
    ]

    # NOTE: CURRENTLY THE PERIODIC BOUNDARY CONDITION IS NOT DONE RIGHT.
    pml_layers = [mp.PML(thickness=d_pml, direction=mp.Z)]
    sim = mp.Simulation(
        cell_size=cell,
        geometry=geometry,
        resolution=resolution,
        sources=sources,
        boundary_layers=pml_layers,
        k_point=mp.Vector3(0,0,0)
    )

    if(not(no_sim)):
        sim.run(until=run_time)

        # DUMP SIMULATION STATE AND DATA
        sim.dump(dirname='./sim_dump')
    else:
        # LOAD SIMULATION DATA
        sim.load(dirname='./sim_dump')
    
    print(f'resolution is {resolution}')
    # PLOTTING THE VECTOR FIELD
    f1 = plt.figure()
    plotZSlice(sim=sim,z=0)
    # vol_srr = mp.Volume(size=mp.Vector3(cell_a,cell_a,0),center=mp.Vector3(0,0,0))
    # sim.plot2D(fields=mp.Ex, output_plane=vol_srr)
    # plt.show()

    f2 = plt.figure()
    num_z = int(cell.z*resolution)
    print(f'num_z is {num_z}')
    temp = sim.get_array(component=mp.Ex)
    print(f'SHAPE OF EX IS {np.shape(temp)}')
    arrowX = sim.get_array(component=mp.Ex)[:,:,int(num_z/2)]
    arrowY = sim.get_array(component=mp.Ey)[:,:,int(num_z/2)]
    plt.quiver(arrowX,arrowY)

    plt.show()
    pdb.set_trace()  

def plotZSlice(sim, z=0):
    vol_srr = mp.Volume(size=mp.Vector3(sim.cell_size.x,sim.cell_size.y,0),center=mp.Vector3(0,0,z))
    sim.plot2D(fields=mp.Ex, output_plane=vol_srr)
    
if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--resolution", type=int, default=10)
    parser.add_argument("--no-sim", type=int, default=0)
    # parser.add_argument("--fcen", type=float, default=3*(c/a))
    # parser.add_argument("--df", type=float, default=1.5*(c/a))

    args = parser.parse_args()
    main(args)
    #TODO: main(args, srr_params), srr_params can be loaded from a config yaml
    #TODO: Sanity checks on arguments

# The quiver plot is misaligned. These corrections need to be done
# Flip along Y axis
# Rotate by -90 about Z