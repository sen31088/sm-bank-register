import flask
from flask import request, render_template, url_for, redirect, Blueprint, session
import bcrypt
from datetime import datetime
import random
from utils.encrypt import encrypt
from models.model_register import Userlogin, Carddetails, Userdata, UserToken, Adminlogin, PasswordresetToken
from utils.sendmail import Sendmail
import uuid
from dotenv import  load_dotenv
import os
import logging

#app = flask.Flask(__name__)

load_dotenv()

app_url = os.getenv("URL")

register_ctrl = Blueprint("user_register", __name__, static_folder='static', template_folder='templates')

#register1_ctrl = Blueprint("register", __name__, static_folder='static', template_folder='templates')

def account_register(from_source):
    user_session = session.get('username')
    if request.method=='POST':
        username_in = request.form.get('username', False)
        password_in1 = request.form.get('password1', False)
        password_in2 = request.form.get('password2', False)
        name_in = request.form.get('fullname', False)
        email_in = request.form.get('email', False)
        username_ln = len(username_in)
        name_ln = len(name_in)
        card_second_last = str(random.randint(1001, 9999))
        card_last = str(random.randint(1001, 9999))
        card_cvv = str(random.randint(100, 999))
        card_start_month = datetime.today().strftime('%b %Y')
        current_year = int(datetime.today().strftime('%Y'))
        end_yr = str(current_year + 3)
        card_end_month = datetime.today().strftime('%b')
        card_end_period = card_end_month + ' ' + end_yr
        card_number_prefix = '4568 3579'
        card_number = str(card_number_prefix + ' ' + card_second_last + ' ' +  card_last)
        encode_card_number = encrypt.encode(card_number)
        encode_cvv_number = encrypt.encode(card_cvv)
        
        if username_ln == 0 or name_ln == 0:
            msg = 'Username is blank'
            if from_source == 'admin':
                return render_template("add-user.html", msg1 = msg, logedin_user = user_session )
            else:
                return render_template("register.html", msg1 = msg)
            
        userid_input =  { 'userid': username_in }

        if Userlogin.get_count(userid_input, limit=1) !=0:
            msg = 'Username '+ username_in + ' Already Taken'
            if from_source == 'admin':
                return render_template("add-user.html", msg1 = msg, logedin_user = user_session )
            else:
                return render_template("register.html", msg1 = msg)
            
        if password_in1 != password_in2:
            msg = 'Passwords Doesnt Match'
            if from_source == 'admin':
                return render_template("add-user.html", msg1 = msg, username = username_in, fullname = name_in, email = email_in, logedin_user = user_session )
            else:
                return render_template("register.html", msg1 = msg, username = username_in, fullname = name_in, email = email_in) 
        
        email_input = { 'email': email_in }
        
        if Userlogin.get_count(email_input, limit=1) !=0:
            msg = 'Email id '+ email_in + ' is already registered'
            if from_source == 'admin':
                return render_template("add-user.html", msg1 = msg, username = username_in, fullname = name_in, logedin_user = user_session )
            else:
                return render_template("register.html", msg1 = msg, username = username_in, fullname = name_in) 
        else:
            password_hashed = bcrypt.hashpw(password_in2.encode('utf-8'), bcrypt.gensalt())
            #Activation_status = account_status
            # TO insert User login Details
            Activation_token = str(uuid.uuid4())
            UserToken.save(username_in, Activation_token )
            Userlogin.save(username_in, password_hashed, name_in, email_in)
            card_name = name_in[0 : 15]
            #To insert Card Details
            input_card_data = {'userid': username_in, 'Name': name_in, 'CardName': card_name, 'Cardnum': encode_card_number , 'CardStartdate': card_start_month, 'CardEnddate': card_end_period, 'Cardcvv': encode_cvv_number }
            Carddetails.save(input_card_data)
            current_last_account1 = Userdata.find_and_sort_documents()
            #current_last_account12 = db_userdata.find().sort("_id", -1).limit(1)
            current_userdata = []
            for i in current_last_account1:
                current_userdata.append(i)
            if not current_userdata:
                    # To insert First User Account Details
                    account_number = '12446001'
                    Userdata.save(username_in, name_in, account_number)
            else:
                new_acc = []
                for i in current_userdata:
                    #print("last account is : ", i)
                    new_acc.append(i["Accno"])
                    last_acc = int(new_acc[0])
                    new_account = str(last_acc + 1)
                # To insert User Account Details
                Userdata.save(username_in, name_in, new_account)
                if from_source == 'admin':
                    msg = 'Registration Sucessful for ' + username_in + ', Email verification link sent.'
                    recipient_email = email_in
                    userid = username_in
                    username_in = name_in
                    activation_url = app_url + "/account-verification/verify/"+ userid + "/" +  Activation_token
                
                    subject = 'SM Bank | Account EMail Verification'
                    message = render_template ('mail-register.html', username_in = username_in, Activation_url = activation_url)
                    Sendmail.send_email(recipient_email, subject, message)
                    return render_template('user-add-sucess.html', user_id = username_in, accname = name_in,logedin_user = user_session, message = msg )
                if from_source == 'user':
                    msg = 'Registration Sucessful for ' + username_in + '. Email verification link sent, Please check your inbox'
                    recipient_email = email_in
                    userid = username_in
                    username_in = name_in
                    subject = 'SM Bank | Account EMail Verification'
                    activation_url = app_url + "/account-verification/verify/"+ userid + "/" +  Activation_token
                    message = render_template ('mail-register.html', username_in = username_in, Activation_url = activation_url)
                    Sendmail.send_email(recipient_email, subject, message)
                    return render_template('index.html', loginmsg = msg)

@register_ctrl.route('/account-verification/verify/<userid>/<token>')
def verify(userid, token):
   
    user_in = userid
    token_in = token
    user_data_found = UserToken.get_data(user_in)
    #print("user_data_found: ", user_data_found)
    userid_found = user_data_found['userid']
    token_found = user_data_found['token']

    if user_in == userid_found and  token_in == token_found:
        print("email Verified")
        UserToken.update(userid_found)
        Userdata.update_Activation_status_status(userid_found)
        Userlogin.update_Activation_status_status(userid_found)
        Userlogin.update_email_verification_status(userid_found)
        UserToken.delete_data(userid_found)
        msg = "Email ID Verified, Your Account will be activated in 24 hrs"
        return render_template('index.html', loginmsg = msg)
    else:
        msg = 'Invalid Token'
        return render_template('index.html', loginmsg = msg)



@register_ctrl.route('/register', methods=('GET','POST'))
def register():
    return render_template("register.html")

@register_ctrl.route('/user-register-from-admin', methods=('GET','POST'))

def user_register_from_admin():

     if request.method=='POST':
        #username_in = request.form.get('username', False)
        #name_in = request.form.get('fullname', False)
        #account_status = 'Activated'
        from_source = 'admin'
        return account_register(from_source)
        #return render_template('user-add-sucess.html', user_id = username_in, accname = name_in)

    
@register_ctrl.route('/user_register', methods=('GET','POST'))
def user_register():
    #account_status = 'Pending'
    from_source = 'user'
    #username_in = request.form.get('username', False)
    return account_register(from_source)
    #msg = 'Registration Sucessful for ' + username_in + ' ,Please login once Account is Activated'
    #return render_template('index.html', loginmsg = msg)


@register_ctrl.route('/admin-register', methods=('GET','POST'))
def admin_register():
    current_admin_login = Adminlogin.get_data()
    #print("current_admin_login is : ", current_admin_login)
    if not current_admin_login:
      return render_template("admin-register.html")
    else:
        msg = "Admin Already registered. Please login"
        return render_template("admin-index1.html", loginmsg = msg)




@register_ctrl.route('/admin_user_register', methods=('GET','POST'))
def admin_user_register():
    if request.method=='POST':
        username_in = request.form.get('username', False)
        password_in1 = request.form.get('password1', False)
        password_in2 = request.form.get('password2', False)
        name_in = request.form.get('fullname', False)
        email_in = request.form.get('email', False)
        username_ln = len(username_in)
        name_ln = len(name_in)

        if username_ln == 0 or name_ln == 0:
            msg = 'Username is blank'
            return render_template("admin-register.html", msg1 = msg)
        #userid_input =  { 'userid': username_in }
        if password_in1 != password_in2:
            msg = 'Passwords Doesnt Match'
            return render_template("admin-register.html", msg1 = msg, username = username_in, fullname = name_in, email = email_in) 
        else:
            password_hashed = bcrypt.hashpw(password_in2.encode('utf-8'), bcrypt.gensalt())
            Adminlogin.save({'userid': username_in, 'password': password_hashed, 'Name': name_in, 'email': email_in})
            msg = 'Registration Sucessful for Admin Username ' + username_in + ' Please login'
            return render_template('admin-index.html', loginmsg = msg)
    return redirect(url_for('home'))


@register_ctrl.route('/forget-password')
def forget_passwd():
        if session.get('otp') is not None:
       # print(" In Route Login session name is true: ", session.get('username'))
          return redirect(url_for('home.home'))
        else:
            #userid_in = session['name']
            #userlogin_data = Userlogin.find_data(userid_in)
            #email_in = userlogin_data['email']
            #send_otp(userid_in)
            return render_template('forget-password.html')

@register_ctrl.route('/api/v1/send-reset-password-link', methods=['POST'])
def api_send_reset_password_link():

    if request.method=='POST':
        userid_in = request.form.get('username', False)
        userlogin_data = Userlogin.find_data(userid_in)
        user_email = userlogin_data['email']
        user_name = userlogin_data['Name']
        
        if userlogin_data == 0:
            msg = 'Invalid username ' + userid_in
            logging.info(f"{userid_in} not found, Invalid username")
            return render_template("forget-password.html", loginmsg = msg)
        else:
            Activation_token = str(uuid.uuid4())
            #Activation_token_encrypt =  fernet.encrypt(Activation_token.encode())
            #Activation_token_str = str(Activation_token_encrypt)
            #print("Activation_token_encrypt is: ", Activation_token_encrypt)
            PasswordresetToken.save(userid_in, Activation_token )
            #Activation_token_decrypt = fernet.decrypt(Activation_token_encrypt.decode())
            #print("Activation_token_decrypt is: ", Activation_token_decrypt)
            #Activation_token_str = str(Activation_token_decrypt)
            subject = 'SM Bank | Password Reset'
            activation_url = app_url + "/password-reset/"+ userid_in + "/" +  Activation_token
            message = render_template ('mail-password-reset.html', username_in = user_name, Activation_url= activation_url)
            Sendmail.send_email(user_email, subject, message)
            logging.info(f"Password Reset Link  sent to {user_name}")
            msg = "Password Reset Link sent to your Registered Email ID."
            return render_template('index.html', loginmsg = msg)



@register_ctrl.route('/password-reset/<userid>/<token>')

def password_reset_verify(userid, token):
    user_in = userid
    token_in = token
    user_data_found = PasswordresetToken.get_data(user_in)
    #print("user_data_found: ", user_data_found)
    userid_found = user_data_found['userid']
    token_found = user_data_found['token']
                
    if user_in == userid_found and  token_in == token_found:
            return render_template("password-reset.html", username = userid_found)
    else:
        msg = "Invalid Password Reset Link"
        return render_template('index.html', loginmsg = msg)

@register_ctrl.route('/api/v1/password-reset' , methods=['POST'])

def password_reset():

    if request.method=='POST':
        userid = request.form.get('username1', False)
        password_in1 = request.form.get('password1', False)
        password_in2 = request.form.get('password2', False)
        
        if password_in1 != password_in2:
            msg = 'Passwords Doesnt Match'
            return render_template("password-reset.html", msg1 = msg, username = userid)
        else:
             password_hashed = bcrypt.hashpw(password_in2.encode('utf-8'), bcrypt.gensalt())
             Userlogin.update_passwd(userid, password_hashed)
             PasswordresetToken.delete_data(userid)
             msg = 'Password updated Sucessfully. Please login.'
             return render_template('index.html', loginmsg = msg)


                

