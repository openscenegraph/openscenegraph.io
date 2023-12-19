---
title: Books
header_group: Documentation
layout: page
---

Several books on using the OpenSceneGraph have been published.
While the [www.osgbooks.com](www.osgbooks.com) website is no longer operating, they should be available for purchase, at least as an ebook, from alternative sources.

<div class="grid-post-list">
    {%- for post in site.categories.books -%}
        <div class="grid-post">
            <h4><a href="{{ post.url | relative_url }}">{{ post.title }}</a></h4>
            {{ post.excerpt }}
            {% if post.excerpt.size != post.content.size %}
                <a href="{{ post.url | relative_url }}">Read more...</a>
            {% endif %}
        </div>
    {%- endfor -%}
</div>