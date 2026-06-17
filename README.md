Developed an NLP-based Food Ordering Chatbot using Dialogflow, FastAPI and MySQL

Overview

The  NLP-based Food Ordering Chatbot is a conversational restaurant ordering system that enables customers to place food orders, modify existing orders, provide delivery details, and track order status through natural language interactions.

The project uses Dialogflow for Natural Language Processing (NLP), FastAPI for backend services, and MySQL for data storage.

Features

Food Ordering:
Place food orders through chatbot
Add multiple food items
View current order
Remove food items from order
Start a new order
Manage incomplete orders

Customer Information:
Collect delivery address
Collect phone number
Store customer details in database

Order Tracking:
Generate unique order IDs
Track order status:
Maintain order history

Restaurant Information:
Store hours inquiry
Greeting and welcome messages
Thank you and conversation ending responses

Website Integration:
Responsive restaurant website
Embedded Dialogflow chatbot
Interactive menu display
Restaurant location information

Technologies Used:
Frontend
HTML5
CSS3
Dialogflow Messenger

Backend:
Python
FastAPI

Database:
MySQL

NLP Platform:
Dialogflow ES

Development Tools:
VS Code
Git
GitHub
ngrok


Project Architecture

User → Website → Dialogflow → FastAPI Webhook → MySQL Database

User interacts with chatbot.
Dialogflow identifies the intent.
Webhook request is sent to FastAPI.
FastAPI processes business logic.
MySQL stores and retrieves order data.
Response is returned to Dialogflow.
User receives the chatbot response.

Menu Items:
Pav Bhaji
Chole Bhature
Pizza
Mango Lassi
Masala Dosa
Biryani
Vada Pav
Rava Dosa
Samosa

Database Tables:
food_items:

Stores menu items and prices.

orders:

Stores ordered food items.

customer_details:

Stores delivery address and phone number.

order_tracking:

Stores order status information.

NLP Concepts Used
Intent Recognition:

The chatbot identifies user intentions such as:

Place Order
Add Item
Remove Item
View Order
Confirm Order
Track Order
Store Hours
New Order
Thank You

Entity Extraction
Extracts information such as:

Food Items
Quantity
Phone Number
Address
Order ID

Context Management
Maintains conversation flow using Dialogflow contexts.

Examples:

ongoing-order
awaiting-address
awaiting-phone
awaiting-orderid

Slot Filling
Automatically collects missing information required to complete an order.

API Endpoints
Home Endpoint:
GET /

Returns application status.

Webhook Endpoint:
POST /webhook

Handles Dialogflow requests and responses.


Installation

Clone Repository
git clone <repository-url>

Navigate to Project
cd food-ordering-chatbot

Create Virtual Environment
python -m venv venv

Activate Virtual Environment
venv\Scripts\activate

Install Dependencies
pip install -r requirements.txt

Run FastAPI Server
uvicorn main:app --reload

Configure ngrok
ngrok http 8000

Copy the generated HTTPS URL and configure it in Dialogflow Fulfillment.

Example:

https://abcd1234.ngrok-free.app/webhook
Running the Website

Open:

index.html

using Live Server in VS Code.

Sample Conversation

User:

I want 2 Pizza

Bot:

So far you have: 2 Pizza. Do you need anything else?

User:

No

Bot:

Please provide your delivery address.

User:

Patancheru Hyderabad

Bot:

Please provide your phone number.

User:

9876543210

Bot:

Awesome! Your order has been placed successfully.
Order ID: #48
Future Enhancements
Online payment gateway integration
Admin dashboard
Order cancellation feature
Customer feedback system
Real-time delivery tracking
Personalized recommendations
Partial quantity modification (e.g., remove 2 dosa)

Author
Yejjavarapu Chandini

B.Tech (ECE)

Malla Reddy Institute of Technology & Science (MRITS)

Project Outcome
This project demonstrates practical implementation of:

Natural Language Processing (NLP)
Conversational AI
FastAPI Backend Development
Database Integration
Web Development
API Integration
Session Management
End-to-End Chatbot Development