from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy.exc import SQLAlchemyError

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///consults.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Consult(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_name = db.Column(db.String(100), nullable=False)
    group = db.Column(db.String(20), nullable=False)
    mentor = db.Column(db.String(100), nullable=False)
    preferred_date = db.Column(db.Date, nullable=False)
    preferred_time = db.Column(db.Time, nullable=False)
    topic = db.Column(db.String(200), nullable=False)
    comments = db.Column(db.Text)
    discord = db.Column(db.String(100), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'student_name': self.student_name,
            'group': self.group,
            'mentor': self.mentor,
            'preferred_date': self.preferred_date.isoformat(),
            'preferred_time': self.preferred_time.isoformat(),
            'topic': self.topic,
            'comments': self.comments,
            'discord': self.discord
        }


@app.route('/add_consult', methods=['POST'])
def add_consult():
    try:
        data = request.json
        new_consult = Consult(
            student_name=data['student_name'],
            group=data['group'],
            mentor=data['mentor'],
            preferred_date=datetime.strptime(data['preferred_date'], '%Y-%m-%d').date(),
            preferred_time=datetime.strptime(data['preferred_time'], '%H:%M').time(),
            topic=data['topic'],
            comments=data['comments'],
            discord=data['discord']
        )
        db.session.add(new_consult)
        db.session.commit()
        return jsonify(new_consult.to_dict()), 201
    except KeyError as e:
        return jsonify({"error": f"Missing required field: {str(e)}"}), 400
    except ValueError as e:
        return jsonify({"error": f"Invalid data format: {str(e)}"}), 400
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": f"Database error: {str(e)}"}), 500
    except Exception as e:
        return jsonify({"error": f"Unexpected error: {str(e)}"}), 500


@app.route('/consults/<int:consult_id>', methods=['GET'])
def get_consult(consult_id):
    consult = Consult.query.get_or_404(consult_id)
    return jsonify(consult.to_dict())


@app.route('/consults', methods=['GET'])
def get_consults():
    consults = Consult.query.all()
    return jsonify([consult.to_dict() for consult in consults])


@app.route('/consults/<int:consult_id>', methods=['PUT'])
def update_consult(consult_id):
    try:
        consult = Consult.query.get_or_404(consult_id)
        data = request.json

        if 'student_name' in data:
            consult.student_name = data['student_name']
        if 'group' in data:
            consult.group = data['group']
        if 'mentor' in data:
            consult.mentor = data['mentor']
        if 'preferred_date' in data:
            consult.preferred_date = datetime.strptime(data['preferred_date'], '%Y-%m-%d').date()
        if 'preferred_time' in data:
            consult.preferred_time = datetime.strptime(data['preferred_time'], '%H:%M').time()
        if 'topic' in data:
            consult.topic = data['topic']
        if 'comments' in data:
            consult.comments = data['comments']
        if 'discord' in data:
            consult.discord = data['discord']

        db.session.commit()
        return jsonify(consult.to_dict()), 200
    except ValueError as e:
        return jsonify({"error": f"Invalid data format: {str(e)}"}), 400
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": f"Database error: {str(e)}"}), 500
    except Exception as e:
        return jsonify({"error": f"Unexpected error: {str(e)}"}), 500


@app.route('/consults/<int:consult_id>', methods=['DELETE'])
def delete_consult(consult_id):
    consult = Consult.query.get_or_404(consult_id)
    db.session.delete(consult)
    db.session.commit()
    return jsonify({'message': f'Заявка с id {consult_id} удалена из базы данных'}), 200


def init_db():
    with app.app_context():
        try:
            db.create_all()
            print("Таблицы успешно созданы.")
        except Exception as e:
            print(f"Ошибка при создании таблиц: {e}")


if __name__ == '__main__':
    init_db()
    app.run(debug=True, port=5001)
