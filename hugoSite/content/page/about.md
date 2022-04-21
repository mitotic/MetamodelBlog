---
author: R. Saravanan
title: About this blog
date: 2022-01-27
description:
keywords: ["about", "contact"]
---

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; *[Metamodel](https://link.springer.com/referenceworkentry/10.1007%2F978-0-387-39940-9_898): a model that consists of statements about models.*

This blog features quirky (not hot) takes on the science and philosophy of
modeling, aimed at a general "science-enthusiast" audience. It is mostly about
climate models, which are arguably the most complex models ever built. But
models from other fields will make a guest appearance now and then. Climate
change will also be discussed as appropriate, because models play an important
role in interpreting it.

As a climate scientist who has worked with a variety of models for over 30
years, I felt there was limited public undestanding of how climate models
worked, and how their predictions should be interpreted. That led me to write
[a book about climate modeling and prediction](https://ClimateDemon.com). In
this blog, I hope to continue discussing some of the topics from the book, such
as the increasing complexity of models, and also explore new topics related to
climate and modeling. (You don't need to have read the book to appreciate this
blog, though.)


*R. Saravanan*

Email: [r@saravanan.us](mailto:r@saravanan.us)
&nbsp;&nbsp;&nbsp; Website: [r.saravanan.us](https:/r.saravanan.us)
&nbsp;&nbsp;&nbsp; Twitter: [@RSarava](https://twitter.com/RSarava)


PS. Among other things, this blog will frequently discuss the shortcomings of
models, especially climate models. It's not because I don't believe in models or
because I'm a climate denier. It's just that having built and worked with
different kinds of models, I am keenly aware of their strengths as well as their
limitations. *I do believe climate change is a serious threat, and we need to
take strong and urgent steps to mitigate carbon emissions. Climate models are
the essential tools used by IPCC to assess our climate futures.* As George Box
noted, "all models are wrong; but some are useful." It is only by analyzing how
models are wrong can one determine which are the most useful.

---

## Why a blog?

Long-form blogs seem to passé in this age of short-form Twitter and Tiktok. But
long-form articles are [still important]({{< relref
"links.md#other-climate-modeling-blogs" >}}), because complex issues cannot be
discussed efficiently in short formats. Keeping with current trends, though,
commenting in this blog is linked to Twitter, and all posts will be
[mirrored on Substack](https://substack.metamodel.blog) to provide a free
subscription for those who prefer to be notified via email. (I don't have a huge
Twitter following, which means you may not see my tweets announcing new posts on
this blog.)

---

## Motivation for the blog

Human nature abhors a prediction vacuum. People always want to know, and often
need to know, what may happen in the future. If a particular source (say,
astronomy) isn't able to provide that information, people will tend to go to a
different source that is willing to provide that information (say,
astrology). Until the weather service started issuing seasonal forecasts using
computer models, people relied on folksy predictions from the
[Old Farmer's Almanac](https://www.almanac.com/) or
[groundhogs named Phil](https://www.groundhog.org/). Today, predictions from
scientific models are used to make decisions that affect millions of people,
often costing many billions of dollars.

Models, scientific or otherwise, will always be used to make decisions. But
[models are frequently misunderstood](https://thebulletin.org/roundtable/the-uncertainty-in-climate-modeling/)
by the general public. All scientists can do is to help ensure that the most
appropriate models are used and that their predictions are interpreted with the
necessary caveats.

The landscape of models is somewhat like the wild west -- there's the good, the
bad, and sometimes even the ugly. It's not easy for an outsider to figure out
which is which because there are no clear rules. The word *model* itself can
mean very different things in diverse fields such as economics, epidemiology,
physics, and climate science. This often results in outsider misconceptions
about how models in a particular field work. 

In climate science, models are not used only for predicting the future, but also
to improve our understanding of phenomena. For example, simple nonlinear models
are used for qualitative understanding of amplifying climate feedbacks, such as
the release of methane from melting permafrost or the increased reflection of
sunlight due to melting icesheets. But such simple models aren't necessarily
good at making quantitative predictions. Misunderstanding the limitations of
models leads to people panicking about tipping points at specific
temperature thresholds or believing in prophecies of imminent doom.

Complex models, which include numerous processes, are used by IPCC and others to
make quantitative predictions of the future. But these complex models do not
necessarily include all the climate feedbacks that can be studied using simpler
models, because we often do not have sufficient data, or powerful enough
computers, to accurately represent these feedbacks. To paraphrase a famous
[quote](https://www.goodreads.com/quotes/1215538-you-go-to-war-with-the-army-you-have-not),
we can only predict with the most comprehensive models we have, not with even
more comprehensive models that we wish to have in the future.

As society has become increasingly reliant on models for climate risk
assessment, there are many important questions need to be addressed, such as:
- What phenomena can be usefully predicted by models?
- How well can these phenomena can be predicted?
- How to choose the best model(s) to use?
- Do we really need to use the most complex and
  expensive models for a particular problem of interest?

The purpose of this blog is to provide the background information to help answer
these questions. What you can expect:
- new posts at roughly 2--3 week intervals
- some posts on fundamental, but unresolved, climate and modeling issues
- some posts on recent developments and publications
- "non-technical" discussions, featuring a mix of science and pop philosophy
- (guest posts on modeling-related issues are welcome)

---

## Technical stuff

As a programmer, I like to roll my own solutions and retain creative control (at
the expense of some convenience). This blog is implemented using open-source
software on a small dedicated virtual linux server. It uses a static web site
generator called [Hugo](https://gohugo.io), with the
[Blist](https://github.com/apvarun/blist-hugo-theme) theme and Nginx as the web
server. Comments on blog posts are handled using
[Remark42](https://remark42.com), a privacy-focused open-source commenting
engine. Commenting on the site requires a "social login" to avoid
spam. Alternatively, you can simply reply to the tweet announcing the blog post
to comment on it.

Markdown is used to format all the content on my laptop. After
previewing locally, the content is pushed to the linux server. Markdown is also
supported for comments. Some modifications were made to the Blist theme and
Remark42 integration to tweak the appearance and functionality of the
blog. (Once it is cleaned up and fully tested, I plan to make the minor code
modifications available on Github.)

Blog posts are mirrored on Substack. Simply copying and pasting the
Hugo-generated web output to the Substack editor appears to work fine for
posting (except for embedded images). This extra bit of effort allows me to
retain flexibility and avoid vendor lock-in, while still making having access to
the Substack platform.

