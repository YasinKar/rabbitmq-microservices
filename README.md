# rabbitmq-microservices

Simple e-commerce backend built using a microservices architecture with rabbitmq message broker and JWT authentication.
backend includes a three services of products, orders and users.
project developed with Django and DRF

## Table of Contents
- [Introduction](#introduction)
- [Features](#features)
- [Installation](#installation)
- [Architecture](#architecture)

## Introduction
This project aims to more scalability in django projects by leveraging microservices architecture and django , I've built a simple e-commerce backend with django microservices structure.

## Features
- **Microservices Architecture**: Backend designed as microservices for improved scalability and maintainability. Each service has its own database.
- **JWT Authentication**: users authentication with JWT standard.
- **Rate Limit**: Limiting requests based on user authentication in apigateway.
- **Direct Access**: Application can only be accessed through apigateway and users cant access microservices directly for more security and comfort

## Installation
To set up this project, follow these steps:

1. **Clone the repository:**
   ```sh
   git clone https://github.com/YasinKar/rabbitmq-microservices.git
   cd rabbitmq-microservices
   ```

2. **Edit .env file**\
  Edit .env file necessary configurations

4. **Run with Docker Compose**
   ```sh
   docker-compose up --build
   ```

## Architecture
Our microservices architecture includes the following components:

1. **API Gateway**\
    It works as the main application and processes requests and sends them to services
2. **Users Service**\
    handling users authentication with JWT standard and users account management.
3. **Porducts Service**\
    handling products management and products inventory.
4. **Orders Service**\
    handling users order.