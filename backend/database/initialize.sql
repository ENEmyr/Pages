create database pages;

use pages;

create table role (
    role_id bigint unsigned not null auto_increment,
    role varchar(300) not null,
    permission char(3) not null default '666',
    primary key (role_id)
);

create table user (
    user_id bigint unsigned not null auto_increment,
    email varchar(300) not null,
    password char(128) not null,
    password_salt char(50) not null,
    first_name varchar(300) not null,
    last_name varchar(300) not null,
    penname varchar(300) not null,
    gender char(1) not null default '0', /* 0 = male, 1 = female */
    role_id bigint unsigned not null, /* 0 = user, 1 = admin */
    image_url varchar(300) not null,
    create_dt datetime not null default CURRENT_TIMESTAMP,
    modified_dt datetime null default null,
    birthdate datetime null default null,
    rank integer not null default 0,
    primary key (user_id),
    foreign key (role_id) references role(role_id)
);

create table category (
    cate_id integer(5) unsigned zerofill not null auto_increment,
    name varchar(300) not null,
    primary key  (cate_id)
);

create table tag (
    tag_id integer(5) unsigned zerofill not null auto_increment,
    name varchar(300) not null,
    primary key  (tag_id)
);

create table page (
    page_id bigint unsigned not null auto_increment,
    user_id bigint unsigned not null,
    title varchar(300) not null,
    content text not null,
    create_dt datetime not null default CURRENT_TIMESTAMP,
    modified_dt datetime null default null,
    popularity integer not null default 0,
    primary key (page_id),
    foreign key (user_id) references user(user_id)
);

create table page_tags (
    page_id bigint unsigned not null,
    tag_id integer(5) unsigned zerofill,
    primary key (page_id, tag_id),
    foreign key (page_id) references page(page_id),
    foreign key (tag_id) references tag(tag_id)
);

create table page_cate (
    page_id bigint unsigned not null,
    cate_id integer(5) unsigned zerofill,
    primary key (page_id, cate_id),
    foreign key (cate_id) references category(cate_id),
    foreign key (page_id) references page(page_id)
);

create table user_followers (
    user_id bigint unsigned not null,
    follower_id bigint unsigned not null,
    primary key (user_id, follower_id),
    foreign key (user_id) references user(user_id),
    foreign key (follower_id) references user(user_id)
);

create table user_followings (
    user_id bigint unsigned not null,
    following_id bigint unsigned not null,
    primary key (user_id, following_id),
    foreign key (user_id) references user(user_id),
    foreign key (following_id) references user(user_id)
);

create table user_favorites (
    user_id bigint unsigned not null,
    page_id bigint unsigned not null,
    primary key (user_id, page_id),
    foreign key (user_id) references user(user_id),
    foreign key (page_id) references page(page_id)
);

create table log_type (
    log_type_id bigint unsigned not null auto_increment,
    detail text not null,
    primary key (log_type_id)
);

create table user_log (
    log_id bigint unsigned not null auto_increment,
    user_id bigint unsigned zerofill not null,
    log_type_id bigint unsigned not null,
    log_dt datetime not null default CURRENT_TIMESTAMP,
    primary key (log_id),
    foreign key  (user_id) references user(user_id),
    foreign key (log_type_id) references log_type(log_type_id)
);

alter database pages character set utf8 collate utf8_unicode_ci;
