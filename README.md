# Metamodel.blog


[Metamodel.blog](https://metamodel.blog) is a social-media-aware static blog implemented using open-source
[Hugo](https://gohugo.io) with
[Blist](https://github.com/apvarun/blist-hugo-theme) theme +
[Remark42](https://remark42.com) for comments.

This repository contains the customizations and enhancements made to the original code.


## Additional Hugo [Front Matter](https://gohugo.io/content-management/front-matter/) variables

- **tweetid:** <tt>numeric id</tt> of Tweet announcing the post. If this is present, Twitter sharing link will default
to liking the tweet and replies to the tweet will be embedded in the comments section

- **comments:** <tt>true</tt> or <tt>false</tt>. If true, commenting (using Remark42) is enabled

- **unlisted:** <tt>true</tt> or <tt>false</tt>. If true, this post will not be listed when deployed. It can still be
  accessed using its URL for testing and sharing privately.

- **featured:** <tt>true</tt> or <tt>false</tt>. If true, this post will be listed in the *Featured Posts* section, below  
the *Recent posts* section, on the home page

- **card:** <tt>URL</tt> for <tt>Twitter/OpenGraph</tt> image for sharing on social media (2:1 aspect ratio preferred)

## Additional Hugo config variables

- **introPosts** = number of articles displayed in *Recent posts* section of the home page 

- **listPosts** = number of posts displayed per page under *All Posts*

- **futurePosts** = <tt>true</tt> or <tt>false</tt>. If ture, display <tt>future.html</html> listing comming attractions

## License

Licensed under [MIT](LICENSE)
