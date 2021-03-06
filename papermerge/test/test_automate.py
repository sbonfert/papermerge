from django.contrib.auth import get_user_model
from django.test import TestCase
from papermerge.core.models import Automate, Folder

User = get_user_model()


TEXT = """
The majority of mortals, Paulinus, complain bitterly of the spitefulness of
Nature, because we are born for a brief span of life, because even this space
that has been granted to us rushes by so speedily and so swiftly that all save
a very few find life at an end just when they are getting ready to live.

Seneca - On the shortness of life
"""


class TestAutomateModel(TestCase):

    def setUp(self):
        self.user = User.objects.create_user('admin')

    def test_automate_match_literal(self):
        am_1 = _create_am_literal(
            "1",
            "Paulinus",
            self.user
        )
        am_2 = _create_am_literal(
            "2",
            "Cesar",
            self.user
        )
        self.assertTrue(
            am_1.is_a_match(TEXT)
        )
        self.assertFalse(
            am_2.is_a_match(TEXT)
        )

    def test_automate_match_all(self):
        # should match because all words occur in
        # text
        am_1 = _create_am_all(
            "1",
            "granted life rushes",
            self.user
        )
        # should not mach, because word quality
        # is not in TEXT
        am_2 = _create_am_all(
            "2",
            "granted life quality rushes",
            self.user
        )
        self.assertTrue(
            am_1.is_a_match(TEXT)
        )
        self.assertFalse(
            am_2.is_a_match(TEXT)
        )

    def test_automate_match_any(self):
        # should match by word 'granted'
        am_1 = _create_am_any(
            "1",
            "what if granted usecase test",
            self.user
        )
        # should not mach, of none of the words
        # is found in TEXT
        am_2 = _create_am_any(
            "2",
            "what if usecase test",
            self.user
        )
        self.assertTrue(
            am_1.is_a_match(TEXT)
        )
        self.assertFalse(
            am_2.is_a_match(TEXT)
        )

    def test_automate_match_regex(self):
        # should match by word life.
        am_1 = _create_am_any(
            "1",
            r"l..e",
            self.user
        )
        # should not mach, there no double digits
        # in the TEXT
        am_2 = _create_am_any(
            "2",
            r"\d\d",
            self.user
        )
        self.assertTrue(
            am_1.is_a_match(TEXT)
        )
        self.assertFalse(
            am_2.is_a_match(TEXT)
        )


def _create_am(name, match, alg, user, is_sensitive):
    dst_folder = Folder.objects.create(
        title="destination Folder",
        user=user
    )
    return Automate.objects.create(
        name=name,
        match=match,
        matching_algorithm=alg,
        is_case_sensitive=is_sensitive,  # i.e. ignore case
        user=user,
        dst_folder=dst_folder
    )


def _create_am_any(name, match, user):
    return _create_am(
        name=name,
        match=match,
        alg=Automate.MATCH_ANY,
        user=user,
        is_sensitive=False
    )


def _create_am_all(name, match, user):
    return _create_am(
        name=name,
        match=match,
        alg=Automate.MATCH_ALL,
        user=user,
        is_sensitive=False
    )


def _create_am_literal(name, match, user):
    return _create_am(
        name=name,
        match=match,
        alg=Automate.MATCH_LITERAL,
        user=user,
        is_sensitive=False
    )


def _create_am_regex(name, match, user):
    return _create_am(
        name=name,
        match=match,
        alg=Automate.MATCH_REGEX,
        user=user,
        is_sensitive=False
    )
