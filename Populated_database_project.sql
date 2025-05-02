show databases;
Drop database if exists Project;
CREATE DATABASE Project;
USE Project;

-- Strong Entities
CREATE TABLE Student(
	StudentID VARCHAR(10) PRIMARY KEY,
    StudentFirstName VARCHAR(100),
    StudentLastName VARCHAR(100),
    Gender VARCHAR(20),
    YearGroup INT,
    Scholarship_Status VARCHAR(10)
);

CREATE TABLE Hostel(
	HostelID INT PRIMARY KEY,
    HostelName VARCHAR(20),
    Num_of_rooms INT,
    location VARCHAR(15)
);

CREATE TABLE Hostel_Manager(
	ManagerId INT PRIMARY KEY,
    ManagerFirstName VARCHAR(100),
    ManagerLastName VARCHAR(100),
    Manager_Password VARCHAR(15) NOT NULL,
    Hostel_id INT,
    FOREIGN KEY (Hostel_id) REFERENCES Hostel(HostelID)
);

CREATE TABLE Room(
	RoomID VARCHAR(7) PRIMARY KEY,
    Room_No INT,
    max_occupants INT,
    num_of_occupants INT,
    Hostel_id INT,
	FOREIGN KEY (Hostel_id) REFERENCES Hostel(HostelID)
);

CREATE TABLE Payment(
	PaymentID INT PRIMARY KEY,
    Amount INT,
    payment_status VARCHAR(10),
    payment_date DATE,
    Student_id VARCHAR(10),
    Hostel_id INT,
    FOREIGN KEY (Hostel_id) REFERENCES Hostel(HostelID),
    FOREIGN KEY (Student_id) REFERENCES Student(StudentID)
);

CREATE TABLE Administration(
	AdminID VARCHAR(5) PRIMARY KEY,
    AdminFirstName VARCHAR(50),
    AdminLastName VARCHAR(50),
    AdminContact VARCHAR(10),
    admin_password VARCHAR(10) NOT NULL
);

-- Weak Entities
CREATE TABLE Reports(
	ReportID INT PRIMARY KEY,
    type_of_report VARCHAR(20),
    Descr VARCHAR(400),
    report_status VARCHAR(20),
    Student_id VARCHAR(10),
    Hostel_id INT,
    FOREIGN KEY (Hostel_id) REFERENCES Hostel(HostelID),
    FOREIGN KEY (Student_id) REFERENCES Student(StudentID)
);

CREATE TABLE Booking(
	Booking_id VARCHAR(7) PRIMARY KEY,
    Student_id VARCHAR(10),
    Hostel_id INT,
    Room_id VARCHAR(7),
    FOREIGN KEY (Hostel_id) REFERENCES Hostel(HostelID),
    FOREIGN KEY (Student_id) REFERENCES Student(StudentID),
    FOREIGN KEY (Room_id) REFERENCES Room(RoomID)
);

CREATE TABLE Roommate_Preference(
	Preference_id VARCHAR(5) PRIMARY KEY,
	student_id VARCHAR(10) NOT NULL,
    study_preference VARCHAR(100), -- Preferred study habits (quiet, soft music, group study)  
    social_preference VARCHAR(100), -- Social habits (introvert, extrovert, amibivert)  
    noise_level VARCHAR(50), -- Desired noise level (quiet, moderate, lively)    
	preferred_roommate_id VARCHAR(10),
    FOREIGN KEY (preferred_roommate_id) REFERENCES Student(StudentID),
    FOREIGN KEY (student_id) REFERENCES Student(StudentID)
);
SELECT * FROM Student;
SHOW TABLES;
-- DUMMY DATA
INSERT INTO Student (StudentID, StudentFirstName, StudentLastName, Gender, YearGroup, Scholarship_Status) VALUES
	(23412027, 'Nana Daasebre', 'Kwaku', 'Male', 2027, 'Yes'),
	(23232026, 'Kwame','Yirenkyi', 'Male', 2026, 'Yes'),
	(33352027, 'Seyram','Apreku', 'Female', 2027, 'No'),
	(11112027, 'Jasmine','Akuaku', 'Female', 2027, 'No'),
	(22992025, 'Wilson','Dangote', 'Male', 2025, 'Yes'),
	(33472027, 'Eugene','Amonoo-Neizer', 'Male', 2027, 'Yes'),
	(21122026, 'Addobea', 'Taylor', 'Female', 2026, 'No'),
	(11772025, 'Jennifer','Anderson', 'Female', 2025, 'No'),
	(20032025, 'William','Owusu', 'Male', 2025, 'No'),
	(90092025, 'Elizabeth','Martinez', 'Female', 2025, 'Yes'),
	(98892025, 'Michael','Boakye', 'Male', 2025, 'Yes'),
	(98892028, 'Ryan','Antwi', 'Male', 2028, 'No'),
	(96692028, 'Amber','Rose', 'Female', 2028, 'Yes'),
	(91112025, 'Diddiella','Arthur', 'Female', 2025, 'No');

-- Hostel first (no dependencies)
INSERT INTO Hostel (HostelID, HostelName, Num_of_rooms, location) VALUES
	(1, 'Wangari Mathaii',50,'On-Campus'),
	(2,'Old Masere',35,'Off-Campus'),
	(3,'Dufie Annex',62,'Off-Campus'),
	(4,'Old Hosanna', 74,'Off-Campus'),
	(5,'New Hosanna','102','Off-Campus'),
	(6,'Columbiana',25,'Off-Campus'),
	(7,'Lambert',12,'Off-Campus'),
	(8,'Tankos Apartment',35,'Off-Campus'),
	(9,'New Masere',72,'Off-Campus'),
	(10,'Dufie Hostel',200, 'Off-Campus'),
	(11,'Charlotte Courts',109,'Off-Campus'),
	(12, 'Ceewus',23,'Off-Campus'),
	(13, 'Hill-Side',57,'Off-Campus'),
	(14,'Oteng-Korankye',41,'On-Campus'),
	(15,'Esther-Sutherland',24,'On-Campus'),
	(16, 'Kofi Tawiah', 32,'On-Campus');

-- Hostel Managers (depends on Hostel)
INSERT INTO Hostel_Manager (ManagerId, ManagerFirstName, ManagerLastName, Manager_Password, Hostel_id) VALUES
	(101,'Kwame','Bempah','bemp4life',14),
	(102,'Rhys','Oppong','iluvfeyre',5),
	(103,'Jeremy','Norman','40inchbelt',11),
	(104,'Ben','Changdar','benito44',15),
	(105,'Danita','Sharon','sannyboo',12),
	(106,'Michael','Martey','viniciusss',7),
	(107,'Opoku','Ware', 'opoksft',3),
	(108,'Jescaps','Allotey','aloletiii',8),
	(109,'Maha','Sangham','singangm',9),
	(110,'Shaun','Quamena','shaunreigns',4),
	(111,'Clement','Nyarko','clemsnyanya',1),
	(112,'Joan','Boateng','jbreeeze',2),
	(113,'Christable','Opoku','chrissyluv',6),
	(114,'Jacob','Armah','amynotinaf',10),
	(115,'Kevin','Frimpong','frimpskev',13),
	(116,'Chairman','Agbozo','agbochair',16);

-- Rooms (depends on Hostel)
INSERT INTO Room (RoomID, Room_No, max_occupants, num_of_occupants, Hostel_id) VALUES  
	-- HostelID 1  
	(1001, 101, 2, 1, 1),  
	(1002, 102, 2, 2, 1),  
	(1003, 103, 2, 1, 1),  
	(1004, 104, 3, 2, 1),  
	(1005, 105, 3, 3, 1),  
	(1006, 106, 4, 2, 1),  
	(1007, 107, 2, 1, 1),  
	(1008, 108, 4, 4, 1),  
	(1009, 109, 3, 2, 1),  
	(1010, 110, 2, 0, 1),  
	-- HostelID 2  
	(1011, 201, 2, 1, 2),  
	(1012, 202, 2, 2, 2),  
	(1013, 203, 2, 1, 2),  
	(1014, 204, 3, 2, 2),  
	(1015, 205, 3, 3, 2),  
	(1016, 206, 4, 2, 2),  
	(1017, 207, 2, 1, 2),  
	(1018, 208, 4, 4, 2),  
	(1019, 209, 3, 2, 2),  
	(1020, 210, 2, 0, 2),  
	-- HostelID 3  
	(1021, 301, 2, 1, 3),  
	(1022, 302, 2, 2, 3),  
	(1023, 303, 2, 1, 3),  
	(1024, 304, 3, 2, 3),  
	(1025, 305, 3, 3, 3),  
	(1026, 306, 4, 2, 3),  
	(1027, 307, 2, 1, 3),  
	(1028, 308, 4, 4, 3),  
	(1029, 309, 3, 2, 3),  
	(1030, 310, 2, 0, 3),  
	-- HostelID 4  
	(1031, 401, 2, 1, 4),  
	(1032, 402, 2, 2, 4),  
	(1033, 403, 2, 1, 4),  
	(1034, 404, 3, 2, 4),  
	(1035, 405, 3, 3, 4),  
	(1036, 406, 4, 2, 4),  
	(1037, 407, 2, 1, 4),  
	(1038, 408, 4, 4, 4),  
	(1039, 409, 3, 2, 4),  
	(1040, 410, 2, 0, 4),  
	-- HostelID 5  
	(1041, 501, 2, 1, 5),  
	(1042, 502, 2, 2, 5),  
	(1043, 503, 2, 1, 5),  
	(1044, 504, 3, 2, 5),  
	(1045, 505, 3, 3, 5),  
	(1046, 506, 4, 2, 5),  
	(1047, 507, 2, 1, 5),  
	(1048, 508, 4, 4, 5),  
	(1049, 509, 3, 2, 5),  
	(1050, 510, 2, 0, 5),  
	-- HostelID 6  
	(1051, 601, 2, 1, 6),  
	(1052, 602, 2, 2, 6),  
	(1053, 603, 2, 1, 6),  
	(1054, 604, 3, 2, 6),  
	(1055, 605, 3, 3, 6),  
	(1056, 606, 4, 2, 6),  
	(1057, 607, 2, 1, 6),  
	(1058, 608, 4, 4, 6),  
	(1059, 609, 3, 2, 6),  
	(1060, 610, 2, 0, 6),  
	-- HostelID 7  
	(1061, 701, 2, 1, 7),  
	(1062, 702, 2, 2, 7),  
	(1063, 703, 2, 1, 7),  
	(1064, 704, 3, 2, 7),  
	(1065, 705, 3, 3, 7),  
	(1066, 706, 4, 2, 7),  
	(1067, 707, 2, 1, 7),  
	(1068, 708, 4, 4, 7),  
	(1069, 709, 3, 2, 7),  
	(1070, 710, 2, 0, 7),  
	-- HostelID 8  
	(1071, 801, 2, 1, 8),  
	(1072, 802, 2, 2, 8),  
	(1073, 803, 2, 1, 8),  
	(1074, 804, 3, 2, 8),  
	(1075, 805, 3, 3, 8),  
	(1076, 806, 4, 2, 8),  
	(1077, 807, 2, 1, 8),  
	(1078, 808, 4, 4, 8),  
	(1079, 809, 3, 2, 8),  
	(1080, 810, 2, 0, 8),  
	-- HostelID 9  
	(1081, 901, 2, 1, 9),  
	(1082, 902, 2, 2, 9),  
	(1083, 903, 2, 1, 9),  
	(1084, 904, 3, 2, 9),  
	(1085, 905, 3, 3, 9),  
	(1086, 906, 4, 2, 9),  
	(1087, 907, 2, 1, 9),  
	(1088, 908, 4, 4, 9),  
	(1089, 909, 3, 2, 9),  
	(1090, 910, 2, 0, 9),  
	-- HostelID 10  
	(1091, 1001, 2, 1, 10),  
	(1092, 1002, 2, 2, 10),  
	(1093, 1003, 2, 1, 10),  
	(1094, 1004, 3, 2, 10),  
	(1095, 1005, 3, 3, 10),  
	(1096, 1006, 4, 2, 10),  
	(1097, 1007, 2, 1, 10),  
	(1098, 1008, 4, 4, 10),  
	(1099, 1009, 3, 2, 10),  
	(1100, 1010, 2, 0, 10),  
	-- HostelID 11  
	(1101, 1101, 2, 1, 11),  
	(1102, 1102, 2, 2, 11),  
	(1103, 1103, 2, 1, 11),  
	(1104, 1104, 3, 2, 11),  
	(1105, 1105, 3, 3, 11),  
	(1106, 1106, 4, 2, 11),  
	(1107, 1107, 2, 1, 11),  
	(1108, 1108, 4, 4, 11),  
	(1109, 1109, 3, 2, 11),  
	(1110, 1110, 2, 0, 11),  
	-- HostelID 12  
	(1111, 1201, 2, 1, 12),  
	(1112, 1202, 2, 2, 12),  
	(1113, 1203, 2, 1, 12),  
	(1114, 1204, 3, 2, 12),  
	(1115, 1205, 3, 3, 12),  
	(1116, 1206, 4, 2, 12),  
	(1117, 1207, 2, 1, 12),  
	(1118, 1208, 4, 4, 12),  
	(1119, 1209, 3, 2, 12),  
	(1120, 1210, 2, 0, 12),  
	-- HostelID 13  
	(1121, 1301, 2, 1, 13),  
	(1122, 1302, 2, 2, 13),  
	(1123, 1303, 2, 1, 13),  
	(1124, 1304, 3, 2, 13),  
	(1125, 1305, 3, 3, 13),  
	(1126, 1306, 4, 2, 13),  
	(1127, 1307, 2, 1, 13),  
	(1128, 1308, 4, 4, 13),  
	(1129, 1309, 3, 2, 13),  
	(1130, 1310, 2, 0, 13),  
	-- HostelID 14  
	(1131, 1401, 2, 1, 14),  
	(1132, 1402, 2, 2, 14),  
	(1133, 1403, 2, 1, 14),  
	(1134, 1404, 3, 2, 14),  
	(1135, 1405, 3, 3, 14),  
	(1136, 1406, 4, 2, 14),  
	(1137, 1407, 2, 1, 14),  
	(1138, 1408, 4, 4, 14),  
	(1139, 1409, 3, 2, 14),  
	(1140, 1410, 2, 0, 14),  
	-- HostelID 15  
	(1141, 1501, 2, 1, 15),  
	(1142, 1502, 2, 2, 15),  
	(1143, 1503, 2, 1, 15),  
	(1144, 1504, 3, 2, 15),  
	(1145, 1505, 3, 3, 15),  
	(1146, 1506, 4, 2, 15),  
	(1147, 1507, 2, 1, 15),  
	(1148, 1508, 4, 4, 15),  
	(1149, 1509, 3, 2, 15),  
	(1150, 1510, 2, 0, 15);  

-- Payments (depends on Student and Hostel)
INSERT INTO Payment (PaymentID, Amount, payment_status, payment_date, Student_id, Hostel_id) VALUES  
	(5011, 7200, 'Paid', '2025-04-23', 23412027, 1),   
	(5012, 5000, 'Pending', '2025-04-23', 23232026, 4),   
	(5013, 5500, 'Overdue', '2025-03-15', 33352027, 5),  
	(5014, 5800, 'Paid', '2025-04-23', 98892028, 6),  
	(5015, 1200, 'Pending', '2025-04-12', 11112027, 7),  
	(5016, 4500, 'Paid', '2025-04-23', 11112027, 8),   
	(5017, 8400, 'Pending', '2025-02-23', 22992025, 10),  
	(5018, 6000, 'Overdue', '2025-02-10', 33472027, 2),    
	(5019, 6500, 'Pending', '2025-04-01', 21122026, 13),  
	(5020, 7050, 'Paid', '2025-04-23', 11772025, 15),  
	(5021, 5500, 'Overdue', '2025-03-15', 11772025, 1),  
	(5022, 4230, 'Pending', '2025-04-13', 20032025, 3),   
	(5023, 1350, 'Pending', '2025-04-03', 90092025, 5),  
	(5024, 4800, 'Overdue', '2025-02-20', 98892025, 7),   
	(5025, 5650, 'Paid', '2025-02-23', 98892028, 9),  
	(5026, 9800, 'Paid', '2025-04-23', 96692028, 10),  
	(5027, 15000, 'Overdue', '2025-04-20', 91112025, 13);
    
-- Administration (no dependencies)
INSERT INTO Administration (AdminID, AdminFirstName, AdminLastName, AdminContact, admin_password) VALUES
	(10001, 'Daasebre', 'Gyamfie', 0247762281, 'breezy45'),
	(10002, 'Seyram', 'Apreku', 0264459663, 'seybaby'),
	(10003, 'Kwame', 'Bofrot',0543347892, 'kwamz25'),
    (10004, 'Jasmine', 'Prince', 0234567890, 'jprincess'),
    (10005, 'Eugene', 'Kobby', 0238888882, 'blacko69');
    


-- Reports (depends on Student and Hostel)
INSERT INTO Reports (ReportID, type_of_report, Descr, report_status, Student_id, Hostel_id) VALUES
	(7001, 'Maintenance', 'Leaky faucet in room 1111', 'Pending', 91112025, 12),
	(7002, 'Complaint', 'Noisy neighbors in room 1087', 'Resolved',98892028, 9),
	(7003, 'Maintenance', 'Broken window in room 301', 'Pending', 98892025, 7),
	(7004, 'Complaint', 'Missing items from room', 'Investigating', 11772025, 1),
	(7005, 'Emergency', 'Power outage in west wing', 'Resolved', 11112027, 8),
	(7006,'Maintenance','The fan just fell from the roof', 'Resolved', 20032025, 4),
	(7007,'Electricity','Our prepaid is done, money has been sent to security', 'Resolved', 91112025,10),
	(7008,'Complaint','Security does not operate on Wednesday evenings', 'Pending', 11772025, 5),
	(7009,'Maintenance','Window nets are torn', 'Investigating', 22992025, 8),
	(7010,'Complaint','Cleaners dont clean my room', 'Investigating', 11772025,5);

-- Booking (depends on Student, Hostel and Room)
INSERT INTO Booking (Booking_id, Student_id, Hostel_id, Room_id) VALUES  
	(6001, 23412027, 1, 1001),  -- Nana Daasebre Kwaku  
	(6002, 23232026, 1, 1002),  -- Kwame Yirenkyi  
	(6003, 33352027, 3, 1021),  -- Seyram Apreku  
	(6004, 11112027, 3, 1022),  -- Jasmine Akuaku  
	(6005, 22992025, 5, 1041),  -- Wilson Dangote  
	(6006, 33472027, 1, 1003),  -- Eugene Amonoo-Neizer  
	(6007, 21122026, 2, 1011),  -- Addobea Taylor  
	(6008, 11772025, 5, 1042),  -- Jennifer Anderson  
	(6009, 20032025, 4, 1033),  -- William Owusu  
	(6010, 90092025, 5, 1043),  -- Elizabeth Martinez  
	(6011, 98892025, 5, 1044),  -- Michael Boakye  
	(6012, 98892028, 2, 1101),  -- Ryan Antwi  
	(6013, 96692028, 2, 1150),  -- Amber Rose  
	(6014, 91112025, 1, 1004);  -- Diddiella Arthur   


-- Roommate Preferences (depends on Student)
INSERT INTO Roommate_Preference (Preference_id, student_id, study_preference, social_preference, noise_level, preferred_roommate_id) VALUES
	(4544, '23412027', 'Quiet', 'Introvert', 'Quiet', NULL),  
	(4545, '23232026', 'Group Study', 'Extrovert', 'Lively', 33352027),  
	(4546, '33352027', 'Soft Music', 'Amibivert', 'Moderate', 11112027),  
	(4547, '11112027', 'Quiet', 'Introvert', 'Quiet', NULL),  
	(4548, '22992025', 'Quiet', 'Extrovert', 'Quiet', 33472027),  
	(4549, '33472027', 'Group Study', 'Amibivert', 'Lively', 23232026),  
	(4550, '21122026', 'Soft Music', 'Introvert', 'Moderate', NULL),  
	(4551, '11772025', 'Group Study', 'Extrovert', 'Lively', 20032025),  
	(4552, '20032025', 'Quiet', 'Amibivert', 'Quiet', NULL),  
	(4553, '90092025', 'Soft Music', 'Introvert', 'Moderate', 98892025),  
	(4554, '98892025', 'Quiet', 'Amibivert', 'Quiet', 98892028),  
	(4555, '98892028', 'Group Study', 'Extrovert', 'Lively', NULL),  
	(4556, '96692028', 'Quiet', 'Introvert', 'Quiet', 91112025),  
	(4557, '91112025', 'Soft Music', 'Amibivert', 'Moderate', NULL);  


-- Qeries for the operations of the Hostel Mnagement System here

-- View Overdue Payments With Student and Hostel Info
-- Features used: Inner Join, Condition (=, > 0), Sorting

SELECT 
    Student.StudentName, 
    Hostel.HostelName, 
    Payment.Amount, 
    Payment.payment_status
FROM 
    Student
INNER JOIN Payment ON Student.StudentID = Payment.Student_id
INNER JOIN Hostel ON Hostel.HostelID = Payment.Hostel_id
WHERE 
    Payment.payment_status = 'Overdue'
    AND Payment.Amount > 0
ORDER BY 
    Payment.Amount DESC;

-- List Hostels and Count of Students per Hostel
-- Features used: Join, Aggregate function (COUNT()), Grouping
SELECT 
    Hostel.HostelName, 
    COUNT(Booking.student_id) AS NumberOfStudents
FROM 
    Hostel
LEFT JOIN Booking ON Hostel.HostelID = Booking.hostel_id
GROUP BY 
    Hostel.HostelName
ORDER BY 
    NumberOfStudents DESC;

-- Find Students Who Haven’t Made Any Payment
-- Features used: Outer Join, IS NULL, Sorting
SELECT 
    Student.StudentName
FROM 
    Student
LEFT JOIN Payment ON Student.StudentID = Payment.Student_id
WHERE 
    Payment.Student_id IS NULL
ORDER BY 
    Student.StudentName;

-- View Reports With Description Like 'Plumbing%'
-- Features used: Join, LIKE wildcard, Ordering
SELECT 
    Reports.Descr, 
    Reports.report_status, 
    Student.StudentName, 
    Hostel.HostelName
FROM 
    Reports
INNER JOIN Student ON Reports.Student_id = Student.StudentID
INNER JOIN Hostel ON Reports.Hostel_id = Hostel.HostelID
WHERE 
    Reports.Descr LIKE 'Plumbing%'
ORDER BY 
    Reports.report_status;
    

-- view reports a particular hostel manager has

SELECT Reports.ReportID, Reports.Descr, Reports.type_of_report, Reports.report_status
From Reports
	JOIN `Hostel_Manager` ON `Hostel_Manager`.Hostel_id = Reports.Hostel_id
    JOIN Student S on Reports.Student_id = Student_id
    WHERE `Hostel_Manager`.ManagerId = "M1";
    

-- Viewing Students in a specific room
SELECT Student.StudentID, Student.StudentName
FROM Student, Booking, Room
WHERE Booking.room_id = Room.RoomID AND Student.StudentID = Booking.`Student_id`
AND Room_id = "R008";


-- Finding fully occupied rooms
SELECT Room.RoomID, Room.Room_No
FROM Room
	JOIN Booking ON Room.RoomID = Booking.room_id
	GROUP BY Room.RoomID, Room.Room_No, Room.num_of_occupants, Room.max_occupants
	HAVING COUNT(Booking.Student_id) = Room.max_occupants;
