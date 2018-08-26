
Using access tokens
=================================

Once you get the access token, you can create a new Client instance with just access_token.

.. code-block:: python

    c = Client(
        access_token="<access_token>",
    )


Getting authorized user's information
~~~~~~~~~~~~~~~~~~~~~~~~~~

This api call gives information about the authorized user.

.. code-block:: python

    print(c.me())


Updating user profile (metadata)
~~~~~~~~~~~~~~~~~~~~~~~~~~


.. code-block:: python

    metadata = {
        "profile": {
            "name": "Emre",
            "location": "Istanbul, Turkey",
            "about": "Developer, STEEM witness.",
            "profile_image": "http://foo.bar/image.png"
        }
    }

    resp = c.update_user_metadata(metadata)


Broadcasting operations
~~~~~~~~~~~~~~~~~~~~~~~~~~

It's possible to

- vote a post
- create a post/comment
- follow/unfollow/ignore/resteem
- claim reward balance
- delete comment
- create custom jsons

via steemconnect's broadcast apis.


.. note::
    All operations live inside the **steemconnect.operations** module. You need to import the corresponding classes before using them.


Voting for a post
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    vote = Vote("account", "author", "permlink", percent)
    c.broadcast([vote.to_operation_structure()])

Creating a comment/post
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    comment = Comment(
        "author",
        "permlink",
        "body",
        title="test title",
        json_metadata={"app":"foo/0.0.1"},
    )
    c.broadcast([comment.to_operation_structure()])

Creating a comment/post with CommentOptions
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    comment = Comment(
        "author",
        "permlink",
        "body",
        title="test title",
        json_metadata={"app":"foo/0.0.1"},
    )

    comment_options = CommentOptions(
          parent_comment=comment,
        allow_curation_rewards=False,
    )

    c.broadcast([
        comment.to_operation_structure(),
        comment_options.to_operation_structure()
    ])



Follow an account
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    follow = Follow("follower", "following")
    c.broadcast([follow.to_operation_structure()])


Unfollow an account
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    unfollow = Unfollow("follower", "following")
    c.broadcast([unfollow.to_operation_structure()])

Mute an account
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    ignore = Mute("follower", "following")
    c.broadcast([ignore.to_operation_structure()])


Resteem a post
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    resteem = Resteem("account", "author", "permlink")
    c.broadcast([resteem.to_operation_structure()])


Claim reward balance
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    claim_reward_balance = ClaimRewardBalance('account', '0.000 STEEM', '1.500 SBD', '1132.996000 VESTS')
    c.broadcast([claim_reward_balance.to_operation_structure()])

Delete comment
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    delete_comment = DeleteComment(
        "author", "permlink"
    )
    c.broadcast([delete_comment.to_operation_structure()])

Create custom jsons
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    custom_json = CustomJson(
        required_auth,
        required_posting_auths,
        id
        json_structure,
    )
    c.broadcast([custom_json.to_operation_structure()])

