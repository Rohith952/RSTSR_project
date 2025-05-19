from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/instagram', methods=['GET', 'POST'])
def instagram():
    result = ""
    if request.method == 'POST':
        username = request.form['username']
        followers = int(request.form['followers'])
        posts = int(request.form['posts'])
        likes = int(request.form['likes'])
        bio = request.form['bio'].strip()

        is_fake = False
        reasons = []

        if posts == 0 and likes > 0:
            is_fake = True
            reasons.append("has likes but no posts")

        real_score = 0
        if followers >= 100:
            real_score += 1
        if posts > 3:
            real_score += 1
        if likes > 20 and posts > 0:
            real_score += 1
        if bio:
            real_score += 1

        if is_fake:
            result = f"🚨 Profile '{username}' is likely FAKE — {', '.join(reasons)}."
        elif real_score >= 2:
            result = f"✅ Profile '{username}' seems REAL."
        else:
            result = f"⚠️ Profile '{username}' is low-activity or suspicious."

    return render_template('instagram.html', result=result)

@app.route('/facebook', methods=['GET', 'POST'])
def facebook():
    result = ""
    if request.method == 'POST':
        username = request.form['username']
        try:
            friends = int(request.form['friends'])
            posts = int(request.form['posts'])
            likes = int(request.form['likes'])
        except ValueError:
            result = "⚠️ Please enter valid numeric values for friends, posts, and likes."
            return render_template('facebook.html', result=result)

        bio = request.form['bio'].strip()
        is_fake = False
        reasons = []
        engagement_ratio = likes / posts if posts > 0 else 0

        if friends < 20:
            is_fake = True
            reasons.append("very few friends")
        if posts == 0 and likes > 0:
            is_fake = True
            reasons.append("has likes but no posts")
        if posts > 0 and engagement_ratio < 1:
            is_fake = True
            reasons.append("low engagement ratio")
        if not bio:
            is_fake = True
            reasons.append("no bio provided")

        real_score = 0
        if friends >= 100:
            real_score += 1
        if posts >= 5:
            real_score += 1
        if engagement_ratio >= 2:
            real_score += 1
        if bio:
            real_score += 1

        if is_fake or real_score <= 1:
            result = f"🚨 Facebook profile '{username}' is likely FAKE — {', '.join(reasons)}."
        elif real_score >= 3:
            result = f"✅ Facebook profile '{username}' seems REAL and active."
        else:
            result = f"⚠️ Facebook profile '{username}' shows low activity or suspicious patterns."

    return render_template('facebook.html', result=result)

# ------------------ ✅ Twitter Route ------------------
@app.route('/twitter', methods=['GET', 'POST'])
def twitter():
    result = ""
    if request.method == 'POST':
        username = request.form['username']
        try:
            followers = int(request.form['followers'])
            tweets = int(request.form['tweets'])
            likes = int(request.form['likes'])
        except ValueError:
            result = "⚠️ Please enter valid numeric values for followers, tweets, and likes."
            return render_template('twitter.html', result=result)

        bio = request.form['bio'].strip()

        is_fake = False
        reasons = []

        engagement_ratio = likes / tweets if tweets > 0 else 0

        if followers < 10:
            is_fake = True
            reasons.append("very few followers")
        if tweets == 0 and likes > 0:
            is_fake = True
            reasons.append("has likes but no tweets")
        if tweets > 0 and engagement_ratio < 1:
            is_fake = True
            reasons.append("low engagement ratio")
        if not bio:
            is_fake = True
            reasons.append("no bio provided")

        real_score = 0
        if followers >= 10:
            real_score += 1
        if tweets >= 2:
            real_score += 1
        if engagement_ratio >= 2:
            real_score += 1
        if bio:
            real_score += 1

        if is_fake or real_score <= 1:
            result = f"🚨 Twitter profile '{username}' is likely FAKE — {', '.join(reasons)}."
        elif real_score >= 3:
            result = f"✅ Twitter profile '{username}' seems REAL and active."
        else:
            result = f"⚠️ Twitter profile '{username}' shows low activity or suspicious patterns."

    return render_template('twitter.html', result=result)

if __name__ == '__main__':
    app.run(debug=True)
