create table wechatuser(id serial primary key,
 username varchar(50) not null,
   _password varchar(125) not null,
    _is_authenticated boolean default false,
    room_id varchar(100) not null);
create table message(
	id serial primary key,
	message text not null,
	room text not null,
	user_id integer references "wechatuser" (id) on delete cascade);
