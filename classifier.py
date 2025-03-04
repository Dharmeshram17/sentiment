# Used to access our youtube API
# googleapiclient = Library --> discovery = model --> Build (instance/object) = function
from googleapiclient.discovery import build
# module that provides sentiment scores based on the words used
#  give us scores of the following categories: Positive, Negative, Neutral
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import matplotlib.pyplot as plt

# YouTube Data API v3 is used to get  comments and likes from youtube videos
API_KEY = 'AIzaSyCu7wdAJ1s9XW2WVBMrcI8ydSJNv6-dLO8'

# Used to communicate with python and youtube data API v3
youtube = build('youtube', 'v3', developerKey=API_KEY)

# The video ID is located in the URL of the video page, right after the "v=" parameter
video_id = 'aZFuYfdrDPc'

# variable to store comments/ empty list
comments_data = []

# Creating a new function called sentiment scores(sentence(comment) to be analyzed)
def sentiment_scores(sentence):
    sia_obj = SentimentIntensityAnalyzer()      # Analyze sentiment of the input
    sentiment_dict = sia_obj.polarity_scores(sentence)    # numerical rating on sentiment score.

    return sentiment_dict

# To retrieve back to back comments
next_page_token = None

while True:
# contains information about a YouTube comment thread, which comprises a top-level comment,likes and replies
    comments_response = youtube.commentThreads().list(
        part='snippet',     # Used to collect information from comments threads
        videoId=video_id,
        maxResults=100,
        pageToken=next_page_token
    ).execute()


    for item in comments_response['items']:
        comment = item['snippet']['topLevelComment']['snippet']['textDisplay']
        like_count = item['snippet']['topLevelComment']['snippet']['likeCount']
# append is used to add an element to the end of the list
        comments_data.append({'comment': comment, 'like_count': like_count})


    next_page_token = comments_response.get('nextPageToken')

    if not next_page_token:
        break

# Print comments and their like counts along with sentiment percentages
total_likes = 0
positive_comments = 0
negative_comments = 0
neutral_comments = 0

for idx, comment_info in enumerate(comments_data, start=1):
    comment = comment_info['comment']
    like_count = comment_info['like_count']
    sentiment_dict = sentiment_scores(comment)
    total_likes += like_count

    # Analyze sentiment and count comments by sentiment
    if sentiment_dict['compound'] >= 0.05:
        sentiment = "Positive"
        positive_comments += 1
    elif sentiment_dict['compound'] <= -0.05:
        sentiment = "Negative"
        negative_comments += 1
    else:
        sentiment = "Neutral"
        neutral_comments += 1

    print(str(idx) + '. Comment: ' + comment)
    print('   Likes: ' + str(like_count))
    print('   Sentiment: ' + sentiment)
    print()

# Calculate sentiment percentages
total_comments = len(comments_data)
positive_percentage = (positive_comments / total_comments) * 100
negative_percentage = (negative_comments / total_comments) * 100
neutral_percentage = (neutral_comments / total_comments) * 100

# Display overall sentiment percentages
print('Total Comments: ' + str(total_comments))
print('Total Likes: ' + str(total_likes))
print('Positive Comments: ' + str(positive_comments) + ' (' + str(positive_percentage) + ' %)')
print('Negative Comments: ' + str(negative_comments) + ' (' + str(negative_percentage) + ' %)')
print('Neutral Comments: ' + str(neutral_comments) + ' (' + str(neutral_percentage) + ' %)')

per = ['Positive', 'Negative', 'Neutral']
percentages = [positive_percentage, negative_percentage, neutral_percentage]

analyzer = ['Positive', 'Negative', 'Neutral']
percentages = [positive_percentage, negative_percentage, neutral_percentage]

plt.bar(analyzer, percentages)
plt.xlabel('per')
plt.ylabel('Percentage')
plt.title('Sentiment Analysis for Video Comments')
plt.show()
