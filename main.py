import flet as ft
import tweepy
import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter
from datetime import datetime
import re
import io

# تكوين واجهة برمجة تطبيقات تويتر
consumer_key = "YOUR_CONSUMER_KEY"
consumer_secret = "YOUR_CONSUMER_SECRET"
access_token = "YOUR_ACCESS_TOKEN"
access_token_secret = "YOUR_ACCESS_TOKEN_SECRET"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

def get_tweets(username, count=200):
    tweets = api.user_timeline(screen_name=username, count=count, tweet_mode="extended")
    return tweets

def analyze_tweets(tweets):
    data = []
    for tweet in tweets:
        data.append({
            'text': tweet.full_text,
            'likes': tweet.favorite_count,
            'retweets': tweet.retweet_count,
            'created_at': tweet.created_at
        })
    df = pd.DataFrame(data)
    return df

def get_most_common_words(df, n=10):
    words = ' '.join(df['text']).lower()
    words = re.findall(r'\b\w+\b', words)
    return Counter(words).most_common(n)

def get_main_topics(df, n=5):
    hashtags = ' '.join(df['text'].str.findall(r'#(\w+)')).split()
    return Counter(hashtags).most_common(n)

def get_tweet_times(df):
    df['hour'] = df['created_at'].dt.hour
    return df['hour'].value_counts().sort_index()

def main(page: ft.Page):
    page.title = "محلل تويتر"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 20

    username_field = ft.TextField(label="اسم المستخدم", autofocus=True)
    analyze_button = ft.ElevatedButton(text="تحليل")
    result_tabs = ft.Tabs(
        selected_index=0,
        animation_duration=300,
        tabs=[
            ft.Tab(text="إحصائيات", content=ft.Container(padding=10)),
            ft.Tab(text="الكلمات الشائعة", content=ft.Container(padding=10)),
            ft.Tab(text="المواضيع الرئيسية", content=ft.Container(padding=10)),
            ft.Tab(text="أوقات التغريد", content=ft.Container(padding=10)),
        ],
    )

    def analyze_twitter(e):
        username = username_field.value
        if not username:
            return

        try:
            tweets = get_tweets(username)
            df = analyze_tweets(tweets)

            # إحصائيات
            stats_text = f"""
            عدد التغريدات: {len(df)}
            مجموع الإعجابات: {df['likes'].sum()}
            مجموع إعادات التغريد: {df['retweets'].sum()}
            متوسط الإعجابات لكل تغريدة: {df['likes'].mean():.2f}
            متوسط إعادات التغريد لكل تغريدة: {df['retweets'].mean():.2f}
            """
            result_tabs.tabs[0].content.content = ft.Text(stats_text)

            # الكلمات الشائعة
            common_words = get_most_common_words(df)
            words, counts = zip(*common_words)
            fig, ax = plt.subplots(figsize=(8, 6))
            ax.bar(words, counts)
            ax.set_title("الكلمات الأكثر شيوعًا")
            ax.set_xlabel("الكلمات")
            ax.set_ylabel("عدد التكرارات")
            plt.xticks(rotation=45, ha='right')
            
            img_bytes = io.BytesIO()
            plt.savefig(img_bytes, format='png')
            img_bytes.seek(0)
            result_tabs.tabs[1].content.content = ft.Image(src_base64=img_bytes.getvalue())

            # المواضيع الرئيسية
            topics = get_main_topics(df)
            topics, counts = zip(*topics)
            fig, ax = plt.subplots(figsize=(8, 6))
            ax.pie(counts, labels=topics, autopct='%1.1f%%')
            ax.set_title("المواضيع الرئيسية")
            
            img_bytes = io.BytesIO()
            plt.savefig(img_bytes, format='png')
            img_bytes.seek(0)
            result_tabs.tabs[2].content.content = ft.Image(src_base64=img_bytes.getvalue())

            # أوقات التغريد
            tweet_times = get_tweet_times(df)
            fig, ax = plt.subplots(figsize=(8, 6))
            ax.bar(tweet_times.index, tweet_times.values)
            ax.set_title("أوقات التغريد")
            ax.set_xlabel("الساعة")
            ax.set_ylabel("عدد التغريدات")
            
            img_bytes = io.BytesIO()
            plt.savefig(img_bytes, format='png')
            img_bytes.seek(0)
            result_tabs.tabs[3].content.content = ft.Image(src_base64=img_bytes.getvalue())

            page.update()
        except Exception as e:
            print(f"Error: {e}")

    analyze_button.on_click = analyze_twitter

    page.add(
        ft.Column([
            username_field,
            analyze_button,
            result_tabs
        ])
    )

ft.app(target=main)
