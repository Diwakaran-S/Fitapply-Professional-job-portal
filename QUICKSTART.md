# FitApply - Quick Start Guide

## 🚀 Quick Setup (5 minutes)

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Start MongoDB
```bash
# Windows
mongod

# macOS
brew services start mongodb-community

# Linux
sudo systemctl start mongod
```

### Step 3: Run Application
```bash
python app.py
```

### Step 4: Open Browser
```
http://localhost:5000
```

---

## 📋 First Time User Guide

### Create Test Account
1. Click **Sign Up** button
2. Enter your details:
   - Full Name: John Doe
   - Email: john@example.com
   - Phone: +1 (555) 000-0000
   - Location: New York, NY
   - Password: password123

### Populate Sample Jobs
1. Navigate to: `http://localhost:5000/admin/seed-jobs`
2. Click **Seed Jobs** button
3. This loads 18 realistic job listings

### Browse & Apply for Jobs
1. Go to **Jobs** page
2. Use search bar or category filters
3. Click **View Details** on any job
4. Add optional cover letter
5. Click **Submit Application**

### Track Applications
1. Click **Dashboard** in navbar
2. View all your applications
3. See status: Pending, Accepted, or Rejected
4. Check statistics at the top

### Update Profile
1. Click **Profile** in navbar
2. Edit your information
3. Add a bio
4. Click **Save Changes**

---

## 🎯 Demo Credentials (Optional)

After creating your account above, you can log in with:
```
Email: john@example.com
Password: password123
```

---

## 📱 Website Navigation

### Public Pages (No Login Required)
- 🏠 **Home** - Features and statistics
- 💼 **Jobs** - Browse all jobs
- ℹ️ **About** - About FitApply
- ❓ **Help** - FAQ and support

### Private Pages (Login Required)
- 📊 **Dashboard** - Track applications
- 👤 **Profile** - Manage profile info
- 💼 **Jobs** - Full access to apply

---

## 🎨 Key Features

✨ **Modern Design**
- Clean, professional interface
- Smooth animations
- Responsive on all devices
- Dark navbar with colorful accents

🔐 **Secure**
- Encrypted passwords
- Session-based login
- Secure application management
- User data protection

📊 **Comprehensive**
- 18+ job categories
- Advanced search & filters
- Real-time application tracking
- Professional dashboard

💼 **User-Friendly**
- Intuitive navigation
- One-click applications
- Clear status updates
- Helpful FAQ section

---

## ❓ Troubleshooting

### "Cannot connect to MongoDB"
- Make sure MongoDB is running (`mongod` command)
- Check MongoDB is installed
- Restart MongoDB if needed

### "Port 5000 already in use"
- Change port in `app.py`: `app.run(port=5001)`
- Or kill process using port 5000

### "No jobs showing up"
- Visit `/admin/seed-jobs` to load sample jobs
- Check if database connection is working

### "Cannot apply for job"
- Make sure you're logged in
- Try refreshing the page
- Clear browser cache if needed

---

## 📞 Need Help?

1. Visit the **Help** page for FAQ
2. Check **About** page for more info
3. Review **README.md** for detailed documentation

---

## 🎓 Learning Resources

### Python & Flask
- Flask Documentation: https://flask.palletsprojects.com/
- Python Security: https://owasp.org/

### MongoDB
- MongoDB Docs: https://docs.mongodb.com/
- PyMongo Guide: https://pymongo.readthedocs.io/

### Web Design
- MDN Web Docs: https://developer.mozilla.org/
- CSS Animations: https://developer.mozilla.org/en-US/docs/Web/CSS/animation

---

## 🎉 You're All Set!

Enjoy exploring FitApply! Start by:
1. Creating an account
2. Seeding sample jobs
3. Browsing and applying for positions
4. Tracking your applications in the dashboard

Happy job hunting! 🚀
