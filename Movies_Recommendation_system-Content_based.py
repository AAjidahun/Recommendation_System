import streamlit as st
import pickle 
import requests
import pandas 

movie_list = pickle.load(open('movies.pkl','rb'))
similarity = pickle.load(open('similarity.pkl','rb'))
st.title("Movie Recommendation")
selected_movie_name=st.selectbox("Enter Movie Name",movie_list['title'])

def recommend(movie):
    rec_data=movie_list[['title','id']].copy()
    index=rec_data['title'].index[rec_data['title']==movie]
    similarity_score = similarity[index[0]]
    rec_data['score']=similarity_score
    recommended_movies = rec_data.sort_values('score',ascending=False)[1:12]['title'].values
    recommended_id= rec_data.sort_values('score',ascending=False)[1:12]['id'].values
    recommended_poster= []
    
    for i in recommended_id:
        poster = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=8392bef86d527087d70782c7b88b2bf9&language=en-US'.format(i)).json()
        poster_pic =  'https://image.tmdb.org/t/p/w500' + poster['poster_path']
        recommended_poster.append(poster_pic)
    return recommended_movies,recommended_poster

if st.button('Recommend'):
    names, poster = recommend(selected_movie_name)
    box1,box2,box3,box4,box5=st.columns(5)
    
    box1.text(names[0])
    box1.image(poster[0],use_column_width=True)
    with box2:
        st.text(names[2])
        st.image(poster[2])
    with box3:
        st.text(names[3])
        st.image(poster[3])
    with box4:
        st.text(names[4])
        st.image(poster[4])
    with box5:
        st.text(names[5])
        st.image(poster[5])