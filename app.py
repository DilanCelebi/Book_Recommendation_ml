from flask import Flask,render_template,request
import pickle
import numpy as np

popular_df = pickle.load(open('popular.pkl','rb'))
pt = pickle.load(open('pt.pkl','rb'))
books = pickle.load(open('books.pkl','rb'))
similarity_scores = pickle.load(open('similarity_scores.pkl','rb'))


app = Flask(__name__, template_folder='/home/dilan/Desktop/book_recommend/')

# Set up search page
@app.route('/')
def index():
       return render_template('search.html',
                           book_name = list(popular_df['Book-Title'].values),
                           author=list(popular_df['Book-Author'].values),
                           image=list(popular_df['Image-URL-M'].values),
                           votes=list(popular_df['Num-Rating'].values),
                           rating=list(popular_df['Avg-Rating'].values)
                           )


@app.route('/recommend')
def recommend_ui():
    return render_template('recommend.html')

@app.route('/recommend_books',methods=['post'])
def recommend():
    user_input = request.form.get('user_input')
    print(user_input)
    
    # convert user input to lowercase
    user_input = user_input.lower()
    
    # convert book titles in pt.index to lowercase
    pt_index_lower = [title.lower() for title in pt.index]
    
    # Find books with matching (partial) titles
    matching_books = []
    for title in pt_index_lower:
        if user_input in title:
            matching_books.append(pt.index[pt_index_lower.index(title)])
    
    if not matching_books:
        print('Book not in database')
        return render_template('recommend.html', data=[])
    
    data = []
    for book_title in matching_books:
        # Index fetch
        index = np.where(pt.index==book_title)[0][0]
        similar_items = sorted(list(enumerate(similarity_scores[index])),key=lambda x:x[1], reverse=True)[1:6]
    
        for i in similar_items:
            item = []
            temp_df = books[books['Book-Title'] == pt.index[i[0]]]
            item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
            item.extend([author.lower() for author in list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values)])
            item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))
        
            data.append(item)
    
    return render_template('recommend.html', data=data)



if __name__ == '__main__':
    app.run(debug=True)