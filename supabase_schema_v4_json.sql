-- V4-kompatibles Supabase-Schema ohne Funktionsreduktion
-- Speichert die bestehenden V4-Payloads 1:1 als JSONB,
-- damit die App nicht auf Mac-Python+SQLite angewiesen ist.

create extension if not exists pgcrypto;

create table if not exists strategy_profiles_v4 (
  user_id uuid not null references auth.users(id) on delete cascade,
  id text not null default 'default',
  data jsonb not null default '{}'::jsonb,
  updated_at timestamptz not null default now(),
  primary key (user_id, id)
);

create table if not exists daily_entries_v4 (
  user_id uuid not null references auth.users(id) on delete cascade,
  entry_date date not null,
  data jsonb not null default '{}'::jsonb,
  updated_at timestamptz not null default now(),
  primary key (user_id, entry_date)
);

create table if not exists weekly_entries_v4 (
  user_id uuid not null references auth.users(id) on delete cascade,
  week_start date not null,
  data jsonb not null default '{}'::jsonb,
  updated_at timestamptz not null default now(),
  primary key (user_id, week_start)
);

alter table strategy_profiles_v4 enable row level security;
alter table daily_entries_v4 enable row level security;
alter table weekly_entries_v4 enable row level security;

drop policy if exists strategy_v4_select_own on strategy_profiles_v4;
drop policy if exists strategy_v4_insert_own on strategy_profiles_v4;
drop policy if exists strategy_v4_update_own on strategy_profiles_v4;
drop policy if exists strategy_v4_delete_own on strategy_profiles_v4;

create policy strategy_v4_select_own on strategy_profiles_v4 for select using (auth.uid() = user_id);
create policy strategy_v4_insert_own on strategy_profiles_v4 for insert with check (auth.uid() = user_id);
create policy strategy_v4_update_own on strategy_profiles_v4 for update using (auth.uid() = user_id) with check (auth.uid() = user_id);
create policy strategy_v4_delete_own on strategy_profiles_v4 for delete using (auth.uid() = user_id);

drop policy if exists daily_v4_select_own on daily_entries_v4;
drop policy if exists daily_v4_insert_own on daily_entries_v4;
drop policy if exists daily_v4_update_own on daily_entries_v4;
drop policy if exists daily_v4_delete_own on daily_entries_v4;

create policy daily_v4_select_own on daily_entries_v4 for select using (auth.uid() = user_id);
create policy daily_v4_insert_own on daily_entries_v4 for insert with check (auth.uid() = user_id);
create policy daily_v4_update_own on daily_entries_v4 for update using (auth.uid() = user_id) with check (auth.uid() = user_id);
create policy daily_v4_delete_own on daily_entries_v4 for delete using (auth.uid() = user_id);

drop policy if exists weekly_v4_select_own on weekly_entries_v4;
drop policy if exists weekly_v4_insert_own on weekly_entries_v4;
drop policy if exists weekly_v4_update_own on weekly_entries_v4;
drop policy if exists weekly_v4_delete_own on weekly_entries_v4;

create policy weekly_v4_select_own on weekly_entries_v4 for select using (auth.uid() = user_id);
create policy weekly_v4_insert_own on weekly_entries_v4 for insert with check (auth.uid() = user_id);
create policy weekly_v4_update_own on weekly_entries_v4 for update using (auth.uid() = user_id) with check (auth.uid() = user_id);
create policy weekly_v4_delete_own on weekly_entries_v4 for delete using (auth.uid() = user_id);

create or replace function set_user_id_and_updated_at_v4()
returns trigger as $func$
begin
  new.user_id := auth.uid();
  new.updated_at := now();
  return new;
end;
$func$ language plpgsql security definer;

drop trigger if exists trg_strategy_profiles_v4_user on strategy_profiles_v4;
create trigger trg_strategy_profiles_v4_user
before insert or update on strategy_profiles_v4
for each row execute function set_user_id_and_updated_at_v4();

drop trigger if exists trg_daily_entries_v4_user on daily_entries_v4;
create trigger trg_daily_entries_v4_user
before insert or update on daily_entries_v4
for each row execute function set_user_id_and_updated_at_v4();

drop trigger if exists trg_weekly_entries_v4_user on weekly_entries_v4;
create trigger trg_weekly_entries_v4_user
before insert or update on weekly_entries_v4
for each row execute function set_user_id_and_updated_at_v4();
