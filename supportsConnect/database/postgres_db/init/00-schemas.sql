-- connect to the correct db 
-- this name is determined in the docker-compose file
\connect supportsconnect_database

-- ALTER USER test PASSWORD 'test';
-- GRANT ALL PRIVILEGES ON DATABASE test TO test;

create domain EmailValue as
    varchar(100) check (value like '%@%.%');

create domain NameValue as varchar(20);

create domain RepetitionType as varchar(10)
    check (value in ('daily','weekly','monthly'));

create table Users (
    id                serial,
    email             EmailValue not null,
    givenName         NameValue not null,
    familyName        NameValue,
    date_of_birth     date,
    primary key (id)
);

create table Recipients (
    id                integer references Users(id),
    recipient_id      serial,
    address           varchar(50),
    primary key (id)
);

create table Support_workers (
    id                  integer references Users(id),
    support_worker_id   serial,
    primary key (id)
);

create table Connected_pairs (
    id                  serial,
    support_worker_id   integer references Support_workers(id),
    recipient_id        integer references Recipients(id),
    date_connected      date,
    primary key (id)
);

create table Appointments (
    id                  serial,
    connected_id        integer references Connected_pairs(id),
    available           boolean not null default true,
    start_time          timestamp not null,
    end_time            timestamp,
    duration            interval,
    repetition          RepetitionType,
    primary key (id)
);

create table Schedules (
    id                  serial,
    support_worker_id   integer references Support_workers(id),
    available_time      timestamp,
    primary key (id)
);

create table Reports (
    id                  serial,
    appointment_id      integer references Appointments(id),
    report_content      text,
    primary key (id)
);