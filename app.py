import flask
import pandas as pd

app = flask.Flask(__name__, template_folder='templates')
d1=pd.read_csv('model/Movie_Id_Titles')
all_titles = [d1['title'][i] for i in range(len(d1['title']))]

def get_recommendations(title):
    column_names = ['user_id', 'item_id', 'rating', 'timestamp']
    data=pd.read_csv('model/u.data',sep='\t',names=column_names)
    movie_data=pd.read_csv('model/Movie_Id_Titles')
    data=pd.merge(data,movie_data,on="item_id")
    ratings = pd.DataFrame(data.groupby('title')['rating'].mean())
    ratings['Number of Rating']=pd.DataFrame(data.groupby('title')['rating'].count())
    md=data.pivot_table(index="user_id",columns="title",values="rating")
    movie_A_ratings=md[title]
    similar_movies=md.corrwith(movie_A_ratings)
    corr_A=pd.DataFrame(similar_movies,columns=["Correlation"])
    corr_A.dropna(inplace=True)
    corr_A=corr_A.join(ratings['Number of Rating'])
    x=corr_A[corr_A["Number of Rating"]>100].sort_values('Correlation',ascending=False)
    y=x.index
    return y
    
# Set up the main route
@app.route('/', methods=['GET', 'POST'])

def main():
    if flask.request.method == 'GET':
        return(flask.render_template('index.html')) 
            
    if flask.request.method == 'POST':
        m_name = flask.request.form['movie_name']
        m_name = m_name.title()
        if m_name not in all_titles:
            return(flask.render_template('negative.html',name=m_name))
        else:         
            result_final = get_recommendations(m_name)
            names = []
            for i in range(len(result_final)):
               names.append(result_final[i])
            return flask.render_template('positive.html',movie_names=names,search_name=m_name)
if __name__ == '__main__':
    app.run(debug=True)