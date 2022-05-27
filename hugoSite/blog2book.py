#!/usr/bin/env python3
# Process Hugo Markdown blog posts to create book using Pandoc

# Example:
#   blog2book.py --posts-dir=content/posts --outdir=public/ebook --output=book.epub --title=MyBlog --author="My Name" --css=pandoc/book.css --last-date-file=lastdate.txt --recent=3 pandoc/title.txt content/page/about.md content/page/links.md

import sys, os, yaml, datetime, subprocess, tempfile, argparse
from pathlib import Path

def expand_date(d):
    return d[:4]+'-'+d[4:6]+'-'+d[6:] if d else ''

def blog2book(posts_dir, output_dir, output_file, site_title, site_author, css_file, last_date_file, force, individual, recent, filenames):
    # Creates modifed copies of markdown files (filenames) in temporary directory
    # making minor changes to Hugo markdown to work with Pandoc by extracting title etc.
    # If last_date_file is specified, add suffix YYYYMMDD to output_file (before extension)
    # If recent > 0, only output recent files
    # returns last post date (YYYYMMDD) as string

    outdir = Path.cwd() / Path(output_dir) if output_dir else Path.cwd()

    filenames = filenames[:]
    if posts_dir:
        if not os.path.isdir(posts_dir):
            raise Exception(posts_dir+ ' not found')
        for fname in os.listdir(posts_dir):
            fpath = posts_dir + '/' + fname
            filenames.append(fpath)

    sections = []
    unnumbered_count = 0
    prev_last_date = ''
    if last_date_file and os.path.isfile(last_date_file):
        with open(last_date_file) as f:
            prev_last_date = f.read().strip()

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
                sections.append( ('', fpath.name, '') )
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
                outname = fpath.name

            with open(inname, "r") as f:
                lines = f.readlines()
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

            title = data.get('title') or data.get('Title') or ''
            pubdate = data.get('date') or data.get('Date') or ''
            thumbnail = data.get('thumbnail') or data.get('Thumbnail') or ''
            pubdate = str(pubdate).replace('-','')

            unnumbered = not pubdate or data.get('unnumbered') or data.get('Unnumbered')

            ntitle = title
            if unnumbered:
                pubdate = ''
                ntitle = ntitle + ' {.unnumbered}'
                unnumbered_count += 1

            sections.append( (pubdate, outname, title) )

            if thumbnail:
                textlines = ['![](image/' + Path(thumbnail).name + ')\n\n'] + textlines

            if pubdate:
                textlines = ['\n<div class="pubdate">'+expand_date(pubdate)+'&nbsp;&nbsp;&nbsp;&nbsp;</div>\n\n'] + textlines

            description = data.get('description') or data.get('Description')
            if description:
                textlines = ['*' + description + '*\n\n'] + textlines

            textlines = ['# ' + ntitle + '\n\n'] + textlines

            with open(Path(tmpdirname) / outname, 'w') as f:
                f.write("".join(textlines))

        if not sections:
            raise Exception('No files to process')

        sections.sort()
        last_date_val = sections[-1][0]

        if last_date_file:
            with open(last_date_file, 'w') as f:
                f.write(last_date_val)

        css_path = str(Path.cwd() / css_file)
        if individual:
            count = 0
            for pdate, fname, title in sections:
                if not pdate:
                    continue
                count += 1

                for extn in ('.epub', '.pdf'):
                    outpath = outdir / (pdate + '-' + Path(fname).stem + extn)

                    if os.path.isfile(outpath) and pdate <= prev_last_date and not force:
                        continue
                
                    pandoc_cmd = ['pandoc', '-s', '-M', 'title='+title, '-M', 'author='+site_title, '--css='+css_path, '-o', str(outpath), '--number-offset='+str(count-1), fname]
                    ##print(pandoc_cmd, file=sys.stderr)
                    create_book = subprocess.run(pandoc_cmd, text=True, cwd=tmpdirname)
                    print('Created', outpath.name, file=sys.stderr)

        if not output_file:
            # No combined output file
            return last_date_val

        if title_path:
            with open(title_path, "r") as f:
                text = f.read()
            if recent:
                text = text.replace('TITLE', site_title+' recent '+expand_date(last_date_val))
            else:
                text = text.replace('TITLE', site_title+' '+expand_date(last_date_val))

            text = text.replace('AUTHOR', site_author)
            text = text.replace('DATE', expand_date(last_date_val) if last_date_file else str(datetime.date.today()) )

            with open(tmpdirname+'/'+title_path.name, 'w') as f:
                f.write(text)

        number_offset = 0
        if recent and len(sections) > unnumbered_count + recent:
            # Retain only 2 most recent posts
            number_offset = len(sections) - recent - unnumbered_count
            sections = sections[:unnumbered_count] + sections[-recent:]
                
        outnames = [fname for (pdate, fname, title) in sections]

        outpath = outdir / output_file
        if last_date_file:
            outpath = Path(outpath.parent / (outpath.stem + '-' + last_date_val + outpath.suffix) )

        if not os.path.isfile(outpath) or last_date_val > prev_last_date or force:
            pandoc_cmd = ['pandoc', '-s', '--css='+str(Path.cwd() / css_file), '-o', str(outpath), '--number-offset='+str(number_offset), '--toc', '--toc-depth=1'] + outnames

            ##print(pandoc_cmd, file=sys.stderr)

            create_book = subprocess.run(pandoc_cmd, text=True, cwd=tmpdirname)

            ##print(create_book, file=sys.stderr)

        return last_date_val

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--title', type=str, required=True, help='site title')
    parser.add_argument('--author', type=str, required=True, help='site author')
    parser.add_argument('--posts-dir', type=str, help='posts directory, e.g., content/posts')
    parser.add_argument('--output-dir', type=str, help='output directory')
    parser.add_argument('--output', type=str, help='Name of combined output file')
    parser.add_argument('--css', type=str, required=True, help='CSS file path')
    parser.add_argument('--last-date-file', type=str, help='read/save last date and append to combined file name')
    parser.add_argument('--force', action='store_true', help='Force creation of files, even if present and up-to-date')
    parser.add_argument('--individual', action='store_true', help='Create individual files for each post')
    parser.add_argument('--recent', type=int, help='Create combined file of recent posts')
    parser.add_argument('files', nargs='*')
    args = parser.parse_args()

    last_date_suffix = blog2book(args.posts_dir, args.output_dir, args.output, args.title, args.author, args.css, args.last_date_file, args.force, args.individual, args.recent, args.files)

    if args.last_date_file:
        print(last_date_suffix)
