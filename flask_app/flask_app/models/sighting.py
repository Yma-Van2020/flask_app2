from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import user
from flask import flash
DATABASE = 'belt_exam2'

class Sighting:
    def __init__( self , data ):
        self.id = data['id']
        self.location = data['location']
        self.what_happened = data['what_happened']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.num_sasquatches = data['num_sasquatches']
        self.date_of_siting = data['date_of_siting']
        self.user_id = data['user_id']
    
    def get_user(self):
        return user.User.getOneById(self.user_id)
        
    @classmethod
    def getAll(cls):
        query = "SELECT * FROM sightings "
        result = connectToMySQL(DATABASE).query_db(query)
        sightings = []
        for sighting in result:
            sightings.append(cls(sighting))
        return sightings  
   
    @classmethod
    def create(cls,data):
        query ="INSERT INTO sightings (location, what_happened, created_at, updated_at, num_sasquatches, date_of_siting, user_id) VALUES (%(location)s, %(what_happened)s, NOW(), NOW(), %(num_sasquatches)s, %(date_of_siting)s, %(user_id)s);"
        return connectToMySQL(DATABASE).query_db(query,data)
        
    
    @classmethod
    def getOneById(cls, id):
        query = "SELECT * FROM sightings WHERE id = %(id)s"
        data = {'id':id}
        result = connectToMySQL(DATABASE).query_db(query,data)
        return cls(result[0])
    
    @classmethod
    def edit(cls,data):
        query = "UPDATE sightings SET location = %(location)s, what_happened = %(what_happened)s, num_sasquatches = %(num_sasquatches)s,date_of_siting = %(date_of_siting)s, updated_at = NOW() WHERE id = %(id)s"
        return connectToMySQL(DATABASE).query_db(query,data)
    
    @classmethod
    def delete(cls,id):
        query = "DELETE FROM sightings WHERE id = %(id)s"
        data = {'id':id}
        return connectToMySQL(DATABASE).query_db(query,data)
    
    @staticmethod
    def validate_sighting(data):
        is_valid = True 
   
        if len(data['location']) < 1:
            flash("* location cannot be empty", "location")
            is_valid = False
        if len(data['what_happened']) < 1 :
            flash("* what happened cannot be empty", "what_happened")
            is_valid = False
        if int(data['num_sasquatches']) < 1:
            flash("* sasquatches has to be at least 1", "num_sasquatches")
            is_valid = False
        if data['date_of_siting'] == "":
            flash("* Fill in the date", "date_of_siting")
            is_valid = False
        if is_valid:
            flash("* sighting created successfully.")
        return is_valid