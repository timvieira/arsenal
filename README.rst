python-extras is a collection of python utilities, recipes, and "gutted"
components of other projects.

This project is a bit large and slightly messy. Part of this is because I
dislike installing software on all of the machine I used (yes, even with
tools as awesome as pip, easy_install, and virtualenv). One of my favorite
passtimes is finding the "utils.py" of many open-source projects and
"borrowing" ideas. Unfortunately, I maybe have forgotten to give credit
where credit is due in my part of this repository. If you find some code
which is missing proper attribution please let me know and I will fix it.

There are a lot of files here. I'd like to highlight a few of my most
useful / favorite things:

Highlights
----------

- misc.py
    A "dumping ground" for odd and ends. Including a try_k_times decorator
    preserve current working directory, redirect_io, timelimit decorator.
    I should really organize this better.

- automain.py
    Automatically constructs a "main function" for any module which
    calls the automain function.

- iterextras.py
    the most useful things here are iterview and sliding_window

- nlp/
    Contains make text-processing utilities useful in natural language
    processing. This directory has gotten big enough to almost become its
    own project.

- debug/
  - breakin.py
    ripped out bzr's infamous breakin feature. enabling this allows the user
    to send a SIGQUIT or SIGBREAK signal to a running process and get an
    interactive shell or pdb session AND even resume the process!

  - ultraTB2.py
    I ripped out ultraTB from IPython (to remove the dependence)
    and make some of the functionality easier to use.

- cache/
   contains the memoize decorator and even a persistence shelve-based variant.

- python-snippets/
    various snippets which I often use as reference. These
    snippets are meant to illustrate some of python's advanced features as
    well as quirks and unexpected behaviors.
