"""
This sample demonstrates an implementation of the Lex Code Hook Interface
in order to serve a sample bot which manages reservations for hotel rooms and car rentals.
Bot, Intent, and Slot models which are compatible with this sample can be found in the Lex Console
as part of the 'BookTrip' template.

For instructions on how to set up and test this bot, as well as additional samples,
visit the Lex Getting Started documentation http://docs.aws.amazon.com/lex/latest/dg/getting-started.html.
"""
import re
import paramiko
import boto3
import json
import datetime
import time
import os
import dateutil.parser
import logging
import pandas as pd
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


# --- Helpers that build all of the responses ---


def elicit_slot(session_attributes, intent_name, slots, slot_to_elicit, message):
    return {
        'sessionAttributes': session_attributes,
        'dialogAction': {
            'type': 'ElicitSlot',
            'intentName': intent_name,
            'slots': slots,
            'slotToElicit': slot_to_elicit,
            'message': message
        }
    }


def confirm_intent(session_attributes, intent_name, slots, message):
    return {
        'sessionAttributes': session_attributes,
        'dialogAction': {
            'type': 'ConfirmIntent',
            'intentName': intent_name,
            'slots': slots,
            'message': message
        }
    }


def close(session_attributes, fulfillment_state, message):
    response = {
        'sessionAttributes': session_attributes,
        'dialogAction': {
            'type': 'Close',
            'fulfillmentState': fulfillment_state,
            'message': message
        }
    }

    return response


def delegate(session_attributes, slots):
    return {
        'sessionAttributes': session_attributes,
        'dialogAction': {
            'type': 'Delegate',
            'slots': slots
        }
    }


# --- Helper Functions ---


def safe_int(n):
    """
    Safely convert n value to int.
    """
    if n is not None:
        return int(n)
    return n


def try_ex(func):
    """
    Call passed in function in try block. If KeyError is encountered return None.
    This function is intended to be used to safely access dictionary.

    Note that this function would have negative impact on performance.
    """

    try:
        return func()
    except KeyError:
        return None


def generate_car_price(location, days, age, car_type):
    """
    Generates a number within a reasonable range that might be expected for a flight.
    The price is fixed for a given pair of locations.
    """

    car_types = ['economy', 'standard', 'midsize', 'full size', 'minivan', 'luxury']
    base_location_cost = 0
    for i in range(len(location)):
        base_location_cost += ord(location.lower()[i]) - 97

    age_multiplier = 1.10 if age < 25 else 1
    # Select economy is car_type is not found
    if car_type not in car_types:
        car_type = car_types[0]

    return days * ((100 + base_location_cost) + ((car_types.index(car_type.lower()) * 50) * age_multiplier))



def isvalid_car_type(car_type):
    car_types = ['economy', 'standard', 'midsize', 'full size', 'minivan', 'luxury']
    return car_type.lower() in car_types


def isvalid_city(city):
    valid_cities = ['new york', 'los angeles', 'chicago', 'houston', 'philadelphia', 'phoenix', 'san antonio',
                    'san diego', 'dallas', 'san jose', 'austin', 'jacksonville', 'san francisco', 'indianapolis',
                    'columbus', 'fort worth', 'charlotte', 'detroit', 'el paso', 'seattle', 'denver', 'washington dc',
                    'memphis', 'boston', 'nashville', 'baltimore', 'portland']
    return city.lower() in valid_cities


def isvalid_room_type(room_type):
    room_types = ['queen', 'king', 'deluxe']
    return room_type.lower() in room_types


def isvalid_date(date):
    try:
        dateutil.parser.parse(date)
        return True
    except ValueError:
        return False


def get_day_difference(later_date, earlier_date):
    later_datetime = dateutil.parser.parse(later_date).date()
    earlier_datetime = dateutil.parser.parse(earlier_date).date()
    return abs(later_datetime - earlier_datetime).days


def add_days(date, number_of_days):
    new_date = dateutil.parser.parse(date).date()
    new_date += datetime.timedelta(days=number_of_days)
    return new_date.strftime('%Y-%m-%d')


def build_validation_result(isvalid, violated_slot, message_content):
    return {
        'isValid': isvalid,
        'violatedSlot': violated_slot,
        'message': {'contentType': 'PlainText', 'content': message_content}
    }

import boto3
def datachunk(para):
    text_list = []
    while para:
        text_list.append(str(para[:4700]))
        para = para[4700:]
    return text_list[:25]

def sentiment(paragraph):
#     s3 = boto3.client("s3")
#     bucket = "lambdalexfile"
#     key = "abbott.txt"
#     file = s3.get_object(Bucket = bucket, Key = key)
#     paragraph = str(file["Body"].read().decode("utf-8"))
    comprehend = boto3.client("comprehend")

    sentiment = comprehend.batch_detect_sentiment(TextList = datachunk(paragraph), LanguageCode = "en")
    return sentiment
    
def entities(paragraph):
#     s3 = boto3.client("s3")
#     bucket = "lambdalexfile"
#     key = "abbott.txt"
#     file = s3.get_object(Bucket = bucket, Key = key)
#     paragraph = str(file["Body"].read().decode("utf-8"))
    comprehend = boto3.client("comprehend")

    entities = comprehend.batch_detect_entities(TextList = datachunk(paragraph), LanguageCode = "en")
    return entities

def keyphrase(paragraph):
#     s3 = boto3.client("s3")
#     bucket = "lambdalexfile"
#     key = "abbott.txt"
#     file = s3.get_object(Bucket = bucket, Key = key)
#     paragraph = str(file["Body"].read().decode("utf-8"))
    comprehend = boto3.client("comprehend")

    keyphrase = comprehend.batch_detect_key_phrases(TextList = datachunk(paragraph), LanguageCode = "en")
    #print(keyphrase)
    return keyphrase

def validate_book_car(slots):
    pickup_city = try_ex(lambda: slots['PickUpCity'])
    pickup_date = try_ex(lambda: slots['PickUpDate'])
    return_date = try_ex(lambda: slots['ReturnDate'])
    driver_age = safe_int(try_ex(lambda: slots['DriverAge']))
    car_type = try_ex(lambda: slots['CarType'])
    stock_analysis = try_ex(lambda: slots['Analysis'])
    analysis_invest = try_ex(lambda: slots['options'])
    invest_type = try_ex(lambda: slots["InvestmentType"])
    ask_questions = try_ex(lambda: slots["Questions"])
    # if analysis_invest=="Analysis":
    if analysis_invest=="Company Analysis":
        if stock_analysis and pickup_city and car_type:
            s3 = boto3.client('s3')
            data = s3.get_object(Bucket='lambdalexfile', Key='Lexfile.csv')
            lexfile = pd.read_csv(data['Body'])
            lexfile['company'] = lexfile['company'].str.lower()
            
            pickup_city = pickup_city.lower()
            filenew= lexfile[lexfile["company"].str.contains(pickup_city, na=False) & (lexfile['Year']==int(car_type))]["lp"]
            filenew = filenew.tolist()[0]
            
            if stock_analysis=="Entity Recognition":
            
                key = entities(filenew)
                
                x = len(pd.DataFrame(key["ResultList"]))
                df = pd.DataFrame()
                for i in range(x):
                    df = df.append(pd.DataFrame(key["ResultList"][1]["Entities"]))
                df = df.drop_duplicates(subset='Type', keep="first")
                df = df[["Type","Text"]]
                entity_df = [tuple(r) for r in df.to_numpy()]
                
                
                return build_validation_result(
                    False,
                    'Analysis',
                    'These are the top 5 entitiy relations in the Edgar report ->\n {}'.format(str(entity_df))
                )
                
                
            if stock_analysis=="Sentiment Analysis":
            
                # s3senti = boto3.client('s3')
                datanew = s3.get_object(Bucket='lambdalexfile', Key='sentiment_score_0704.csv')
                sents = pd.read_csv(datanew['Body'])
                pickup=(str(pickup_city))
                car=(str(car_type))
                sents['company'] = sents['company'].str.lower()
                pickup = pickup.lower()
    
                pos= sents[sents["company"].str.contains(pickup, na=False) & (sents['year']==int(car))]["positive_score"]
                neg= sents[sents["company"].str.contains(pickup, na=False) & (sents['year']==int(car))]["negative_score"]
    
    
                return build_validation_result(
                    False,
                    'Analysis',
                    'The Positive and Negative score for {} are {} and {}'.format(pickup_city,str(pos.tolist()[0]),str(neg.tolist()[0]))
                )
                
            if stock_analysis=="Key Phrases":
    
                key = keyphrase(filenew)
    
                x = len(pd.DataFrame(key["ResultList"]))
                df = pd.DataFrame()
                for i in range(x):
                    df = df.append(pd.DataFrame(key["ResultList"][i]["KeyPhrases"]))
                new_df = df.sort_values(["Score"], ascending = (False))
                new_df = df.drop_duplicates(subset='Text', keep="first").head(10)
                key_phrase = new_df["Text"].tolist()
    
    
                return build_validation_result(
                    False,
                    'Analysis',
                    'The top 10 key phrases used in the report are -> {}'.format(str(key_phrase))
                )
                
            if stock_analysis=="General Info":
    
                data = s3.get_object(Bucket='lambdalexfile', Key='company_url.csv')
                info_df = pd.read_csv(data['Body'])
                pickup_city_lower = pickup_city.lower()
                info= info_df[info_df["Name"].str.contains(pickup_city_lower, na=False)]["Symbol"]
    
    
                return build_validation_result(
                    False,
                    'Analysis',
                    'Click this -> {}'.format(str(info.tolist()[0]))
                )

            if ask_questions:

                client = boto3.client('ec2')
                s3_client = boto3.client('s3')
                # getting instance information
                describeInstance = client.describe_instances()
                hostPublicIP=["52.53.203.198"]
                # downloading pem filr from S3
                s3_client.download_file('paramikotest','ec2key.pem', '/tmp/file.pem')

                # reading pem file and creating key object
                key = paramiko.RSAKey.from_private_key_file("/tmp/file.pem")
                # an instance of the Paramiko.SSHClient
                ssh_client = paramiko.SSHClient()
                # setting policy to connect to unknown host
                ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                host=hostPublicIP[0]
                # connecting to server
                ssh_client.connect(hostname=host, username="ubuntu", pkey=key)
                #x="When was the company founded?"
                x=ask_questions
                #comp = "american.txt"

                pickup=(str(pickup_city))
                comp = pickup_city+".txt"
                # command list
                
                
                commands = ['python3.6 -W ignore bertrun.py "{}" "{}" '.format(x,comp)]
                for command in commands:
                    stdin , stdout, stderr = ssh_client.exec_command(command)
                # re.sub('[b\\n]', '', stdout.read())
                line=stdout.read()

                return build_validation_result(
                    False,
                    'Questions',
                    'Answer -> {}'.format(line.decode('utf-8'))
                        )
            
            if ask_questions=="invest":
                
                return build_validation_result(
                    True,
                    'Questions',
                    'Continue'.format()
                        )

              
                
                
                

    if pickup_date:
        if not isvalid_date(pickup_date):
            return build_validation_result(False, 'PickUpDate', 'I did not understand your departure date.  When would you like to pick up your car rental?')
        if datetime.datetime.strptime(pickup_date, '%Y-%m-%d').date() <= datetime.date.today():
            return build_validation_result(False, 'PickUpDate', 'Reservations must be scheduled at least one day in advance.  Can you try a different date?')

    if return_date:
        if not isvalid_date(return_date):
            return build_validation_result(False, 'ReturnDate', 'I did not understand your return date.  When would you like to return your car rental?')

    if pickup_date and return_date:
        if dateutil.parser.parse(pickup_date) >= dateutil.parser.parse(return_date):
            return build_validation_result(False, 'ReturnDate', 'Your return date must be after your pick up date.  Can you try a different return date?')

        if get_day_difference(pickup_date, return_date) > 30:
            return build_validation_result(False, 'ReturnDate', 'You can reserve a car for up to thirty days.  Can you try a different return date?')

    if driver_age is not None and driver_age < 18:
        return build_validation_result(
            False,
            'DriverAge',
            'Your driver must be at least eighteen to rent a car.  Can you provide the age of a different driver?'
        )

    if car_type and not isvalid_car_type(car_type) and analysis_invest=="Investment" or stock_analysis=="continue":
        return build_validation_result(
            False,
            'CarType',
            'Okay ! Now go and ask Anuj and Ankita.   Say Hi to do another analysis')


    return {'isValid': True}

def validate_hotel(slots):
    amount = try_ex(lambda: slots['Dollar'])
    cat_type = try_ex(lambda: slots['categoryNew'])
    invest_type = try_ex(lambda: slots['InvestmentTypeNew'])
    s3 = boto3.client('s3')
    data = s3.get_object(Bucket='lambdalexfile', Key='return_new.csv')
    df = pd.read_csv(data['Body'])
    # df = str(data["Body"].read().decode("utf-8"))
    
    if amount and cat_type and invest_type:
    
        # if cat_type=="Both" and invest_type=="Low risk":
       #
       #      num_investments = 4
       #      amount = int(amount)
       #      i_percompany = amount/num_investments
       #
       #      df = df[df['return']> 0] #Remove negative returns from consideration
       #
       #      df_safe = df.sort_values('return',ascending=False).groupby('sector').head(1)
       #      df_safe = df_safe.head(num_investments)
       #
       #      df_safe['return'] = (i_percompany * df_safe['return'])/100
       #      df_safe['final'] = i_percompany + df_safe['return']
       
            # df_safe[["return"]].head()
            
            # df_safe["return"].tolist()[0]
            # df_safe["return"].tolist()[1]
            # df_safe["return"].tolist()[2]
            
            # df_safe["company_name"].tolist()[0]
            # df_safe["company_name"].tolist()[1]
            # df_safe["company_name"].tolist()[2]
            
            return build_validation_result(
            False,
            'Dollar',
            "Hello"
            #'The investment amount is {}, The following would be the best return in the selected options. {} would return {},   {} would return {},  {} would return {}, Total sum will be {}'.format(str(amount),df_safe["company_name"].tolist()[0],df_safe["final"].tolist()[0],df_safe["company_name"].tolist()[1],df_safe["final"].tolist()[1],df_safe["company_name"].tolist()[2],df_safe["final"].tolist()[2],str(df_safe[["final"]].head(4).sum().tolist()[0]))
        )  
        
        # if cat_type=="Both" and invest_type=="High Risk":
            
        
        # if cat_type=="Stocks" and invest_type=="Low risk":
        
        
        # if cat_type=="Stocks" and invest_type=="High Risk":
    
    
    
    return {'isValid': True}
# """ --- Functions that control the bot's behavior --- """


def book_hotel(intent_request):
    """
    Performs dialog management and fulfillment for booking a hotel.

    Beyond fulfillment, the implementation for this intent demonstrates the following:
    1) Use of elicitSlot in slot validation and re-prompting
    2) Use of sessionAttributes to pass information that can be used to guide conversation
    """

    # amount = try_ex(lambda: intent_request['currentIntent']['slots']['Dollar'])
    # cat_type = try_ex(lambda: intent_request['currentIntent']['slots']['categoryNew'])
    # invest_type = try_ex(lambda: intent_request['currentIntent']['slots']['InvestmentTypeNew'])
    #
    session_attributes = intent_request['sessionAttributes'] if intent_request['sessionAttributes'] is not None else {}
    #
    # # Load confirmation history and track the current reservation.
    # reservation = json.dumps({
    #     'Dollar': amount,
    #     'categoryNew': cat_type,
    #     'InvestmentTypeNew': invest_type,
    #
    # })
    #
    # session_attributes['currentReservation'] = reservation

    if intent_request['invocationSource'] == 'DialogCodeHook':
        # Validate any slots which have been specified.  If any are invalid, re-elicit for their value
        validation_result = validate_hotel(intent_request['currentIntent']['slots'])
        if not validation_result['isValid']:
            slots = intent_request['currentIntent']['slots']
            slots[validation_result['violatedSlot']] = None

            return elicit_slot(
                session_attributes,
                intent_request['currentIntent']['name'],
                slots,
                validation_result['violatedSlot'],
                validation_result['message']
            )

        # Otherwise, let native DM rules determine how to elicit for slots and prompt for confirmation.  Pass price
        # back in sessionAttributes once it can be calculated; otherwise clear any setting from sessionAttributes.
        if location and checkin_date and nights and room_type:
            # The price of the hotel has yet to be confirmed.
            price = generate_hotel_price(location, nights, room_type)
            session_attributes['currentReservationPrice'] = price
        else:
            try_ex(lambda: session_attributes.pop('currentReservationPrice'))

        session_attributes['currentReservation'] = reservation
        return delegate(session_attributes, intent_request['currentIntent']['slots'])

    # Booking the hotel.  In a real application, this would likely involve a call to a backend service.
    logger.debug('bookHotel under={}'.format(reservation))

    try_ex(lambda: session_attributes.pop('currentReservationPrice'))
    try_ex(lambda: session_attributes.pop('currentReservation'))
    session_attributes['lastConfirmedReservation'] = reservation

    return close(
        session_attributes,
        'Fulfilled',
        {
            'contentType': 'PlainText',
            'content': 'Thanks, I have placed your reservation.   Please let me know if you would like to book a car '
                       'rental, or another hotel.'
        }
    )

# --- Intents ---





def book_car(intent_request):
    """
    Performs dialog management and fulfillment for booking a car.

    Beyond fulfillment, the implementation for this intent demonstrates the following:
    1) Use of elicitSlot in slot validation and re-prompting
    2) Use of sessionAttributes to pass information that can be used to guide conversation
    """
    slots = intent_request['currentIntent']['slots']
    pickup_city = slots['PickUpCity']
    pickup_date = slots['PickUpDate']
    return_date = slots['ReturnDate']
    driver_age = slots['DriverAge']
    car_type = slots['CarType']
    stock_analysis = slots['Analysis']
    analysis_invest = slots['options']
    invest_type = slots["InvestmentType"]
    ask_questions = slots["Questions"]
    confirmation_status = intent_request['currentIntent']['confirmationStatus']
    session_attributes = intent_request['sessionAttributes'] if intent_request['sessionAttributes'] is not None else {}
    last_confirmed_reservation = try_ex(lambda: session_attributes['lastConfirmedReservation'])
    if last_confirmed_reservation:
        last_confirmed_reservation = json.loads(last_confirmed_reservation)
    confirmation_context = try_ex(lambda: session_attributes['confirmationContext'])

    # Load confirmation history and track the current reservation.
    reservation = json.dumps({
        'ReservationType': 'Car',
        'PickUpCity': pickup_city,
        'PickUpDate': pickup_date,
        'ReturnDate': return_date,
        'CarType': car_type
        
    })
    session_attributes['currentReservation'] = reservation

    if pickup_city and pickup_date and return_date and driver_age and car_type:
        # Generate the price of the car in case it is necessary for future steps.
        price = generate_car_price(pickup_city, get_day_difference(pickup_date, return_date), driver_age, car_type)
        session_attributes['currentReservationPrice'] = price

    if intent_request['invocationSource'] == 'DialogCodeHook':
        # Validate any slots which have been specified.  If any are invalid, re-elicit for their value
        validation_result = validate_book_car(intent_request['currentIntent']['slots'])
        if not validation_result['isValid']:
            slots[validation_result['violatedSlot']] = None
            return elicit_slot(
                session_attributes,
                intent_request['currentIntent']['name'],
                slots,
                validation_result['violatedSlot'],
                validation_result['message']
            )

        # Determine if the intent (and current slot settings) has been denied.  The messaging will be different
        # if the user is denying a reservation he initiated or an auto-populated suggestion.
        if confirmation_status == 'Denied':
            # Clear out auto-population flag for subsequent turns.
            try_ex(lambda: session_attributes.pop('confirmationContext'))
            try_ex(lambda: session_attributes.pop('currentReservation'))
            if confirmation_context == 'AutoPopulate':
                return elicit_slot(
                    session_attributes,
                    intent_request['currentIntent']['name'],
                    {
                        'PickUpCity': None,
                        'PickUpDate': None,
                        'ReturnDate': None,
                        'DriverAge': None,
                        'CarType': None
                    },
                    'PickUpCity',
                    {
                        'contentType': 'PlainText',
                        'content': 'Where would you like to make your car reservation?'
                    }
                )

            return delegate(session_attributes, intent_request['currentIntent']['slots'])

        if confirmation_status == 'None':
            # If we are currently auto-populating but have not gotten confirmation, keep requesting for confirmation.
            if (not pickup_city and not pickup_date and not return_date and not driver_age and not car_type)\
                    or confirmation_context == 'AutoPopulate':
                if last_confirmed_reservation and try_ex(lambda: last_confirmed_reservation['ReservationType']) == 'Hotel':
                    # If the user's previous reservation was a hotel - prompt for a rental with
                    # auto-populated values to match this reservation.
                    session_attributes['confirmationContext'] = 'AutoPopulate'
                    return confirm_intent(
                        session_attributes,
                        intent_request['currentIntent']['name'],
                        {
                            'PickUpCity': last_confirmed_reservation['Location'],
                            'PickUpDate': last_confirmed_reservation['CheckInDate'],
                            'ReturnDate': add_days(
                                last_confirmed_reservation['CheckInDate'], last_confirmed_reservation['Nights']
                            ),
                            'CarType': None,
                            'DriverAge': None
                        },
                        {
                            'contentType': 'PlainText',
                            'content': 'Is this car rental for your {} night stay in {} on {}?'.format(
                                last_confirmed_reservation['Nights'],
                                last_confirmed_reservation['Location'],
                                last_confirmed_reservation['CheckInDate']
                            )
                        }
                    )

            # Otherwise, let native DM rules determine how to elicit for slots and/or drive confirmation.
            return delegate(session_attributes, intent_request['currentIntent']['slots'])

        # If confirmation has occurred, continue filling any unfilled slot values or pass to fulfillment.
        if confirmation_status == 'Confirmed':
            # Remove confirmationContext from sessionAttributes so it does not confuse future requests
            try_ex(lambda: session_attributes.pop('confirmationContext'))
            if confirmation_context == 'AutoPopulate':
                if not driver_age:
                    return elicit_slot(
                        session_attributes,
                        intent_request['currentIntent']['name'],
                        intent_request['currentIntent']['slots'],
                        'DriverAge',
                        {
                            'contentType': 'PlainText',
                            'content': 'How old is the driver of this car rental?'
                        }
                    )
                elif not car_type:
                    return elicit_slot(
                        session_attributes,
                        intent_request['currentIntent']['name'],
                        intent_request['currentIntent']['slots'],
                        'CarType',
                        {
                            'contentType': 'PlainText',
                            'content': 'What type of car would you like? Popular models are '
                                       'economy, midsize, and luxury.'
                        }
                    )

            return delegate(session_attributes, intent_request['currentIntent']['slots'])

    # Booking the car.  In a real application, this would likely involve a call to a backend service.
    logger.debug('bookCar at={}'.format(reservation))
    del session_attributes['currentReservationPrice']
    del session_attributes['currentReservation']
    session_attributes['lastConfirmedReservation'] = reservation
    return close(
        session_attributes,
        'Fulfilled',
        {
            'contentType': 'PlainText',
            'content': 'Thanks, I have placed your reservation.'
        }
    )


# --- Intents ---


def dispatch(intent_request):
    """
    Called when the user specifies an intent for this bot.
    """

    logger.debug('dispatch userId={}, intentName={}'.format(intent_request['userId'], intent_request['currentIntent']['name']))

    intent_name = intent_request['currentIntent']['name']

    # Dispatch to your bot's intent handlers
    if intent_name == 'BookHotel':
        return book_hotel(intent_request)
    elif intent_name == 'BookCar':
        return book_car(intent_request)

    raise Exception('Intent with name ' + intent_name + ' not supported')


# --- Main handler ---


def lambda_handler(event, context):
    """
    Route the incoming request based on intent.
    The JSON body of the request is provided in the event slot.
    """
    # By default, treat the user request as coming from the America/New_York time zone.
    os.environ['TZ'] = 'America/New_York'
    time.tzset()
    logger.debug('event.bot.name={}'.format(event['bot']['name']))

    return dispatch(event)
