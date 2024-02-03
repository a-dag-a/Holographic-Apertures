## Update (3 Feb 2024)
Finally have a good way of thinking about the frequency selectivity problem (why is the ckt model frequency selective while the gemepetric aperture-FFT picture not frequency slecetive).
It is not correct to think that there is no 'resonance' behaviour (ie sudden opacity at some frequency) in the gemeotric aperture-FFT picture. Imagine sweeping the wavelength from 0 to a large value. Initially the far field FT will look like a 'clean' image of the aperture (it's FT imaged at small wavelength). As wavelength approaches some critical dimension of the aperture (eg wavelength = diameter of circular aperture) there will be complete opacity. This goes away at longer wvelengths.
	To complete the argument, consider the real life behaviour of a microwave door screen. The holes are apertures that allow BOTH optical (utlra small wavelength) and low freq RF (very long wavelength) to pass through. But it is OPAQUE at a particular frequency of 2.4GHz! There you go. 



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
