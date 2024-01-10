---
layout: page
title: How to upload Screenshots
hidden: true
---
{% raw %}
To upload screenshots to the new OpenSceneGraph site, simply follow these instructions:

1. Fork and clone [https://github.com/openscenegraph/openscenegraph.io](https://github.com/openscenegraph/openscenegraph.io).
   GitHub have a [guide for absolute beginners](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/working-with-forks/fork-a-repo) if you don't know how to do this.
1. Create a Markdown file with today's date and your (lowercased) project/company name in its filename in `gallery/_posts`.
   The format is effectively `yyyy-mm-dd-your-name-here.md`.
1. Start the file with three dashes (`---`) on a line, then YAML front matter, then another three dashes on a line.
   The supported fields are:
   ```yaml
   layout: post # this is required
   title:  OpenMW # the title shown in the screenshots list and at the top of your article
   show_link_in_gallery: true # if you want to write an article in addition to your screenshots, add this
   images: # a YAML list of image objects
   ```
1. Add your images/videos to a subdirectory of `img/gallery` named after your project/company.
   Ensure they're in a widely-supported format, e.g. PNG, JPEG, GIF, WEBP, H.264 MP4/WEBM.
1. List your images/videos in your YAML front matter.
   The supported fields for each image are:
   ```yaml
   file: img/gallery/openmw/image.png # required. The path to your image.
   label: A pretty picture # a caption to show with your image
   is_video: false # whether this is a video rather than a static image. Defaults to false if absent.
   ```
1. Optionally, write an article about your project and how it uses the OpenSceneGraph in Markdown (specifically [Kramdown](https://kramdown.gettalong.org/quickref.html)) below the second triple dash (`---`) line.
   * You can include your images individually in your article with `![]({% link img/gallery/openmw/image.png %})`.
     This also works with images that aren't in your front-matter `images` list.
   * You can include a gallery of all your images with `{% include image-gallery.html image_list=page.images %}`.
     This also works with custom lists in your front matter that use the same format as `images`---just replace `page.images` with `page.my_custom_list`.
1. Save your work and commit it to a branch, then push it to your fork.
1. Create a Pull Request for the branch on the fork to bring it into the main repo.
1. We'll review your proposal and if appropriate, publish it to the site.

Feel free to take a look at [the existing posts](https://github.com/openscenegraph/openscenegraph.io/tree/main/gallery/_posts) for examples to copy.

{% endraw %}
