import unittest

import responses

from steemconnect.client import Client
from steemconnect.operations import *


class TestClient(unittest.TestCase):

    def test_get_login_url(self):
        c = Client(
            "client_id"
            "client_secret"
        )

        self.assertEqual(
            c.get_login_url("http://localhost", "login"),
            "https://v2.steemconnect.com/oauth2/authorize?client_id"
            "=client_idclient_secret&redirect_uri=http%3A%2F%2Flocalh"
            "ost&scope=login")

    def test_get_login_url_override_defaults(self):
        c = Client(
            oauth_base_url="http://foo.bar/oauth2/",
            client_id="client_id",
            client_secret="client_secret"
        )

        self.assertEqual(
            c.get_login_url("http://localhost", "login"),
            "http://foo.bar/oauth2/authorize?client_id=client_id&"
            "redirect_uri=http%3A%2F%2Flocalhost&scope=login")

    @responses.activate
    def test_get_access_token(self):

        def request_callback(request):
            self.assertEqual(
                request.url,
                "https://v2.steemconnect.com/api/oauth2/token/")

            self.assertEqual(
                request.body,
                'grant_type=authorization_code&code=code&client_id='
                'client_id&client_secret=client_secret'
            )
            return 200, {}, json.dumps({"access_token": "foo"})

        c = Client(
            client_id="client_id",
            client_secret="client_secret"
        )
        responses.add_callback(
            responses.POST,
            'https://v2.steemconnect.com/api/oauth2/token/',
            callback=request_callback,
        )

        c.get_access_token("code")

    @responses.activate
    def test_refresh_access_token(self):

        def request_callback(request):
            self.assertEqual(
                request.url,
                "https://v2.steemconnect.com/api/oauth2/token/")

            self.assertEqual(
                request.body,
                'refresh_token=refresh_token&client_id=client_id&'
                'client_secret=client_secret&scope=login'
            )
            return 200, {}, json.dumps({"access_token": "foo"})

        c = Client(
            client_id="client_id",
            client_secret="client_secret"
        )
        responses.add_callback(
            responses.POST,
            'https://v2.steemconnect.com/api/oauth2/token/',
            callback=request_callback,
        )

        c.refresh_access_token("refresh_token", "login")

    @responses.activate
    def test_me(self):

        def request_callback(request):
            self.assertEqual(
                request.url,
                "https://v2.steemconnect.com/api/me/")

            return 200, {}, json.dumps({"access_token": "foo"})

        c = Client(
            access_token="foo"
        )
        responses.add_callback(
            responses.POST,
            'https://v2.steemconnect.com/api/me/',
            callback=request_callback,
        )

        c.me()

    def test_op_upvote(self):
        vote = Vote(
            "voter", "author", "permlink", 100)

        self.assertEqual(vote.voter, "voter")
        self.assertEqual(vote.author, "author")
        self.assertEqual(vote.permlink, "permlink")
        self.assertEqual(vote.weight, 10000)

    def test_op_downvote(self):
        vote = Vote(
            "voter", "author", "permlink", -50)

        self.assertEqual(vote.voter, "voter")
        self.assertEqual(vote.author, "author")
        self.assertEqual(vote.permlink, "permlink")
        self.assertEqual(vote.weight, -5000)

    def test_comment(self):
        comment = Comment(
            "author",
            "permlink",
            "body",
            title="title",
            json_metadata={"app": "testapp/0.0.1", "tags": ["test"]},
        )

        self.assertEqual(comment.author, "author")
        self.assertEqual(comment.permlink, "permlink")
        self.assertEqual(comment.body, "body")
        self.assertEqual(comment.title, "title")
        self.assertEqual(
            comment.json_metadata,
            json.dumps({"app": "testapp/0.0.1", "tags": ["test"]}))

    def test_comment_options(self):
        comment_options = CommentOptions(
            "author",
            "permlink",
            allow_curation_rewards=False,
        )

        self.assertEqual(comment_options.author, "author")
        self.assertEqual(comment_options.permlink, "permlink")
        self.assertEqual(
            comment_options.allow_curation_rewards, False)

    def test_comment_options_comment_injection(self):
        comment = Comment(
            "author",
            "permlink",
            "body",
            title="title",
            json_metadata={"app": "testapp/0.0.1", "tags": ["test"]},
        )

        comment_options = CommentOptions(
            parent_comment=comment,
            allow_curation_rewards=False,
        )

        self.assertEqual(comment_options.author, "author")
        self.assertEqual(comment_options.permlink, "permlink")
        self.assertEqual(
            comment_options.allow_curation_rewards, False)

    def test_delete_comment(self):
        delete_comment = DeleteComment(
            "author", "permlink"
        )

        self.assertEqual(delete_comment.author, "author")
        self.assertEqual(delete_comment.permlink, "permlink")

    def test_follow(self):
        follow = Follow("follower", "following")

        self.assertEqual(follow.follower, "follower")
        self.assertEqual(follow.following, "following")
        self.assertEqual(follow.what, ["blog",])

    def test_unfollow(self):
        unfollow = Unfollow("follower", "following")

        self.assertEqual(unfollow.follower, "follower")
        self.assertEqual(unfollow.following, "following")
        self.assertEqual(unfollow.what, [])

    def test_mute(self):
        ignore = Mute("follower", "following")

        self.assertEqual(ignore.follower, "follower")
        self.assertEqual(ignore.following, "following")
        self.assertEqual(ignore.what, ["ignore"])

    def test_reblog(self):
        resteem = Resteem("account", "author", "permlink")

        self.assertEqual(resteem.account, "account")
        self.assertEqual(resteem.author, "author")
        self.assertEqual(resteem.permlink, "permlink")

    def test_claim_reward_balance(self):
        claim_reward_balance = ClaimRewardBalance(
            'account', '0.000 STEEM', '1.500 SBD', '1132.996000 VESTS'
        )

        self.assertEqual(claim_reward_balance.account, "account")
        self.assertEqual(claim_reward_balance.reward_steem, "0.000 STEEM")
        self.assertEqual(claim_reward_balance.reward_sbd, "1.500 SBD")
        self.assertEqual(
            claim_reward_balance.reward_vests, "1132.996000 VESTS")

    def test_custom_json(self):

        custom_json = CustomJson(
            [],
            ["author"],
            "testcustomjson",
            {"foo": "<i>bar"}
        )

        self.assertEqual(custom_json.required_auth, [])
        self.assertEqual(custom_json.required_posting_auths, ["author"])
        self.assertEqual(custom_json.custom_operation_id, "testcustomjson")
        self.assertEqual(custom_json.structure, {"foo": "<i>bar"})


if __name__ == '__main__':
    unittest.main()