# Label news snippets with Snorkel

The main goal of this notebook is to demonstrate the use of semi supervised data labelling technique to label news about cleantech in accordance with UN Sustainable Goal 13 - Climate Action and 7 - Affordable and Clean Energy. 

## Dataset: 
Techcrunch news article snapshot of 2011-2021 with 32,000 news. All copyright belongs to TechCrunch.  

For validation data, 3,000 news were labelled manually with 2 categories: CLEANTECH and NOTRELEVANT

### Columns:
 - **date_gmt(datetime)** - published date
 - **link(string)** - source article link
 - **clean_text (string)** - news article summary, concatenated with header
 - **categories (string)** - article categories ids
 - **tags (string)** - tag ids assigned to the article
 - **author(digit)** - the reporter id who is the author of the news article
 - **_embedded(string)** - string with dictionaries that contain some descriptive info on authors, categories and tags


## Main ideas:

1. All news tags and categories were analyzed with `calc_count_stats.py` script, and were divided into cleantech/notrelevant. 
2. Data were enriched with unsupervised topics model using Gensim with `gensim_model.py`script. Topics were then used as one of the inputs in snorkel functions. 
3. Snorkel functions focused on: keywords matching, cleantech/not cleantech abbrevations, news categories, news tags, cleantech funds mentioned, mentions of cleantech/not cleantech startups, authors that write on topics not in cleantech.  

## Functions performance:

| function name                       | j  | Polarity | Coverage | Overlaps | Conflicts | Correct | Incorrect | Emp. Acc. |
|-------------------------------------|----|----------|----------|----------|-----------|---------|-----------|-----------|
| lf_cleantech_keywords               | 0  | [0]      | 0.021927 | 0.018605 | 0.010299  | 32      | 34        | 0.484848  |
| lf_notcleantech_keywords            | 1  | [1]      | 0.001661 | 0.001661 | 0.000000  | 5       | 0         | 1.000000  |
| lf_contains_cleantech_abbrv         | 2  | [0]      | 0.019269 | 0.014618 | 0.007641  | 36      | 22        | 0.620690  |
| lf_contains_notcleantech_abbrv      | 3  | [1]      | 0.023256 | 0.021595 | 0.000997  | 69      | 1         | 0.985714  |
| lf_cleantech_startups               | 4  | []       | 0.000000 | 0.000000 | 0.000000  | 0       | 0         | 0.000000  |
| lf_notcleantech_startups            | 5  | [1]      | 0.011296 | 0.007973 | 0.001329  | 33      | 1         | 0.970588  |
| lf_cleantech_funds                  | 6  | []       | 0.000000 | 0.000000 | 0.000000  | 0       | 0         | 0.000000  |
| lf_contains_notcleantech_categories | 7  | [1]      | 0.273422 | 0.246512 | 0.008970  | 821     | 2         | 0.997570  |
| lf_contains_cleantech_categories    | 8  | [0]      | 0.025249 | 0.019269 | 0.008306  | 62      | 14        | 0.815789  |
| lf_contains_cleantech_tags          | 9  | [0]      | 0.074751 | 0.052824 | 0.031561  | 127     | 98        | 0.564444  |
| lf_contains_notcleantech_tags       | 10 | [1]      | 0.638538 | 0.379734 | 0.035880  | 1877    | 45        | 0.976587  |
| lf_notcleantech_authors             | 11 | [1]      | 0.052824 | 0.046844 | 0.001661  | 155     | 4         | 0.974843  |
| lf_notcleantech_topics              | 12 | [1]      | 0.224252 | 0.187375 | 0.009635  | 664     | 11        | 0.983704  |

## Model results:

### LabelModel - produces a set of noise-aware probibalistic training labels

| Measure | Value |
| --- | --- |
| accuracy  | 0.949  |
| recall  | 0.95  |
|precision | 0.99 |

### MajorityLabelVoter model - takes the most popular label from functions on per datapoint basis

| Measure | Value |
| --- | --- |
| accuracy  | 0.964  |
| recall  | 0.966  |
|precision | 0.99 |

## Run the notebook: 

To run the notebook execute `poetry install` and then  `poetry run jupyter lab`. 
