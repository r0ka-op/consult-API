from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from sqlalchemy.exc import SQLAlchemyError

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///consults.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
CORS(app)


class Consult(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_name = db.Column(db.String(100), nullable=False)
    mentor = db.Column(db.String(100), nullable=False)
    topic = db.Column(db.String(200), nullable=False)
    comments = db.Column(db.Text)
    is_accepted = db.Column(db.Boolean, default=False)
    specialization = db.Column(db.String(10), nullable=False)  # Новое поле

    def to_dict(self):
        return {
            'id': self.id,
            'student_name': self.student_name,
            'specialization': self.specialization,
            'mentor': self.mentor,
            'topic': self.topic,
            'comments': self.comments,
            'is_accepted': self.is_accepted,
        }


@app.route('/add_consult', methods=['POST'])
def add_consult():
    try:
        data = request.json
        if 'specialization' not in data or data['specialization'] not in ['web', 'net']:
            return jsonify({"error": "specialization must be either 'web' or 'net'"}), 400

        new_consult = Consult(
            student_name=data['student_name'],
            specialization=data['specialization'],
            mentor=data['mentor'],
            topic=data['topic'],
            comments=data['comments']
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
        if 'mentor' in data:
            consult.mentor = data['mentor']
        if 'topic' in data:
            consult.topic = data['topic']
        if 'comments' in data:
            consult.comments = data['comments']
        if 'is_accepted' in data:
            consult.is_accepted = data['is_accepted']
        if 'specialization' in data:  # Обработка обновления специализации
            if data['specialization'] not in ['web', 'net']:
                return jsonify({"error": "specialization must be either 'web' or 'net'"}), 400
            consult.specialization = data['specialization']

        db.session.commit()
        return jsonify(consult.to_dict()), 200
    except ValueError as e:
        return jsonify({"error": f"Invalid data format: {str(e)}"}), 400
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": f"Database error: {str(e)}"}), 500
    except Exception as e:
        return jsonify({"error": f"Unexpected error: {str(e)}"}), 500


@app.route('/consults/toggle-status/<int:consult_id>', methods=['PATCH'])
def toggle_consult_status(consult_id):
    try:
        consult = Consult.query.get_or_404(consult_id)
        consult.is_accepted = not consult.is_accepted
        db.session.commit()
        return jsonify(consult.to_dict()), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": f"Database error: {str(e)}"}), 500
    except Exception as e:
        return jsonify({"error": f"Unexpected error: {str(e)}"}), 500


@app.route('/consults/<int:consult_id>/accept', methods=['PATCH'])
def accept_consult(consult_id):
    try:
        consult = Consult.query.get_or_404(consult_id)
        consult.is_accepted = True
        db.session.commit()
        return jsonify(consult.to_dict()), 200
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
    # init_db()
    app.run(debug=True, port=8000)