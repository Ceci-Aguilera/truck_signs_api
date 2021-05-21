# TRUCKS SIGNS DESIGNS WEBSITE

This website is to sell truck's signs.

## PAGES :
- Home Page (Show logos to sell)
- Order Page (Make Order)
- Order Summary Page (Show summary of order and Sell selected logo)
- Prices Page (Show prices of all products)
- How to (Show how to apply product on truck)
- Contact us (Show contact info and contact form)

## API INFO:
### Urls:
- url: http://domainName

    - On GET Request:

      The API returns a json file that contains an array of all trucks. The truck model that is sent to the frontend App has only two propieties:
        - 'single_image' => contains the absolute url of the truck image to be displayed.
        - 'pk' => the unique pk of each truck

    - When a truck is selected the user should be redirected to http://domainName/trucks-signs/create-order/pk to make the order. The pk prop is given in the json file.



- url: http://domainName/trucks-signs/products-price

  - On GET Request:

    The API returns a json file that contains an array of all products:
      - 'name_of_type_of_product' => The type of product
      - 'single_image' => contains the absolute url of the truck image to be displayed.
      - 'pk' => the unique pk of each truck

      - When a product is selected the user should be redirected to http://domainName/trucks-signs/create-order/pk to make the order. The pk prop is given in the json file.


- url: http://domainName/trucks-signs/create-order/pk

  - On Get Request:

    The Frontend App should provide the pk of truck to access this page and the Frontend App should also provide a form with the following parameters:

      - company name  (optional)
      - DOT Number  (optional)
      - Origin  (optional)
      - VIN Number  (optional)
      - Truck Number (optional)
      - Comments (Text that will only be sent if user wants email to ... is set to True)
      - Color of Product(pk of color)

      - user email
      - if user wants email to be sent to him (bool)
      - address of user (give two lines for this)
      - city
      - state
      - zipcode
      - country

      The Frontend App should only call the GET method after fetching possible product colors from http://domainName/trucks-signs/retrieve-product-colors, which returns the following json file

      [
        {

          "id": 1,
          "color_in_hex": "#000000",
          "color_nickname": "Black"

        },

        {

          .
          .
          .
        }

      ]

    - On POST Request:

      The Frontend App should submit the form as {

        'order' : form,
        'color': pk_of_color or 'None',

      }

      The API will return either the pk of the order or a Message of Error

      After Post request redirect user to http://domainName/trucks-signs/order-summary/pk if order pk is returned


- url: http://domainName/trucks-signs/order-summary/pk

      The API on GET method will return a json file with a summary of the order that includes:
      - user email
      - address of user (two lines)
      - city
      - state
      - zipcode
      - country
      - order_date_made
      - product type
      - total cost


    - On POST Request:

      The Fontend App should provide the following data:

      {

        'card_num':card_num,
        'exp_month':exp_month,
        'exp_year':exp_year,
        'cvc':cvc

      }

      This data is from the user credit card
      The API will return either:

      {'message':'Order Done'}

      or

      {'message':'Error in order'}



## INSTALLED PACKAGES:
- Django:
  - Rest Framework: pip3 install djangorestframework
  - Stripe: pip3 install stripe

## CHANGES TO MAKE TO DEPLOY:
- Create a default ColorModel obj and a PoductType Model before uploading any product
