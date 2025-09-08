---
layout: default
title: Posts
permalink: /posts/
---


<div class="container">
    <div class="posts-list">
      {% for post in site.posts %}
        <div class="post-item">
          <h2><a href="{{ post.url }}">{{ post.title }}</a></h2>
          <p class="post-date">{{ post.date | date: "%B %d, %Y" }}</p>
          <p class="post-excerpt">{{ post.excerpt | strip_html | truncate: 150 }}</p>
          <a href="{{ post.url }}" class="read-more">Read More</a>
        </div>
      {% endfor %}
    </div>
</div>
