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
.. ***

2. Install PyPy packages
.. code-block:: sh
  $ pip install -r requirements.txt
  $ cd portalproject
.. ***

3. Enter your Email, Password, etc. in `.env`
  - DEBUG=True (or False)
  - DB_USER='<DB_USER>'
  - DB_PASSWORD='<DB_PASSWORD>'
  - SECRET_KEY='<SECRET_KEY>'
  - EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
  - EMAIL_ADMIN=admin@example.com
  - EMAIL_HOST=smtp.example.com
  - EMAIL_PORT=587
  - EMAIL_USE_TLS=True
  - EMAIL_HOST_USER=admin@example.com
  - DEFAULT_FROM_EMAIL=admin@example.com
  - EMAIL_HOST_PASSWORD='admin_email_password'

License
=======

Distributed under the MIT License. See `LICENSE.txt` for more information.
