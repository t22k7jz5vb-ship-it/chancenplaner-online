
create table if not exists strategy_profiles (
  user_id uuid not null references auth.users(id) on delete cascade,
  id text not null default 'default',
  motto_langfristig text not null default '',
  fokus_woche text not null default '',
  identitaet text not null default '',
  lebenssinn_mission text not null default '',
  werte_rollen_glaubenssaetze text not null default '',
  langfristige_ziele_10_jahre text not null default '',
  mittelfristige_ziele_2_5_jahre text not null default '',
  kurzfristige_ziele_1_jahr text not null default '',
  prioritaeten_dieser_woche text not null default '',
  updated_at timestamptz not null default now(),
  primary key (user_id, id)
);

create table if not exists daily_entries (
  user_id uuid not null references auth.users(id) on delete cascade,
  entry_date date not null,
  tag_im_zyklus integer not null default 1,
  gesetz_index integer not null default 1,
  gesetz_titel text not null default '',
  gesetz_text text not null default '',
  chance_des_tages text not null default '',
  dankbarkeit text not null default '',
  wichtigste_aufgabe_602020 text not null default '',
  gesetz_heute_umsetzung text not null default '',
  erfolg_1 text not null default '',
  erfolg_2 text not null default '',
  erfolg_3 text not null default '',
  erfolg_4 text not null default '',
  erfolg_5 text not null default '',
  reflexion_aufgabe_status text not null default '',
  reflexion_aufgabe_warum text not null default '',
  reflexion_gesetz_status text not null default '',
  reflexion_gesetz_warum text not null default '',
  updated_at timestamptz not null default now(),
  primary key (user_id, entry_date)
);

alter table strategy_profiles enable row level security;
alter table daily_entries enable row level security;

drop policy if exists strategy_select_own on strategy_profiles;
drop policy if exists strategy_insert_own on strategy_profiles;
drop policy if exists strategy_update_own on strategy_profiles;
drop policy if exists strategy_delete_own on strategy_profiles;

create policy strategy_select_own on strategy_profiles for select using (auth.uid() = user_id);
create policy strategy_insert_own on strategy_profiles for insert with check (auth.uid() = user_id);
create policy strategy_update_own on strategy_profiles for update using (auth.uid() = user_id) with check (auth.uid() = user_id);
create policy strategy_delete_own on strategy_profiles for delete using (auth.uid() = user_id);

drop policy if exists entries_select_own on daily_entries;
drop policy if exists entries_insert_own on daily_entries;
drop policy if exists entries_update_own on daily_entries;
drop policy if exists entries_delete_own on daily_entries;

create policy entries_select_own on daily_entries for select using (auth.uid() = user_id);
create policy entries_insert_own on daily_entries for insert with check (auth.uid() = user_id);
create policy entries_update_own on daily_entries for update using (auth.uid() = user_id) with check (auth.uid() = user_id);
create policy entries_delete_own on daily_entries for delete using (auth.uid() = user_id);

create or replace function set_user_id_strategy_profiles()
returns trigger as $$
begin
  new.user_id := auth.uid();
  new.updated_at := now();
  return new;
end;
$$ language plpgsql security definer;

create or replace function set_user_id_daily_entries()
returns trigger as $$
begin
  new.user_id := auth.uid();
  new.updated_at := now();
  return new;
end;
$$ language plpgsql security definer;

drop trigger if exists trg_strategy_profiles_user on strategy_profiles;
create trigger trg_strategy_profiles_user
before insert or update on strategy_profiles
for each row execute function set_user_id_strategy_profiles();

drop trigger if exists trg_daily_entries_user on daily_entries;
create trigger trg_daily_entries_user
before insert or update on daily_entries
for each row execute function set_user_id_daily_entries();
