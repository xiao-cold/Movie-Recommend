# 全部电影信息

## 字段说明

- `movieId` 电影 ID
- `tmdbId` TMDB 电影 ID ( 若无则为 0 )
- `original_title` 原始电影名 ( 英文,若无则为空 )
- `year` 年份 ( 若无则为 0)
- `title` 电影名 ( 中文，若无中文则为原始电影名，若无原始电影名则为空 )
- `overview` 电影简介 ( 中文简介，若无则为空 )
- `poster_path` 用于获取 `tmdb` 海报的 `poster_path` ( 若无则为空 )
- `director` 导演 ( 若无则为空 )
- `cast` 演员 ( 以 '|' 分隔，若无则为空 )
- `genres` 类型 ( 以 '|' 分隔，若无则为 `(no genres listed)` )
- `vote_count` 评分人数 ( 若无则为 0 )
- `vote_average` 平均评分 ( 若无则为 0.0 )

