# python -m streamlit run app.py

#imported streamlit library for making our web  app
import streamlit as st  
# imported preprocessor file and helper file
import preprocessor,helper
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter
# it helps to give title for our website
st.sidebar.title("Whatsapp Chat Analyser") 

# it helps in uploading file in our website
uploaded_file = st.sidebar.file_uploader("Choose a file")  
if uploaded_file is not None:
    
    bytes_data = uploaded_file.getvalue()
    #extracted data was in byte format so we are converting it into string(utf-8)
    data = bytes_data.decode('utf-8')
    # we are calling preprocess function from preprocessor file which we have imported
    df = preprocessor.preprocess(data)
    # to display dataframe in streamlit we use dataframe function
    #st.dataframe(df)
    
    # we are extracting unqiue user from user column from our dataframe and saving in into another list
    user_list = df['user'].unique().tolist()
    
    
    #we are removing group_notification from our list if it is present
    s = 'group_notification'
    if s in user_list:
        user_list.remove('group_notification')
    user_list.sort()
    
    
    #it help in showing overall in top of list
    user_list.insert(0,'Overall')
    
    
    # we made drop down menu for every single person in our list
    selected_user = st.sidebar.selectbox("Show analysis wrt",user_list)
    
    if st.sidebar.button("Show Analysis"):
        st.title("Top Statistics")
        num_message,words,num_media_message,links = helper.fetch_stats(selected_user,df)
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.header('Total Messages')
            st.title(num_message)
        with col2:
            st.header('Total Words')
            st.title(words)
        with col3:
            st.header('Media Shared')
            st.title(num_media_message)
        with col4:
            st.header('Links Shared')
            st.title(links)
            
        
        #Monthly timeline
        st.title("Monthly Timeline")
        timeline = helper.monthly_timeline(selected_user,df)
        fig,ax = plt.subplots()
        ax.plot(timeline['time'], timeline['message'],color='green')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        
        # Daily timeline
        st.title("Daily Timeline")
        daily_timeline = helper.daily_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(daily_timeline['only_date'], daily_timeline['message'], color='black')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)
        
        
        # Activity map
        st.title('Activity Map')
        col1,col2 = st.columns(2)

        with col1:
            st.header("Most busy day")
            busy_day = helper.week_activity_map(selected_user,df)
            fig,ax = plt.subplots()
            ax.bar(busy_day.index,busy_day.values,color='purple')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        with col2:
            st.header("Most busy month")
            busy_month = helper.month_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_month.index, busy_month.values,color='orange')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        st.title("Weekly Activity Map")
        user_heatmap = helper.activity_heatmap(selected_user,df)
        fig,ax = plt.subplots()
        ax = sns.heatmap(user_heatmap)
        st.pyplot(fig)
        
        
        #finding busy user
        if selected_user == 'Overall':
            st.title('Most Busy User')
            x, newdf = helper.most_busy_user(df)

            fig, ax = plt.subplots()
    
            col1, col2 = st.columns(2)
            
            with col1:
                ax.bar(x.index,x.values)
                plt.xticks(rotation='vertical')
                st.pyplot(fig)
            with col2:
                st.dataframe(newdf)
        
        
        #Word Cloud       
        st.title("Word Cloud")
        df_wc = helper.create_word_cloud(selected_user,df)
        fig, ax = plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)
        
        
        #Most Common Word
        st.title("Most Common Words")
        col1, col2 = st.columns([1,2])
        most_common_df=helper.most_common_word(selected_user,df)
        
        with col1:
            st.dataframe(most_common_df)
        with col2:
            fig, ax = plt.subplots()
            ax.barh(most_common_df[0],most_common_df[1])
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

    
    
        #Most Used Emoji
        emoji_df=helper.emoji_helper(selected_user,df)
        st.title("Emoji Analysis")
        
        col1,col2 = st.columns(2)

        with col1:
            st.dataframe(emoji_df)
        with col2:
            fig,ax = plt.subplots()
            ax.pie(emoji_df[1].head(),labels=emoji_df[0].head(),autopct="%0.2f")
            st.pyplot(fig)