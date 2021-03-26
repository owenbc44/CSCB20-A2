--Creating tables
CREATE TABLE IF NOT EXISTS students(
	susername VARCHAR(256) NOT NULL PRIMARY KEY,
	password VARCHAR(256) NOT NULL,
	sessionn VARCHAR(256)
	);
	
CREATE TABLE IF NOT EXISTS instructors(
	iusername VARCHAR(256) NOT NULL PRIMARY KEY,
	password VARCHAR(256) NOT NULL,
	sessionn VARCHAR(256)
	);
	
CREATE TABLE IF NOT EXISTS feedback(
	iusername VARCHAR(256) NOT NULL,
	question VARCHAR(256) NOT NULL,
	comment VARCHAR(256),
	FOREIGN KEY(iusername) REFERENCES instructors(iusername)
	);
	
CREATE TABLE IF NOT EXISTS marks(
	susername VARCHAR(256) NOT NULL,
	mark_id VARCHAR(256) NOT NULL,
	mark INTEGER NOT NULL,
	FOREIGN KEY(susername) REFERENCES students(susername),
	CHECK (mark_id IN ('Q1', 'Q2', 'Q3', 'Q4', 'A1', 'A2', 'A3', 'Final')),
	CHECK (value > -1 and value <101)
	);
	
CREATE TABLE IF NOT EXISTS remark_requests(
	susername VARCHAR(256) NOT NULL PRIMARY KEY,
	mark_id VARCHAR(256) NOT NULL,
	comment VARCHAR(256),
	FOREIGN KEY(susername) REFERENCES students(susername)
	);
	
--Inserting values

INSERT INTO students VALUES('student1', 'student1', 'LEC01');
INSERT INTO students VALUES('student2', 'student2', 'LEC02');
INSERT INTO students VALUES('student3', 'student3', 'LEC01');
INSERT INTO students VALUES('a', 'a', 'LEC02');

INSERT INTO instructors VALUES('instructor1', 'instructor1', 'LEC01');
INSERT INTO instructors VALUES('instructor2', 'instructor2', 'LEC02');
INSERT INTO instructors VALUES('instructor3', 'instructor3', 'LEC01');
INSERT INTO instructors VALUES('a', 'a', 'LEC02');

INSERT INTO feedback VALUES('instructor1', 'What do you like about the instructor teaching?', 'Nothing');
INSERT INTO feedback VALUES('instructor1', 'What do you recommend the instructor to do to improve their teaching?', 'I do not know');
INSERT INTO feedback VALUES('instructor1', 'What do you like about the labs?', 'Not sure, have not been');
INSERT INTO feedback VALUES('instructor1', 'What do you recommend the lab instructors to do to improve their lab teaching?', 'Give me a reason to attend');
INSERT INTO feedback VALUES('instructor1', 'What do you like about the instructor teaching?', 'Everything');
INSERT INTO feedback VALUES('instructor1', 'What do you like about the labs?', 'Love the labs');

INSERT INTO marks VALUES('a', 'Q1', 52);
INSERT INTO marks VALUES('a', 'Q2', 94);
INSERT INTO marks VALUES('a', 'Q3', 76);
INSERT INTO marks VALUES('a', 'Q4', 83);
INSERT INTO marks VALUES('a', 'A1', 62);
INSERT INTO marks VALUES('a', 'A2', 43);
INSERT INTO marks VALUES('a', 'A3', 94);
INSERT INTO marks VALUES('a', 'Final', 85);
INSERT INTO marks VALUES('student1', 'Q1', 100);
INSERT INTO marks VALUES('student1', 'Q2', 0);
INSERT INTO marks VALUES('student1', 'Q3', 75);
INSERT INTO marks VALUES('student1', 'Q4', 63);
INSERT INTO marks VALUES('student1', 'A1', 69);
INSERT INTO marks VALUES('student1', 'A2', 64);
INSERT INTO marks VALUES('student1', 'A3', 79);
INSERT INTO marks VALUES('student1', 'Final', 84);
INSERT INTO marks VALUES('student2', 'Q1', 10);
INSERT INTO marks VALUES('student2', 'Q2', 68);
INSERT INTO marks VALUES('student2', 'Q3', 74);
INSERT INTO marks VALUES('student2', 'Q4', 30);
INSERT INTO marks VALUES('student2', 'A1', 58);
INSERT INTO marks VALUES('student2', 'A2', 99);

INSERT INTO marks VALUES('student2', 'A2', 'my last answer was graded wrong');
INSERT INTO marks VALUES('student1', 'Q2', 'my first answer was graded wrong');
INSERT INTO marks VALUES('a', 'Final', 'question 4 was graded wrong because ...');
