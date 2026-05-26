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

    def test_dev_index_contains_year_planning_view_from_screenshots(self):
        html = INDEX.read_text(encoding='utf-8')
        self.assertIn('id="yearPlanToggleBtn"', html)
        self.assertIn('id="yearPlanningView"', html)
        self.assertIn('Jahresplanung', html)
        for text in [
            'Erfolgsfragen',
            'Worüber bin ich zur Zeit in meinem beruflichen und in meinem privaten Leben am glücklichsten?',
            'Was motiviert mich am meisten?',
            'Was macht mich am selbstsichersten?',
            'Wem vertraue ich und wer vertraut mir?',
            'Was begeistert mich zur Zeit in meinem Leben am meisten?',
            'Worauf bin ich zur Zeit in meinem Leben am stolzesten?',
            'Wofür bin ich jetzt in meinem Leben am dankbarsten?',
            'Was genieße ich zur Zeit in meinem Leben am meisten?',
            'Wozu habe ich mich derzeit verpflichtet?',
            'Wen liebe ich, wer liebt mich?',
            'Inwieweit ist der heutige Tag eine Chance?',
            'Was habe ich heute/gestern gegeben?',
            'Wessen Tag habe ich bereichert?',
            'Was habe ich lernen dürfen?',
            'Wie hat der heutige/gestrige Tag mein Leben bereichert, und wie kann ich diesen Tag als ein Instrument für mein weiteres Leben nutzen?',
            'Worüber habe ich mich von Herzen gefreut?',
            'Der Kompass',
            'Identität',
            'Lebenssinn',
            'Mission-Statement',
            'Werte',
            'Glaubenssätze',
            'Leitsätze',
            'Lehren aus meiner Vergangenheit (2024)',
            'Meine größten Erfolge',
            'Die größten Erfolge meines Lebens',
        ]:
            self.assertIn(text, html)
        for field_id in [
            'year-success-question-1',
            'year-compass-identity',
            'year-guiding-principles',
            'year-lessons-past',
            'year-successes-2025',
            'year-life-successes',
        ]:
            self.assertIn(f'id="{field_id}"', html)

    def test_year_planning_uses_section_buttons_and_single_column_success_questions(self):
        html = INDEX.read_text(encoding='utf-8')
        self.assertIn('class="year-section-nav"', html)
        ordered_buttons = [
            'data-year-section="year-section-compass">Kompass',
            'data-year-section="year-section-guiding">Leitsätze',
            'data-year-section="year-section-success">Erfolgsfragen',
            'data-year-section="year-section-lessons">Lehren',
            'data-year-section="year-section-successes">Erfolge',
            'data-year-section="year-section-life-successes">Lebenserfolge',
        ]
        positions = [html.index(button) for button in ordered_buttons]
        self.assertEqual(positions, sorted(positions))
        for section_id in [
            'year-section-compass',
            'year-section-guiding',
            'year-section-success',
            'year-section-lessons',
            'year-section-successes',
            'year-section-life-successes',
        ]:
            self.assertIn(f'id="{section_id}"', html)
        self.assertNotIn('data-year-section="year-section-tips"', html)
        self.assertNotIn('id="year-section-tips"', html)
        self.assertIn('class="year-questions year-questions-single"', html)
        self.assertIn('function setYearPlanningSection', html)
        self.assertNotIn('data-year-section="year-section-lessons">Lehren 2024', html)
        self.assertNotIn('data-year-section="year-section-successes-2025">Erfolge 2025', html)

    def test_weekly_planning_contains_tips_as_callable_button(self):
        html = INDEX.read_text(encoding='utf-8')
        self.assertIn('id="weeklyTipsBtn"', html)
        self.assertIn('id="weeklyTipsPanel"', html)
        self.assertIn('id="closeWeeklyTipsBtn"', html)
        self.assertIn('function setWeeklyTipsVisible', html)
        self.assertIn('Tipps von Bodo Schäfer', html)
        self.assertLess(html.index('id="weeklyView"'), html.index('id="weeklyTipsBtn"'))
        self.assertLess(html.index('id="weeklyTipsBtn"'), html.index('id="weeklyTipsPanel"'))
        for text in [
            'Wie Du die Woche planst',
            'Lege die großen Steine zuerst hinein.',
            'So planst Du den Tag',
            'Schaue zurück auf den vorangegangenen Tag',
            'Checkliste für die Auswertung bzw. Reflexion der Woche',
            'Welche Ziele habe ich erreicht?',
            'Bin ich meinem Lebenssinn gefolgt?',
            'Habe ich mich als Experte positioniert bzw. habe ich an meiner Positionierungsstrategie gearbeitet?',
        ]:
            self.assertIn(text, html)

    def test_year_planning_long_text_blocks_have_full_page_textareas(self):
        html = INDEX.read_text(encoding='utf-8')
        self.assertIn('.year-full-page-textarea', html)
        for field_id in [
            'year-guiding-principles',
            'year-lessons-past',
            'year-successes-2025',
            'year-life-successes',
        ]:
            self.assertIn(f'id="{field_id}" class="year-full-page-textarea note-editor"', html)

    def test_note_blocks_are_auto_growing_editors_without_inner_scrollbar(self):
        html = INDEX.read_text(encoding='utf-8')
        self.assertIn('.note-editor {', html)
        self.assertIn('overflow-y: visible;', html)
        self.assertIn('contenteditable="true"', html)
        self.assertIn('function initRichTextEditors', html)
        self.assertIn('Object.defineProperty(editor, \'value\'', html)
        self.assertIn('initRichTextEditors();', html)
        self.assertNotIn('<textarea', html)

    def test_notes_do_not_have_custom_format_toolbar(self):
        html = INDEX.read_text(encoding='utf-8')
        self.assertNotIn('class="card format-toolbar"', html)
        self.assertNotIn('data-format-command="bold"', html)
        self.assertNotIn('data-format-command="italic"', html)
        self.assertNotIn('data-format-command="underline"', html)
        self.assertNotIn('function applyFormatCommand', html)
        self.assertNotIn('function initFormatToolbar', html)
        self.assertNotIn('document.execCommand(command, false, null)', html)
        self.assertNotIn('initFormatToolbar();', html)

    def test_main_view_contains_subtle_goal_buttons_and_separate_goal_pages(self):
        html = INDEX.read_text(encoding='utf-8')
        self.assertIn('id="dailyMainContent"', html)
        expected = [
            ('goalLong10', '10-Jahres-Ziele – Kurzfassung', 'openTenYearGoalsBtn', 'tenYearGoalsDetail', 'closeTenYearGoalsBtn'),
            ('goalMid25', '2–5-Jahres-Ziele – Kurzfassung', 'openMidTermGoalsBtn', 'midTermGoalsDetail', 'closeMidTermGoalsBtn'),
            ('goalShort1', '1-Jahres-Ziele – Kurzfassung', 'openShortTermGoalsBtn', 'shortTermGoalsDetail', 'closeShortTermGoalsBtn'),
        ]
        for summary_id, label, open_id, detail_id, close_id in expected:
            self.assertIn(f'id="{summary_id}"', html)
            self.assertIn(label, html)
            self.assertIn(f'id="{open_id}"', html)
            self.assertIn(f'id="{detail_id}"', html)
            self.assertIn(f'id="{close_id}"', html)
        self.assertGreaterEqual(html.count('class="subtle-open-btn"'), 3)
        for title in ['10-Jahres-Ziele', '2–5-Jahres-Ziele', '1-Jahres-Ziele']:
            self.assertIn(title, html)
        for field_id in ['goal10Date', 'goal10Being', 'goal10Doing', 'goal10Having', 'goalMidDate', 'goalMidBeing', 'goalMidDoing', 'goalMidHaving', 'goalShortDate', 'goalShortBeing', 'goalShortDoing', 'goalShortHaving']:
            self.assertIn(f'id="{field_id}"', html)
        for label in ['Datum', 'Sein:', 'Tun:', 'Haben:']:
            self.assertIn(label, html)
        self.assertIn('function openGoalDetail', html)
        self.assertIn('function closeGoalDetail', html)
        self.assertIn("dailyMainContent.style.display = isVisible ? 'none' : 'block'", html)
        for listener in ['openTenYearGoalsBtn.addEventListener', 'openMidTermGoalsBtn.addEventListener', 'openShortTermGoalsBtn.addEventListener', 'closeTenYearGoalsBtn.addEventListener', 'closeMidTermGoalsBtn.addEventListener', 'closeShortTermGoalsBtn.addEventListener']:
            self.assertIn(listener, html)

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
