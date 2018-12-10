

steemconnect-python-client
======================================================

steemconnect-python-client is a simple **yet powerful** library to interact with the Steemconnect. Steemconnect
is a central-single sign on solution for steem based applications. It's considered a secure layer for certain
actions and backed by the Steemit inc.

Steemconnect implements Oauth2 for the authorization logic.

What can you do with this client?
----------

- Implementing Authorization/Authentication flow through OAuth
- Broadcasting supported operations to the STEEM blockchain with the user of your app.

Installation
-------------

steemconnect-python-client requires python3.6 and above. Even though it's easy to make it compatible
with lower versions, it's doesn't have support by design to keep the library simple.

You can install the library by typing to your console:

.. code-block:: bash

    $ (sudo) pip install steemconnect

After that, you can continue with  :doc:`/gettingstarted`.

Documentation Pages
-----------

.. toctree::
   :maxdepth: 5

   gettingstarted
   usingtheaccesstoken
   broadcast
   hot-signing
   example-flask-app

