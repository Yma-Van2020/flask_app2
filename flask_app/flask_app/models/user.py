from flask_app.config.mysqlconnection import connectToMySQL
import re
from flask import flash
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 
PW_REGEX = re.compile(r"^(?=.*[A-Z])(?=.*\d)[A-Za-z\d]{8,}$")
DATABASE = "belt_exam2"
from flask_app.models import sighting

class User:
    def __init__( self , data ):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']              
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.sightings = []

    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    @classmethod
    def create(cls, data ):
        query = "INSERT INTO users ( first_name , last_name , email , password, created_at, updated_at ) VALUES ( %(first_name)s , %(last_name)s , %(email)s ,%(password)s, NOW() , NOW() );"
        return connectToMySQL(DATABASE).query_db( query, data )
    
    @classmethod
    def get_user_with_sightings( cls , data ):
        print(data)
        query = "SELECT * FROM users LEFT JOIN sightings ON sightings.user_id = users.id WHERE users.id = %(id)s;"
        
        results = connectToMySQL(DATABASE).query_db( query , data )
        print(results)
        user = cls( results[0] )
        for row_from_db in results:
            print(row_from_db)
            sighting_data = {
                "id" : row_from_db["sightings.id"],
                "location" : row_from_db["location"],
                "what_happened" : row_from_db["what_happened"],
                "created_at" : row_from_db["sightings.created_at"],
                "updated_at" : row_from_db["sightings.updated_at"],
                "num_sasquatches" : row_from_db["num_sasquatches"],
                "date_of_siting" : row_from_db["date_of_siting"],
                "user_id":row_from_db["user_id"]
            }
            user.sightings.append(sighting.Sighting( sighting_data )) 
        return user
    
    @classmethod
    def get_by_email(cls,data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL(DATABASE).query_db(query,data)
        print(results)
        if len(results) < 1:
            return False
        return cls(results[0])
    
    @classmethod
    def getAll(cls):
        query = "SELECT * FROM users"
        result = connectToMySQL(DATABASE).query_db(query)
        userss = []
        for user in result:
            userss.append(cls(user))
        return userss
    
    @classmethod
    def getOneById(cls,id):
        query = "SELECT * FROM users WHERE id = %(id)s"
        data = {'id':id}
        results = connectToMySQL(DATABASE).query_db(query,data)
        return cls(results[0])
    
    @classmethod
    def update(cls,data):
        query = "UPDATE users SET first_name = %(first_name)s, last_name = %(last_name)s, email = %(email)s, updated_at = NOW() WHERE id = %(id)s"
        return connectToMySQL(DATABASE).query_db(query,data)
    
    
      
    @staticmethod
    def validate_user(data):
        is_valid = True 
   
        if len(data["email"]) == 0:
            flash("* Email cannot be empty", "email")
            is_valid = False
        if not EMAIL_REGEX.match(data['email']): 
            flash("* Invalid email format. Should meet username@emaildomain.com", "email")
            is_valid = False  
        all_users = User.getAll()
        for user in all_users:
            if (user.email == data['email']):
                flash('Email already in database!', "email")
                is_valid = False
        if len(data['first_name']) < 2 or not data['first_name'].isalpha():
            flash("* First name must be at least 2 characters and only letters", "first_name")
            is_valid = False
        if len(data['last_name']) < 2 or not data['last_name'].isalpha():
            flash("* Last name must be at least 2 characters and only letters", "last_name")
            is_valid = False
        if not PW_REGEX.match(data['password']): 
            flash("* Password should be at least 8 characters with one uppercase and one number no special characters", "password")
            is_valid = False
        if data['password'] != data["cpassword"]:
            flash("* Both passwords don't match", "password")
            is_valid = False
        if is_valid:
            flash("* Registration was successful", "first_name")
        return is_valid
    
  