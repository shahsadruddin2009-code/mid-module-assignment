# 🐍 PythonAnywhere Deployment Guide

## 🚀 Deploy Online Bookstore Flask App to PythonAnywhere

### 📋 **Your New URLs**
- **🟢 Production:** `https://shahsadruddin2009.pythonanywhere.com`
- **🟡 Staging:** `https://staging-bookstore.pythonanywhere.com`

## 🔧 **Setup Instructions**

### 1️⃣ **Create PythonAnywhere Account**
1. Go to [PythonAnywhere](https://www.pythonanywhere.com)
2. Sign up with username: `shahsadruddin2009`
3. Choose the free "Beginner" account to start

### 2️⃣ **Upload Your Code**
#### **Option A: Git Clone (Recommended)**
```bash
# Open a Bash console on PythonAnywhere
cd ~
git clone https://github.com/shahsadruddin2009-code/mid-module-assignment.git
cd mid-module-assignment/online-bookstore-flask
```

#### **Option B: File Upload**
1. Use the "Files" tab in PythonAnywhere dashboard
2. Upload your project files to `/home/shahsadruddin2009/`

### 3️⃣ **Install Dependencies**
```bash
# In PythonAnywhere Bash console
cd ~/mid-module-assignment/online-bookstore-flask
pip3.10 install --user -r requirements.txt
```

### 4️⃣ **Configure Web App**
1. Go to **"Web"** tab in PythonAnywhere dashboard
2. Click **"Add a new web app"**
3. Choose **"Manual configuration"**
4. Select **"Python 3.10"**
5. Click **"Next"**

### 5️⃣ **Web App Configuration**

#### **WSGI Configuration File**
Edit `/var/www/shahsadruddin2009_pythonanywhere_com_wsgi.py`:

```python
import sys
import os

# Add your project directory to Python path
project_home = '/home/shahsadruddin2009/mid-module-assignment/online-bookstore-flask'
if project_home not in sys.path:
    sys.path.insert(0, project_home)

# Set environment variables
os.environ['FLASK_APP'] = 'app.py'
os.environ['FLASK_ENV'] = 'production'

# Import your Flask app
from app import app as application

if __name__ == "__main__":
    application.run()
```

#### **Static Files Configuration**
- **URL:** `/static/`
- **Directory:** `/home/shahsadruddin2009/mid-module-assignment/online-bookstore-flask/static/`

#### **Source Code Directory**
- **Directory:** `/home/shahsadruddin2009/mid-module-assignment/online-bookstore-flask/`

### 6️⃣ **Environment Variables** (Optional)
Create `.env` file in your project directory:
```bash
FLASK_ENV=production
SECRET_KEY=your-secret-key-here
DEBUG=False
```

### 7️⃣ **Database Setup** (If using SQLite)
```bash
# In PythonAnywhere console
cd ~/mid-module-assignment/online-bookstore-flask
python3.10 -c "from app import app; app.app_context().push(); from models import *; # Initialize DB if needed"
```

## 🔄 **Deployment Process**

### **For Updates:**
1. **Pull latest changes:**
   ```bash
   cd ~/mid-module-assignment/online-bookstore-flask
   git pull origin main
   ```

2. **Reload web app:**
   - Go to PythonAnywhere Web tab
   - Click **"Reload"** button

### **For New Dependencies:**
```bash
pip3.10 install --user -r requirements.txt
```

## 🎯 **Quick Commands for PythonAnywhere**

### **Check Logs:**
- Go to **"Web"** tab → **"Log files"**
- Check **Error log** and **Access log**

### **Restart App:**
- **"Web"** tab → **"Reload"** button

### **Open Console:**
- **"Consoles"** tab → **"Bash"** or **"Python"**

## 📊 **Monitoring & Health Checks**

Your health endpoints will be available at:
- `https://shahsadruddin2009.pythonanywhere.com/health`
- `https://shahsadruddin2009.pythonanywhere.com/metrics`

## 🔒 **Security Notes**

1. **Debug Mode:** Ensure `debug=False` in production
2. **Secret Key:** Use environment variables for sensitive data
3. **HTTPS:** PythonAnywhere provides HTTPS by default
4. **Domain:** Free accounts get `username.pythonanywhere.com`

## 📈 **Scaling Options**

### **Free Account Limits:**
- 1 web app
- 512MB storage
- Limited CPU seconds per day

### **Paid Plans:**
- **Hacker ($5/month):** More CPU, custom domains
- **Web Developer ($12/month):** Multiple web apps, more storage

## 🛠️ **Troubleshooting**

### **Common Issues:**
1. **Import Errors:** Check Python path in WSGI file
2. **Static Files Not Loading:** Verify static files configuration
3. **App Not Starting:** Check error logs in Web tab

### **Debug Commands:**
```bash
# Check Python version
python3.10 --version

# Test app locally
python3.10 app.py

# Check installed packages
pip3.10 list --user
```

## 🚀 **Benefits of PythonAnywhere**

✅ **Free tier available**
✅ **Python-focused hosting**
✅ **Built-in code editor**
✅ **Easy database management**
✅ **Scheduled tasks support**
✅ **SSH access**
✅ **No credit card required for free tier**

---

## 🎉 **You're Ready!**

Your Flask app will be live at:
**`https://shahsadruddin2009.pythonanywhere.com`**

Need help? Check PythonAnywhere's excellent [help documentation](https://help.pythonanywhere.com/) or their community forums!