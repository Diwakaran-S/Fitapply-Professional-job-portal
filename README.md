# FitApply - Professional Job Application Platform

A modern, feature-rich job application platform built with Flask, MongoDB, and professional UI/UX design.

## 🌟 Features

✅ **User Authentication**
- Secure signup and login system
- Password hashing with werkzeug
- Session management
- User profile management

✅ **Job Management**
- Browse 18+ different job categories
- Advanced search and filtering
- Job detail pages with requirements
- One-click job applications

✅ **User Dashboard**
- Track all applications in one place
- Real-time application status updates
- Application statistics (pending, accepted, rejected)
- Quick action buttons

✅ **Professional Design**
- Modern, clean UI with animations
- Responsive design (mobile, tablet, desktop)
- Smooth transitions and hover effects
- Professional color scheme and typography

✅ **Additional Pages**
- Home page with stats and features
- About us page
- Help & FAQ section
- User profile management
- Professional footer with links

## 📋 Job Categories (18+ Types)

1. **Backend Development** - Python, Node.js, Java
2. **Frontend Development** - React, Vue, TypeScript
3. **Full Stack Development** - MERN stack, MEAN stack
4. **DevOps** - Kubernetes, Docker, CI/CD
5. **Data Science** - ML, Data Analysis, SQL
6. **Mobile Development** - iOS, Android, React Native
7. **UX/UI Design** - Figma, Design Systems
8. **QA/Testing** - Selenium, Test Automation
9. **Database Administration** - PostgreSQL, MongoDB
10. **Cloud Architecture** - AWS, Azure, GCP
11. **Cybersecurity** - Security, Penetration Testing
12. **Machine Learning** - Deep Learning, AI
13. **Technical Project Management** - Agile, Leadership
14. **Solutions Architecture** - System Design
15. **API Development** - REST, GraphQL
16. **Frontend Leadership** - React, Web Performance
17. **Backend Architecture** - Microservices, System Design

## 🗄️ Database Schema

### MongoDB Collections

#### Users Collection
```javascript
{
  _id: ObjectId,
  full_name: String,
  email: String (unique),
  password: String (hashed),
  phone: String,
  location: String,
  bio: String,
  profile_image: String,
  created_at: DateTime
}
```

#### Jobs Collection
```javascript
{
  _id: ObjectId,
  title: String,
  company: String,
  category: String,
  location: String,
  salary: String,
  description: String,
  requirements: [String],
  image: String,
  posted_at: DateTime
}
```

#### Applications Collection
```javascript
{
  _id: ObjectId,
  user_id: ObjectId (ref: Users),
  job_id: ObjectId (ref: Jobs),
  job_title: String,
  company: String,
  cover_letter: String,
  applied_at: DateTime,
  status: String (pending/accepted/rejected)
}
```

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- MongoDB installed and running locally
- pip (Python package manager)

### Installation

1. **Clone or navigate to the project directory**
```bash
cd "d:\Internships\Cognifyz (Full Stack)\Task 6"
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Start MongoDB**
```bash
# Windows
mongod

# macOS/Linux
brew services start mongodb-community
```

4. **Run the Flask application**
```bash
python app.py
```

5. **Access the application**
Open your browser and navigate to:
```
http://localhost:5000
```

## 📝 First Time Setup

1. **Visit the seed jobs page** (demo admin feature)
   - Navigate to: `http://localhost:5000/admin/seed-jobs`
   - Click "Seed Jobs" to populate 18 sample jobs into the database
   - This creates realistic job listings for testing

2. **Create a test account**
   - Click "Sign Up" on the home page
   - Fill in your details
   - You'll be redirected to login

3. **Browse and apply for jobs**
   - Visit the "Jobs" page
   - Search by title, company, or filter by category
   - Click "View Details" on any job
   - Submit an application

4. **Check your dashboard**
   - View all your applications in one place
   - Track application status (pending, accepted, rejected)
   - See application statistics

## 🏗️ Project Structure

```
Task 6/
├── app.py                  # Main Flask application
├── requirements.txt        # Python dependencies
├── static/
│   └── style.css          # Professional styling with animations
└── templates/
    ├── base.html          # Base template with navbar & footer
    ├── index.html         # Home page
    ├── signup.html        # User registration
    ├── login.html         # User login
    ├── jobs.html          # Jobs listing page
    ├── job_detail.html    # Job detail & apply page
    ├── dashboard.html     # User dashboard
    ├── profile.html       # User profile management
    ├── about.html         # About us page
    ├── help.html          # Help & FAQ
    ├── seed_jobs.html     # Admin seed jobs page
    ├── 404.html           # Page not found
    └── 500.html           # Server error
```

## 🎨 Design Features

### Animations & Interactions
- ✨ Fade-in animations on page load
- 🎯 Slide-in animations for sidebar content
- 🔄 Smooth hover effects on buttons and cards
- 📊 Bouncing animations on hero images
- 💫 Pulse effects on loading states

### Responsive Design
- 📱 Mobile-first approach
- 💻 Optimized for tablets
- 🖥️ Full desktop support
- ⚡ Fast loading times

### Color Scheme
- **Primary**: Cyan (#06b6d4)
- **Secondary**: Purple (#8b5cf6)
- **Success**: Green (#10b981)
- **Danger**: Red (#ef4444)
- **Warning**: Amber (#f59e0b)
- **Dark**: Slate (#1f2937)

## 🔐 Security Features

✅ Password hashing with werkzeug
✅ Session-based authentication
✅ SQL injection prevention (MongoDB parameterized queries)
✅ CSRF protection ready (add CSRF token in forms)
✅ Secure password requirements (min 6 characters)
✅ Email validation

## 📚 User Flows

### Sign Up Flow
1. User clicks "Sign Up"
2. Fills registration form
3. System validates data
4. Password is hashed
5. User account is created
6. User is redirected to login

### Job Application Flow
1. User logs in
2. Browses jobs (with search & filters)
3. Clicks "View Details" on a job
4. Adds optional cover letter
5. Clicks "Submit Application"
6. Application is saved to database
7. User sees confirmation message
8. Application appears in dashboard

### Dashboard Flow
1. User logs in
2. Visits dashboard
3. Sees application statistics
4. Views all applications with status
5. Can browse more jobs
6. Can update profile

## 🛠️ API Endpoints

| Route | Method | Description |
|-------|--------|-------------|
| `/` | GET | Home page |
| `/signup` | GET, POST | User registration |
| `/login` | GET, POST | User login |
| `/logout` | GET | User logout |
| `/jobs` | GET | Browse jobs (with filters) |
| `/job/<job_id>` | GET | Job detail page |
| `/job/<job_id>/apply` | POST | Submit job application |
| `/dashboard` | GET | User dashboard |
| `/profile` | GET | User profile page |
| `/profile/update` | POST | Update user profile |
| `/about` | GET | About page |
| `/help` | GET | Help & FAQ |
| `/admin/seed-jobs` | GET, POST | Seed sample jobs (demo) |

## 💡 Usage Tips

1. **Test Different Scenarios**
   - Create multiple accounts
   - Apply to various jobs
   - Check application status in dashboard

2. **Explore All Pages**
   - Home page with statistics
   - Job browsing with filters
   - Dashboard for tracking
   - Profile management
   - Help section with FAQs

3. **Use the Seed Function**
   - Visit `/admin/seed-jobs` to populate sample jobs
   - Provides 18 realistic job listings
   - Perfect for testing all features

## 🚀 Next Steps & Enhancements

Potential features to add:
- Email notifications for application updates
- User profile image uploads
- Job recommendations based on skills
- Company profiles and reviews
- Advanced filtering (salary range, experience level)
- Export applications as PDF
- Admin panel for job management
- Payment integration for employers
- Real-time notifications
- Application messaging system

## 🐛 Troubleshooting

### MongoDB Connection Error
```
✗ MongoDB connection failed
```
**Solution**: Ensure MongoDB is running. Start with `mongod`

### Port Already in Use
```
Address already in use: ('0.0.0.0', 5000)
```
**Solution**: Change port in `app.py` or kill the process using port 5000

### Template Not Found
```
TemplateNotFound: login.html
```
**Solution**: Ensure all HTML files are in the `templates/` directory

### Database Issues
- Clear browser cache
- Restart MongoDB
- Re-seed the jobs database

## 📞 Support

For issues or questions:
1. Check the Help page at `/help`
2. Review the FAQ section
3. Check error messages in console
4. Ensure all dependencies are installed

## 📄 License

This project is built for educational purposes as part of the Cognifyz Full Stack Internship.

## 👨‍💻 Built With

- **Backend**: Flask (Python)
- **Database**: MongoDB
- **Frontend**: HTML5, CSS3, Vanilla JavaScript
- **Security**: werkzeug
- **Package Manager**: pip

---

**Version**: 1.0.0  
**Last Updated**: November 2025  
**Status**: Production Ready ✅
