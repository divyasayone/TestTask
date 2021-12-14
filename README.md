# TestProject - Events Management

A website for events publishing after stripe payement. .[refer](https://justdjango.com/blog/django-stripe-payments-tutorial)

## Requirements
1. python version
2. virtual environment
      Create/Activate the Django environment to run. 

   make sure that all wanted packages are installed and updated in activated env.
     ```
     Refer Requirements.txt
     pip install -r requirements.txt
     
    ```
3. Database and migrations
   check whether the DB connection credentials are correct in .env .
do pending migration if have any. (to affect the changes in DB).
4. stripe account and webhook order checkout status
   create stripe online simple payment account key,and config to .ENV file for furthur process
