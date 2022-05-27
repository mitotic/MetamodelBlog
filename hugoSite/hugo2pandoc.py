#!/usr/bin/env python3
# Process Hugo Markdown blog posts to create book using Pandoc

import sys, os, yaml, datetime, subprocess, tempfile
from pathlib import Path


def hugo2pandoc(output_file, site_title, site_author, last_date_opt, recent, filenames):
    # Creates modifed copies of markdown files (filenames) in temporary directory
    # making minor changes to Hugo markdown to work with Pandoc by extracting title etc.
    # If last_date_opt is true, add suffix YYYYMMDD to output_file (before extension)
    # If recent > 0, only output recent files
    # returns last post date (YYYYMMDD) as string

    sections = []
    unnumbered_count = 0
    last_date_val = ''
    title_path = None
    with tempfile.TemporaryDirectory() as tmpdirname:
        imgdir = tmpdirname + '/image'
        os.mkdir(imgdir)

        for filename in filenames:
            inname = filename
            fpath = Path(Path.cwd() / filename)

            if fpath.name.startswith('.') or fpath.name.startswith('_'):
                # Skip hidden files
                continue

            if fpath.suffix == '.txt':
                # Frontmatter for epub (YAML)
                title_path = fpath
                sections.append( ('', fpath.name) )
                unnumbered_count += 1
                continue

            if os.path.isdir(fpath):
                outname = fpath.parent.name + fpath.suffix
                index_file = filename + '/index.md'
                if not os.path.isfile(index_file):
                    raise Exception(index_file + ' not found')
                outname = fpath.name + '.md'
                inname = index_file
                postimgdir = str(fpath/'image')
                if os.path.isdir(postimgdir):
                    for imgfile in os.listdir(postimgdir):
                        if imgfile.startswith('.'):
                            continue
                        # Symlink images to directory
                        destname = imgdir+'/'+imgfile
                        if os.path.exists(destname):
                            raise Exception('Duplicate image name '+imgfile)
                        os.symlink(postimgdir+'/'+imgfile, destname)
            else:
                outname = fpath.stem + '-mod' + fpath.suffix

            lines = open(inname, "r").readlines()
            frontmatter = None
            textlines = None
            for line in lines:
                if frontmatter is None:
                    if line.lstrip().startswith('---'):
                        frontmatter = []
                    else:
                        continue
                else:
                    if textlines is None:
                        if line.lstrip().startswith('---'):
                            textlines = []
                        else:
                            frontmatter.append(line)
                    else:
                        textlines.append(line)

            preface = "".join(frontmatter)
            data = yaml.load(preface, Loader=yaml.FullLoader)

            if data.get('draft') or data.get('Draft') or data.get('unlisted') or data.get('Unlisted'):
                continue

            title = data.get('title') or data.get('Title')
            pubdate = data.get('date') or data.get('Date')
            thumbnail = data.get('thumbnail') or data.get('Thumbnail')

            unnumbered = not pubdate or data.get('unnumbered') or data.get('Unnumbered')

            if unnumbered:
                pubdate = ''
                title = title + ' {.unnumbered}'
                unnumbered_count += 1

            sections.append( (str(pubdate), outname) )

            if thumbnail:
                textlines = ['![](image/' + Path(thumbnail).name + ')\n\n'] + textlines

            if pubdate:
                textlines = ['\n' + '<div class="pubdate">'+ str(pubdate) + '&nbsp;&nbsp;&nbsp;&nbsp;</div>' + '\n\n'] + textlines

            description = data.get('description') or data.get('Description')
            if description:
                textlines = ['*' + description + '*\n\n'] + textlines

            textlines = ['# ' + title + '\n\n'] + textlines

            f = open(Path(tmpdirname) / outname, 'w')
            f.write("".join(textlines))
            f.close()

        sections.sort()
        last_date_val = sections[-1][0]
        last_date_suffix = last_date_val.replace('-','')

        if title_path:
            text = open(title_path, "r").read()
            if recent:
                text = text.replace('TITLE', site_title+' recent '+last_date_val)
            else:
                text = text.replace('TITLE', site_title+' '+last_date_val)

            text = text.replace('AUTHOR', site_author)
            text = text.replace('DATE', last_date_val if last_date_opt else str(datetime.date.today()) )

            f = open(tmpdirname+'/'+title_path.name, 'w')
            f.write(text)
            f.close()

        number_offset = 0
        if recent and len(sections) > unnumbered_count + recent:
            # Retain only 2 most recent posts
            number_offset = len(sections) - recent - unnumbered_count
            sections = sections[:unnumbered_count] + sections[-recent:]
                
        outnames = [fname for (dat, fname) in sections]

        outpath = Path(output_file)
        if last_date_opt:
            outpath = Path(outpath.parent / (outpath.stem + '-' + last_date_suffix + outpath.suffix) )

        pandoc_cmd = ['pandoc', '-s', '--css='+str(Path.cwd() /'pandoc/book.css'), '-o', str(Path.cwd() / outpath), '--number-offset='+str(number_offset), '--toc', '--toc-depth=1'] + outnames

        ##print(pandoc_cmd, file=sys.stderr)

        create_book = subprocess.run(pandoc_cmd, text=True, cwd=tmpdirname)

        ##print(create_book, file=sys.stderr)

        return last_date_suffix
