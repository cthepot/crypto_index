from flask import render_template, flash, redirect, url_for, request, g
from app import app, db
from flask_login import current_user, login_user, login_required, logout_user
from app.models import Asset, Quote, User, Index, IndexAsset
from app.forms import LoginForm, RegistrationForm, ResetPasswordRequestForm, ResetPasswordForm, CreateIndexForm, \
    CreateIndexAssetForm
from app.email import send_password_reset_email
from sqlalchemy import func, and_
from app.quote import QuoteThread
from app.queries import latest_quotes
from datetime import datetime


@app.before_first_request
def quote_thread():
    quote_thread = QuoteThread()
    quote_thread.daemon = True
    quote_thread.name = "Quote Thread"
    quote_thread.start()


@app.route('/')
@app.route('/index', methods=["GET", "POST"])
def index():
    page = request.args.get("page", 1, type=int)
    assets = Asset.query.join(Quote, (Quote.assetname == Asset.assetname)) \
        .with_entities(Asset.assetname, Asset.rank, Asset.slug,
                       Quote.price_usd, Quote.last_updated, Quote.market_cap_usd, Quote.volume_24h_usd,
                       Quote.percent_change_24h_usd) \
        .order_by(Asset.rank.asc()) \
        .group_by(Asset.assetname, Asset.rank, Asset.slug,
                  Quote.price_usd, Quote.last_updated, Quote.market_cap_usd, Quote.volume_24h_usd,
                  Quote.percent_change_24h_usd) \
        .paginate(page, app.config["ASSETS_PER_PAGE"], False)
    index = Index.query.all()
    next_url = url_for('index', page=assets.next_num) \
            if assets.has_next else None
    prev_url = url_for('index', page=assets.prev_num) \
            if assets.has_prev else None
    return render_template("index.html", title="Home", assets=assets.items, index=index, next_url=next_url,
                           prev_url=prev_url)


@app.route('/quotes', methods=["GET", "POST"])
def quotes():
    page = request.args.get("page", 1, type=int)
    quotes = latest_quotes.paginate(page, app.config["ASSETS_PER_PAGE"], False)
    quotes_count = Quote.query.count()
    next_url = url_for('quotes', page=quotes.next_num) \
        if quotes.has_next else None
    prev_url = url_for('quotes', page=quotes.prev_num) \
        if quotes.has_prev else None
    return render_template("quotes.html", title="Home", next_url=next_url, prev_url=prev_url,
                           quotes_count=quotes_count, quotes=quotes.items)


@app.route('/assets/<slug>')
@login_required
def assets(slug):
    slug = Asset.query.filter_by(slug=slug).first_or_404()
    quote = Quote.query.filter_by(assetname=slug.assetname).first()
    return render_template("assets.html", slug=slug, quote=quote)


@app.route('/baskets', methods=["GET", "POST"])
@login_required
def builder():
    assets = Asset.query.all()  # query those who have a quote
    index_all = Index.query.filter_by(user_id=current_user.id).all()
    form = CreateIndexForm()
    if form.validate_on_submit():
        index = Index(name=form.name.data, user_id=current_user.id, amount=form.amount.data)
        db.session.add(index)
        db.session.commit()
        flash("Your index is now live!")
        return redirect(url_for('builder'))
    return render_template("basket_index.html", title="Cryptocurrency Index Builder", assets=assets,
                           index_all=index_all, form=form)


@app.route('/baskets/<index_id>', methods=["GET", "POST"])
@login_required
def basket(index_id):
    index_id = Index.query.filter_by(id=index_id).first_or_404()
    page = request.args.get("page", 1, type=int)
    assoc_count = IndexAsset.query.filter_by(index_id=index_id.id).count()
    index_asset = IndexAsset.query.filter_by(index_id=index_id.id).subquery()
    sq = latest_quotes.subquery()
    test = db.session.query(index_asset.c.asset_id, index_asset.c.allocation, sq)\
        .join(sq, (sq.c.id_cmc == index_asset.c.asset_id))\
        .paginate(page, app.config["ASSETS_PER_PAGE"], False)
    form = CreateIndexAssetForm()
    form.asset_id.choices = [(g.id_cmc, g.assetname) for g in latest_quotes.all()]
    if form.validate_on_submit():
        index_asset = IndexAsset(asset_id=form.asset_id.data, index_id=index_id.id, allocation=form.allocation.data)
        db.session.add(index_asset)
        db.session.commit()
        flash("You've added an asset to your basket!")
        # check url_for documentation and change builder to basket
        return redirect(url_for('builder'))
    return render_template("basket_single.html", title="Basket builder", index_id=index_id, form=form,
                             test=test.items, assoc_count=assoc_count)



@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash("Invalid username or password")
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('index'))
    return render_template('login.html', title="Sign in", form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_password_reset_email(user)
        flash('Check your email for the instructions to reset your password')
        return redirect(url_for('login'))
    return render_template('reset_password_request.html',
                           title='Reset Password', form=form)


@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    user = User.verify_reset_password_token(token)
    if not user:
        return redirect(url_for('index'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash('Your password has been reset.')
        return redirect(url_for('login'))
    return render_template('reset_password.html', form=form)
