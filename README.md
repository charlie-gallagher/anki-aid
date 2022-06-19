# Download Audio for Anki Flashcards
Let me be clear -- this is exclusively for the Czech language. Maybe some
time I'll generalize this, but for now, it's just Czech. Really, this is just a
tool to make my life easier, and to work on my Python skills.

# Setting up the environment
I have a `requirements.txt` file and a virtual environment. I don't know what
the deal is with virtual environments and git, though -- should I exclude the
`env` folder entirely? It looks like yes, that is the typical case. Here's my
[source](https://medium.com/wealthy-bytes/the-easiest-way-to-use-a-python-virtual-environment-with-git-401e07c39cde),
which I admit is a Medium article but whatever. This stuff is so common it
_should_ be hard to get wrong.

I didn't know, though, that I have to run `source env/bin/deactivate` when I'm
done with the environment. I guess it makes sense. I was planning on just
starting another session. It's not like a Bash script can auto-run when I change
working directory... At least not without an alias.

I just had an idea for a `cd` alias that automatically checks a standard
location for scripts to run on occurrence of a `cd`, and this works like a LIFO.
You push files to the standard location, for example when you run some custom
venv init script. Then they are automatically deleted. Timestamp controls the
order in which they are executed. I like it.

Anyway, back to focusing on the problem at hand.

# Design
I want to query two different sites for audio results: Shtooka and Forvo. I have
a Forvo API token, and Shtooka is open source, but I need to query some slightly
annoying XML-formatted index files to find out which files to download. I've
already done the hard work there in R, but I'm looking for a more programmatic
approach this time.

At the highest level, I want two options. (A) Pass in a single word and have it
saved to the Anki media directory (`collection.media`), and (B) pass a text file
of words and do the same thing. At the end, print a summary of what succeeded
and what failed.

For the actual searching, the following steps are taken:

- Check Shtooka
- Check Forvo
  - Prefer 'preferred users'
  - Otherwise get whatever has the most upvotes

## Shtooka
Broadly, two steps:

1. Check for local copies of the indices. If they do not exist, "install" them
   (GET and save locally).
2. Search the XML files for the requested word. Once it's found, find the
   corresponding URL and GET the file.

For parsing XML, it looks like `xml.etree.ElementTree` is the standard library
module that gets recommended the most. I also wonder if I'd be able to use
`BeautifulSoup` instead. Not sure.




---

Charlie Gallagher, June 2022
