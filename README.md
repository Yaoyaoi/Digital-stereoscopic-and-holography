# 3D display technology
## Project1
1. A user interface to load image files, and display results. 
2. Integrating multiple image views into an integrated image according to the sub-pixel mapping of an autostereoscopic 3D monitor (N to 1). 
3. (Not done) Reconstruct the multiple view images from the integrated image (1 to
N). 
4. Wobble the images reconstructed in ‘C’ to simulate the 3D effect. 
5. The integrated image, reconstructed images, and the wobble image
should be shown in the user interface developed in ‘A’.
## Project2 (all done)
1. Familiarize with the given source code to understand the hologram generation and 
reconstruction process. This is beneficial to your development even if you are not using the 
template in your work. In the basic outcome, the image is a planar image that is parallel to 
the hologram. In another words, all the image pixels have identical distance to the hologram.
2. Extract the phase component of the hologram to obtain a phase-only hologram, and use it to 
reconstruct the image. Evaluate the quality of the reconstructed image.
3. Generate a phase-only hologram with the noise addition method. Reconstruct the image from 
the phase-only hologram and evaluate its quality.
4. Generate a phase-only hologram with the grid-cross down-sampling method. Reconstruct the 
image from the phase-only hologram and evaluate its quality.
5. In steps ‘A’ to ‘D’, the image is a planar and parallel the hologram. In this first advance 
outcome, partition the image uniformly into an upper and a lower sections. Each section is 
located at a different distance from the hologram (e.g. 0.16m and 0.18m for the upper and 
lower sections, respectively). Generate the phase-only holograms for this double-depth image 
with the noise addition, and the down-sampling methods. From the phase-only hologram you 
generated, reconstruct the images at the 2 depth planes, and evaluate their qualities.
6. The second advanced outcome is to generate a phase-only hologram of the double-depth 
image with the one-step-phase-retrieval (OSPR) method. In this method multiple subholograms are generated, and their reconstructed images are averaged out to reduce the noise. 
Evaluate the q