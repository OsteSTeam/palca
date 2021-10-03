# PALCA - Asteroid Light Curve Tool
 PALCA (Potato Asteroid Light Curve Application) is an asteroid light curve tool that builds light curves using an OBJ model built on p5, a Processing implementation. Input a model, light and distance conditions, and get a visualisation together with both light curve end effective reflection surface.
 Created for NASA SpaceApps 2021 challenge by oste s team (Y. Vasylyshyn, E. Dudka, O. Lukina, A. Sportko, M. Tatarovskyi, G. Titov), from Kyiv Polytechnic Institute and Kyiv National University for the "When Light Curves Throw Us Curve Balls" challenge:
 https://2021.spaceappschallenge.org/challenges/statements/when-light-curves-throw-us-curve-balls/teams/oste-s-team/project
 
 The application is ready to be used for astronomical research - for evaluating light curves of objects. Also may find use in astronomical education.
 

Made with Pycharm using Numpy, P5 (Processing implementation for Python), and matplotlib

![alt text](https://github.com/[OsteSTeam]/[palca]/blob/[main]/photo_2021-10-03_20-49-28.jpg?raw=true)

# How to use the app

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

Wait for the program to render the object in a full rotation and show the graphs. Note that the stellar magnitude scale less values are brighter.

# Technical details


The asteroid is loaded from an OBJ file. Each face is loaded as an array of 3D vectors, each representing a vertex. The rotation matrix is applied to find coordinates after rotation. At first, faces are sorted from farthest to closest based on Z-coordinates of their centers. Then, normals are calculated and faces with normals pointing away from the camera are excluded from rendering. Vertexes are projected on the camera plane.

Using the normals calculated before, we can find the brightness values of faces. Faces are treated as ideal Lambertian diffuse surfaces that reflect light in all directions. The color means the percent of light a face reflects: black reflects none, white reflects all.

The total brightness of asteroid pixels is added up. Bluish background pixels are ignored. Divided by a scale factor, this number yields total effective surface (i.e. how large a perfectly reflective surface must be to reflect the same amount as the asteroid). 

For each frame, after calculating the total effective surface, the program calculates the stellar magnitude and puts these values in arrays. After a full rotation, these values are fed into matplotlib functions to build plots.


# Applications

The advantages of our solution are:
1) Efficiency in simulation of light and reflection.
2) Effective and straightforward graphic approach in calculating brightness.
3) Unsophisticated and open-source code, which makes it accessible and easily modifiable.
Those advantages allow us to determine the most appropriate applications and target audiences for this tool. At this stage, we estimate that this project (provided a user-friendly interface is developed) may find its use in the sphere of education. It allows students to study the relationship between the shape of an asteroid and its light curve hands on. Furthermore, we believe (and intend) that this application may be used as scientific tool.

# Perspectives
1) Using mtl files to model irregularities in surface reflection and texture
2) Better interface (including web app, currently in development)
3) Faster, more productive render engine
4) More shading models

# Disclaimer

This software is provided "AS IS" without any warranty inclusing accuracy, useability and stability. The authors are not responsible for any damage.
Quirks, crashes and some incorrectly ordered faces may happen when processing large (>400-500 faces) files.
Any commmits are welcome.

