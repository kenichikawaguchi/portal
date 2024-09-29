<a id="readme-top"></a>
<!-- ABOUT THE PROJECT -->
## About The Project

This code is for writing a blog in Django and publishing it on the internet.

### Built With

This section should list any major frameworks/libraries used to bootstrap your project. Leave any add-ons/plugins for the acknowledgements section. Here are a few examples.

* [![Django][django-shield]][django-url]
* [![Bootstrap][Bootstrap.com]][Bootstrap-url]


<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- GETTING STARTED -->
## Getting Started

This is an example of how you may utilize this project in your environment.

### Installation

_Below is the instruction for installing and setting up your app._

1. Clone the repo
  ```sh
  $ git clone https://github.com/kenichikawaguchi/portal.git
  $ cd portal
  ```
2. Install PyPy packages
  ```sh
  $ pip install -r requirements.txt
  $ cd portalproject
  ```
3. Enter your Email, Password, etc. in `.env`
  ```py
  DEBUG=True (or False)
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
  ```
<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[django-shield]: https://img.shields.io/badge/-Django-092E20.svg?style=for-the-badge&logo=django
[django-url]: https://www.djangoproject.com/

[product-screenshot]: images/screenshot.png
[Next.js]: https://img.shields.io/badge/next.js-000000?style=for-the-badge&logo=nextdotjs&logoColor=white
[Next-url]: https://nextjs.org/
[React.js]: https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB
[React-url]: https://reactjs.org/
[Vue.js]: https://img.shields.io/badge/Vue.js-35495E?style=for-the-badge&logo=vuedotjs&logoColor=4FC08D
[Vue-url]: https://vuejs.org/
[Angular.io]: https://img.shields.io/badge/Angular-DD0031?style=for-the-badge&logo=angular&logoColor=white
[Angular-url]: https://angular.io/
[Svelte.dev]: https://img.shields.io/badge/Svelte-4A4A55?style=for-the-badge&logo=svelte&logoColor=FF3E00
[Svelte-url]: https://svelte.dev/
[Laravel.com]: https://img.shields.io/badge/Laravel-FF2D20?style=for-the-badge&logo=laravel&logoColor=white
[Laravel-url]: https://laravel.com
[Bootstrap.com]: https://img.shields.io/badge/Bootstrap-563D7C?style=for-the-badge&logo=bootstrap&logoColor=white
[Bootstrap-url]: https://getbootstrap.com
[JQuery.com]: https://img.shields.io/badge/jQuery-0769AD?style=for-the-badge&logo=jquery&logoColor=white
[JQuery-url]: https://jquery.com
