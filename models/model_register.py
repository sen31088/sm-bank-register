from config import DB_Config

class Userlogin:
    collection = DB_Config.col_userlogin

    @classmethod
    def save(cls, username_in, password_hashed, name_in, email_in):
        input_data = {'userid': username_in, 'password': password_hashed, 'Name': name_in, 'email': email_in, 'Activation_status': 'Awating Email confirmation', 'Email_verfication_status': 'Not Verified' }
        return cls.collection.insert_one(input_data)
    
    @classmethod
    def update_email_verification_status(cls, userid):
        userid_in = { "userid": userid }
        verfication_status = { "$set": { "Email_verfication_status": 'Verified' } }
        return cls.collection.update_one(userid_in, verfication_status)
    
    @classmethod
    def update_Activation_status_status(cls, userid):
        userid_in = { "userid": userid }
        verfication_status = { "$set": { "Activation_status": 'Pending' } }
        return cls.collection.update_one(userid_in, verfication_status)
    
    @classmethod
    def update_passwd(cls, userid, passwd):
        userid_in = { "userid": userid }
        new_password = { "$set": { "password": passwd } }
        return cls.collection.update_one(userid_in, new_password)
    

    @classmethod
    def get_data(cls):
        return list(cls.collection.find())
    
    @classmethod
    def get_count(cls, data, limit=None):
        count = cls.collection.count_documents(data, limit=limit)
        return count
    
    @classmethod
    def find_data(cls, username_in):
       try:
        data = {'userid': username_in}
        output = cls.collection.find_one(data)
        if output:
            return dict(output)
        else:
            return 0
       except Exception as e:
           return {'error': str(e)}
       

class PasswordresetToken:
    collection = DB_Config.col_passwordtoken

    @classmethod
    def save(cls, username_in, token):
        input_data = {'userid': username_in, 'token': token, 'verified' : False }
        return cls.collection.insert_one(input_data)
    

    @classmethod
    def get_data(cls, username_in):
        query = {'userid': username_in}
        return dict(cls.collection.find_one(query))
    
    @classmethod
    def update(cls, userid):
        userid_in = { "userid": userid }
        verfication_status = { "$set": { "verified": True } }
        return cls.collection.update_one(userid_in, verfication_status)
    
    @classmethod
    def delete_data(cls, user_id):
        result = cls.collection.delete_one({'userid': user_id})
        return result.deleted_count > 0
    

class UserToken:
    collection = DB_Config.col_usertoken

    @classmethod
    def save(cls, username_in, token):
        input_data = {'userid': username_in, 'token': token, 'verified' : False }
        return cls.collection.insert_one(input_data)
    

    @classmethod
    def get_data(cls, username_in):
        query = {'userid': username_in}
        return dict(cls.collection.find_one(query))
    
    @classmethod
    def update(cls, userid):
        userid_in = { "userid": userid }
        verfication_status = { "$set": { "verified": True } }
        return cls.collection.update_one(userid_in, verfication_status)
    
    @classmethod
    def delete_data(cls, user_id):
        result = cls.collection.delete_one({'userid': user_id})
        return result.deleted_count > 0


    
    

    
class Carddetails:
    collection = DB_Config.col_carddetails

    @classmethod
    def save(cls, data):
        return cls.collection.insert_one(data)

    @classmethod
    def get_data(cls):
        return list(cls.collection.find())

class Userdata:
    collection = DB_Config.col_userdata
    
    @classmethod
    def save(cls, username_in, name_in, new_account):
        input_data = {"userid": username_in,"Name": name_in,"Accno": new_account ,"Accbal":"10000", 'Activation_status': 'Awating Email confirmation'}
        return cls.collection.insert_one(input_data)
    
    @classmethod
    def update_Activation_status_status(cls, userid):
        userid_in = { "userid": userid }
        verfication_status = { "$set": { "Activation_status": 'Pending' } }
        return cls.collection.update_one(userid_in, verfication_status)
    
    
       
    @classmethod
    def update(cls, data):
        return cls.collection.update_one(data)

    @classmethod
    def get_data(cls):
        return list(cls.collection.find())
    
    @classmethod
    def get_data_one(cls, data):
        return list(cls.collection.find_one(data))
    
    
    @classmethod
    def find_and_sort_documents(cls, sort_field='_id', sort_order= -1, limit1=1):
        cursor = cls.collection.find().sort(sort_field, sort_order).limit(limit1)
        return list(cursor)

class Adminlogin:
    collection = DB_Config.col_adminlogin

    @classmethod
    def save(cls, data):
        return cls.collection.insert_one(data)

    @classmethod
    def get_data(cls):
        return list(cls.collection.find())
    
    @classmethod
    def get_count(cls, data, limit=None):
        count = cls.collection.count_documents(data, limit=limit)
        return count

class Admindata:
    collection = DB_Config.col_admindata

    @classmethod
    def save(cls, data):
        return cls.collection.insert_one(data)
    @classmethod
    def update(cls, data):
        return cls.collection.update_one(data)

    @classmethod
    def get_data(cls):
        return list(cls.collection.find())
    
    @classmethod
    def get_data_one(cls, data):
        return list(cls.collection.find_one(data))
    
    @classmethod
    def find_and_sort_documents(cls, sort_field='_id', sort_order= -1, limit1=1):
        cursor = cls.collection.find().sort(sort_field, sort_order).limit(limit1)
        return list(cursor)