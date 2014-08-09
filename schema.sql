drop table if exists users;
create table users (
        id integer primary key autoincrement,
        mc_user text not null,
        email text not null,
        server_hostname text not null,
        server_ip text not null,
        key text not null,
        play_time int not null,
        expires int not null
);
