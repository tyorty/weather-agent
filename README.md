[README.txt](https://github.com/user-attachments/files/25840205/README.txt)
DEPLOY TO RENDER.COM - 5 STEPS
================================

1. CREATE GITHUB REPO
   - Go to github.com and sign in (free account)
   - Click New Repository, name it "weather-agent", click Create
   - Upload all 3 files: app.py, requirements.txt, static/index.html

2. SIGN UP AT RENDER.COM
   - Go to render.com, sign up free with your GitHub account

3. CREATE WEB SERVICE
   - Click New > Web Service
   - Connect your weather-agent GitHub repo
   - Settings:
       Name:         weather-agent
       Runtime:      Python 3
       Build Command: pip install -r requirements.txt
       Start Command: gunicorn app:app

4. ADD YOUR ANTHROPIC API KEY
   - In Render dashboard, go to Environment
   - Add variable:  ANTHROPIC_API_KEY = (your key from console.anthropic.com)

5. DEPLOY
   - Click Deploy. Wait ~2 minutes.
   - Render gives you a URL like: https://weather-agent-xxxx.onrender.com
   - Open that URL on ANY phone or browser - it works!

COST: Free (Render free tier, Open-Meteo is free, Anthropic charges fractions of a cent per query)
