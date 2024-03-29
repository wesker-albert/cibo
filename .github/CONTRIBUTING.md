# Style Guide

Nitpicking is welcomed and encouraged, and so is pushback.

## General Principles

- Be aware of your surroundings. Try to emulate the patterns found in like-files.
- If you see something, say something-- but be kind in the way you say it.
- Strive for excellence. If you know of potentially better ways to style and format
existing patterns, please suggest them.
- Always be ` a e s t h e t i c `.

## Editor

This project is fully intended to be worked on using VS Code.

We leverage dev containers to make sure the local dev environment is clean and
homogenous. There are also a bunch of meticulously curated stylistic settings, rules
and recommended extensions included.

Please use VS Code when interacting with this project.

## File Structure

We don't like huge monolithic files here. We prefer thoughtful, bitesized files that
preferably contain reusable patterns. With the exception of text or JSON documents,
and within reason, please try to keep under 300 lines of code per file.

Directory structure is also preferred to be kept as flat as possible, without being
cluttersome. Introducing sub-directories should be thoughtfully planned, and
discussed.

## CHANGELOG

The CHANGELOG is automatically generated when a PR is merged to `master`, or a new
release is published. Don't worry about updating it manually.

## Pull-Request Naming

PR naming is kind of important, for reasons I'll later point out.

- Follow [APA-style title case](https://apastyle.apa.org/style-grammar-guidelines/capitalization/title-case).
- No period at the end.
- No longer than a brief sentence.

Including the substrings `!ignore` or `!automated` will result in the PR not showing
up in the CHANGELOG.

**Names should begin with one of the following *present-tense* verbs**:
- Add, Create, Implement
- Change, Refactor, Update, Move, Revise
- Deprecate
- Remove, Delete
- Fix, Repair
- Secure

One reason for the above, is the CHANGELOG generator looks for these terms, and then
will [categorize the merge commits](.gitchangelog/.gitchangelog.rc#L10-L18)
accordingly.

Another reason is that it makes git log searching much easier and more reliable.

## Makefile

Make the Makefile work for you. If you find you're constantly reusing a specific
terminal command while working in this repository, it may be a good addition and
useful alias for others.

## Python

OOP is king.

This project leverages some pretty strong automated linting, formatting, and type
checking libraries. Pull requests will not pass checks if there are any failures
within.

In-code disabling of linting or checking rules is highly frowned upon. Very, very
seldomly it may be necessary, primarily due to bugs or limitations with the tools we
use. Explore all avenues to avoid it, however.

### Docstrings

Docstrings are enforced (with the exception of tests) and follow Google-style
templating.

You can quickly generate a docstring template by typing ` ``` ` followed by
pressing `Enter`. A blank template will be generated, which includes existing args,
returns, and raises if performed below a method.

One-line docstrings are acceptable for classes, exceptions, and simple methods that
require no more than one argument.

### Comments

Comments are encouraged at developer discretion. If a comment helps explain some
unusual concept or chain of code, go for it. Just don't comment every single step in
a module. As much as this repository should be friendly to those looking to learn,
code-coddling shouldn't necessary.
