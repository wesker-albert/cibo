# Style Guide

Nitpicking is welcomed and encouraged, just as much as pushback.

## General Principles

- Be aware of your surroundings. Try to emulate the patterns and in like-files.
- If you see something, say something-- but be kind in the way you say it.
- Strive for excellence. If you know of potentially better ways to style and format
existing patterns, please suggest it.
- Always be ` a e s t h e t i c `.

## File Structure

We don't like huge monolithic files here. We prefer thoughtful, bitesized files and
preferably reusable ones. With the exception of text or JSON documents, please try to
keep lines of code under 300 per file. Within reason, of course.

Directory structure is also preferred to be kept as flat as possible, without being
cluttersome. Introducing sub-directories should be thoughtfully planned.

## CHANGELOG

The CHANGELOG is automatically generated with the command:

```bash
make generate_changelog
```

Always, always, always make sure to do this as the last step before submitting a PR.
Any PR where the CHANGELOG isn't updated, should always have that change requested.

## Makefile

Make the Makefile work for you. If you find you're constantly reusing a specific
terminal command while working in this repository, it may be a good addition and
useful alias for others.


## Python

OOP is king.

This project leverages some pretty strong automated linting, formatting, and type
checking libraries. PR requests should be denied if there are any failures within.

In-code disabling of linting or checking rules is highly frowned upon. Very, very
seldomly it may be necessary, priarily due to bugs or limitations with the tools we
use. Explore all avenues to avoid it, however.

Docstrings are enforced (with the exception of tests), and follow the Google style
standard. You can quickly generate a docstring template by typing ` ``` ` followed by
pressing `Enter`. A blank template will be generated, which includes existing args,
returns, and raises if performed below a method.