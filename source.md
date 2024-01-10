---
layout: page
title: Source
permalink: /source
---

## Official repositories

### Main repository

The vast majority of the OpenSceneGraph is built from one Git repository, hosted at [https://github.com/openscenegraph/OpenSceneGraph](https://github.com/openscenegraph/OpenSceneGraph).
This includes:
* The core `osg` namespace.
  * Headers are in the [`include/osg`](https://github.com/openscenegraph/OpenSceneGraph/tree/master/include/osg) directory.
  * Source files are in the [`src/osg`](https://github.com/openscenegraph/OpenSceneGraph/tree/master/src/osg) directory.
* Ancillary namespaces such as `osgUtil` and `osgDB` necessary to do anything productive like create windows or load models.
  * Headers are in a subdirectory of [`include`](https://github.com/openscenegraph/OpenSceneGraph/tree/master/include) corresponding to the namespace name.
  * Source files are in a subdirectory of [`src`](https://github.com/openscenegraph/OpenSceneGraph/tree/master/src) corresponding to the namespace name.
* The OpenThreads library
  * Headers are in the [`include/OpenThreads`](https://github.com/openscenegraph/OpenSceneGraph/tree/master/include/OpenThreads) directory.
  * Source files are in the [`src/OpenThreads`](https://github.com/openscenegraph/OpenSceneGraph/tree/master/src/OpenThreads) directory.
* Nodekits for particular features, such as `osgText` for text rendering.
  * Headers are in a subdirectory of [`include`](https://github.com/openscenegraph/OpenSceneGraph/tree/master/include) corresponding to the nodekit name.
  * Source files are in a subdirectory of [`src`](https://github.com/openscenegraph/OpenSceneGraph/tree/master/src) corresponding to the nodekit name.
* Plugins to load various model and image formats, plus miscellaneous utilities like script integration.
  * Each plugin has a subdirectory in the [`src/osgPlugins`](https://github.com/openscenegraph/OpenSceneGraph/tree/master/src/osgPlugins) directory.
* Examples for many features and rendering techniques.
  * Each example has a subdirectory in the [`examples`](https://github.com/openscenegraph/OpenSceneGraph/tree/master/examples) directory.
* Utility applications.
  * Each application has a subdirectory in the [`applications`](https://github.com/openscenegraph/OpenSceneGraph/tree/master/applications) directory.

Notably, these are not split into separate Git repositories, unlike the VulkanSceneGraph.
If you do not require all components, they can be disabled when configuring the CMake project.

### Data repository

Test data, in particular models and shaders required for the provided examples, is available in the [OpenSceneGraph-Data](https://github.com/openscenegraph/OpenSceneGraph-Data) repository.

### osgQt

Integration with the Qt GUI system is provided by the [osgQt](https://github.com/openscenegraph/osgQt) repository.
However, this has been unmaintained for an extended period, and in particular, is incompatible with Qt6 (released in 2020) and has minor issues with Qt5 (initially released in 2012, EOL 2023).
Qt4 reached its End of Life in 2015.

### VirtualPlanetBuilder

[VirtualPlanetBuilder](https://github.com/openscenegraph/VirtualPlanetBuilder) is a terrain database creation tool that is able to read a wide range of geospatial imagery and elevation data and build from small area terrain database to massive whole planet paged databases.

### This website

The source code for this website is hosted at [https://github.com/openscenegraph/openscenegraph.io](https://github.com/openscenegraph/openscenegraph.io).
It has now been migrated to the main OpenSceneGraph GitHub organisation but is still unfinished.

## Third-party repositories

Will be listed here at some point...
