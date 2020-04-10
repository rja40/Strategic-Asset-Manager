"""
This sample demonstrates an implementation of the Lex Code Hook Interface
in order to serve a sample bot which manages reservations for hotel rooms and car rentals.
Bot, Intent, and Slot models which are compatible with this sample can be found in the Lex Console
as part of the 'BookTrip' template.

For instructions on how to set up and test this bot, as well as additional samples,
visit the Lex Getting Started documentation http://docs.aws.amazon.com/lex/latest/dg/getting-started.html.
"""
import pandas as pd
import boto3
import json
# import datetime
import time
import os
# import dateutil.parser
import logging

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


# --- Helpers that build all of the responses ---



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


  


# --- Helper Functions ---



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




# def get_day_difference(later_date, earlier_date):
#     later_datetime = dateutil.parser.parse(later_date).date()
#     earlier_datetime = dateutil.parser.parse(earlier_date).date()
#     return abs(later_datetime - earlier_datetime).days


# def add_days(date, number_of_days):
#     new_date = dateutil.parser.parse(date).date()
#     new_date += datetime.timedelta(days=number_of_days)
#     return new_date.strftime('%Y-%m-%d')



""" --- Functions that control the bot's behavior --- """


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
    confirmation_status = intent_request['currentIntent']['confirmationStatus']
    session_attributes = intent_request['sessionAttributes'] if intent_request['sessionAttributes'] is not None else {}
    # last_confirmed_reservation = try_ex(lambda: session_attributes['lastConfirmedReservation'])
    # if last_confirmed_reservation:
    #     last_confirmed_reservation = json.loads(last_confirmed_reservation)
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

    # if pickup_city and pickup_date and return_date and driver_age and car_type:
    #     # Generate the price of the car in case it is necessary for future steps.
    #     price = generate_car_price(pickup_city, get_day_difference(pickup_date, return_date), driver_age, car_type)
    #     session_attributes['currentReservationPrice'] = price
    
    
    # Booking the car.  In a real application, this would likely involve a call to a backend service.
    logger.debug('bookCar at={}'.format(reservation))
    # del session_attributes['currentReservationPrice']
    del session_attributes['currentReservation']
    session_attributes['lastConfirmedReservation'] = reservation
    s3 = boto3.client('s3')
    data = s3.get_object(Bucket='lambdalexfile', Key='chatbot.csv')
    # contents = data['Body'].read().decode("utf-8")
    df = pd.read_csv(data['Body'])
    
    new = df[df['type']==pickup_city]["amount"]
    if new.empty==True:
        new=pd.Series([999])
    
    # print(initial_df["Name"])
    return close(
        session_attributes,
        'Fulfilled',
        {
            'contentType': 'PlainText',
            'content': 'Thanks {}, I finally have placed your reservation.'.format(str(new.tolist()[0]))
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
    # if intent_name == 'BookHotel':
    #     return book_hotel(intent_request)
    if intent_name == 'BookCar':
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
