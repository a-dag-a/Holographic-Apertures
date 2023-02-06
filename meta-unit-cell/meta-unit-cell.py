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
    normalizationRun = args.normalizationRun
    print(f'no_sim flag is {no_sim}')    
    sim_dump_dir = 'sim_dump' if normalizationRun else 'sim_norm_dump'

    # Parse the frequency range for the input pulse
    # a = 1e-6
    # realLife2mp_freq = lambda f: f/(c/a)
    # src_fcen = realLife2mp_freq(args.fcen)
    # src_df = realLife2mp_freq(args.df)

    # GEOMETRY
    # Main geometric parameters =======
    space_factor = 140/5 # multplicative factor for 5 um -> 140 um ring edge length
    d_padding = 25#*(140/5) # NOT SCALING
    d_pml = 2#*(140/5) # NOT SCALING

    srr_sq_outer = 5*space_factor
    srr_track = 1*space_factor
    srr_gap = (srr_track/4)#*0
    srr_metalThickness = 0
    srr_sq_inner = srr_sq_outer-2*srr_track
    
    # resolution = 10/space_factor
    # resolution = 0.5
    resolution = 1

    # src_fcen = 3/space_factor
    # src_df = 1.5/space_factor
    # run_time = 30*space_factor

    src_fcen = 0.001#0.005#0.05 #0.5#0.001
    src_df = src_fcen/2 #0.07#0.0005
    run_time=30
    monitor_z = 0.5*d_padding
    # =================================
    cell_a = srr_sq_outer+srr_track
    cell = mp.Vector3(cell_a,cell_a,2*d_padding+2*d_pml)
    geometry = []
    if(not(normalizationRun)):
        geometry = [
            mp.Block(size=mp.Vector3(srr_sq_outer,srr_sq_outer,0),center=mp.Vector3(0,0,0),material=mp.metal),
            mp.Block(size=mp.Vector3(srr_sq_inner,srr_sq_inner,0),center=mp.Vector3(0,0,0),material=mp.air),
            mp.Block(size=mp.Vector3(srr_gap,srr_track,0),center=mp.Vector3(0,-srr_sq_outer/2+srr_track/2,0),material=mp.air)
        ]
    # if(srr_gap!=0):
    
    # SOURCES =================================================================
    
    sources = [
        mp.Source(
            src=mp.ContinuousSource(frequency=src_fcen,fwidth=src_df),
            component=mp.Ex,
            center=mp.Vector3(0,0,-d_padding),
            size=mp.Vector3(cell_a,cell_a,0)
        )
    ]
    
    #FIXME: GAUSSIAN SOURCE YIELDS AN ALMOST EMTPY SOLUTION
    # sources = [
    #     mp.Source(
    #         src=mp.GaussianSource(src_fcen,src_df),
    #         component=mp.Ex,
    #         center=mp.Vector3(0,0,-d_padding),
    #         size=mp.Vector3(cell_a,cell_a,0)
    #     )
    # ]

    pml_layers = [mp.PML(thickness=d_pml, direction=mp.Z)]
    
    fr_tran = mp.FluxRegion(size=mp.Vector3(cell_a,cell_a,0), center=mp.Vector3(0,0,monitor_z), direction=mp.Z)
    fr_refl = mp.FluxRegion(size=mp.Vector3(cell_a,cell_a,0), center=mp.Vector3(0,0,-monitor_z), direction=mp.Z)
    
    sim = mp.Simulation(
        cell_size=cell,
        geometry=geometry,
        resolution=resolution,
        sources=sources,
        boundary_layers=pml_layers,
        k_point=mp.Vector3(0,0,0),
        # symmetries = [mp.Mirror(mp.X)] # Symmetry doesnt work out, for some reason..
        # eps_averaging=False
    )

    if(not(no_sim)):
        sim.run(until=run_time)

        # DUMP SIMULATION STATE AND DATA
        sim.dump(dirname=sim_dump_dir)
    else:
        # LOAD SIMULATION DATA
        sim.load(dirname=sim_dump_dir)
    
    print(f'resolution is {resolution}')
    # PLOTTING THE VECTOR FIELD
    f1 = plt.figure()
    plotXSlice(sim=sim,x=0)
    f2=plt.figure()
    plotYSlice(sim=sim,y=0)
    f3=plt.figure()
    plotZSlice(sim=sim,z=0)
    # vol_srr = mp.Volume(size=mp.Vector3(cell_a,cell_a,0),center=mp.Vector3(0,0,0))
    # sim.plot2D(fields=mp.Ex, output_plane=vol_srr)
    # plt.show()

    # f4 = plt.figure()
    # num_z = int(cell.z*resolution)
    # print(f'num_z is {num_z}')
    # temp = sim.get_array(component=mp.Ex)
    # print(f'SHAPE OF EX IS {np.shape(temp)}')
    # arrowX = sim.get_array(component=mp.Ex)[:,:,int(num_z/2)]
    # arrowY = sim.get_array(component=mp.Ey)[:,:,int(num_z/2)]
    # plt.quiver(arrowX,arrowY)

    # plt.show()

    nfreq = 101
    flux_tran = sim.add_flux(src_fcen, src_df, nfreq, fr_tran)
    flux_refl = sim.add_flux(src_fcen, src_df, nfreq, fr_refl)
    # pdb.set_trace()

    data_tran = mp.get_fluxes(flux_tran)
    f5 = plt.figure()
    plt.plot(flux_tran.freq, data_tran)
    plt.show()

    return sim, flux_tran, flux_refl

def plotXSlice(sim, x=0, component=mp.Ex):
    vol = mp.Volume(size=mp.Vector3(0,sim.cell_size.y,sim.cell_size.z),center=mp.Vector3(x,0,0))
    sim.plot2D(fields=mp.Ex, output_plane=vol)
    plt.title(f'X Slice at x = {x}')

def plotYSlice(sim, y=0, component=mp.Ex):
    vol = mp.Volume(size=mp.Vector3(sim.cell_size.x,0,sim.cell_size.z),center=mp.Vector3(0,y,0))
    sim.plot2D(fields=mp.Ex, output_plane=vol)
    plt.title(f'Y Slice at y = {y}')

def plotZSlice(sim, z=0, component=mp.Ex):
    vol = mp.Volume(size=mp.Vector3(sim.cell_size.x,sim.cell_size.y,0),center=mp.Vector3(0,0,z))
    sim.plot2D(fields=mp.Ex, output_plane=vol)
    plt.title(f'Z Slice at z = {z}')

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--resolution", type=int, default=10)
    parser.add_argument("--no-sim", type=int, default=0)
    parser.add_argument("--normalizationRun", type=int, default=0)
    # parser.add_argument("--fcen", type=float, default=3*(c/a))
    # parser.add_argument("--df", type=float, default=1.5*(c/a))

    args = parser.parse_args()
    sim, flux_tran, flux_refl = main(args)
    #TODO: main(args, srr_params), srr_params can be loaded from a config yaml
    #TODO: Sanity checks on arguments

# The quiver plot is misaligned. These corrections need to be done
# Flip along Y axis
# Rotate by -90 about Z