import unittest
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
INDEX = BASE / 'index.html'
CONFIG = BASE / 'config.example.js'
SCHEMA = BASE / 'supabase_schema_v4_json.sql'


class OnlineArtifactsTests(unittest.TestCase):
    def test_required_files_exist(self):
        self.assertTrue(INDEX.exists(), 'index.html fehlt')
        self.assertTrue(CONFIG.exists(), 'config.example.js fehlt')
        self.assertTrue(SCHEMA.exists(), 'supabase_schema_v4_json.sql fehlt')

    def test_index_contains_v4_auth_and_supabase_hooks(self):
        html = INDEX.read_text(encoding='utf-8')
        self.assertIn('supabase.createClient', html)
        self.assertIn('id="loginForm"', html)
        self.assertIn('id="logoutBtn"', html)
        self.assertIn('id="appShell"', html)
        self.assertIn("strategy_profiles_v4", html)
        self.assertIn("daily_entries_v4", html)
        self.assertIn("weekly_entries_v4", html)
        self.assertIn('auth.onAuthStateChange', html)
        self.assertIn('Woche planen', html)
        self.assertNotIn("fetch('/api/strategy'", html)
        self.assertNotIn("fetch('/api/entries/", html)
        self.assertNotIn("fetch('/api/weekly/", html)

    def test_config_has_placeholders(self):
        js = CONFIG.read_text(encoding='utf-8')
        self.assertIn('YOUR_SUPABASE_URL', js)
        self.assertIn('YOUR_SUPABASE_ANON_KEY', js)

    def test_schema_has_v4_auth_bound_tables(self):
        sql = SCHEMA.read_text(encoding='utf-8').lower()
        self.assertIn('create table if not exists strategy_profiles_v4', sql)
        self.assertIn('create table if not exists daily_entries_v4', sql)
        self.assertIn('create table if not exists weekly_entries_v4', sql)
        self.assertIn('auth.uid()', sql)
        self.assertIn('jsonb not null default', sql)


if __name__ == '__main__':
    unittest.main()
