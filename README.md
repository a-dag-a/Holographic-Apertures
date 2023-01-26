The idea here is that




## Why then, are some meta-atoms polarization sensitive?
If metal regions dumbly screen out the electric field like an opaque mask, then it seems that they have no sensitivity to the incident polarization.
- But real metamaterial atoms in the literature are VERY sensitive to polarization.
- So is there really something more to it than just the 'opaque screening' story?
- Here's the explanation: The geometry and symmetry of the atom are very important. The role of the metal is to screen out tangential electric fields.
	- In the interior of a metal domain, any polarization qualifies as 'tangential' and will be fully screened out/cancelled.
	- But at the boundaries of the metal geometry, we should resolve the incident E vector into components that are tangential and normal to the metal boundary (of course, all in the plane of the mask). Only the tangential field gets cancelled by the metal, leaving the 'normal' polarization field to propagate along freely.
	- Thus the EDGES of the unit cell produce a CORONA of locally-edge-normal polarizations.
	- This explains why a unit cell with broken circular symmetry (ie not a circle) is sensitive to the incident polarization.
	- So different polarizations strike the metal edges in different angles, making for different responses.

- The models that describe the far-field response of an atom based on e;ectrica; behabiour like inductance, capacitance, and the plasma frequency are all basically another way of analyzing the metamaterial-mask.

## Expect an interesting connection with Babinet's theorem

# TODO:
Verify the polarization sensitivity in COMSOL.
- Can use periodic ports to ease simulation time.
- Extract the phase slip in the far field.
- Compare this with the phase value at the ceneter of the Fourier Transform of the 2D mask unit cell.
