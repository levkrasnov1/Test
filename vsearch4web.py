from flask import Flask, render_template, request, escape
from vsearch import search4letters

''' This aplication for search vowels, or letters in the phrase, or word, which we input '''

app = Flask(__name__)

import psycopg2
from psycopg2 import Error

# def for keep our data in database (PostgreSql)
def log_request(req: 'flask_request', res: str) -> None:
    
       
    try:
        connection = psycopg2.connect(user = 'postgres',
                                      password = '12081993',
                                      host = '127.0.0.1',
                                      port = '5432',
                                      database = 'vsearchlogDB')
        cursor = connection.cursor()
        _SQL = '''INSERT INTO log (phrase, letters, ip, browser_string, results)
                values
                (%s, %s, %s, %s, %s)'''
        cursor.execute(_SQL, (req.form['phrase'],
                              req.form['letters'],
                              req.remote_addr,
                              escape(req.user_agent),
                              res,))
        connection.commit()
        
    except (Exception, Error) as error:
        print('Ошибка при работе с PostgreSQL', error) 
    finally:
        if connection:
            cursor.close()
            connection.close()
            print('соединение с PostgreSQL закрыто') 


#previous version
'''def log_request(req: 'flask_request', res: str) -> None:
    with open('vsearch.log', 'a') as log:
        print(req.form, req.remote_addr, req.user_agent, res, file = log, sep = '|')''' 
        
# This def contains basic functional of our application
@app.route('/search4', methods = ['POST'])
def do_search() -> 'html':
    phrase = request.form['phrase']
    letters = request.form['letters']
    title = 'Here are your results:'
    results = str(search4letters(phrase, letters))
    log_request(request, results)
    return render_template('results.html',
                           the_title = title,
                           the_phrase = phrase,
                           the_letters = letters,
                           the_results = results)

#  def for entry page                                                   
@app.route('/')
@app.route('/entry')
def entry_page() -> 'html':
    return render_template('entry.html',
                           the_title='Welcome to search4letters on the web!')

# def for keep our applicate's data in document vsearch.log
@app.route('/viewlog')
def view_the_log() -> 'html':
    contents = []
    with open('vsearch.log') as log:
        for line in log:
            contents.append([])
            for item in line.split('|'):
                contents[-1].append(escape(item))
    titles = ('Form Data', 'Remote_addr', 'User_agent', 'Results')
    return render_template('viewlog.html',
                            the_title = 'View log',
                            the_row_titles = titles,
                            the_data = contents,)

if __name__ == '__main__':
    app.run(debug = True)

