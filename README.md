# Hawberry 

Hawberry is a super simple static site generator that I wrote because I wanted something even simpler and less opinionated than what's currently available.

You can use Hawberry to generate basic websites from single page landing pages to personal blogs to your uncles coffee shop. If you use it as a blog, you can write your posts in markdown.

It's designed to be so simple that you can pick up how to use it and the architecture in less than ten minutes. 

## Concepts 

There's just three main entities you need to be aware of:

`page` - pages on your site. For example, the home page, about page, or the page about your cat. These are standalone HTML files.

`post` - blog post content which are stored as a collection of markdown files. 

`layout` - base templates that serve as skeleton for both your posts and pages.

The only thing you _really_ need to generate a hawberry site are pages. By default, you'll have a home page called `index.html`. 

You don't need posts in your site (like if you're building a landing page) or even layouts if you don't care much for reuse.


## Getting started 

pip install hawberry

## Usage 

* `hb new site PATH` - Creates a new hawberry site at specified path. This creates a default directory structure
* `hb build` - Generates your static site to `./public`. Run this in your sites root directory.
* `hb serve` - Serves your site locally and rebuilds in the background when local files change
* `hb new post` - Generates a new post
* `hb new page` - Generates a new page

## Directory Structure 

* config.json
* layouts
** default.html
** post.html
* posts
** hello-world.md
* sections 
* index.html
* assets
** css
** javascript
* public

Lets go over what each directory or file is for:

| File / Directory | Description |
|------------------|-------------|
|                  |             |
|                  |             |
|                  |             |
|                  |             |

## Posts

Here's what a typical post file looks like (note: you don't need all the metadata that I've included. The only required key is `title`):

```
---
title: "Hello world"
date: 2019-03-26T08:47:11+01:00
draft: true
layout: post
permalink: /my-posts/:title
tags: ["python", "python3"]
---

# Heading

Hello World
```

I'm assuming you know markdown, so I'll just go over what each metadata key does. 

| Key       | Required | Description                                                        |
|-----------|----------|--------------------------------------------------------------------|
| title     | Yes      | Title of your post, i.e "How to Install Hawberry"                  |
| date      | No       | Date published                                                     |
| draft     | No       | If `true`, it will not be published. All posts start off as drafts |
| layout    | No       | Which html skeleton to use. Defaults to `layouts/default.html`     |
| permalink | No       | What the URL should look like. Defaults to `/posts/:title`         |
| tags      | No       | Tags. Useful for SEO or post filtering                             |


