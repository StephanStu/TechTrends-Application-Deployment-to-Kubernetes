import sqlite3

from flask import Flask, jsonify, json, render_template, request, url_for, redirect, flash
from werkzeug.exceptions import abort
# Include logging package
import logging, sys
# Include date + time package
from datetime import datetime

# Global variables
# Total amount of connections to the database.
db_connection_count = 0
# Total amount of posts in the database
post_count = 0

# Function to get a database connection.
# This function connects to database with the name `database.db`
def get_db_connection():
    global db_connection_count
    connection = sqlite3.connect('database.db')
    connection.row_factory = sqlite3.Row
    db_connection_count = db_connection_count + 1
    return connection

# Function to get a post using its ID
def get_post(post_id):
    connection = get_db_connection()
    post = connection.execute('SELECT * FROM posts WHERE id = ?',
                        (post_id,)).fetchone()
    connection.close()
    return post

# Function to count the number of posts in the database
def get_post_count():
    connection = get_db_connection()
    posts =  connection.execute('SELECT * FROM posts')
    count = len(posts.fetchall())
    connection.close()
    return count

# Function to generate handlers for logging
def create_logging_handlers():
    # set logger to handle STDOUT and STDERR
    stdout_handler =  logging.StreamHandler(stream=sys.stdout) # stdout handler `
    stderr_handler =  logging.StreamHandler(stream=sys.stderr) # stderr handler
    file_handler = logging.FileHandler(filename='app.log')
    handlers = [stderr_handler, stdout_handler, file_handler]
    return handlers


# Define the Flask application
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your secret key'

# Define the main route of the web application
@app.route('/')
def index():
    connection = get_db_connection()
    posts = connection.execute('SELECT * FROM posts').fetchall()
    connection.close()
    return render_template('index.html', posts=posts)

# Define how each individual article is rendered
# If the post ID is not found a 404 page is shown
@app.route('/<int:post_id>')
def post(post_id):
    post = get_post(post_id)
    if post is None:
        # Log accessing non-existing arcticles here
        app.logger.error('A non-existing article is accessed and a 404 page is returned!')
        return render_template('404.html'), 404
    else:
        # Log accessing existing arcticles here
        app.logger.debug('Article "%s" retrieved!', post["title"])
        return render_template('post.html', post=post)

# Define the About Us page
@app.route('/about')
def about():
    # Log accessing "About Us" here
    app.logger.debug('The "About Us" page is retrieved!')
    return render_template('about.html')

# Define the post creation functionality
@app.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required!')
        else:
            connection = get_db_connection()
            connection.execute('INSERT INTO posts (title, content) VALUES (?, ?)',
                         (title, content))
            connection.commit()
            connection.close()
            # Log that a new article is created here
            app.logger.debug('Article "%s" created!', title)
            return redirect(url_for('index'))

    return render_template('create.html')

# Define the health-endpoint
@app.route('/healthz', methods=['GET'])
def get_health():
    response = app.response_class(
            response=json.dumps({"result": "OK - healthy"}),
            status=200,
            mimetype='application/json'
    )
    app.logger.debug('Health request successful!')
    return response

# Define the metrics endpoint
@app.route('/metrics', methods=['GET'])
def get_metrics():
    global post_count
    global db_connection_count
    post_count = get_post_count()
    response = app.response_class(
            response=json.dumps({"db_connection_count": db_connection_count, "post_count": post_count}),
            status=200,
            mimetype='application/json'
    )
    app.logger.debug('Metrics request successful!')
    return response

# start the application on port 3111
if __name__ == "__main__":
    # Initialize the logging
    format_output = '%(levelname)s:%(name)s:%(asctime)s, %(message)s'
    logging.basicConfig(format=format_output, level=logging.DEBUG, handlers=create_logging_handlers())
    # Starts the application on host:port
    app.run(host='0.0.0.0', port='3111')
