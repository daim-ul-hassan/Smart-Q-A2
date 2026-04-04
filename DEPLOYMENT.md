# 🚀 Deploy to Streamlit Cloud - Complete Guide

This guide will help you deploy your Smart Book Q&A Crew app to Streamlit Cloud for free!

## 📋 Prerequisites

1. ✅ GitHub account (you already have your code on GitHub)
2. ✅ Google Gemini API key (from https://aistudio.google.com/apikey)
3. ✅ Streamlit Cloud account (free - sign up with GitHub)

---

## 🎯 Step-by-Step Deployment

### Step 1: Push Latest Changes to GitHub

Your code is already updated for Streamlit Cloud compatibility. Just push the changes:

```bash
git add .
git commit -m "Add Streamlit Cloud deployment support"
git push origin main
```

### Step 2: Sign Up for Streamlit Cloud

1. Go to: **https://streamlit.io/cloud**
2. Click **"Sign up"** or **"Sign in"**
3. Use your **GitHub account** to authenticate
4. You'll be redirected to your Streamlit Cloud dashboard

### Step 3: Create a New App

1. Click **"New app"** button
2. Fill in the details:
   - **Repository**: `daim-ul-hassan/Smart-Q-A2`
   - **Branch**: `main`
   - **Main file path**: `app.py`
3. Click **"Advanced settings"** (important!)

### Step 4: Configure Secrets (API Key)

In the **Advanced settings** section, find **"Secrets"** and add:

```toml
[google]
api_key = "YOUR_ACTUAL_GOOGLE_API_KEY_HERE"
```

Replace `YOUR_ACTUAL_GOOGLE_API_KEY_HERE` with your real Google Gemini API key.

**Get your API key:**
- Go to: https://aistudio.google.com/apikey
- Sign in with Google
- Click "Create API Key"
- Copy the key

### Step 5: Deploy!

1. Click **"Deploy!"** button
2. Wait 2-5 minutes for the build to complete
3. Your app will be live at: `https://your-app-name.streamlit.app`

---

## ⚙️ Configuration Details

### What Changed for Streamlit Cloud?

✅ **Updated app.py** - Now supports both local (.env) and cloud (secrets.toml) configurations  
✅ **Added secrets template** - `.streamlit/secrets.toml.example` shows the format  
✅ **Updated .gitignore** - Prevents accidental secret commits  
✅ **requirements.txt** - Already includes all dependencies  

### How It Works

The app automatically detects where it's running:
- **Local**: Uses `.env` file for API key
- **Streamlit Cloud**: Uses Secrets configuration

No code changes needed when switching between environments!

---

## 🔧 Managing Your Deployment

### Update Your App

After making changes locally:

```bash
git add .
git commit -m "Your update message"
git push origin main
```

Streamlit Cloud will **automatically redeploy** within 1-2 minutes!

### View Logs

1. Go to your app on Streamlit Cloud
2. Click **"Manage app"** → **"Logs"**
3. See real-time logs for debugging

### Update API Key

1. Go to your app on Streamlit Cloud
2. Click **"Manage app"** → **"Settings"** → **"Secrets"**
3. Update the API key
4. Click **"Save"**
5. The app will restart automatically

---

## ❗ Important Notes

### ⚠️ Persistent Storage Limitation

**Streamlit Cloud doesn't provide persistent storage!** This means:

❌ Uploaded documents will be deleted after each session  
❌ Vector store (chroma_db/) won't persist between sessions  

**Solutions:**

**Option 1: Pre-build the vector store locally**
```bash
# Build vector store on your computer
python rag_setup.py

# Commit chroma_db to Git (if small enough)
git add chroma_db/
git commit -m "Add pre-built vector store"
git push
```

**Option 2: Use cloud storage** (advanced)
- Store documents in Google Drive, Dropbox, or AWS S3
- Modify app.py to download documents on startup
- Build vector store dynamically

**Option 3: Hybrid approach** (recommended for now)
- Keep the app on Streamlit Cloud for demo/testing
- Run locally with full features for production use

### 💰 Cost

✅ **Streamlit Cloud is FREE** for public apps  
✅ Includes:
  - Unlimited apps
  - Automatic deployments
  - Custom domains (optional)
  - SSL certificates

---

## 🐛 Troubleshooting

### Problem: "Module not found" errors
**Solution:** Make sure all dependencies are in `requirements.txt`

### Problem: "API key not configured"
**Solution:** Check your Secrets configuration in Streamlit Cloud dashboard

### Problem: App won't start
**Solution:** 
1. Check logs in Streamlit Cloud dashboard
2. Make sure `app.py` is the correct main file
3. Verify all imports work

### Problem: Documents disappear
**Solution:** This is expected on Streamlit Cloud. Use one of the persistence solutions above.

---

## 🎓 Alternative: Deploy Locally

If you want full control and persistent storage:

### Option 1: Run on Your Computer
```bash
streamlit run app.py
```
Access at: http://localhost:8501

### Option 2: Deploy to Your Own Server
- Use Docker
- Deploy to AWS, Azure, or DigitalOcean
- Full control over storage and resources

---

## 📊 What You Get with Streamlit Cloud

✅ Public URL accessible from anywhere  
✅ Automatic HTTPS/SSL  
✅ Auto-scaling  
✅ Zero server management  
✅ Easy updates via Git  
✅ Free tier available  

---

## 🚀 Quick Deploy Checklist

- [ ] Code pushed to GitHub
- [ ] Streamlit Cloud account created
- [ ] New app created pointing to your repo
- [ ] API key added to Secrets
- [ ] App deployed successfully
- [ ] Tested the deployed app

---

## 💡 Pro Tips

1. **Test locally first** - Make sure everything works before deploying
2. **Keep requirements minimal** - Faster deployment times
3. **Use caching** - Streamlit's `@st.cache_data` for better performance
4. **Monitor usage** - Check your Streamlit Cloud dashboard
5. **Custom domain** - Available in paid plans

---

## 🆘 Need Help?

- **Streamlit Docs**: https://docs.streamlit.io/streamlit-cloud
- **Community Forum**: https://discuss.streamlit.io/
- **GitHub Issues**: https://github.com/streamlit/streamlit/issues

---

**Ready to deploy?** Follow the steps above and your app will be live in minutes! 🎉
