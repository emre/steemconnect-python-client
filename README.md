steemconnect-python-client is a simple yet powerful library to interact with the [Steemconnect](https://steemconnect.com). There was no *production ready* library for Python (Or I couldn't find it.) so I have decided to write my own.

SteemConnect V2 implements OAUTH standards. If you don't know about it, you can read the [SteemConnect wiki](https://github.com/steemit/steemconnect/wiki/OAuth-2) to learn the workflow and the token based authorization.

Also, you need to register your app into steemconnect before working with them. This will provide ```client_id``` and ```client_secret``` information which you will need to interact with the API.

<img src="https://s14.postimg.cc/keqd7rrht/Screen_Shot_2018-04-19_at_7.54.58_PM.png">
<center><sup>SteemConnect application management screen</sup></center>

#### Installation

```
$ (sudo) pip install steemconnect
```

#### Authorization Workflow

```
c = Client(
	client_id="app_name",
	client_secret="client_secret",
)
```

After getting the Client instance:

```
auth_url = c.get_login_url(
    "callback_url_to_your_app",
    "login,vote",
)
```

This will return a full login URL which you redirect users and after they login, you get the access_token in the query string with the specified callback url.

Access tokens has a limited lifetime, so if you need to refresh them in your own without authenticating the user again, you can add ```get_refresh_token=True``` parameter to this function.

If you set this as True, callback url will have a authorization code instead of an access token. With this code, you can ask access tokens first:

```
tokens = c.get_access_token(
    code,
) 
```

Example output:

```
 {
     'access_token': 'access_token_string',
     'expires_in': 604800,
     'username': 'emrebeyler',
     'refresh_token': 'refresh_token_string'
 }
```

As you can see, the lifetime of this token is 604800 seconds. After it expires, you can refresh it with ```refresh_access_token``` method.

```
c.refresh_access_token(
    access_token_response.get("refresh_token"),
    "login,vote" # scopes
)
```

#### Revoking the access token

This method revokes the passed access token.

```
self.c.revoke_token(tokens.get("access_token"))
```

#### SC2 api to interact with the chain

Once you get the access token, you can create a new Client instance with just access_token.

```
c = Client(
    access_token="access_token",
)
```

#### /me endpoint

This endpoint returns information about the authorized user.

```
print(c.me())
```

#### Updating user metadata

Updates the metadata of authorized user.

```
metadata = {
    "profile": {
        "name": "Emre", 
        "location": "Istanbul, Turkey",
        "about": "Developer, STEEM witness.",
        "profile_image": "http://foo.bar/image.png"
    }
}

resp = self.c.update_user_metadata(metadata)
```


#### /broadcast endpoint

All supported operations are located at the ```steemconnect.operations``` module.

##### Voting

```
vote = Vote("account", "author", "permlink", percent)
c.broadcast([vote.to_operation_structure()])
```

##### Creating a Comment

```
comment = Comment(
    "author",
    "permlink",
    "body",
    title="test title",
    json_metadata={"app":"foo/0.0.1"},
)
c.broadcast([comment.to_operation_structure()])

```

##### Creating a Comment with CommentOptions

```
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
	comment_options. comment.to_operation_structure()
])

```

##### Follow

```
follow = Follow("follower", "following")
c.broadcast([follow.to_operation_structure()])
```

##### Unfollow

```
unfollow = Unfollow("follower", "following")
c.broadcast([unfollow.to_operation_structure()])
```

##### Ignore

```
ignore = Mute("follower", "following")
c.broadcast([ignore.to_operation_structure()])
```

##### Resteem

```
resteem = Resteem("account", "author", "permlink")
c.broadcast([resteem.to_operation_structure()])
```

##### Claim Reward Balance

```
claim_reward_balance = ClaimRewardBalance('account', '0.000 STEEM', '1.500 SBD', '1132.996000 VESTS')
c.broadcast([claim_reward_balance.to_operation_structure()])
```

##### Delete Comment

```
delete_comment = DeleteComment(
    "author", "permlink"
)
c.broadcast([delete_comment.to_operation_structure()])
```

##### CustomJson

```
custom_json = CustomJson(
    required_auth,
    required_posting_auths,
    id
    json_structure,
)
c.broadcast([custom_json.to_operation_structure()])
```

#### Hot Signing Links

hot_sign() method creates a SteemConnect specific URL which you can redirect users and expect them 
to broadcast operations are not supported in the api. (transfer, create_delegation, etc.)

It has an optional **redirect_uri** parameter. If you pass that information, SteemConnect will redirect 
the user to that URL after the operation succeeds.

Example usage:

```
url = self.c.hot_sign(
    "transfer",
    {
        "to": "emreberyler",
        "amount": "0.001 SBD",
        "memo": "Donation",
    },
    redirect_uri="http://localhost"
)
```

This will generate [this URL](https://v2.steemconnect.com/sign/transfer?to=emrebeyler&amount=1+SBD&memo=Donation), (which sends 1 SBD to me with a memo as "Donation".)

