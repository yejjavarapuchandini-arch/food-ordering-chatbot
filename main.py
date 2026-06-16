from fastapi import FastAPI, Request
from db_helper import (
    get_order_status,
    insert_order_item,
    get_next_order_id,
    get_total_order_price,
    insert_order_tracking,
    insert_customer_details
)
from generic_helper import extract_session_id
from generic_helper import get_str_from_food_dict



app = FastAPI()

inprogress_orders = {}
pending_quantity = {}
customer_details = {}


def handle_place_order(parameters, session_id):
    return "What would you like to order?"


def handle_order_item(parameters, session_id):

    food_items = parameters.get("food_item", [])
    quantities = parameters.get("number", [])

    if not isinstance(food_items, list):
        food_items = [food_items]

    if not isinstance(quantities, list):
        quantities = [quantities]

    if len(food_items) != len(quantities):
        return "Please provide quantity for all food items."

    # Create dictionary
    new_food_dict = dict(
        zip(
            food_items,
            [int(float(qty)) for qty in quantities]
        )
    )

    print("NEW FOOD DICT:")
    print(new_food_dict)

    if session_id not in inprogress_orders:
        inprogress_orders[session_id] = {}

    current_order = inprogress_orders[session_id]

    for item, qty in new_food_dict.items():

        if item in current_order:
            current_order[item] += qty
        else:
            current_order[item] = qty

    print("CURRENT ORDERS:")
    print(inprogress_orders)

    order_str = get_str_from_food_dict(
    inprogress_orders[session_id])

    return (
        f"So far you have: {order_str}. "
        f"Do you needanything else?"
    )


def handle_order_remove(parameters, session_id):

    food_items = parameters.get("food_items", [])

    if not isinstance(food_items, list):
        food_items = [food_items]

    if session_id not in inprogress_orders:
        return (
            "I'm having trouble finding your order. "
            "Can you place a new order?"
        )

    current_order = inprogress_orders[session_id]

    removed_items = []
    no_such_items = []

    for item in food_items:

        found_key = None

        for key in current_order.keys():

            if key.lower() == item.lower():
                found_key = key
                break

        if found_key:
            removed_items.append(found_key)
            del current_order[found_key]

        else:
            no_such_items.append(item)

    fulfillment_text = ""

    if removed_items:
        fulfillment_text += (
            f"Removed {', '.join(removed_items)} from your order. "
        )

    if no_such_items:
        fulfillment_text += (
            f"Your current order does not have "
            f"{', '.join(no_such_items)}. "
        )

    if len(current_order) == 0:

        fulfillment_text += "Your order is empty!"

    else:

        order_str = get_str_from_food_dict(
            current_order
        )

        fulfillment_text += (
        f"Remaining items in your order: "
        f"{order_str}. "
        f"Would you like to continue ordering?"
)

    return fulfillment_text

def handle_view_order(parameters, session_id):

    if session_id not in inprogress_orders:
        return "Your order is empty."

    order = inprogress_orders[session_id]

    return "Your current order: " + get_str_from_food_dict(order)


def handle_confirm_order(parameters, session_id):

    if session_id not in inprogress_orders:
        return "Your order is empty."

    order = inprogress_orders[session_id]

    return (
        "Your order contains: "
        + get_str_from_food_dict(order)
        + ". Please provide your delivery address."
    )


# def handle_address(parameters, session_id):

#     city = parameters.get("city")
#     house_number = parameters.get("house_number")
#     street_name = parameters.get("street_name")
#     locality = parameters.get("locality")

#     missing = []

#     if not city:
#         missing.append("city")

#     if not house_number:
#         missing.append("house number")

#     if not street_name:
#         missing.append("street name")

#     if not locality:
#         missing.append("locality")

#     if missing:
#         return (
#             "Please provide: "
#             + ", ".join(missing)
#         )

#     return (
#         f"Address received: {house_number}, "
#         f"{street_name}, {locality}, {city}. "
#         f"Please provide your phone number."
#     )

def handle_address(parameters, session_id):

    address = parameters.get("address")

    if isinstance(address, list):
        address = "".join(str(x) for x in address)

    if session_id not in customer_details:
        customer_details[session_id] = {}

    customer_details[session_id]["address"] = address

    return (
        f"Address received: {address}. "
        f"Please provide your phone number."
    )


def handle_phone_number(parameters, session_id):

    try:

        phone = parameters.get("phone-number")

        print("PHONE:", phone)
        print("SESSION:", session_id)
        print("CUSTOMER DETAILS:", customer_details)
        print("INPROGRESS ORDERS:", inprogress_orders)

        if session_id not in customer_details:
            customer_details[session_id] = {}

        customer_details[session_id]["phone"] = phone

        address = customer_details.get(
            session_id,
            {}
        ).get(
            "address",
            "Unknown Address"
        )

        print("ADDRESS:", address)

        order_id, order_total = complete_order(session_id)


        if order_id == -1:
            return "Sorry, I couldn't process your order."

        insert_customer_details(
            order_id,
            address,
            phone
        )

        if session_id in customer_details:
            del customer_details[session_id]

        return (
            f"Awesome! Your order has been placed successfully. "
            f"Order ID: #{order_id}. "
            f"Total Amount: ₹{order_total}. "
            f"You can pay at the time of delivery."
        )

    except Exception as e:

        print("PHONE INTENT ERROR:", str(e))

        return f"ERROR: {str(e)}"

def handle_quantity(parameters, session_id):

    qty = int(parameters.get("number"))

    item = pending_quantity[session_id][0]

    if session_id not in inprogress_orders:
        inprogress_orders[session_id] = {}

    inprogress_orders[session_id][item] = qty

    del pending_quantity[session_id]

    return f"Added {qty} {item}. Anything else?"


def handle_track_order(parameters, session_id):

    order_id = parameters.get("number")

    if isinstance(order_id, list):
        order_id = order_id[0]

    status = get_order_status(int(order_id))

    if status == "Order not found":
        return (
            f"Order ID {order_id} was not found. "
            f"Please enter a valid order ID."
        )

    return f"Your order status is: {status}"


def complete_order(session_id):


    if session_id not in inprogress_orders:
        print("SESSION NOT FOUND")
        return -1, 0

    order = inprogress_orders[session_id]

    print("ORDER FOUND:", order)

    order_id, order_total = save_to_db(order)

    del inprogress_orders[session_id]

    return order_id, order_total

def handle_new_order(session_id):

    if session_id in inprogress_orders:
        del inprogress_orders[session_id]

    if session_id in customer_details:
        del customer_details[session_id]

    if session_id in pending_quantity:
        del pending_quantity[session_id]

    return (
        "Your previous order has been cleared. "
        "What would you like to order?"
    )

def handle_remove_quantity(parameters, session_id): #partial removal

    item = parameters.get("food_item")
    qty = int(float(parameters.get("number")))

    if session_id not in inprogress_orders:
        return "Your order is empty."

    current_order = inprogress_orders[session_id]

    found_item = None

    for key in current_order:
        if key.lower() == item.lower():
            found_item = key
            break

    if not found_item:
        return f"{item} is not in your order."

    current_qty = current_order[found_item]

    if qty >= current_qty:
        del current_order[found_item]

        if len(current_order) == 0:
            return "Your order is now empty."

        return (
            f"Removed all {found_item}. "
            f"Remaining order: "
            f"{get_str_from_food_dict(current_order)}"
        )

    current_order[found_item] -= qty

    return (
        f"Removed {qty} {found_item}. "
        f"Remaining order: "
        f"{get_str_from_food_dict(current_order)}"
    )


def save_to_db(order):

    next_order_id = get_next_order_id()

    for food_item, quantity in order.items():

        print(
            "FOOD ITEM SENT TO MYSQL =",
            repr(food_item)
        )

        insert_order_item(
            food_item,
            quantity,
            next_order_id
        )

    insert_order_tracking(
        next_order_id,
        "in progress"
    )

    order_total = get_total_order_price(
        next_order_id
    )

    return next_order_id, order_total


@app.get("/")
def home():
    return {"message": "Food Ordering Chatbot API Running"}


@app.post("/webhook")
async def webhook(request: Request):

    print("\n===== WEBHOOK HIT =====")

    body = await request.json()

    print("FULL PAYLOAD:")
    print(body)

    query_result = body.get("queryResult", {})

    parameters = query_result.get("parameters", {})

    print("PARAMETERS:")
    print(parameters)

    intent_name = (
        query_result
        .get("intent", {})
        .get("displayName")
    )

    print("INTENT:", intent_name)

    session_id = extract_session_id(query_result)

    print("SESSION:", session_id)

    response = "Intent not handled."

    if intent_name == "PlaceOrder":
        response = handle_place_order(parameters, session_id)

    elif intent_name == "OrderItemIntent":
        response = handle_order_item(parameters, session_id)

    elif intent_name == "OrderRemove":
        response = handle_order_remove(parameters, session_id)

    elif intent_name == "ViewOrderIntent":
        response = handle_view_order(parameters, session_id)

    elif intent_name == "ConfirmOrderIntent":
        response = handle_confirm_order(parameters, session_id)

    elif intent_name == "AddressIntent":
        response = handle_address(parameters, session_id)

    elif intent_name == "PhoneNumberIntent":
        response = handle_phone_number(parameters, session_id)

    elif intent_name == "TrackOrderIDIntent":
        response = handle_track_order(parameters, session_id)

    elif intent_name == "Track coOrder":
        response = handle_track_order(parameters, session_id)

    elif intent_name == "QuantityIntent":
        response = handle_quantity(parameters, session_id)

    elif intent_name == "OrderCompleteIntent":
        response = handle_confirm_order(parameters, session_id)

    elif intent_name == "NewOrderIntent":
        response = handle_new_order(session_id)

    elif intent_name == "RemoveQuantityIntent":
        response = handle_remove_quantity(parameters,session_id)

    return {
        "fulfillmentText": response
    }