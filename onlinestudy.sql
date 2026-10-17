create database VIVAN_CH;
use VIVAN_CH;

create table instructor(
	i_id int primary key auto_increment,
    i_name varchar(50),
    i_email varchar(50),
    i_type varchar(50)
);
describe instructor;
create table student(
	s_id int primary key auto_increment,
    s_name varchar(50) not null,
    s_email varchar(50),
    s_course varchar(50)
);
describe student;
create table assessment(
	a_id int primary key auto_increment,
    a_marks int,
    a_type varchar(50)
);
describe assessment;
create table grade(
	g_no int primary key auto_increment,
    g_score float check(g_score>=6.0 || g_score<6.0)
);
describe grade;
create table submission(
	su_id int primary key auto_increment,
    su_date date,
    su_timestamp timestamp
);
describe submission;
create table fees(
	f_id int primary key auto_increment,
    f_amount int default '229000'
);
describe fees;
create table reciept(
	r_no int primary key auto_increment,
    r_date date,
    r_course varchar(50)
);
describe reciept;
create table teaching(
	i_type varchar(50) references instructor(i_type)
);
describe teaching;
create table nonteaching(
	i_type varchar(50) references instructor(i_type)
);
describe nonteaching;
alter table student add i_id int;
alter table student
add foreign key(i_id) references instructor(i_id);
describe student;
alter table submission add s_id int;
alter table submission
add foreign key(s_id) references student(s_id);
alter table submission add a_id int;
alter table submission
add foreign key(a_id) references assesment(a_id);
describe submission;
alter table grade add a_id int;
alter table grade
add foreign key(a_id) references assesment(a_id);
describe grade;
alter table fees add s_id int;
alter table fees
add foreign key(s_id) references student(s_id);
alter table reciept add s_id int;
alter table reciept
add foreign key(s_id) references student(s_id);
describe instructor;
describe teaching;
describe nonteaching;
describe student;
describe assessment;
describe submission;
describe grade;
describe fees;
describe reciept;