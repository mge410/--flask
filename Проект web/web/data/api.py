import flask
from flask import jsonify, request
from . import db_session
from .attribute import Attribute
from . personage import Person


blueprint = flask.Blueprint(
    'personage_api',
    __name__,
    template_folder='templates'
)


@blueprint.route('/api/person_base_info/<int:pers_id>', methods=['GET'])
def get_one_pers(pers_id):
    db_sess = db_session.create_session()
    pers = db_sess.query(Person).get(pers_id)
    if not pers:
        return jsonify({'error': 'Not found'})
    return jsonify(
        {
            'pers': pers.to_dict(only=(
                'name', 'content'))
        }
    )


@blueprint.route('/api/person_pro_info/<int:pers_id>', methods=['GET'])
def get_one_pers_pro(pers_id):
    db_sess = db_session.create_session()
    pers = db_sess.query(Person).get(pers_id)
    if not pers:
        return jsonify({'error': 'Not found'})
    return jsonify(
        {
            'pers': pers.to_dict(only=(
                'name', 'content', 'like', 'img', 'is_private', 'user_id'))
        }
    )


@blueprint.route('/api/atribut_base_info/<int:atribut_id>', methods=['GET'])
def get_one_atribut(atribut_id):
    db_sess = db_session.create_session()
    atribut = db_sess.query(Attribute).get(atribut_id)
    if not atribut:
        return jsonify({'error': 'Not found'})
    return jsonify(
        {
            'atribut': atribut.to_dict(only=(
                'name', 'description'))
        }
    )


@blueprint.route('/api/atribut_pro_info/<int:atribut_id>', methods=['GET'])
def get_one_atribut_pro(atribut_id):
    db_sess = db_session.create_session()
    atribut = db_sess.query(Attribute).get(atribut_id)
    if not atribut:
        return jsonify({'error': 'Not found'})
    return jsonify(
        {
            'atribut': atribut.to_dict(only=(
                'id', 'name', 'description', 'img'))
        }
    )


@blueprint.route('/api/atribut_add', methods=['POST'])
def create_news():
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not all(key in request.json for key in
                 ['img', 'description', 'name']):
        return jsonify({'error': 'Bad request'})
    db_sess = db_session.create_session()
    atrib = Attribute(
        img=request.json['img'],
        description=request.json['description'],
        name=request.json['name'],
    )
    db_sess.add(atrib)
    db_sess.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/atribut_del/<int:id>', methods=['DELETE'])
def delete_news(id):
    db_sess = db_session.create_session()
    atribyte = db_sess.query(Attribute).get(id)
    if not atribyte:
        return jsonify({'error': 'Not found'})
    db_sess.delete(atribyte)
    db_sess.commit()
    return jsonify({'success': 'OK'})