from flask import Blueprint, Response, render_template, request, url_for
from flask_login import login_required

from usaon_benefit_tool import db
from usaon_benefit_tool.forms import FORMS_BY_MODEL
from usaon_benefit_tool.models.tables import Link

assessment_links_bp = Blueprint('links', __name__, url_prefix='/links')
Form = FORMS_BY_MODEL[Link]


@assessment_links_bp.route('', methods=['POST'])
@login_required
def post(assessment_id: str):
    """Add an entry to the assessment's link collection."""
    assessment_link = Link()
    form = Form(request.form, obj=assessment_link)

    if form.validate():
        form.populate_obj(assessment_link)
        db.session.add(assessment_link)
        db.session.commit()

    return Response(
        status=201,
        headers={
            'HX-Redirect': url_for(
                'assessment.view_assessment_overview',
                assessment_id=assessment_id,
            ),
        },
    )


@assessment_links_bp.route('/form', methods=['GET'])
@login_required
def form(assessment_id: str):
    """Return a form to add an entry to the assessment's link collection."""
    assessment_link = Link()
    form = Form(obj=assessment_link)
    form_attrs = (
        f"hx-post={url_for('assessment.links.post', assessment_id=assessment_id)}"
    )

    return render_template(
        'partials/modal_form.html',
        title="Add a link",
        form_attrs=form_attrs,
        form=form,
    )
