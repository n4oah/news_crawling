------------------------- TBL_NEWS -------------------------
CREATE TABLE tbl_news (
    posting_id INTEGER PRIMARY KEY,
    crawling_url TEXT NOT NULL,
    title TEXT NOT NULL,
    content TEXT,
    write_date TIMESTAMP NOT NULL,
    image_file BYTEA[],
    image_url TEXT[],
    author_email TEXT NOT NULL,
    like_count INTEGER DEFAULT 0,
    warm_count INTEGER DEFAULT 0,
    unlike_count INTEGER DEFAULT 0,
    angry_count INTEGER DEFAULT 0,
    want_count INTEGER DEFAULT 0,
    recom_count INTEGER DEFAULT 0,
    crawling_gtm TIMESTAMP DEFAULT NOW()
);
------------------------- TBL_NEWS -------------------------

------------------------- TBL_NEWS COMMENT -------------------------
COMMENT ON TABLE tbl_news IS '기사 테이블';
COMMENT ON COLUMN tbl_news.posting_id IS '수집 본문 일련번호';
COMMENT ON COLUMN tbl_news.crawling_url IS '기사 URL';
COMMENT ON COLUMN tbl_news.title IS '기사 제목';
COMMENT ON COLUMN tbl_news.content IS '기사 내용';
COMMENT ON COLUMN tbl_news.write_date IS '기사 작성 날짜';
COMMENT ON COLUMN tbl_news.image_file IS '기사 이미지 파일';
COMMENT ON COLUMN tbl_news.image_url IS '기사 이미지 URL;
COMMENT ON COLUMN tbl_news.like_count IS '좋아요 수';
COMMENT ON COLUMN tbl_news.warm_count IS '훈훈해요 수';
COMMENT ON COLUMN tbl_news.sad_count IS '슬퍼요 수';
COMMENT ON COLUMN tbl_news.angry_count IS '화나요 수';
COMMENT ON COLUMN tbl_news.want_count IS '후속기사 원해요 수';
COMMENT ON COLUMN tbl_news.crawling_gtm IS '수집 일자';
------------------------- TBL_NEWS COMMENT -------------------------

------------------------- TBL_NEWS_COMMENT -------------------------
CREATE TABLE tbl_news_comment (
    posting_sub_id INTEGER PRIMARY KEY,
    posting_id INTEGER REFERENCES tbl_news(posting_id),
    section_author_name TEXT NOT NULL,
    section_context TEXT NOT NULL,
    section_write_date TIMESTAMP NOT NULL,
    helpful_vote_count INTEGER DEFAULT 0,
    unhelpful_vote_count INTEGER DEFAULT 0,
    reply_count INTEGER DEFAULT 0,
    crawling_gmt TIMESTAMP DEFAULT NOW()
);
------------------------- TBL_NEWS_COMMENT -------------------------

------------------------- TBL_NEWS_COMMENT COMMENT -------------------------
COMMENT ON TABLE tbl_news_comment IS '기사 댓글 테이블';
COMMENT ON COLUMN tbl_news_comment.posting_sub_id IS '수집 댓글 일련번호';
COMMENT ON COLUMN tbl_news_comment.posting_id IS '수집 본문 일련번호';
COMMENT ON COLUMN tbl_news_comment.section_author_name IS '작성자 아이디';
COMMENT ON COLUMN tbl_news_comment.section_context IS '본문';
COMMENT ON COLUMN tbl_news_comment.section_write_date IS '작성일자';
COMMENT ON COLUMN tbl_news_comment.helpful_vote_count IS '찬성 수';
COMMENT ON COLUMN tbl_news_comment.unhelpful_vote_count IS '반대 수';
COMMENT ON COLUMN tbl_news_comment.reply_count IS '답글 수';
COMMENT ON COLUMN tbl_news_comment.crawling_gmt IS '수집일자';
------------------------- TBL_NEWS_COMMENT COMMENT -------------------------