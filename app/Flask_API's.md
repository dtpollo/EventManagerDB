# API Structure and Development

Each Python script in this project corresponds to a specific table in the database and follows a consistent, modular structure. While the core layout is similar, each script is slightly customized to meet the specific data and validation needs of the corresponding table.

---

## Script Structure per Table

All scripts follow the naming convention:

**File name:** `TableName_app.py`

### Structure Overview:

1. **Header**
2. **Model**
3. **Marshmallow Schema**
4. **Endpoints (CRUD)**

---

### 1. Header

This section is where we import the required libraries such as `Flask`, `Blueprint`, `SQLAlchemy`, and `Marshmallow`.

* Each script defines its own `Blueprint`.
* That Blueprint is later imported and registered in `main.py` to activate the associated API routes.

```python
attendee_bp = Blueprint('attendee_bp', __name__)
```

---

### 2. Model

The model defines a SQLAlchemy class that maps directly to a table in the database.

* Each attribute in the class maps to a column in the table.
* You should define data types, primary keys, and constraints such as `nullable`, `unique`, etc.
* NOTE: mistakes in types or missing lengths for strings may cause the app to fail.

```python
class Attendee(db.Model):
    __tablename__ = 'attendee'
    att_id = Column(Integer, primary_key=True)
    att_name = Column(String(100), nullable=False)
    ...
```

---

### 3. Marshmallow Schema

This section includes a Marshmallow schema class. Like a translator, it validates and converts Python objects to and from JSON.

* Essential for data validation before interacting with the database.
* Also helpful for front-end frameworks like React, Vue, or Django REST.

```python
class AttendeeSchema(Schema):
    att_email = fields.Email(required=True)
    att_phone = fields.Str(validate=validate.Regexp(r'^09[0-9]{8}$'))
```

NOTE: Keep field names consistent with your database model to avoid bugs.

---

### 4. Endpoints (CRUD Operations)

Each script includes several Flask route definitions to handle CRUD operations.

```python
@attendee_bp.route('/attendees', methods=['GET'])
```

You can test the endpoints with `curl` in the terminal:

```bash
curl http://localhost:5000/attendees
```

Remeber :

* Flask defaults to port `5000`. If you change it, make sure all scripts use the same port.
* Always include error handling so issues are easier to detect and resolve.

Typical routes to implement:

* **GET** → Retrieve data
* **POST** → Create data
* **PUT** → Update data
* **DELETE** → Remove data

---

## main.py

This is the central file that brings all scripts together. Its layout typically includes:

1. **Header:** Import libraries and all Blueprints.
2. **Database Configuration:** Set up connection parameters (user, password, host, port).
3. **Blueprint Registration:** Register each module of Blueprint.
4. **Server Initialization:** Run the app and initialize the database.

Example:

```python
app.register_blueprint(attendee_bp)
...
if __name__ == '__main__':
    db.create_all()
    app.run()
```

---

## Extra Notes

* `use_db.py` stores a centralized instance of `db = SQLAlchemy()` to avoid repetition.
* All Python scripts and configuration files live in the `flask_api` folder.

---

You can create additional modules for new tables or customize your APIs. Keeping your code modular, well documented, and consistent makes your project easier to scale.
Good luck!

