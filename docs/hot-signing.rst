
Hot signing
=================================

client's hot_sign() method creates a SteemConnect specific URL which you can redirect users and expect them
to broadcast operations are not supported in the api. (transfer, create_delegation, etc.)

.. function::  hot_sign(self, operation, params, redirect_uri=None):


   :param operation: String. Operation name. Ex: transfer.
   :param params: Dict. Operation data.
   :param redirect_uri: String. Optional. If you pass that, SteemConnect will redirect
the user to that URL after the operation succeeds.

Example: A transfer to emrebeyler with 1 SBD
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    url = self.c.hot_sign(
        "transfer",
        {
            "to": "emrebeyler",
            "amount": "1 SBD",
            "memo": "Donation",
        },
        redirect_uri="http://localhost"
    )
