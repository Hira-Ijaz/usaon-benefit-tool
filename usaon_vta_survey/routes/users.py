from flask import render_template

from usaon_vta_survey.models.tables import User
from usaon_vta_survey.routes.root import root_blueprint


@root_blueprint.route('/users')
def view_users():
    users = User.query.order_by(User.name).all()
    return render_template(
        'users.html',
        users=users,
    )
