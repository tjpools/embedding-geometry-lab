```text
MAN(7)                           Book Two Man Pages                        MAN(7)

NAME
       man - what this lookup layer is, and what it is not

SYNOPSIS
       man <name>          read book2/man/<name>.md
       man -k <word>        scan man/README.md's index table

DESCRIPTION
       This directory is Book Two's man-page layer: a terse, structured,
       tool-oriented reference for the transformer's components, one page per
       operation. It exists beside the narrative chapters, not instead of
       them. A man page tells you what a component does and where its
       boundaries are. It does not teach, motivate, or argue; that work
       belongs to the chapter named in its SOURCE section.

       Each page follows one fixed layout:

           NAME        one line: what it is called, what it does
           SYNOPSIS     the operation's signature or defining equation
           DESCRIPTION  what the operation computes, in the fewest words that
                        remain accurate
           NOTES        the boundaries this page must not cross - what the
                        operation is not, what it does not prove, and how it
                        relates to neighboring operations without collapsing
                        into them
           SEE ALSO     other pages whose operations this one depends on or
                        is depended on by
           SOURCE       the exact chapter and probe whose evidence this page
                        is grounded in

       The README.md index in this directory is the apropos table: name,
       section, one-line description, and source chapter for every page.
       analytics/analyze.py checks it automatically (see engine/manpages.py):
       every page must carry all six sections, every SEE ALSO reference must
       resolve to a page that exists, every SOURCE citation must resolve to
       a chapter that exists, and the index must match the files on disk
       exactly. A page that fails any of these checks is incomplete, not
       merely under-written.

HISTORY
       Unix man pages gave a programmer working at a terminal a lookup table
       for the machine: terse enough to read at a glance, structured enough
       to search, and scoped to one tool at a time. `man 2 write` did not
       explain I/O in general; it explained one system call, its arguments,
       and its return values, and pointed elsewhere for the rest.

       This layer applies that same discipline to a different machine. A
       Transformer is assembled from named, callable operations - attention,
       softmax, a feed-forward stage, a residual addition - each with a
       precise contract and a precise boundary. Treating those operations as
       lookup entries, rather than folding them back into prose, is the same
       instinct that produced /usr/share/man: the tool is inspectable in
       pieces, and each piece deserves its own terse entry.

NOTES
       This page is about the convention, not about any transformer
       component. It has no mathematical claim to verify and therefore no
       chapter probe backing it; its SOURCE is the man-page layer itself.

SEE ALSO
       attention(2), transformer-block(8), execution-trace(1)

SOURCE
       book2/man/README.md; established August 31, 2026.
```
