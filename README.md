# Metamodel.blog


[Metamodel.blog](https://metamodel.blog) is a social-media-aware static blog implemented using open-source
[Hugo](https://gohugo.io) with
[Blist](https://github.com/apvarun/blist-hugo-theme) theme +
[Remark42](https://remark42.com) for comments.

This repository contains the customizations and enhancements made to the original code.


## Additional Hugo [Front Matter](https://gohugo.io/content-management/front-matter/) variables

- **Tweetid:** <tt>numeric id</tt> of Tweet announcing the post. If this is present, Twitter sharing link will default
to liking the tweet and replies to the tweet will be embedded in the comments section

- **Comments:** <tt>true</tt> or <tt>false</tt>. If true, commenting (using Remark42) is enabled

- **Unlisted:** <tt>true</tt> or <tt>false</tt>. If true, this post will not be listed when deployed. It can still be
  accessed using its URL for testing and sharing privately.

- **Unnumbered:** <tt>true</tt> or <tt>false</tt>. If true, this page will not be numbered as a section by Pandoc.

- **Featured:** <tt>true</tt> or <tt>false</tt>. If true, this post will be listed in the *Featured Posts* section, below  
the *Recent posts* section, on the home page

- **Thumbnail:** <tt>URL</tt> for image to be displayed above article title

- **Card:** <tt>URL</tt> for <tt>Twitter/OpenGraph</tt> image for sharing on social media (2:1 aspect ratio preferred)

## Additional Hugo config variables

- **introPosts** = number of articles displayed in *Recent posts* section of the home page 

- **listPosts** = number of posts displayed per page under *All Posts*

- **futurePosts** = <tt>true</tt> or <tt>false</tt>. If ture, display <tt>future.html</html> listing comming attractions

## Additional notes

- Use <tt>\&deg;</tt> for degree symbol

- Use double space at end of line to force linebreak

- Use <tt>\!\[](url)</tt> to insert images to be Pandoc friendly

- Set <tt>Summary:</tt> to descriptive string if first paragraph is not suitable for use as a summary for the RSS feed

## Blog installation

    #install hugo
	#install node

    hugo new site metablog
    cd metablog
	cp themes/blist/package.json .

	sudo npm install
	sudo npm i -g postcss-cli
	sudo npm install tailwindcss


    # Copy exampleSite and test it
cd themes/blist/exampleSite/
hugo serve --themesDir ../..

cd ../../..

cp themes/blist/package-lock.json .
cp themes/blist/exampleSite/config.toml .

    # EDIT top line of config.toml to set theme = 'blist'

    cp themes/blist/exampleSite/static/* static
    cp -r themes/blist/exampleSite/content/* content

    hugo server -D   # http://localhost:1313/

    # Copy (or symlink) all directories in hugoSite to this directory

## License

Licensed under [MIT](LICENSE)
