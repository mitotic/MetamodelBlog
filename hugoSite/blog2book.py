#!/usr/bin/env python3
# Process Hugo Markdown blog posts to create book using Pandoc

# Example:
#   blog2book.py --posts-dir=content/posts --outdir=public/ebook --output=book.epub --title=MyBlog --author="My Name" --css=pandoc/book.css --last-date-file=lastdate.txt --recent=3 pandoc/title.txt content/page/about.md content/page/links.md

import sys, os, yaml, datetime, subprocess, tempfile, argparse
from pathlib import Path

def expand_date(d):
    return d[:4]+'-'+d[4:6]+'-'+d[6:] if d else ''

def blog2book(posts_dir, output_dir, output_file, site_title, site_author, css_file, cover_image, last_date_file, force, individual, recent, filenames):
    # Creates modifed copies of markdown files (filenames) in temporary directory
    # making minor changes to Hugo markdown to work with Pandoc by extracting title etc.
    # If last_date_file is specified, add suffix YYYYMMDD to output_file (before extension)
    # If recent > 0, only output recent files
    # returns last post date (YYYYMMDD) as string

    title_name = 'title.txt'
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

            if fpath.name == title_name:
                # Frontmatter for epub (YAML)
                title_path = fpath
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
            card = data.get('card') or data.get('Card') or ''
            pubdate = str(pubdate).replace('-','')

            author = data.get('author') or data.get('Author') or site_author

            unnumbered = not pubdate or data.get('unnumbered') or data.get('Unnumbered')

            ntitle = title
            if unnumbered:
                pubdate = ''
                ntitle = ntitle + ' {.unnumbered}'
                unnumbered_count += 1

            feature = card or thumbnail
            if feature:
                feature = str(fpath / ('image/' + Path(feature).name))

            sections.append( (pubdate, outname, title, author, feature) )

            if thumbnail:
                textlines = ['![](image/' + Path(thumbnail).name + ')\n\n'] + textlines

            if pubdate:
                textlines = ['\n<div class="pubdate">'+expand_date(pubdate)+'&nbsp;&nbsp;&nbsp;&nbsp;</div>\n\n'] + textlines

            description = data.get('description') or data.get('Description')
            if description:
                textlines = ['*' + description + '*\n\n'] + textlines

            textlines = ['# ' + ntitle + '\n\n'] + textlines

            with open(Path(tmpdirname) / outname, 'w') as f:
                f.write(''.join(textlines))

        if not sections:
            raise Exception('No files to process')

        sections.sort()
        last_date_val = sections[-1][0]
        last_feature = sections[-1][-1]

        if last_date_file:
            with open(last_date_file, 'w') as f:
                f.write(last_date_val)

        css_path = str(Path.cwd() / css_file)
        pdf_options = [ '-V', 'colorlinks', '-V', 'geometry:margin=1.2in' ]
        extensions = ('.epub', '.pdf')

        if individual:
            count = 0
            for pdate, fname, title, author, feature in sections:
                if not pdate:
                    continue
                count += 1

                pandoc_cmd = ['pandoc', '-s', '-M', 'title='+title, '-M', 'rights='+author, '--css='+css_path, '--number-offset='+str(count-1)]
                if cover_image:
                    imgpath = 'image/'+pdate+'-cover.png'
                    annotate_image(cover_image, tmpdirname+'/'+imgpath, text=title, feature_image=feature, top_margin=0.075, bot_margin=0.25)
                    pandoc_cmd += [ '--epub-cover-image='+imgpath ]

                for extn in extensions:
                    outpath = outdir / (pdate + '-' + Path(fname).stem + extn)

                    if os.path.isfile(outpath) and pdate <= prev_last_date and not force:
                        continue

                    pandoc_cmd2 = pandoc_cmd[:]
                    
                    if extn == '.pdf':
                        pandoc_cmd2 += ['-M', 'author='+site_title+'/'+author] + pdf_options
                    else:
                        pandoc_cmd2 += ['-M', 'author='+site_title]

                    pandoc_cmd2 += ['-o', str(outpath) ]
                    pandoc_cmd2 += [ fname ]

                    ##print(pandoc_cmd, file=sys.stderr)
                    create_book = subprocess.run(pandoc_cmd2, text=True, cwd=tmpdirname)
                    print('Created', outpath.name, file=sys.stderr)

        if not output_file:
            # No combined output file
            return last_date_val

        if recent:
            cover_text = 'Recent posts ' + expand_date(last_date_val)
        else:
            cover_text = 'All posts ' + expand_date(last_date_val)

        if title_path:
            with open(title_path, "r") as f:
                text = f.read()

            text = text.replace('TITLE', site_title+' '+cover_text)
            text = text.replace('AUTHOR', site_author)
            text = text.replace('DATE', expand_date(last_date_val) if last_date_file else str(datetime.date.today()) )

            with open(tmpdirname+'/'+title_path.name, 'w') as f:
                f.write(text)

        if recent and len(sections) > unnumbered_count + recent:
            # Retain only 2 most recent posts
            number_offset = len(sections) - recent - unnumbered_count
            mdfiles = [fname for (pdate, fname, title, author, feature) in sections[-recent:]]
        else:
            # All posts
            number_offset = 0
            mdfiles = [fname for (pdate, fname, title, author, feature) in sections]

        pandoc_cmd = ['pandoc', '-s', '--css='+str(Path.cwd() / css_file), '--number-offset='+str(number_offset), '--toc', '--toc-depth=1']

        if cover_image:
            imgpath = 'image/CoverImage.png'
            annotate_image(cover_image, tmpdirname+'/'+imgpath, text=cover_text, feature_image=last_feature, top_margin=0.075, bot_margin=0.25)
            pandoc_cmd += [ '--epub-cover-image='+imgpath ]

        outpath = outdir / output_file
        if outpath.suffix in extensions:
            suffixes = [ outpath.suffix ]
        else:
            suffixes = extensions[:]

        outprefix = str( Path(outpath.parent / outpath.stem) )
        if last_date_file:
            outprefix += '-' + last_date_val
        
        for extn in suffixes:
            outfile = outprefix + extn

            if not force and os.path.isfile(outfile) and last_date_val >= prev_last_date:
                continue

            pandoc_cmd2 = pandoc_cmd[:]
            if extn == '.pdf':
                pandoc_cmd2 += pdf_options + ['-M', 'title='+site_title+' '+cover_text]
            elif title_path:
                pandoc_cmd2 += [title_name]

            pandoc_cmd2 += ['-o', outfile ] + mdfiles

            ##print(pandoc_cmd2, file=sys.stderr)

            create_book = subprocess.run(pandoc_cmd2, text=True, cwd=tmpdirname)

            ##print(create_book, file=sys.stderr)
            print('Created', outfile, file=sys.stderr)

        return last_date_val

def annotate_image(cover_image, out_image, text='', feature_image=None, top_margin=0.1, bot_margin=0.1, fontname='DejaVuSans', fontdir='', fontsize=80, text_width=16, text_color='#000000'):
    # Example: annotate_image('cover.png', 'newcover.png', text='The quick brown fox', feature_image='feature.png', top_margin=0.075, bot_margin=0.25)
    from PIL import Image, ImageDraw, ImageFont
    import site, textwrap

    image = Image.open(cover_image)
    draw  = ImageDraw.Draw(image)
    img_wid, img_ht = image.size

    if not fontdir:
        fontdir = site.getsitepackages()[0] + '/matplotlib/mpl-data/fonts/ttf'
    font = ImageFont.truetype(fontdir+'/'+fontname+'.ttf', fontsize, encoding='unic')
    lines = '\n'.join(textwrap.wrap(text, width=text_width))
    txwid, txht = font.getsize_multiline(lines)

    txfrac = txht / img_ht

    # Fractional available height
    avail_frac = 1.0 - (txfrac + top_margin + bot_margin)

    if feature_image and avail_frac > 0:
        try:
            image2 = Image.open(feature_image)
            img2_wid, img2_ht = image2.size

            # Fractional height occupied by feature image
            img2_frac = (img_wid * (img2_ht/img2_wid)) / img_ht

            if img2_frac > avail_frac:
                # Shrink feature image
                img2_frac = avail_frac

            img2_ht2 = int(img2_frac * img_ht)
            img2_wid2 = int(img2_ht2*(img2_wid/img2_ht))

            image2 = image2.resize( (img2_wid2, img2_ht2) )

            xoffset = int(0.5*(img_wid -img2_wid2))
            yoffset = int( (top_margin + txfrac + 0.5*(avail_frac - img2_frac))*img_ht )

            image.paste(image2, (xoffset,yoffset) )
        except Exception as inst:
            print('annotate_image:', inst, file=sys.stderr)

    draw.multiline_text( (int(0.5*(img_wid-txwid)), int(top_margin*img_ht)), lines, fill=text_color, font=font)

    image.save(out_image,'PNG')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--title', type=str, required=True, help='site title')
    parser.add_argument('--author', type=str, required=True, help='site author')
    parser.add_argument('--posts-dir', type=str, help='posts directory, e.g., content/posts')
    parser.add_argument('--output-dir', type=str, help='output directory')
    parser.add_argument('--output', type=str, help='Name of combined output file')
    parser.add_argument('--css', type=str, required=True, help='CSS file path')
    parser.add_argument('--cover_image', type=str, help='Annotatable cover image file')
    parser.add_argument('--last-date-file', type=str, help='read/save last date and append to combined file name')
    parser.add_argument('--force', action='store_true', help='Force creation of files, even if present and up-to-date')
    parser.add_argument('--individual', action='store_true', help='Create individual files for each post')
    parser.add_argument('--recent', type=int, help='Create combined file of recent posts')
    parser.add_argument('files', nargs='*')
    args = parser.parse_args()

    last_date_suffix = blog2book(args.posts_dir, args.output_dir, args.output, args.title, args.author, args.css, args.cover_image, args.last_date_file, args.force, args.individual, args.recent, args.files)

    if args.last_date_file:
        print(last_date_suffix)
