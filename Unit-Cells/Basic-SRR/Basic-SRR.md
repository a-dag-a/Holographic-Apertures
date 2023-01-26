## Analytical Fourier Transform for SRR aperture
The basic Split-Ring-Resonator is the aperture function: $1-f(r,\theta)$, where 
$$ f(r, \theta) = \mbox{circ}\left(\frac{r}{R+t}\right) - \mbox{circ}\left(\frac{r}{R}\right)-\mbox{patch}_{(\beta,R,t)}\left(r, \theta \right)$$
where the last 'patch' function is simply a patch of sector angle $\beta$ from an annular ring of inner radius $R$ and thickness $t$. The patch is taken to be from the 'northern-most' part of the ring.

The FT of the patch can be found as follows: We put together several rotated copies of the patch function so as to obtain a complete ring. Of course, this is assuming that $\beta$ divides the full $360^o$ of the ring, so that $2\pi/\beta$ is rational (an assumption which we now make). This means that $$\Sigma_{m=0}^{N} \mbox{patch}_{(\beta,R,t)}\left(r, \theta - \frac{2\pi m}{\beta} \right) = \mbox{circ}\left(\frac{r}{R+t}\right) - \mbox{circ}\left(\frac{r}{R}\right)$$
Fourier transforming this gives: $$ \mbox{patch}_{(\beta,R,t)}\left(\rho, \phi \right). F(\beta) = \mbox{somb}(\rho (R+t)) - \mbox{somb}(\rho R)$$
// Get it? sombre-$\rho$ !?
- [ ] Find this factor $F(\beta)$. Hope $1/F(\beta)$ doesnt explode..

(The irrational case $2\pi/\beta \neq {Z}$ makes for a very interesting aside (that could be a deep hole!), so lets venture there some other day!)

## This treatment works well because of the binary nature of metallic masks
Dielectric masks require a little more thought, in terms of $E_{||}$ and $D_\perp$
## Connection to Holography
The meta-atom aperture is basically a transmission hologram of an object, which when illuminated by a plane polarized 'reference' wave, creates a holographic image of that object.