from flask import Flask, render_template, request, session, redirect, url_for, flash, jsonify
from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from datetime import datetime
import os

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'your-secret-key-change-in-production')


MONGO_URI = "mongodb://localhost:27017/"
try:
    client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
    client.admin.command('ping')
    db = client['fitapply']
    print("✓ MongoDB connected successfully")
except Exception as e:
    print(f"✗ MongoDB connection failed: {e}")
    db = None


users_col = db['users'] if db is not None else None
jobs_col = db['jobs'] if db is not None else None
applications_col = db['applications'] if db is not None else None



def login_required(f):
    """Decorator to require login"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please login first', 'danger')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function


def get_current_user():
    """Get current logged-in user"""
    if 'user_id' not in session:
        return None
    from bson.objectid import ObjectId
    return users_col.find_one({'_id': ObjectId(session['user_id'])})



@app.route('/')
def index():
    """Home page"""
    total_jobs = jobs_col.count_documents({}) if jobs_col is not None else 0
    total_users = users_col.count_documents({}) if users_col is not None else 0
    return render_template('index.html', total_jobs=total_jobs, total_users=total_users)


@app.route('/about')
def about():
    """About page"""
    return render_template('about.html')


@app.route('/help')
def help():
    """Help/FAQ page"""
    return render_template('help.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    """User signup"""
    if request.method == 'POST':
        full_name = request.form.get('full_name')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        phone = request.form.get('phone')
        location = request.form.get('location')

        
        if not all([full_name, email, password, confirm_password]):
            flash('All fields are required', 'danger')
            return redirect(url_for('signup'))

        if password != confirm_password:
            flash('Passwords do not match', 'danger')
            return redirect(url_for('signup'))

        if len(password) < 6:
            flash('Password must be at least 6 characters', 'danger')
            return redirect(url_for('signup'))

        
        if users_col.find_one({'email': email}):
            flash('Email already registered', 'danger')
            return redirect(url_for('signup'))

        
        user_data = {
            'full_name': full_name,
            'email': email,
            'password': generate_password_hash(password),
            'phone': phone,
            'location': location,
            'created_at': datetime.utcnow(),
            'profile_image': 'https://ui-avatars.com/api/?name=' + full_name.replace(' ', '+'),
            'bio': ''
        }

        result = users_col.insert_one(user_data)
        flash('Account created successfully! Please login', 'success')
        return redirect(url_for('login'))

    return render_template('signup.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login"""
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = users_col.find_one({'email': email})

        if user and check_password_hash(user['password'], password):
            session['user_id'] = str(user['_id'])
            session['user_name'] = user['full_name']
            session['user_email'] = user['email']
            flash(f'Welcome back, {user["full_name"]}!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid email or password', 'danger')

    return render_template('login.html')


@app.route('/logout')
def logout():
    """User logout"""
    session.clear()
    flash('You have been logged out', 'info')
    return redirect(url_for('index'))



@app.route('/jobs')
def jobs():
    """List all jobs"""
    category = request.args.get('category', '')
    search = request.args.get('search', '')

    query = {}
    if category:
        query['category'] = category
    if search:
        query['$text'] = {'$search': search}

    jobs_list = list(jobs_col.find(query).limit(50)) if jobs_col is not None else []
    categories = jobs_col.distinct('category') if jobs_col is not None else []

    return render_template('jobs.html', jobs=jobs_list, categories=categories, search=search)


@app.route('/job/<job_id>')
def job_detail(job_id):
    """Job detail page"""
    from bson.objectid import ObjectId
    job = jobs_col.find_one({'_id': ObjectId(job_id)})

    if not job:
        flash('Job not found', 'danger')
        return redirect(url_for('jobs'))


    user_applied = False
    if 'user_id' in session:
        user_applied = applications_col.find_one({
            'user_id': ObjectId(session['user_id']),
            'job_id': ObjectId(job_id)
        }) is not None

    return render_template('job_detail.html', job=job, user_applied=user_applied)


@app.route('/job/<job_id>/apply', methods=['POST'])
@login_required
def apply_job(job_id):
    """Apply for a job"""
    from bson.objectid import ObjectId

    job_id_obj = ObjectId(job_id)
    user_id_obj = ObjectId(session['user_id'])
    job = jobs_col.find_one({'_id': job_id_obj})

    if not job:
        return jsonify({'error': 'Job not found'}), 404

   
    if applications_col.find_one({'user_id': user_id_obj, 'job_id': job_id_obj}):
        return jsonify({'error': 'Already applied'}), 400

    application = {
        'user_id': user_id_obj,
        'job_id': job_id_obj,
        'job_title': job['title'],
        'company': job['company'],
        'cover_letter': request.form.get('cover_letter', ''),
        'applied_at': datetime.utcnow(),
        'status': 'pending'
    }

    applications_col.insert_one(application)
    flash('Application submitted successfully!', 'success')
    return redirect(url_for('job_detail', job_id=job_id))



@app.route('/dashboard')
@login_required
def dashboard():
    """User dashboard"""
    from bson.objectid import ObjectId

    user_id_obj = ObjectId(session['user_id'])
    applications = list(applications_col.find({'user_id': user_id_obj}))


    total_applications = len(applications)
    pending_count = applications_col.count_documents({'user_id': user_id_obj, 'status': 'pending'})
    accepted_count = applications_col.count_documents({'user_id': user_id_obj, 'status': 'accepted'})
    rejected_count = applications_col.count_documents({'user_id': user_id_obj, 'status': 'rejected'})

    return render_template('dashboard.html',
                         applications=applications,
                         total_applications=total_applications,
                         pending_count=pending_count,
                         accepted_count=accepted_count,
                         rejected_count=rejected_count)


@app.route('/profile')
@login_required
def profile():
    """User profile"""
    user = get_current_user()
    return render_template('profile.html', user=user)


@app.route('/profile/update', methods=['POST'])
@login_required
def update_profile():
    """Update user profile"""
    from bson.objectid import ObjectId

    user_id_obj = ObjectId(session['user_id'])
    update_data = {
        'full_name': request.form.get('full_name'),
        'phone': request.form.get('phone'),
        'location': request.form.get('location'),
        'bio': request.form.get('bio')
    }

    users_col.update_one({'_id': user_id_obj}, {'$set': update_data})
    session['user_name'] = update_data['full_name']

    flash('Profile updated successfully', 'success')
    return redirect(url_for('profile'))



@app.route('/admin/seed-jobs', methods=['GET', 'POST'])
def seed_jobs():
    """Admin route to seed sample jobs - FOR DEMO ONLY"""
    if request.method == 'POST':
        sample_jobs = [
            {
                'title': 'Senior Python Developer',
                'company': 'TechCorp Solutions',
                'category': 'Backend',
                'location': 'New York, NY',
                'salary': '$120,000 - $160,000',
                'description': 'Looking for an experienced Python developer with 5+ years of experience.',
                'requirements': ['Python 3.9+', 'FastAPI/Django', 'PostgreSQL', 'Docker', 'AWS'],
                'posted_at': datetime.utcnow(),
                'image': 'https://images.unsplash.com/photo-1517694712202-14dd9538aa97?w=400'
            },
            {
                'title': 'Frontend React Developer',
                'company': 'WebFlow Studios',
                'category': 'Frontend',
                'location': 'San Francisco, CA',
                'salary': '$110,000 - $150,000',
                'description': 'Join our team to build amazing user interfaces with React and TypeScript.',
                'requirements': ['React 18+', 'TypeScript', 'Tailwind CSS', 'Next.js', 'Testing'],
                'posted_at': datetime.utcnow(),
                'image': 'https://images.unsplash.com/photo-1517694712202-14dd9538aa97?w=400'
            },
            {
                'title': 'Full Stack Developer',
                'company': 'CloudBase Inc',
                'category': 'Full Stack',
                'location': 'Remote',
                'salary': '$100,000 - $140,000',
                'description': 'Build end-to-end solutions with modern web technologies.',
                'requirements': ['Node.js', 'React', 'MongoDB', 'Docker', 'AWS'],
                'posted_at': datetime.utcnow(),
                'image': 'https://images.unsplash.com/photo-1517694712202-14dd9538aa97?w=400'
            },
            {
                'title': 'DevOps Engineer',
                'company': 'InfraCloud Systems',
                'category': 'DevOps',
                'location': 'Seattle, WA',
                'salary': '$130,000 - $170,000',
                'description': 'Manage and optimize our cloud infrastructure using Kubernetes and CI/CD.',
                'requirements': ['Kubernetes', 'Docker', 'AWS/GCP', 'Terraform', 'Jenkins'],
                'posted_at': datetime.utcnow(),
                'image': 'https://images.unsplash.com/photo-1517694712202-14dd9538aa97?w=400'
            },
            {
                'title': 'Data Scientist',
                'company': 'Analytics Pro',
                'category': 'Data Science',
                'location': 'Boston, MA',
                'salary': '$115,000 - $155,000',
                'description': 'Work with cutting-edge ML models and big data technologies.',
                'requirements': ['Python', 'Machine Learning', 'SQL', 'Spark', 'TensorFlow'],
                'posted_at': datetime.utcnow(),
                'image': 'https://images.unsplash.com/photo-1517694712202-14dd9538aa97?w=400'
            },
            {
                'title': 'Mobile App Developer (iOS)',
                'company': 'AppMaster Studio',
                'category': 'Mobile',
                'location': 'Los Angeles, CA',
                'salary': '$100,000 - $140,000',
                'description': 'Develop high-performance iOS applications using Swift.',
                'requirements': ['Swift', 'iOS SDK', 'Xcode', 'SwiftUI', 'CocoaPods'],
                'posted_at': datetime.utcnow(),
                'image': 'https://images.unsplash.com/photo-1517694712202-14dd9538aa97?w=400'
            },
            {
                'title': 'Mobile App Developer (Android)',
                'company': 'AppMaster Studio',
                'category': 'Mobile',
                'location': 'Austin, TX',
                'salary': '$95,000 - $135,000',
                'description': 'Create innovative Android applications using Kotlin.',
                'requirements': ['Kotlin', 'Android Studio', 'Jetpack', 'MVVM', 'Firebase'],
                'posted_at': datetime.utcnow(),
                'image': 'https://images.unsplash.com/photo-1517694712202-14dd9538aa97?w=400'
            },
            {
                'title': 'UX/UI Designer',
                'company': 'Design Innovations',
                'category': 'Design',
                'location': 'Remote',
                'salary': '$80,000 - $120,000',
                'description': 'Design beautiful and intuitive user experiences for web and mobile apps.',
                'requirements': ['Figma', 'User Research', 'Prototyping', 'Design Systems', 'CSS Basics'],
                'posted_at': datetime.utcnow(),
                'image': 'https://images.unsplash.com/photo-1561070791-2526d30994b5?w=400'
            },
            {
                'title': 'QA Engineer',
                'company': 'QualityAssure Corp',
                'category': 'QA',
                'location': 'Denver, CO',
                'salary': '$75,000 - $110,000',
                'description': 'Ensure software quality through comprehensive testing strategies.',
                'requirements': ['Selenium', 'Python', 'API Testing', 'JIRA', 'SQL'],
                'posted_at': datetime.utcnow(),
                'image': 'https://images.unsplash.com/photo-1517694712202-14dd9538aa97?w=400'
            },
            {
                'title': 'Database Administrator',
                'company': 'DataVault Systems',
                'category': 'Database',
                'location': 'Chicago, IL',
                'salary': '$105,000 - $145,000',
                'description': 'Manage and optimize large-scale database systems.',
                'requirements': ['PostgreSQL', 'MongoDB', 'Oracle', 'Backup/Recovery', 'Performance Tuning'],
                'posted_at': datetime.utcnow(),
                'image': 'https://images.unsplash.com/photo-1517694712202-14dd9538aa97?w=400'
            },
            {
                'title': 'Cloud Architect',
                'company': 'CloudFirst Solutions',
                'category': 'Cloud',
                'location': 'Remote',
                'salary': '$140,000 - $180,000',
                'description': 'Design scalable cloud solutions for enterprise clients.',
                'requirements': ['AWS', 'Azure', 'GCP', 'Architecture Design', 'Security'],
                'posted_at': datetime.utcnow(),
                'image': 'https://images.unsplash.com/photo-1517694712202-14dd9538aa97?w=400'
            },
            {
                'title': 'Cybersecurity Analyst',
                'company': 'SecureNet Inc',
                'category': 'Security',
                'location': 'Arlington, VA',
                'salary': '$110,000 - $150,000',
                'description': 'Protect systems and data from cyber threats.',
                'requirements': ['Network Security', 'Penetration Testing', 'SIEM', 'Compliance', 'Python'],
                'posted_at': datetime.utcnow(),
                'image': 'https://images.unsplash.com/photo-1517694712202-14dd9538aa97?w=400'
            },
            {
                'title': 'Machine Learning Engineer',
                'company': 'AIVision Labs',
                'category': 'AI/ML',
                'location': 'San Jose, CA',
                'salary': '$125,000 - $165,000',
                'description': 'Build and deploy ML models for real-world applications.',
                'requirements': ['Python', 'TensorFlow', 'PyTorch', 'Deep Learning', 'SQL'],
                'posted_at': datetime.utcnow(),
                'image': 'https://images.unsplash.com/photo-1517694712202-14dd9538aa97?w=400'
            },
            {
                'title': 'Technical Project Manager',
                'company': 'ProjectFlow Inc',
                'category': 'Management',
                'location': 'New York, NY',
                'salary': '$95,000 - $135,000',
                'description': 'Lead technical teams and deliver projects on time.',
                'requirements': ['Agile/Scrum', 'Leadership', 'JIRA', 'Communication', 'Technical Knowledge'],
                'posted_at': datetime.utcnow(),
                'image': 'https://images.unsplash.com/photo-1517694712202-14dd9538aa97?w=400'
            },
            {
                'title': 'Solutions Architect',
                'company': 'EnterpriseTech Solutions',
                'category': 'Architecture',
                'location': 'Boston, MA',
                'salary': '$130,000 - $170,000',
                'description': 'Design comprehensive solutions for enterprise customers.',
                'requirements': ['System Design', 'Cloud', 'Microservices', 'Communication', 'Business Acumen'],
                'posted_at': datetime.utcnow(),
                'image': 'https://images.unsplash.com/photo-1517694712202-14dd9538aa97?w=400'
            },
            {
                'title': 'API Developer',
                'company': 'APIHub Services',
                'category': 'Backend',
                'location': 'Remote',
                'salary': '$100,000 - $140,000',
                'description': 'Design and develop RESTful and GraphQL APIs.',
                'requirements': ['REST APIs', 'GraphQL', 'Node.js/Python', 'MongoDB', 'Git'],
                'posted_at': datetime.utcnow(),
                'image': 'https://images.unsplash.com/photo-1517694712202-14dd9538aa97?w=400'
            },
            {
                'title': 'Frontend Lead',
                'company': 'UI Excellence',
                'category': 'Frontend',
                'location': 'San Francisco, CA',
                'salary': '$120,000 - $160,000',
                'description': 'Lead frontend team and set technical direction.',
                'requirements': ['React', 'Web Performance', 'Leadership', 'TypeScript', 'CSS Architecture'],
                'posted_at': datetime.utcnow(),
                'image': 'https://images.unsplash.com/photo-1517694712202-14dd9538aa97?w=400'
            },
            {
                'title': 'Backend Architect',
                'company': 'BackendMasters',
                'category': 'Backend',
                'location': 'Seattle, WA',
                'salary': '$135,000 - $175,000',
                'description': 'Architect scalable backend systems and microservices.',
                'requirements': ['Microservices', 'System Design', 'Python/Java', 'Redis', 'Kafka'],
                'posted_at': datetime.utcnow(),
                'image': 'https://images.unsplash.com/photo-1517694712202-14dd9538aa97?w=400'
            }
        ]

       
        jobs_col.delete_many({})
        jobs_col.insert_many(sample_jobs)

        flash(f'Successfully seeded {len(sample_jobs)} jobs!', 'success')
        return redirect(url_for('jobs'))

    return render_template('seed_jobs.html')


@app.route('/admin/applications')
def admin_applications():
    """Admin panel to view and manage applications"""
    
    applications = list(applications_col.find())
    
   
    for app in applications:
        user = users_col.find_one({'_id': app['user_id']})
        app['user_name'] = user['full_name'] if user else 'Unknown'
        app['user_email'] = user['email'] if user else 'Unknown'
    
    return render_template('admin_applications.html', applications=applications)


@app.route('/admin/application/<app_id>/update-status', methods=['POST'])
def update_application_status(app_id):
    """Update application status"""
    from bson.objectid import ObjectId
    
    status = request.form.get('status')
    app_id_obj = ObjectId(app_id)
    
    if status not in ['pending', 'accepted', 'rejected']:
        flash('Invalid status', 'danger')
        return redirect(url_for('admin_applications'))
    
    applications_col.update_one({'_id': app_id_obj}, {'$set': {'status': status}})
    flash(f'Application status updated to {status}', 'success')
    return redirect(url_for('admin_applications'))



@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404


@app.errorhandler(500)
def server_error(error):
    return render_template('500.html'), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
