import logging
from unittest import skip
from unittest.mock import Mock

from django.test import TestCase
from splinter import Browser

from esea_scraper.management.commands.scrape_esea import identify_page_type, parse_gamepage
from esea_scraper.models import Game

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def set_up_browser_for_testing():
    browser = Browser('chrome', incognito=True, headless=False)
    browser.driver.set_window_size(640, 480)
    return browser


class TestPageTypeChecker(TestCase):
    def setUp(self):
        self.browser = set_up_browser_for_testing()

    def test_baseline_game_page_properly_identified(self):
        game_id = 14633571

        url = 'https://play.esea.net/match/{}'.format(game_id)
        self.browser.visit(url)
        page_type = identify_page_type(self.browser)

        self.assertEqual(page_type, Game.BASE)

    def test_game_page_with_match_recap_properly_identified(self):
        game_id = 14633572

        url = 'https://play.esea.net/match/{}'.format(game_id)
        self.browser.visit(url)
        page_type = identify_page_type(self.browser)

        self.assertEqual(page_type, Game.EXTENDED)

    def test_invalid_match_properly_identified(self):
        game_id = 14633573

        url = 'https://play.esea.net/match/{}'.format(game_id)
        self.browser.visit(url)
        page_type = identify_page_type(self.browser)

        self.assertEqual(page_type, Game.INVALID)

    def test_forfeit_match_properly_identified(self):
        game_id = 14633581

        url = 'https://play.esea.net/match/{}'.format(game_id)
        self.browser.visit(url)
        page_type = identify_page_type(self.browser)

        self.assertEqual(page_type, Game.FORFEIT)


class TestParseBaselineGamepage(TestCase):
    def setUp(self):
        self.browser = set_up_browser_for_testing()

    def test_base_scrape(self):
        game_id = 14633571
        url = 'https://play.esea.net/match/{}'.format(game_id)
        self.browser.visit(url)
        game_data = parse_gamepage(self.browser, Game.BASE)

        self.assertIn('A', game_data)
        self.assertIn('B', game_data)
        game_data_A = game_data['A']
        game_data_B = game_data['B']
        self.assertIn('score', game_data_A)
        self.assertIn('score', game_data_B)
        self.assertIn('players', game_data_A)
        self.assertIn('players', game_data_B)
        self.assertEquals(game_data_A['score'], 16)
        self.assertEquals(game_data_B['score'], 8)

        ren = game_data_A['players'][0]
        self.assertEquals(ren.name, 'RenZ')
        self.assertEquals(ren.rms, '13.86')
        self.assertEquals(ren._id, '1194196')
        self.assertEquals(ren.kills, '18')
        self.assertEquals(ren.deaths, '17')
        self.assertEquals(ren.headshot_p, '19.57')
        self.assertEquals(len(game_data_A['players']), 5)

        dj = game_data_B['players'][0]
        self.assertEquals(dj.name, 'djay')
        self.assertEquals(dj.rms, '9.51')
        self.assertEquals(dj._id, '441321')
        self.assertEquals(dj.kills, '27')
        self.assertEquals(dj.deaths, '17')
        self.assertEquals(dj.headshot_p, '22.97')
        self.assertEquals(len(game_data_A['players']), 5)


class TestParseExtendedGamepage(TestCase):
    def setUp(self):
        self.browser = set_up_browser_for_testing()

    def test_extended_scrape(self):
        game_id = 14633572
        url = 'https://play.esea.net/match/{}'.format(game_id)
        self.browser.visit(url)
        game_data = parse_gamepage(self.browser, Game.EXTENDED)

        # Mock('esea_scraper/management/commands/scrape_esea/get_team_players')

        self.assertIn('A', game_data)
        self.assertIn('B', game_data)
        game_data_A = game_data['A']
        game_data_B = game_data['B']
        self.assertIn('score', game_data_A)
        self.assertIn('score', game_data_B)
        self.assertIn('players', game_data_A)
        self.assertIn('players', game_data_B)
        self.assertEquals(game_data_A['score'], 16)
        self.assertEquals(game_data_B['score'], 11)

        ren = game_data_A['players'][0]
        self.assertEquals(ren.name, 'Volkh')
        self.assertEquals(ren.rms, '17.02')
        self.assertEquals(ren._id, '1770355')
        self.assertEquals(ren.kills, '28')
        self.assertEquals(ren.deaths, '15')
        self.assertEquals(ren.headshot_p, '11.96')
        self.assertEquals(len(game_data_A['players']), 5)

        dj = game_data_B['players'][0]
        self.assertEquals(dj.name, 'Znorux')
        self.assertEquals(dj.rms, '11.07')
        self.assertEquals(dj._id, '1064860')
        self.assertEquals(dj.kills, '21')
        self.assertEquals(dj.deaths, '20')
        self.assertEquals(dj.headshot_p, '17.65')
        self.assertEquals(len(game_data_A['players']), 5)


@skip
class TestParseForfeitedGamepage(TestCase):
    def setUp(self):
        self.browser = set_up_browser_for_testing()

    def test_forfeited_scrape(self):
        assert False,  'we definitely have"t written this yet'

