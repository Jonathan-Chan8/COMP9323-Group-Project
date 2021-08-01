-- connect to the correct db
-- this name is determined in the docker-compose file
\connect supportsconnect_database

-- ALTER USER test PASSWORD 'test';
-- GRANT ALL PRIVILEGES ON DATABASE test TO test;

-- table names are all plural and only the first letter is capitalized
-- use '_' to separate words in a table name
-- use 'camel case' in attribute names

create domain EmailValue as
    varchar(100) check (value like '%@%.%');

create domain NameValue as varchar(20);

create domain RepetitionType as varchar(10)
    check (value in ('daily','weekly','monthly'));

create domain Description as varchar(50);

create table Users (
    id                serial,
    email             EmailValue not null,
    password          varchar(20) not null,
    accountType       char(1) not null check (accountType in ('g', 'c', 'w')),  --guardian/client/worker
    firstName         NameValue not null,
    lastName          NameValue,
    dateOfBirth       date,
    age               integer,
    gender            varchar(6) check (gender in ('male','female','other')),
    contactNo         varchar(15),
    homeAddress       Description,
    shortBio          varchar(140),
    primary key (id)
);

create table Clients (
    id                integer references Users(id),
    asGuardian        boolean not null,
    address           Description not null,
    allergies         Description,
    likes             Description,
    dislikes          Description,
    healthNeeds       Description,
    primary key (id)
);

create table Support_workers (
    id                  integer references Users(id),
    languages           Description,
    interests           Description,
    primary key (id)
);

create table Work_histories  (
    id                serial,
    worker            integer references Support_workers(id),
    location          Description,
    startDate         date,
    endDate           date,
    primary key (id)
);

create table Trainings (
    id                serial,
    worker            integer references Support_workers(id),
    subject           NameValue,
    institution       NameValue,
    startDate         date,
    endDate           date,
    primary key (id)
);

create table Connected_pairs (
    id                  serial,
    supportWorkerId     integer references Support_workers(id),
    clientId            integer references Clients(id),
    dateConnected       date,
    primary key (id)
);

create table Shifts (
    id                  serial,
    connectedId         integer references Connected_pairs(id),
    shiftStatus         boolean not null default true,
    workerStatus        boolean not null default true,
    clientStatus        boolean not null default true,
    startTime           timestamp not null,
    endTime             timestamp,
    duration            interval,
    frequency           RepetitionType,
    primary key (id)
);

create table Activities (
    id                  serial,
    shift               integer references Shifts(id),
    location            Description,
    primary key (id)
);

create table Reports (
    id                  serial,
    activity            integer references Activities(id),
    mood                varchar(10) not null check (mood in ('Angry','Sad','Moderate','Happy','Hyperactive')),
    incident            boolean default false,
    incidentReport      text,
    sessionReport       text,
    primary key (id)
);
