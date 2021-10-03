# palca
 PALCA (Potato Asteroid Light Curve Application) is an asteroid light curve tool that builds light curves using an OBJ model built on p5, a Processing implementation. Input a model, light and distance conditions, and get a visualisation together with both light curve end effective reflection surface.
 Created for NASA SpaceApps 2021 challenge by oste s team (U. Vasylyshin, E. Dudka, O. Lukina, A. Sportko, M. Tatarovsky, G. Titov)

Made with Pycharm using Numpy, P5, and matplotlib

How to use the app:
Save an OBJ model, to get correct magnitude values the model coordinates must be in kilometers. To prevent lagging, make sure the model has less than 400 faces. To be rendered correctly, all faces must be triangulated.

For reference, in app window the Z axis faces towards the observer, X faces right and Y faces down.

Launch the program.

Choose whether you would like to use default settings or define your own:

1) Asteroid albedo (from 0 to 1), default 0.04
2) Distance between the light source and the asteroid (in AU), default 5.2 (at Jupiter orbit)
3) Distance between the asteroid and the observer (in AU), default 5.2
4) Solar luminosity (in solar luminosity units), default 1 Lsun
5) Light direction as a vector, default [0,0,1]
6) Path to .obj file

Wait for the program to render the object in a full rotation.

