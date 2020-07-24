# README

## Problem Statement

A "life pro tip" is defined as a concise and specific tip that can improve people's lives. The popular website, Reddit has many forums dedicated to helping people improve their lives. Two of the more popular subreddits to gain these tidbits of advice are [r/LifeProTips](https://www.reddit.com/r/LifeProTips/) and [r/UnethicalLifeProTips](https://www.reddit.com/r/UnethicalLifeProTips/). Both provide advice, but due to the nature of the content, their mission statements are very different.

[r/LifeProTips](https://www.reddit.com/r/LifeProTips/) has the mission to provide "tips that improve your life in one way or another". In order to ensure that the subreddit does provide good advice, the moderators of the site specifically ban any tips deemed to be common sense, common courtesies or unethical. Any posts suggesting behaviors that are illegal in the United States are also banned. 

[r/UnethicalLifeProTips](https://www.reddit.com/r/UnethicalLifeProTips/) is the complete of opposite of [r/LifeProTips](https://www.reddit.com/r/LifeProTips/). They allow users to post tips that will likely improve lives but might be harmful to others and/or condone behaviors bordering on illegal. Although the moderators suggest the advice is just for fun and should not be followed, several people come to the site to find and request unethical advice. 

Given the constrasting missions of the two subreddits, it is imperative that no Unethical Life Pro Tips ever be posted to [r/LifeProTips](https://www.reddit.com/r/LifeProTips/). However, in a recent update to the popular website Reddit, a backend engineer accidentally programmed all of the posts that were submitted to the 'Unethical Life Pro Tips' subreddit to be posted to the 'Life Pro Tips' subreddit. ***As the data scientist on the team, I have been assigned the task of building a classificiation model that can accurately classify posts from each subreddit so that r/Life Pro Tips can be free of unethical advice and [r/UnethicalLifeProTips](https://www.reddit.com/r/UnethicalLifeProTips/) can continue to offer new, unethical content.***

## Executive Summary
Data was collected from r/LifeProTips and r/UnethicalLifeProTips on July 18, 2020 using the [Pushift Reddit API](https://github.com/pushshift/api). In total, 2677 posts from r/LifeProTips were collected, corresponding to 15 days worth of data, and 3961 posts from r/UnethicalLifeProTips were collected, corresponding to approximately 40 weeks of data. Posts were aggreggated into a single data frame and data was cleaned according to standard protocol (handling null values, confirming data types, and searching for any abnormal values). Because text data can contain many symbols and phrases that do not add value to a sentence, any symbols or tags (e.g. '[request]') were removed to the best of my abilities. Additionally, in order to make the task more challenging, the 'LPT' and 'ULPT' tags were also removed from posts. Basic features were engineered to allow for examination of full text in the post, post length in characters, post length in words, and sentiment polarity (-1 = Negative, 1 = Positive).

Once the data had been clean, text preprocessing was conducted to expand contractions in the text, and posts were tokenized and  words were reduced to their word stems using a Porter stemmer. In order to be compatible with the text vectorizers, the stemmed words were joined as a string. At this point, the data frame was considered ready for exploratory data analysis and modeling. The data dictionary can be found below. 

During EDA, distributions for all numeric features were explored, the most frequent word counts were generated per subreddit. Sentiment analysis with TextBlob was also conducted to determine if polarity differed by subreddit. 

Following EDA, the data was prepared for modeling. Prior to beginning the modeling process, preliminary analyses were conducted to determine the best vectorizer for the data. These analyses revealed that a Tfidf Vectorizer performed better than a Count Vectorizer in Logisitic Regression models, so only Tfidf was used for these models. A 70/30 train test split was conducted, and a column transformer with a Tfidf Vectorizer was created to vectorizer the stemmed text, while also maintaining the original form of any numeric features. 

During the modeling process, for each model (except for the Baseline/Null Model), a pipeline was created. Pipelines contained the column transformer (Tfidf Vectorizer) and a classification model. GridSearchCV was used to tune hyperparameters, and model performance was evaluated using the accuracy metric. The models built were: 
1. Baseline/Null Model
2. Logistic Regression
3. Logistic Regression with L2 Regularization
4. Multinomial Bayes
5. K-Nearest Neighbors (KNN)
6. Decision Tree
7. Bagging Classifier
8. Random Forest
9. Voting Classifier

In this repository my work flow will be described, and I will select and evaluate a model to classify by posts from the r/LifeProTips and r/UnethicalLifeProTips subreddits.

## Contents of Repository
1. [Raw Data](https://git.generalassemb.ly/jlu90/project_3/tree/master/data)
2. [Data Retrieval Notebook](https://git.generalassemb.ly/jlu90/project_3/blob/master/code/01-Scraping%20from%20Reddit.ipynb)
3. [Project Notebook](https://git.generalassemb.ly/jlu90/project_3/blob/master/code/Project%203%20-%20Life%20Pro%20Tips%20vs.%20Unethical%20Life%20Pro%20Tips%20Classification.ipynb)

## Data Dictionary

The clean, preprocessed data used for EDA and modeling can be found [here](https://git.generalassemb.ly/jlu90/project_3/blob/master/data/subreddits_preprocessed.csv).

|Column| Data Type| Description|
|---|---|---|
subreddit| String| Source of data
suthor|String| Author of post
num_comments|Integer|Number of comments a post received
score|Integer|Score of post
timestamp|Datetime|Date of post
original_text|String|Text from original post
post_length_char|Integer|Character length of post
post_length_words|Integer|Word count of post
is_unethical|Integer|Binary variable denoting if a post came from Unethical Life Pro Tips
stemmer_text|String|Post with stemmed text
polarity|Float|Positive or negative sentiment of post ranging from 1 (positive) to -1 (negative)
sentiment_cat|String|Category of sentiment based on polarity score


## Key Findings and Conclusions
For this problem, I was tasked with building a classification model that could accurately distinguish posts from the r/LifeProTipsSubreddit from the r/UnethicalLifeProTips Subreddit. The best-performing model was a Random Forest Classifier with an accuracy of 78% and a sensitivity of 90.6%. This model is good at accurately predicting posts from the r/UnethicalLifeProTips Subreddit, but it performs almost at Baseline for posts from r/LifeProTips. Although the consequences of posting genuine Life Pro Tips to r/UnethicalLifeProTips are probably minimal (unless it encourages people to behave more ethically!), to truly accomplish the task at hand, prior to being production-ready, we should try to improve the overall accuracy score. 

To begin the next round of improvements, we will learn from our models and manually prune features from the vector of words. Once the dimensionality of the models has been reduced, we will be able to tune our models in hopes of improving the overall accuracy.
