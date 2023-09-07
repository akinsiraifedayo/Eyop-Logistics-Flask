@app.route("/product/<int:product_id>", methods=["product", "GET"])
def show_product(product_id):
    requested_product = db.session.query(Product).get(product_id)
    comments =  db.session.query(Comment).filter_by(blog_id=product_id)
    form = CommentForm()
    product_id=product_id
    if request.method == "product":
        if current_user.is_authenticated:
            comment= Comment(
                author=current_user,
                blog=requested_product,
                text=form.comment.data,
            )
            db.session.add(comment)
            db.session.commit()
        else:
            flash("danger You need to be logged in to product comments")
            return redirect(url_for("login"))
        return redirect(url_for("show_product", product_id=product_id, product=requested_product, form=form, all_comments=comments))
    return render_template("blog-details.html", product_id=product_id, product=requested_product, form=form, all_comments=comments)