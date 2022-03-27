import streamlit as st
import preprocessor
import pandas as pd
import helper
import matplotlib.pyplot as plt
import seaborn as sns
st.sidebar.title("Whatsapp Chat Analyzer")

upload_file=st.sidebar.file_uploader("Choose a file")
if upload_file is not None:
    bytes_data=upload_file.getvalue()
    data=bytes_data.decode("utf-8")
    df=preprocessor.preprocess(data)
    # st.dataframe(df)
    user_list=df['User'].unique().tolist()
    user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0, "Overall")
    selected_user=st.sidebar.selectbox("Show Analysis Wrt", user_list)
    if st.sidebar.button("Show Analysis"):
        num_messages,words,num_media,no_of_links=helper.fetch_stats(selected_user, df)

        # group_create = helper.group_created_date(selected_user,df)
        st.title("Group Created On")
        st.text(df['date'][0])



        st.title("Top Statistics")
        col1,col2,col3,col4=st.columns(4)
        with col1:
            st.header("Total Messages")
            st.title(num_messages)
        with col2:
            st.header("Total Words")
            st.title(words)
        with col3:
            st.header('Media shared')
            st.title(num_media)
        with col4:
            st.header('Links shared')
            st.title(no_of_links)
        # Monthly Timeline
        st.title("Monthly Timeline")
        timeline=helper.monthly_timeline(selected_user,df)
        fig,ax=plt.subplots()
        ax.plot(timeline['time'], timeline['Message'],color='green')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        # Daily Timeline
        # This Month to month plot
        st.title("Daily Timeline")
        daily_timeline = helper.daily_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(daily_timeline['only_date'], daily_timeline['Message'], color='black')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        # Weekly activity
        st.title("Activity Map")
        col1,col2=st.columns(2)
        with col1:
            st.header("Most Busy Day")
            busy_day=helper.weekly_activity(selected_user,df)
            fig,ax=plt.subplots()
            ax.bar(busy_day.index,busy_day.values)
            plt.xticks(rotation='vertical')
            st.pyplot(fig)
        # Monthly Activity
        with col2:
            st.header("Most Busy Month")
            busy_month = helper.monthly_activity(selected_user, df)
            fig,ax = plt.subplots()
            ax.bar(busy_month.index, busy_month.values,color='orange')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        # HeatMap-->
        st.title("Weekly HeatMap")
        user_heatmap=helper.activity_heatmap(selected_user,df)
        fig,af=plt.subplots()
        af=sns.heatmap(user_heatmap)
        st.pyplot(fig)


        # Finding the busiest users in the group (Group Level)
        if selected_user=='Overall':
            st.title('Most Busy Users')
            x ,new_df= helper.most_busy_user(df)
            fig,ax=plt.subplots()
            col1,col2=st.columns(2)
            ax.bar(x.index,x.values)
            with col1:
                ax.bar(x.index,x.values)
                plt.xticks(rotation='vertical')
                st.pyplot(fig)
            with col2:
                st.dataframe(new_df)

        # WordCloud Generates
        # Python version 3.7 (Required)

        # Most Common Words
        #st.header()
        most_common_df=helper.most_common_words(selected_user,df)
        fig,ax=plt.subplots()
        ax.barh(most_common_df[0],most_common_df[1])
        plt.xticks(rotation='vertical')
        st.title('Most 20 Common Words')
        st.pyplot(fig)

        # Emoji Analysis
        emoji_df=helper.emoji_helper(selected_user,df)
        st.title('Emojis Analysis')
        col1,col2,col3=st.columns(3)
        if len(emoji_df) !=0:
            with col1:
                st.dataframe(emoji_df)
            with col2:
                fig,ax=plt.subplots()
                ax.pie(emoji_df[1].head(),labels=emoji_df[0].head(),autopct="%0.2f")
                st.pyplot(fig)
            with col3:
                fig, ax = plt.subplots()
                ax.bar(emoji_df[0].head(), emoji_df[1].head())
                st.pyplot(fig)
        else:
            st.title("This Person didn't use any emojis")




