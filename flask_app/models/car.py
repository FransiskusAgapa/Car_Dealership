from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import user


class Car:
    db_schema_name = "car_deals"
    def __init__(self,data):
        self.id = data['id']
        self.price = data['price']
        self.model = data['model']
        self.make = data['make']
        self.year = data['year']
        self.description = data['description']
        self.user_id = data['user_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.owner = None

        # @staticmethod for data validation
    @staticmethod
    def validate_car_data(car):
            is_valid = True
            if int(car['price']) == 0:
                flash("Invalid Price")
                is_valid = False
            if len(car['model']) == 0:
                flash("Model is required")
                is_valid = False
            if len(car['make']) == 0:
                flash("Make is required")
                is_valid = False
            if int(car['year']) == 0:
                flash("Invalid Year")
                is_valid = False
            if len(car['description']) == 0:
                flash("Description is required")
                is_valid = False
            return is_valid

    # @classmethod for data processing
    # Create
    @classmethod
    def save_car(cls,car_data):
            query = """
            INSERT INTO cars (price,model,make,year,description,user_id,created_at,updated_at) VALUES (%(price)s,%(model)s,%(make)s,%(year)s,%(description)s,%(user_id)s,NOW(),NOW());
            """
            print("[ Create A Car ]")
            return connectToMySQL(cls.db_schema_name).query_db(query,car_data)
        
    # Read
    @classmethod
    def read_all_cars(cls):
            query = """
            SELECT * FROM cars;
            """
            group_of_cars = connectToMySQL(cls.db_schema_name).query_db(query)
            all_cars = []
            for each_car in group_of_cars:
                all_cars.append(cls(each_car))
            print("[ Read All Cars ]")
            return all_cars
        
    @classmethod
    def read_one_car(cls, car_id):
            query = """
            SELECT * FROM cars WHERE id = %(id)s;
            """
            car_data = {
                "id":car_id
            }
            the_car = connectToMySQL(cls.db_schema_name).query_db(query,car_data)
            print(f"[ Read One Car ID:{car_id} ]")
            return cls(the_car[0])
        

    @classmethod
    def get_all_cars_with_users(cls):
            query = """
            SELECT * FROM cars LEFT JOIN users ON users.id = cars.user_id;
            """
            group_of_users_and_cars = connectToMySQL(cls.db_schema_name).query_db(query)
            cars = []
            for each_user_data in group_of_users_and_cars:
                this_user = cls(each_user_data)
                this_user.owner = user.User(
                    {
                        "id":each_user_data['users.id'],
                        "first_name":each_user_data['first_name'],
                        "last_name":each_user_data['last_name'],
                        "email":each_user_data['email'],
                        "password":each_user_data['password'],
                        "created_at":each_user_data['created_at'],
                        "updated_at":each_user_data["updated_at"]
                    }
                )
                cars.append(this_user)
            return cars
    
    @classmethod
    def get_one_car_with_user(cls,user_id):
        query = """
            SELECT * FROM cars LEFT JOIN users ON users.id = %(id)s;
            """
        the_car_and_user = connectToMySQL(cls.db_schema_name).query_db(query)
        return the_car_and_user
        
    # Update
    @classmethod
    def update_car_data(cls,data):
            query = """
            UPDATE cars SET price=%(price)s,model=%(model)s,make=%(make)s,year=%(year)s,description=%(description)s,updated_at=NOW() WHERE id = %(id)s;
            """
            print("[ Update Car Data ]")
            return connectToMySQL(cls.db_schema_name).query_db(query,data)

    # Delete
    @classmethod
    def delete_car(cls,car_id):
            query = """
            DELETE FROM cars WHERE id = %(id)s;
            """
            car_to_delete = {
                "id":car_id
            }

            print("[ Delete Car ]")
            return connectToMySQL(cls.db_schema_name).query_db(query,car_to_delete)
