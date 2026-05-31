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
            'Orientierungssätze',
            'Lehren aus meiner Vergangenheit (2024)',
            'Meine größten Erfolge',
            'Die größten Erfolge meines Lebens',
        ]:
            self.assertIn(text, html)
        self.assertNotIn('Wenn die Werte klar sind, fallen Entscheidungen leicht.', html)
        for field_id in [
            'year-success-question-1',
            'year-compass-identity',
            'year-guiding-principles',
            'year-lessons-past',
            'year-successes-2025',
            'year-life-successes',
        ]:
            self.assertIn(f'id="{field_id}"', html)
        self.assertNotIn('id="year-compass-beliefs"', html)

    def test_year_planning_uses_section_buttons_and_single_column_success_questions(self):
        html = INDEX.read_text(encoding='utf-8')
        self.assertIn('class="year-section-nav"', html)
        ordered_buttons = [
            'data-year-section="year-section-compass">Kompass',
            'data-year-section="year-section-guiding">Orientierungssätze',
            'data-year-section="year-section-success">Erfolgsfragen',
            'data-year-section="year-section-lessons">Lehren',
            'data-year-section="year-section-successes">Erfolge',
            'data-year-section="year-section-life-successes">Lebenserfolge',
            'data-year-section="year-section-helpful">Hilfreiches',
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
            'year-section-helpful',
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

    def test_year_planning_has_helpful_reference_section(self):
        html = INDEX.read_text(encoding='utf-8')
        self.assertIn('data-year-section="year-section-helpful">Hilfreiches', html)
        self.assertIn('id="year-section-helpful"', html)
        self.assertNotIn('Langfristige Orientierung, Erfolgsfragen und Jahresblöcke.', html)
        self.assertNotIn('Aus dem Ziele-Blatt: Datum, Sein, Tun und Haben. Die Kurzfassung steht auf der Hauptseite; hier ist die ausführliche Seite.', html)
        self.assertNotIn('.year-card .note-editor,', html)
        self.assertNotIn('.goal-detail-page input[type="text"] { background: rgba(255, 255, 255, 0.03); }', html)
        for title in ['Finanzen', 'Problemlösung', 'Angst', 'Beziehungen']:
            self.assertIn(f'<h3>{title}</h3>', html)
        for marker in [
            'von Bodo Schäfer',
            'Lege Deine Ziele fest.',
            'Überprüfe Deine Ziele.',
            'Was ist gut an diesem Problem?',
            'Solltest Du Angst haben',
            '24 goldene Regeln, um Menschen das zu geben, was sie brauchen',
            'Sende dem anderen still Deine besten Wünsche, wenn Du an ihn denkst.'
        ]:
            self.assertIn(marker, html)
        self.assertIn('class="helpful-section-grid"', html)
        self.assertIn('helpful-reference-card', html)

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

    def test_note_editors_are_italic_by_default(self):
        html = INDEX.read_text(encoding='utf-8')
        self.assertIn('.note-editor {', html)
        self.assertIn('font-style: italic;', html)

    def test_motto_and_focus_use_note_editors_instead_of_plain_text_inputs(self):
        html = INDEX.read_text(encoding='utf-8')
        self.assertIn('<label for="mottoLong">Motto: (langfr.)</label>', html)
        self.assertIn('<div id="mottoLong" class="note-editor" contenteditable="true"></div>', html)
        self.assertNotIn('<input id="mottoLong" type="text">', html)
        self.assertIn('<label for="focusWeek">Fokus: (diese Woche)</label>', html)
        self.assertIn('<div id="focusWeek" class="note-editor" contenteditable="true"></div>', html)
        self.assertNotIn('<input id="focusWeek" type="text">', html)

    def test_strategy_week_navigation_keeps_kw_label_and_arrows_together_on_the_right(self):
        html = INDEX.read_text(encoding='utf-8')
        self.assertIn('.weekly-focus-section { display: grid; gap: 12px; margin-top: 6px; padding: 16px; border: 1px solid var(--border); border-radius: 14px; background: rgba(255, 255, 255, 0.03); }', html)
        self.assertIn('.weekly-focus-header { display: flex; align-items: center; justify-content: space-between; gap: 12px; flex-wrap: wrap; }', html)
        self.assertIn('.weekly-focus-title { margin: 0; color: var(--accent); font-size: 1rem; }', html)
        self.assertIn('.week-block-nav { display: flex; align-items: center; justify-content: flex-end; gap: 10px; flex-wrap: wrap; margin-bottom: 0; }', html)
        self.assertIn('.week-block-nav .week-label-strong { font-size: 1rem; }', html)
        self.assertIn('.week-block-nav-actions { display: inline-flex; align-items: center; gap: 10px; }', html)
        self.assertIn('<h3 class="weekly-focus-title">Wochenfokus</h3>', html)
        self.assertIn('strategyWeekLabel.textContent = formatWeekLabel(weekStart);', html)
        self.assertNotIn('strategyWeekLabel.textContent = formatWeekRange(weekStart);', html)
        self.assertLess(html.index('class="weekly-focus-section"'), html.index('id="strategyWeekLabel"'))
        self.assertLess(html.index('id="strategyWeekLabel"'), html.index('id="strategyWeekPrevBtn"'))
        self.assertLess(html.index('id="strategyWeekPrevBtn"'), html.index('id="strategyWeekNextBtn"'))
        self.assertLess(html.index('id="strategyWeekNextBtn"'), html.index('id="mottoLong"'))

    def test_main_compass_fields_are_read_only_mirrors_of_year_planning(self):
        html = INDEX.read_text(encoding='utf-8')
        self.assertIn('<label for="identityBlock">Identität</label>', html)
        self.assertNotIn('<div class="meta">Bearbeitung in der Jahresplanung.</div>', html)
        self.assertIn('<div id="identityBlock" class="note-editor readonly-mirror" contenteditable="false"></div>', html)
        self.assertIn('<label for="purposeBlock">Lebenssinn</label>', html)
        self.assertIn('<div id="purposeBlock" class="note-editor readonly-mirror" contenteditable="false"></div>', html)
        self.assertIn('<label for="missionBlock">Mission-Statement</label>', html)
        self.assertIn('<div id="missionBlock" class="note-editor readonly-mirror" contenteditable="false"></div>', html)
        self.assertIn('<label for="valuesBlock">Werte</label>', html)
        self.assertIn('<div id="valuesBlock" class="note-editor readonly-mirror" contenteditable="false"></div>', html)
        self.assertIn('.readonly-mirror {', html)
        self.assertIn('background: rgba(255, 255, 255, 0.03)', html)
        self.assertIn('cursor: default;', html)
        self.assertIn('function syncMainCompassMirrors()', html)
        self.assertIn("fields.identityBlock.value = fields.yearCompassIdentity.value;", html)
        self.assertIn("fields.purposeBlock.value = fields.yearCompassPurpose.value;", html)
        self.assertIn("fields.missionBlock.value = fields.yearCompassMission.value;", html)
        self.assertIn("fields.valuesBlock.value = fields.yearCompassValues.value;", html)
        self.assertIn("['yearCompassIdentity', 'yearCompassPurpose', 'yearCompassMission', 'yearCompassValues'].forEach(key => {", html)

    def test_app_uses_fixed_standard_font_size_without_selector(self):
        html = INDEX.read_text(encoding='utf-8')
        self.assertIn('body { margin: 0;', html)
        self.assertIn('font-size: 1rem;', html)
        self.assertNotIn('--app-font-size', html)
        self.assertNotIn('id="fontSizeSelect"', html)
        self.assertNotIn('FONT_SIZE_STORAGE_KEY', html)
        self.assertNotIn('function applyFontSize(fontSize)', html)

    def test_success_fields_use_note_editors_instead_of_plain_text_inputs(self):
        html = INDEX.read_text(encoding='utf-8')
        for field_id, label in [
            ('success1', 'Erfolg 1'),
            ('success2', 'Erfolg 2'),
            ('success3', 'Erfolg 3'),
            ('success4', 'Erfolg 4'),
            ('success5', 'Erfolg 5'),
        ]:
            self.assertIn(f'<label for="{field_id}">{label}</label>', html)
            self.assertIn(f'<div id="{field_id}" class="note-editor" contenteditable="true"></div>', html)
            self.assertNotIn(f'<input id="{field_id}" type="text">', html)

    def test_autosave_waits_five_minutes_in_dev(self):
        html = INDEX.read_text(encoding='utf-8')
        self.assertIn('strategyAutosaveTimer = setTimeout(() => saveStrategy().catch(error => showStatus(`Fehler: ${error.message}`, true)), 300000);', html)
        self.assertIn('dailyAutosaveTimer = setTimeout(() => saveEntry().catch(error => showStatus(`Fehler: ${error.message}`, true)), 300000);', html)
        self.assertIn('weeklyAutosaveTimer = setTimeout(() => saveWeeklyEntry().catch(error => showStatus(`Fehler: ${error.message}`, true)), 300000);', html)
        self.assertNotIn(')), 300);', html)

    def test_strategy_week_fields_do_not_fallback_to_global_strategy_defaults(self):
        html = INDEX.read_text(encoding='utf-8')
        self.assertIn("fields.mottoLong.value = hasOwn('motto_langfristig') ? (entry.motto_langfristig || '') : '';", html)
        self.assertIn("fields.focusWeek.value = hasOwn('fokus_woche') ? (entry.fokus_woche || '') : '';", html)
        self.assertIn("fields.priorityWeek.value = hasOwn('prioritaeten_dieser_woche') ? (entry.prioritaeten_dieser_woche || '') : '';", html)
        self.assertNotIn("fields.mottoLong.value = hasOwn('motto_langfristig') ? (entry.motto_langfristig || '') : (strategyDefaults.motto_langfristig || '');", html)
        self.assertNotIn("fields.focusWeek.value = hasOwn('fokus_woche') ? (entry.fokus_woche || '') : (strategyDefaults.fokus_woche || '');", html)
        self.assertNotIn("fields.priorityWeek.value = hasOwn('prioritaeten_dieser_woche') ? (entry.prioritaeten_dieser_woche || '') : (strategyDefaults.prioritaeten_dieser_woche || '');", html)

    def test_daily_view_has_day_navigation_buttons_without_clear_button(self):
        html = INDEX.read_text(encoding='utf-8')
        for snippet in [
            'id="displayDate"',
            'id="weekLabel"',
            'id="todayBtn"',
            '>Heute</button>',
            'id="prevDayBtn"',
            '>←</button>',
            'id="nextDayBtn"',
            '>→</button>',
            'function shiftCurrentDate(days)',
            'function setCurrentDate(dateStr)',
            "prevDayBtn.addEventListener('click', () => shiftCurrentDate(-1).catch(error => showStatus(`Fehler: ${error.message}`, true)));",
            "todayBtn.addEventListener('click', () => setCurrentDate(todayString()).catch(error => showStatus(`Fehler: ${error.message}`, true)));",
            "nextDayBtn.addEventListener('click', () => shiftCurrentDate(1).catch(error => showStatus(`Fehler: ${error.message}`, true)));"
        ]:
            self.assertIn(snippet, html)
        self.assertNotIn('id="clearBtn"', html)
        self.assertNotIn('>Diesen Tag leeren</button>', html)
        self.assertNotIn("document.getElementById('clearBtn').addEventListener", html)
        self.assertLess(html.index('id="displayDate"'), html.index('id="weekLabel"'))
        self.assertLess(html.index('id="weekLabel"'), html.index('id="todayBtn"'))
        self.assertLess(html.index('id="todayBtn"'), html.index('id="prevDayBtn"'))
        self.assertLess(html.index('id="prevDayBtn"'), html.index('id="nextDayBtn"'))

    def test_goals_are_read_only_on_main_view_and_editable_in_year_planning(self):
        html = INDEX.read_text(encoding='utf-8')
        self.assertIn('<label for="goalLong10Mirror">10-Jahres-Ziele – Kurzfassung</label>', html)
        self.assertIn('<div id="goalLong10Mirror" class="note-editor readonly-mirror" contenteditable="false"></div>', html)
        self.assertIn('<label for="goalMid25Mirror">2–5-Jahres-Ziele – Kurzfassung</label>', html)
        self.assertIn('<div id="goalMid25Mirror" class="note-editor readonly-mirror" contenteditable="false"></div>', html)
        self.assertIn('<label for="goalShort1Mirror">1-Jahres-Ziele – Kurzfassung</label>', html)
        self.assertIn('<div id="goalShort1Mirror" class="note-editor readonly-mirror" contenteditable="false"></div>', html)
        self.assertNotIn('id="openTenYearGoalsBtn"', html)
        self.assertNotIn('id="openMidTermGoalsBtn"', html)
        self.assertNotIn('id="openShortTermGoalsBtn"', html)
        self.assertIn('data-year-section="year-section-compass">Kompass</button>', html)
        self.assertIn('data-year-section="year-section-goals">Ziele</button>', html)
        self.assertIn('data-year-section="year-section-guiding">Leitsätze</button>', html)
        self.assertLess(html.index('data-year-section="year-section-compass">Kompass</button>'), html.index('data-year-section="year-section-goals">Ziele</button>'))
        self.assertLess(html.index('data-year-section="year-section-goals">Ziele</button>'), html.index('data-year-section="year-section-guiding">Leitsätze</button>'))
        self.assertIn('id="year-section-goals"', html)
        for field_id in ['goalLong10', 'goal10Date', 'goal10Being', 'goal10Doing', 'goal10Having', 'goalMid25', 'goalMidDate', 'goalMidBeing', 'goalMidDoing', 'goalMidHaving', 'goalShort1', 'goalShortDate', 'goalShortBeing', 'goalShortDoing', 'goalShortHaving']:
            self.assertIn(f'id="{field_id}"', html)
        self.assertIn('function syncMainGoalMirrors()', html)
        self.assertIn("fields.goalLong10Mirror.value = fields.goalLong10.value;", html)
        self.assertIn("fields.goalMid25Mirror.value = fields.goalMid25.value;", html)
        self.assertIn("fields.goalShort1Mirror.value = fields.goalShort1.value;", html)
        self.assertIn("['goalLong10', 'goalMid25', 'goalShort1'].forEach(key => {", html)

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
