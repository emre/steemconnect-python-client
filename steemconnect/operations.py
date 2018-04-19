import json

from .mixins import CustomJsonMixin


class Vote:

    def __init__(self, voter, author, permlink, percent):
        self.voter = voter
        self.author = author
        self.permlink = permlink
        self.weight = percent * 100

    def to_operation_structure(self):
        return [
            "vote", {
                "voter": self.voter,
                "author": self.author,
                "permlink": self.permlink,
                "weight": self.weight
            }
        ]


class Comment:

    def __init__(self, author, permlink, body, title=None,
                 parent_author=None, parent_permlink=None, json_metadata=None):
        self.author = author
        self.permlink = permlink
        self.body = body
        self.title = title
        self.parent_author = parent_author
        self.parent_permlink = parent_permlink
        self.json_metadata = json.dumps(json_metadata) if json_metadata else ''

    def to_operation_structure(self):
        return [
            "comment", {
                "parent_author": self.parent_author or "",
                "parent_permlink": "test",
                "author": self.author,
                "permlink": self.permlink,
                "title": self.title or "",
                "body": self.body,
                "json_metadata": self.json_metadata or "",
            }
        ]


class CommentOptions:

    def __init__(self, author=None, permlink=None, extensions=None,
                 allow_curation_rewards=None, max_accepted_payout=None,
                 percent_steem_dollars=None, allow_votes=True,
                 parent_comment=None):
        if parent_comment:
            self.author = parent_comment.author
            self.permlink = parent_comment.permlink
        else:
            self.author = author
            self.permlink = permlink
        self.extensions = extensions or "",
        self.allow_curation_rewards = allow_curation_rewards is True or False
        self.max_accepted_payout = max_accepted_payout or "1000.000 SBD"
        self.percent_steem_dollars = percent_steem_dollars or 10000
        self.allow_votes = allow_votes or True

    def to_operation_structure(self):
        return [
            "comment_options", {
                "author": self.author,
                "permlink": self.permlink or "",
                "allow_curation_rewards": self.allow_curation_rewards,
                "max_accepted_payout": self.max_accepted_payout,
                "percent_steem_dollars": self.percent_steem_dollars,
                "allow_votes": self.allow_votes,
            }
        ]


class DeleteComment:

    def __init__(self, author, permlink):
        self.author = author
        self.permlink = permlink

    def to_operation_structure(self):
        return [
            "delete_comment", {
                "author": self.author,
                "permlink": self.permlink
            }
        ]


class Follow(CustomJsonMixin):

    def __init__(self, follower, following):
        self.follower = follower
        self.following = following
        self.what = ["blog"]

    def to_operation_structure(self):
        return self.get_base_op_structure(
            [],
            [self.follower],
            "follow",
            ["follow", {
                "follower": self.follower,
                "following": self.following,
                "what": self.what,
            }]
        )


class Unfollow(Follow):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.what = []


class Mute(Follow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.what = ["ignore"]


class Resteem(CustomJsonMixin):

    def __init__(self, account, author, permlink):
        self.account = account
        self.author = author
        self.permlink = permlink

    def to_operation_structure(self):
        return self.get_base_op_structure(
            [],
            [self.account],
            "follow",
            ["reblog", {
                "account": self.account,
                "author": self.author,
                "permlink": self.permlink,
            }]
        )


class ClaimRewardBalance:

    def __init__(self, account, reward_steem, reward_sbd, reward_vests):
        self.account = account
        self.reward_steem = reward_steem
        self.reward_vests = reward_vests
        self.reward_sbd = reward_sbd

    def to_operation_structure(self):
        return [
            "claim_reward_balance", {
                "account": self.account,
                "reward_steem": self.reward_steem,
                "reward_sbd": self.reward_sbd,
                "reward_vests": self.reward_vests,
            }
        ]


class CustomJson(CustomJsonMixin):

    def __init__(self, required_auth, required_posting_auths,
                 custom_operation_id, structure):
        self.required_auth = required_auth
        self.required_posting_auths = required_posting_auths
        self.custom_operation_id = custom_operation_id
        self.structure = structure

    def to_operation_structure(self):
        return self.get_base_op_structure(
            self.required_auth,
            self.required_posting_auths,
            self.custom_operation_id,
            self.structure
        )
