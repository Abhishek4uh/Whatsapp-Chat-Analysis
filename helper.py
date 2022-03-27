from urlextract import URLExtract
import pandas as pd
from collections import Counter
import emoji
extractor=URLExtract()
def fetch_stats(selected_user,df):
    if selected_user!='Overall':
        df=df[df['User']==selected_user]
    # Fetch the number of Messages
    num_messages=df.shape[0]
    # Fetch the total number of words
    words=[]
    for message in df['Message']:
        words.extend(message.split())
    # Fetch number of Media File is shared
    num_media= df[df['Message']=='<Media omitted>\n'].shape[0]
    # No of links Shared in the Group
    links = []
    for message in df['Message']:
        links.extend(extractor.find_urls(message))
    return num_messages,len(words),num_media,len(links)

def most_busy_user(df):
    x = df['User'].value_counts().head()
    df = round((df['User'].value_counts() / df.shape[0]) * 100, 2).reset_index().rename(
        columns={'index': 'Name', 'user': 'percent'})
    return x,df

def most_common_words(selected_user,df):
    f = open('stop_hinglish.txt', 'r')
    stop_word = f.read()
    if selected_user!='Overall':
        df=df[df['User']==selected_user]
    temp = df[df['User'] != 'group_notification']
    temp = temp[temp['Message'] != '<Media omitted>\n']
    words = []
    for mess in temp['Message']:
        for word in mess.lower().split():
            if word not in stop_word:
                words.append(word)
    most_common_df = pd.DataFrame(Counter(words).most_common(20))
    return most_common_df

def emoji_helper(selected_user,df):
    if selected_user!='Overall':
        df=df[df['User']==selected_user]
    emojis = []
    for message in df['Message']:
        emojis.extend([c for c in message if c in emoji.UNICODE_EMOJI['en']])
    emoji_df=pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))
    return emoji_df

def monthly_timeline(selected_user,df):
    if selected_user!='Overall':
        df=df[df['User']== selected_user]
    timeline = df.groupby(['Year', 'month_num', 'month']).count()['Message'].reset_index()
    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + "-" + str(timeline['Year'][i]))
    timeline['time'] = time
    return timeline

def daily_timeline (selected_user,df):
    if selected_user != 'Overall':
        df = df[df['User'] == selected_user]
    daily_timeline = df.groupby('only_date').count()['Message'].reset_index()
    return daily_timeline

def weekly_activity(selected_user,df):
    if selected_user!='Overall':
        df=df[df['User']== selected_user]
    return df['day_name'].value_counts()

def monthly_activity(selected_user,df):
    if selected_user!='Overall':
        df=df[df['User']== selected_user]
    return df['month'].value_counts()

def activity_heatmap(selected_user,df):
    if selected_user!='Overall':
        df=df[df['User']== selected_user]
    user_heatmap = df.pivot_table(index='day_name', columns='period', values='Message', aggfunc='count').fillna(0)
    return user_heatmap


