from flask import Flask, render_template, request, redirect, url_for, flash, session, send_file
from datetime import datetime
import os
from flask_sqlalchemy import SQLAlchemy
import logging
from gtts import gTTS

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.secret_key = os.urandom(24)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(100), nullable=False)
    image_url = db.Column(db.String(500), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    category = db.Column(db.String(50), nullable=False)

def create_sample_posts():
    try:
        sample_posts = [
            {
                'title': 'Unusual Places I Find Inspiration',
                'content': '''Most people assume inspiration strikes in predictable places: art galleries, nature walks, a good book. Sure, those work. But if I'm honest? My creativity has a habit of showing up in the weirdest corners of life — places I never expected, places that don't look creative at all.

🛒 1. The Grocery Store (Alone, Late at Night)
There's something weirdly cinematic about walking down empty aisles under flickering fluorescent lights. My brain starts writing dialogue between strangers who might've passed each other in the cereal aisle. I build characters based on the sad guy buying only instant noodles or the overly enthusiastic woman comparing almond milks. It's like people-watching with a plot twist.

🧼 2. Long Showers (Cliché, But for a Reason)
It's not just the warm water — it's the white noise, the isolation, the zero expectations. It's one of the few places where my brain has to slow down. I've solved creative problems mid-rinse that hours of focused effort couldn't crack.

📺 3. Cringey Reality TV
Yep. Love Is Blind, Kitchen Nightmares, you name it. People acting absurdly human under pressure? That's character development gold. And somewhere between the drama and the awkward eye contact, I get weird ideas about storytelling, emotion, and how not to design a dating app.

🗑️ 4. Trash Days and Thrift Stores
There's something poetic about discarded things. I once saw a broken lamp on the curb and imagined a whole backstory. Who broke it? Was it an accident or a fight? Why keep it so long, and why toss it now? Inspiration hides in things that have been used, loved, or forgotten.

🧠 5. Boredom
When I'm stuck in a line, waiting for a download, or just staring at a wall — my brain gets itchy. That's usually when the oddest (and often best) ideas bubble up. Boredom is underrated creative fuel. It's when your brain finally has time to wander without direction.

📓 6. Overheard Conversations
I once got the entire premise for a short story from a one-liner I heard on a bus: "I don't care if he has a boat, I'm not getting back with him." Boom. Character. Conflict. Mystery. If you ever feel blocked, just eavesdrop (ethically, of course).

Final Thought
Inspiration doesn't always wear a neon sign. It hides in bad TV, mundane errands, and half-baked thoughts during boring meetings. The trick is to stop waiting for it to show up dressed like a muse — and start noticing when it's hiding in plain sight.''',
                'author': 'Creative Explorer',
                'image_url': 'https://images.unsplash.com/photo-1519681393784-d120267933ba?ixlib=rb-1.2.1&auto=format&fit=crop&w=1350&q=80',
                'category': 'Creativity'
            },
            {
                'title': 'Hidden Gems of Southeast Asia: A Backpacker\'s Guide',
                'content': '''Southeast Asia is a treasure trove of experiences, but beyond the well-trodden paths of Bangkok and Bali lie some truly magical places that most tourists never discover. Here's my guide to the region's best-kept secrets:

🌴 1. Koh Rong Samloem, Cambodia
Forget the party scene of its bigger sister island. This tiny paradise offers bioluminescent plankton that lights up the water at night, creating a magical swimming experience under the stars.

🏮 2. Hoi An, Vietnam
This UNESCO World Heritage site is more than just lanterns and tailors. Venture into the countryside to discover organic farms, traditional pottery villages, and the most authentic Vietnamese cooking classes you'll ever find.

🏝️ 3. El Nido, Philippines
While most tourists head to Boracay, El Nido offers pristine beaches, hidden lagoons, and some of the best island-hopping experiences in the world. Don't miss the secret beaches only accessible through small cave openings!

🍜 4. Luang Prabang, Laos
This sleepy town comes alive at dawn with the daily alms-giving ceremony. The local night market offers the most authentic Laotian street food you'll ever taste.

🌅 5. Gili Islands, Indonesia
These three tiny islands offer everything from party vibes to complete solitude. The best part? No motorized vehicles - just bicycles and horse-drawn carts!

Travel Tips:
• Always carry small bills for local markets
• Learn basic phrases in the local language
• Respect local customs and dress codes
• Try street food - it's often the best food
• Travel slow - the real magic happens when you stay longer

Remember: The best travel experiences often come from getting lost, making local friends, and saying "yes" to unexpected opportunities!''',
                'author': 'Wanderlust Explorer',
                'image_url': 'https://images.unsplash.com/photo-1520250497591-112f2f40a3f4?ixlib=rb-1.2.1&auto=format&fit=crop&w=1350&q=80',
                'category': 'Travel'
            },
            {
                'title': 'The Art of Perfect Pasta: A Beginner\'s Guide',
                'content': '''Pasta is more than just a meal - it's a canvas for creativity in the kitchen. Whether you're a complete beginner or looking to up your pasta game, here's everything you need to know:

🍝 1. Choosing the Right Pasta
• Long pasta (spaghetti, linguine) pairs best with oil-based sauces
• Short pasta (penne, fusilli) works well with chunky sauces
• Fresh pasta cooks in 2-3 minutes
• Dried pasta needs 8-12 minutes

🧂 2. The Perfect Water
• Use a large pot (4-6 quarts per pound of pasta)
• Salt the water like the sea (about 2 tablespoons per gallon)
• Never add oil to the water
• Keep it at a rolling boil

🍅 3. Classic Sauces Made Simple
• Aglio e Olio: Garlic, olive oil, red pepper flakes
• Carbonara: Eggs, cheese, pancetta, black pepper
• Pesto: Basil, pine nuts, garlic, olive oil, parmesan
• Marinara: Tomatoes, garlic, basil, olive oil

🧀 4. Cheese Matters
• Parmesan: The king of pasta cheeses
• Pecorino: Sharp and salty, perfect for carbonara
• Ricotta: Creamy and mild, great for stuffed pasta
• Mozzarella: Melts beautifully in baked dishes

🔥 5. Common Mistakes to Avoid
• Overcooking the pasta
• Rinsing the pasta after cooking
• Using pre-grated cheese
• Not saving pasta water
• Adding sauce to pasta instead of pasta to sauce

Pro Tip: Always save a cup of pasta water before draining. The starchy water helps bind the sauce to the pasta and creates a silky texture.

Remember: The best pasta dishes are made with love, patience, and quality ingredients. Don't be afraid to experiment and make the recipe your own!''',
                'author': 'Pasta Master',
                'image_url': 'https://images.unsplash.com/photo-1551183053-bf91a1d81141?ixlib=rb-1.2.1&auto=format&fit=crop&w=1350&q=80',
                'category': 'Cooking'
            },
            {
                'title': 'One Piece: The Greatest Anime Journey Ever Told',
                'content': '''Join us on an epic adventure through the world of One Piece! From Luffy's humble beginnings in East Blue to the grand adventures in the New World, this masterpiece by Eiichiro Oda has captured hearts worldwide. 

Key highlights:
• The incredible world-building and mythology
• Character development and emotional storytelling
• The perfect blend of action, comedy, and drama
• Themes of friendship, dreams, and freedom
• The mysteries of the Void Century and the Will of D''',
                'author': 'Monkey D. Luffy',
                'image_url': 'https://images.unsplash.com/photo-1634157703702-3c124b455499?ixlib=rb-1.2.1&auto=format&fit=crop&w=1350&q=80',
                'category': 'Anime'
            },
            {
                'title': 'Pirates of the Caribbean: A Legendary Saga',
                'content': '''Yo ho, yo ho, a pirate's life for me! Dive into the swashbuckling world of Pirates of the Caribbean, where Captain Jack Sparrow's eccentric adventures have redefined pirate storytelling.

Key highlights:
• Johnny Depp's iconic portrayal of Jack Sparrow
• The perfect blend of action, humor, and supernatural elements
• Stunning visual effects and memorable ship battles
• The rich mythology of cursed treasures and sea legends
• Unforgettable characters and their complex relationships''',
                'author': 'Captain Jack Sparrow',
                'image_url': 'https://images.unsplash.com/photo-1531259683007-016a7b628fc3?ixlib=rb-1.2.1&auto=format&fit=crop&w=1350&q=80',
                'category': 'Movies'
            }
        ]
        
        for post_data in sample_posts:
            post = Post(**post_data)
            db.session.add(post)
        db.session.commit()
        logger.info("Sample posts created successfully")
    except Exception as e:
        logger.error(f"Error creating sample posts: {str(e)}")
        db.session.rollback()

@app.route('/')
def home():
    try:
        category = request.args.get('category')
        logger.info(f"Category filter: {category}")
        if category:
            posts = Post.query.filter_by(category=category).order_by(Post.date_posted.desc()).all()
            logger.info(f"Found {len(posts)} posts in category {category}")
        else:
            posts = Post.query.order_by(Post.date_posted.desc()).all()
            logger.info(f"Retrieved {len(posts)} posts from database")
        return render_template('index.html', posts=posts, current_category=category)
    except Exception as e:
        logger.error(f"Error in home route: {str(e)}")
        return "An error occurred", 500

@app.route('/post/<int:post_id>')
def post(post_id):
    try:
        post = Post.query.get_or_404(post_id)
        return render_template('post.html', post=post)
    except Exception as e:
        logger.error(f"Error in post route: {str(e)}")
        return "Post not found", 404

@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        try:
            title = request.form['title']
            content = request.form['content']
            image_url = request.form['image_url']
            category = request.form.get('category', 'Blog')
            
            # Get the current user's username from the session or use a default
            current_user = session.get('username')
            if not current_user:
                flash('Please set your name before creating a post', 'warning')
                return redirect(url_for('create'))
            
            new_post = Post(
                title=title,
                content=content,
                author=current_user,
                image_url=image_url,
                category=category
            )
            db.session.add(new_post)
            db.session.commit()
            flash('Post created successfully!', 'success')
            return redirect(url_for('home'))
        except Exception as e:
            logger.error(f"Error creating post: {str(e)}")
            db.session.rollback()
            flash('An error occurred while creating the post', 'error')
            return redirect(url_for('create'))
    return render_template('create.html')

@app.route('/audio-blog')
def audio_blog():
    return render_template('audio_blog.html')

@app.route('/save-audio-blog', methods=['POST'])
def save_audio_blog():
    try:
        title = request.form.get('title')
        content = request.form.get('content')
        category = request.form.get('category')
        
        if not title or not content:
            flash('Title and content are required!', 'error')
            return redirect(url_for('audio_blog'))
        
        new_post = Post(
            title=title,
            content=content,
            category=category,
            author='Voice-to-Blog User',
            image_url='https://images.pexels.com/photos/3155666/pexels-photo-3155666.jpeg'
        )
        
        db.session.add(new_post)
        db.session.commit()
        flash('Blog post created successfully!', 'success')
        return redirect(url_for('home'))
    except Exception as e:
        logger.error(f"Error saving audio blog: {str(e)}")
        db.session.rollback()
        flash('An error occurred while saving the post', 'error')
        return redirect(url_for('audio_blog'))

@app.route('/debug/posts')
def debug_posts():
    try:
        posts = Post.query.all()
        return {
            'total_posts': len(posts),
            'posts': [{
                'id': post.id,
                'title': post.title,
                'category': post.category,
                'author': post.author
            } for post in posts]
        }
    except Exception as e:
        return {'error': str(e)}

@app.route('/edit-post/<int:post_id>', methods=['GET', 'POST'])
def edit_post(post_id):
    post = Post.query.get_or_404(post_id)
    current_user = session.get('username', 'Guest')
    
    # Check if the current user is the author of the post
    if post.author != current_user:
        flash('You are not authorized to edit this post', 'error')
        return redirect(url_for('home'))
        
    if request.method == 'POST':
        try:
            post.title = request.form['title']
            post.content = request.form['content']
            post.image_url = request.form['image_url']
            post.category = request.form.get('category', 'Blog')
            
            db.session.commit()
            flash('Post updated successfully!', 'success')
            return redirect(url_for('home'))
        except Exception as e:
            logger.error(f"Error updating post: {str(e)}")
            db.session.rollback()
            flash('An error occurred while updating the post', 'error')
            return redirect(url_for('edit_post', post_id=post_id))
    return render_template('edit_post.html', post=post)

@app.route('/delete-post/<int:post_id>', methods=['POST'])
def delete_post(post_id):
    try:
        post = Post.query.get_or_404(post_id)
        current_user = session.get('username', 'Guest')
        
        # Check if the current user is the author of the post
        if post.author != current_user:
            flash('You are not authorized to delete this post', 'error')
            return redirect(url_for('home'))
            
        db.session.delete(post)
        db.session.commit()
        flash('Post deleted successfully!', 'success')
    except Exception as e:
        logger.error(f"Error deleting post: {str(e)}")
        db.session.rollback()
        flash('An error occurred while deleting the post', 'error')
    return redirect(url_for('home'))

@app.route('/text-to-speech/<int:post_id>')
def text_to_speech(post_id):
    try:
        post = Post.query.get_or_404(post_id)
        
        # Create audio directory if it doesn't exist
        audio_dir = os.path.join(app.static_folder, 'audio')
        if not os.path.exists(audio_dir):
            os.makedirs(audio_dir)
            
        # Generate unique filename for the audio
        audio_file = f'post_{post_id}.mp3'
        audio_path = os.path.join(audio_dir, audio_file)
        
        # Check if audio file already exists
        if not os.path.exists(audio_path):
            # Create text-to-speech
            tts = gTTS(text=post.content, lang='en', slow=False)
            tts.save(audio_path)
            
        return send_file(audio_path, as_attachment=False)
    except Exception as e:
        logger.error(f"Error in text-to-speech conversion: {str(e)}")
        flash('An error occurred while converting text to speech', 'error')
        return redirect(url_for('post', post_id=post_id))

@app.route('/set-name', methods=['GET', 'POST'])
def set_name():
    if request.method == 'POST':
        username = request.form.get('username')
        if username and len(username.strip()) > 0:
            session['username'] = username.strip()
            flash('Name set successfully!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Please enter a valid name', 'error')
    return render_template('set_name.html')

@app.route('/my-posts')
def my_posts():
    current_user = session.get('username')
    if not current_user:
        flash('Please set your name before viewing your posts', 'warning')
        return redirect(url_for('set_name'))
    
    posts = Post.query.filter_by(author=current_user).order_by(Post.date_posted.desc()).all()
    return render_template('my_posts.html', posts=posts)

if __name__ == '__main__':
    try:
        with app.app_context():
            logger.info("Creating database tables...")
            db.create_all()
            # Check if we need to add sample posts
            if Post.query.count() == 0:
                logger.info("No posts found, creating sample posts...")
                create_sample_posts()
            else:
                logger.info(f"Found {Post.query.count()} existing posts")
    except Exception as e:
        logger.error(f"Error during startup: {str(e)}")
    
    logger.info("Starting Flask application...")
    app.run(debug=True, host='0.0.0.0', port=5000) 