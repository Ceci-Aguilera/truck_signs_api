# Trucks Signs API

#### Table of Contents
* [Overview](#overview)
* [Models explained](#models)
* [Views explained](#views)


### <a name="overview"></a> Overview
This Website API uses : Django Rest Framework, Stripe (for payment management), and the PostgreSQL database
This is a simple website to sell truck signs, the main page should show some logos examples and extra info:
![image info](./.readme-assets/Web-Home.jpg)


### <a name="models"></a> Models

The **Category Model** is to classify the products, so far the available classifications are Truck Logo, Side One Lettering, Fire Extinguisher Logo, and Number Logo.
Each **Category** has its own particular number of lettering lines and the price of a lettering line depends on the lettering line type. Also the final product's price is based on the amount of lettering lines, hence the necessity for the models **LetteringItemCategory** and **ProductVariation**.

A **ModelsNameVariation** is **ModelName** with extra attributes, and so the **ProductVariation** model is a **Product** model with the extra attributes the customer will choose.


### <a name="models"></a> Views
