# Metamodel.blog

This is static blog using
[Hugo](https://gohugo.io) with
[Blist](https://github.com/apvarun/blist-hugo-theme) theme +
[Remark42](https://remark42.com) for comments.

This repository contains the modifications made to the Blist theme for implementing the
[Metamodel.blog](https://metamodel.blog) website.

## Additional Hugo [Front Matter](https://gohugo.io/content-management/front-matter/) variables

- **tweetid:** <tt>numeric id of Tweet announcing the post</tt>. If this is present, Twitter sharing link will default
to liking the tweet and replies to the tweet will be embedded in the comments section

- **comments:** <tt>true</tt> or <tt>false</tt>. If true, commenting (using Remark42) is enabled

- **featured:** <tt>true</tt> or <tt>false</tt>. If true, this post will be listed in the *Featured Posts* section, below
the *Recent posts* section, on the home page

- **card:** <tt>URL for Twitter/OpenGraph image</tt> for sharing on social media (2:1 aspect ratio preferred)

## Additional Hugo config variables

- **introPosts** = number of articles displayed in *Recent posts* section of the home page 

- **listPosts** = number of posts displayed per page under *All Posts*

- **futurePosts** = <tt>true</tt> or <tt>false</tt>. If ture, display <tt>future.html</html> listing comming attractions

## License

Licensed under [MIT](LICENSE)
