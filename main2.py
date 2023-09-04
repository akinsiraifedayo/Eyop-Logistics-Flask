@app.route('/register', methods=["POST", "GET"])
def registerz():
    form = RegisterForm()
    if request.method == "POST":
        pwd = form.password.data
        new_user = User(
            email=form.email.data,
            name=form.name.data,
            password= generate_password_hash(password=pwd, method="pbkdf2:sha256", salt_length=8)
        )
        try:
            db.session.add(new_user)
            db.session.commit()
        except IntegrityError:
            flash("Email is registered already, Kindly login instead")
            return redirect(url_for("login"))
        else:
            new_user = db.session.query(User).filter_by(email=form.email.data).first()
            login_user(new_user)
            return redirect(url_for("get_all_posts"))
       
    return render_template("register.html", form=form)


@app.route('/login', methods=["POST", "GET"])
def loginz():
    form = LoginForm()
    print("here")
    if request.method == "POST":
        try:
            user=db.session.query(User).filter_by(email=form.email.data).first()
        except:
            flash("This email does not exist")
            return redirect(url_for("login"))
        else:
            is_match = check_password_hash(user.password, form.password.data)
            if is_match:
                login_user(user)
                return redirect(url_for("get_all_posts"))
            else:
                flash("Incorrect Password")
                return redirect(url_for("login"))
            
    return render_template("login.html", form=form)


@app.route('/logout')
@login_required
def logoutz():
    logout_user()
    return redirect(url_for('get_all_posts'))


@app.route("/post/<int:post_id>", methods=["POST", "GET"])
def show_postz(post_id):
    requested_post = db.session.query(BlogPost).get(post_id)
    comments =  db.session.query(Comment).filter_by(blog_id=post_id)
    form = CommentForm()
    if request.method == "POST":
        if current_user.is_authenticated:
            comment= Comment(
                author=current_user,
                blog=requested_post,
                text=form.comment.data,
            )
            db.session.add(comment)
            db.session.commit()
        else:
            flash("You need to be logged in to post comments")
            return redirect(url_for("login"))
        return redirect(url_for("show_post", post_id=post_id, post=requested_post, form=form, all_comments=comments))
    return render_template("post.html", post=requested_post, form=form, all_comments=comments)


@app.route("/about")
def aboutz():
    return render_template("about.html")


@app.route("/contact")
def contactz():
    return render_template("contact.html")


@app.route("/new-post", methods=["POST", "GET"])
def add_new_postz():
    form = CreatePostForm()
    if form.validate_on_submit():
        new_post = BlogPost(
            title=form.title.data,
            subtitle=form.subtitle.data,
            body=form.body.data,
            img_url=form.img_url.data,
            author=current_user,
            date=date.today().strftime("%B %d, %Y")
        )
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for("get_all_posts"))
    return render_template("make-post.html", form=form)


@app.route("/edit-post/<int:post_id>", methods=["POST", "GET"])
@admins_only
def edit_postz(post_id):
    post = BlogPost.query.get(post_id)
    edit_form = CreatePostForm(
        title=post.title,
        subtitle=post.subtitle,
        img_url=post.img_url,
        # author=post.author,
        body=post.body
    )
    if edit_form.validate_on_submit():
        post.title = edit_form.title.data
        post.subtitle = edit_form.subtitle.data
        post.img_url = edit_form.img_url.data
        # post.author = edit_form.author.data
        post.body = edit_form.body.data
        db.session.commit()
        return redirect(url_for("show_post", post_id=post.id))

    return render_template("make-post.html", form=edit_form)


@app.route("/delete/<int:post_id>")
@admins_only
def delete_postz(post_id):
    post_to_delete = BlogPost.query.get(post_id)
    db.session.delete(post_to_delete)
    db.session.commit()
    return redirect(url_for('get_all_posts'))