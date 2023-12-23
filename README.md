# Voronoi

Simple Python computational geometry code for computing 
voronoi diagrams, and its dual graph, the Delauney triangulation.

## Description

**Voronoi diagrams** are a type of tesselation pattern that emerges when every point in a plane is 
segmented into n cells through the computation of euclidean distances for a given set of n points.

For example, if n = 6, then the euclidean distance between every point in the plane and each n-th given
point will be calculated. Each point will be colour-assigned to whichever n-th point it is closest to, 
creating colour-separated sites. 

The pattern of voronoi diagrams may look familiar, that's because it shows up quite often: from cells 
to giraffe coat patterns. You can read more about it here, from this article which inspired me to 
create this repository. [the-fascinating-world-of-voronoi-diagrams](https://towardsdatascience.com/the-fascinating-world-of-voronoi-diagrams-da8fc700fa1b#:~:text=Voronoi%20patterns%20in%20nature&text=From%20microscopic%20cells%20in%20onion,that%20they%20form%20efficient%20shapes.)

**Delauney triangulations** are known as the dual graph of the Voronoi diagrams. The Delauney is an efficient
triangulation in which for a given set of points, no point is inside the circumcircle of any triangle within
the Delauney triangulation. 

![voronoi diagram](https://github.com/t9nz/voronoi/blob/main/voronoi.png?raw=true)
![delauney triangulation](https://github.com/t9nz/voronoi/blob/main/delauney.png?raw=true)

## Getting Started

### Dependencies

* Pygame 2.5.2
* Matplotlib 3.5.1
* Numpy 1.22.0

### Installing

* Clone the repository

### Executing program

* Run voronoi.py in the voronoi folder
* Run delauney_triangulation.py in the delauney folder
```
python voronoi.py
python delauney_triangulation.py
```

## Notes

Feel free to open a pull request if you see any changes to make. :-)

## Authors

[@t9nz](https://github.com/t9nz)

## Version History

* 0.1
    * Initial Release

## License

This project is licensed under the MIT License - see the LICENSE.md file for details

## Acknowledgments

Math resources/references, 
* [readme-template](https://gist.github.com/DomPizzie/7a5ff55ffa9081f2de27c315f5018afc)
* [circumcircle-point-check](https://stackoverflow.com/questions/39984709/how-can-i-check-wether-a-point-is-inside-the-circumcircle-of-3-points)
* [circumcircle-calculation](https://mathworld.wolfram.com/Circumcircle.html)
* [bowyer-watson](https://en.wikipedia.org/wiki/Bowyer%E2%80%93Watson_algorithm)
* [delauney-triangulation](https://en.wikipedia.org/wiki/Delaunay_triangulation)