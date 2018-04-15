class SuperDomain:
    def __str__(self):
        prop = self.__dict__
        return ', '.join([key + ':' + str(prop[key]) for key in prop])


class News(SuperDomain):
    posting_id      = None
    crawling_url    = None
    title           = None
    content         = None
    write_date      = None
    image_file      = None
    image_url       = None
    like_count      = None
    warm_count      = None
    sad_count       = None
    angry_count     = None
    want_count      = None
    crawling_gtm    = None


class NewsComment(SuperDomain):
    posting_sub_id          = None
    posting_id              = None
    section_author_name     = None
    section_context         = None
    section_write_date      = None
    helpful_vote_count      = None
    unhelpful_vote_count    = None
    reply_count             = None
    crawling_gmt            = None

