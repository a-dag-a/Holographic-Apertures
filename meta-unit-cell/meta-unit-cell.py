import meep as mp
import numpy as np
import matplotlib.pyplot as plt

def main(args):
    resolution = args.resolution
    no_sim = args.no_sim

    # GEOMETRY

    d_padding = 10
    d_pml = 2

    srr_sq_outer = 5
    srr_track = 1
    srr_sq_inner = srr_sq_outer-2*srr_track
    srr_gap = srr_track/2
    # resolution = 10

    cell_a = srr_sq_outer+srr_track

    cell = mp.Vector3(cell_a,cell_a,2*d_padding+2*d_pml)
    geometry = [
        mp.Block(size=mp.Vector3(srr_sq_outer,srr_sq_outer,0),center=mp.Vector3(0,0,0),material=mp.metal),
        mp.Block(size=mp.Vector3(srr_sq_inner,srr_sq_inner,0),center=mp.Vector3(0,0,0),material=mp.air),
        mp.Block(size=mp.Vector3(srr_gap,srr_track,0),center=mp.Vector3(0,-srr_sq_outer/2+srr_track/2,0),material=mp.air),
        mp.Block(size=mp.Vector3(srr_track,2*srr_gap,0),center=mp.Vector3(-srr_sq_outer/2+srr_track/2,0,0),material=mp.air)
    ]

    # SOURCES
    src_fcen = 3
    src_df = 1.5

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

    run_sim=True
    # run_sim=False

    if(not(no_sim)):
        sim.run(until=30)

        # sim.plot2D(fields=mp.Ez)
        # plt.show()

        # DUMP SIMULATION STATE AND DATA
        sim.dump(dirname='./sim_dump')
    else:
        sim.load(dirname='./sim_dump')
        

    # PLOTTING THE VECTOR FIELD
    f1 = plt.figure()
    vol_srr = mp.Volume(size=mp.Vector3(cell_a,cell_a,0),center=mp.Vector3(0,0,0))
    sim.plot2D(fields=mp.Ex, output_plane=vol_srr)
    # plt.show()


    # def showVectorField2D(volume,vector='E'):
    #     # returns a plot object
    #     plt.

    f2 = plt.figure()
    arrowX = sim.get_array(component=mp.Ex)[:,:,120]
    arrowY = sim.get_array(component=mp.Ey)[:,:,120]
    plt.quiver(arrowX,arrowY)
    plt.show()

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--resolution", type=int, default=10)
    parser.add_argument("--no-sim", type=int, default=0)

    args = parser.parse_args()
    main(args)


# The quiver plot is misaligned. These corrections need to be done
# Flip along Y axis
# Rotate by -90 about Z