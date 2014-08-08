drop table if exists users;
create table users (
        id integer primary key autoincrement;
        mc_user text not null,
        email text not null,
        
);
