# Wildlife-Corridors

PYTHON exercise to identify smaller connections between polygons

One of the central issues for forest ecology, involve to answer how expand the capacity of interbreeding populations of native species, when isolated by human activity. The called connectivity, is dependent of several environmental factors, however, will always be greater, in the shortest distance between the habitats fragments.

In principle, the  line represent  the more interesting site for the implementation of the ecological corridors. However, the current ecological condition of the site is crucial to  viability and functionality of the link, but the analysis of this, is a story for another script.

The script attached, consists in PYTHON exercise to identify smaller connections between the habitat fragment  (polygons // input shapefile), resulting in wildlife corridors (lines // output shapefile).
Basic Function: Create line between the closest vertices of the polygons in shapefile
It works pairing all input polygons, but is limited to save smaller lines (< 10000 m) 
Conditions of base shapefile: 1: isolated and non-overlapping polygons; 2: Single Class; 3: No multipart.
