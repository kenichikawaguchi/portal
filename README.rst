======
Portal
======

This code is for writing a blog in Django and publishing it on the internet.
Thanks for checkint it out.

Installation
============

Below is the instruction for installing and setting up your app.

1. Clone the repo

.. code-block:: sh

  $ git clone https://github.com/kenichikawaguchi/portal.git
  $ cd portal
  $ python -m venv venv
  $ source venv/bin/activate

.. ***

2. Install pip packages

.. code-block:: sh

  (venv) $ pip install -r requirements.txt
  (venv) $ cd portalproject

.. ***

3. Enter your Email, Password, etc. in `.env`

.. code-block:: sh

  DEBUG=True (or False)
  HOSTS='<ALLOWED_HOSTS>'
  DB_USER='<DB_USER>'
  DB_PASSWORD='<DB_PASSWORD>'
  SECRET_KEY='<SECRET_KEY>'
  EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
  EMAIL_ADMIN=admin@example.com
  EMAIL_HOST=smtp.example.com
  EMAIL_PORT=587
  EMAIL_USE_TLS=True
  EMAIL_HOST_USER=admin@example.com
  DEFAULT_FROM_EMAIL=admin@example.com
  EMAIL_HOST_PASSWORD='admin_email_password'

.. ***

Preparation for REST API Access Authentication
============

Below is how to create Token for REST API.

1. Migrate

.. code-block:: sh

  $ python manage.py migrate

.. ***

2. Create Token

.. code-block:: sh

  $ python manage.py drf_create_token <username>

.. ***

3. Confirm your Token

.. code-block:: sh

  $ python manage.py shell

.. ***

.. code-block:: python

  from rest_framework.authtoken.models import Token
  Token.objects.all()

.. ***

Example of Post Blogpost
============

.. code-block:: python

  import requests

  # ===== Setting =====
  API_URL = "http://127.0.0.1:8000/api/blogpost/"  # API ENDPOINT
  TOKEN = "<your token here>"           # Token created with drf_create_token

  headers = {
      "Authorization": f"Token {TOKEN}",
      "Content-Type": "application/json",
  }

  # ===== Data for post =====
  data = {
      "title": "python script posting",
      "content": "This is an article posted from python script.",
      "category": 1  # If you need. Otherwise: None
  }

  # ===== POST Request =====
  response = requests.post(API_URL, json=data, headers=headers)

  # ===== Confirm the response =====
  if response.status_code == 201:
      print("Success")
      print(response.json())
  else:
      print("Failed")
      print(response.status_code, response.text)
.. ***

License
=======

Distributed under the MIT License. See `LICENSE.txt <./LICENSE>`_ for more information.
