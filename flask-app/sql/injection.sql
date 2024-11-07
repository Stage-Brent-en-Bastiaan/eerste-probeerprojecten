-- Maak de database aan (als deze nog niet bestaat)
ATTACH DATABASE 'database.db' AS db;

-- Maak de tabel patienten aan
CREATE TABLE IF NOT EXISTS db.patienten (
    Afdeling INTEGER,
    Kamer INTEGER,
    Familienaam TEXT,
    Voornaam TEXT,
    Geboortedatum TEXT,
    Dieet TEXT,
    Laatste_bevraging TEXT
);

-- Voeg 30 regels dummiedata toe
INSERT INTO db.patienten (Afdeling, Kamer, Familienaam, Voornaam, Geboortedatum, Dieet, Laatste_bevraging) VALUES
(1, 101, 'Jansen', 'Jan', '1980-05-12', 'Normaal', '2024-09-30'),
(1, 102, 'Pietersen', 'Anne', '1992-03-20', 'Vegetarisch', '2024-09-29'),
(2, 201, 'De Vries', 'Sophie', '1975-11-15', 'Glutenvrij', '2024-09-28'),
(2, 202, 'Van der Meer', 'Kees', '1988-07-25', 'Lactosevrij', '2024-09-27'),
(1, 103, 'Verhoeven', 'Maria', '1955-01-10', 'Normaal', '2024-09-26'),
(1, 104, 'Bakker', 'Pieter', '1968-06-30', 'Vegan', '2024-09-25'),
(3, 301, 'Hendriks', 'Laura', '1985-08-18', 'Dieet', '2024-09-24'),
(3, 302, 'Smit', 'Tom', '1970-02-22', 'Normaal', '2024-09-23'),
(2, 203, 'Groot', 'Eva', '1990-12-12', 'Glutenvrij', '2024-09-22'),
(2, 204, 'Kramer', 'Joris', '1983-04-05', 'Vegetarisch', '2024-09-21'),
(1, 105, 'De Jong', 'Hannah', '1995-09-09', 'Lactosevrij', '2024-09-20'),
(1, 106, 'Faber', 'Liam', '1981-03-14', 'Vegan', '2024-09-19'),
(3, 303, 'Schmidt', 'Nina', '1960-07-02', 'Dieet', '2024-09-18'),
(3, 304, 'Willems', 'Bart', '1978-11-23', 'Normaal', '2024-09-17'),
(2, 205, 'Brouwer', 'Julia', '1993-10-30', 'Glutenvrij', '2024-09-16'),
(2, 206, 'Mans', 'Rick', '1986-01-19', 'Vegetarisch', '2024-09-15'),
(1, 107, 'Meijer', 'Zoe', '1972-05-21', 'Lactosevrij', '2024-09-14'),
(1, 108, 'Visser', 'Ruben', '1991-04-04', 'Vegan', '2024-09-13'),
(3, 305, 'Hermans', 'Jade', '1984-12-25', 'Dieet', '2024-09-12'),
(3, 306, 'Hofman', 'Jasper', '1987-08-09', 'Normaal', '2024-09-11'),
(2, 207, 'Noord', 'Lara', '1998-06-17', 'Glutenvrij', '2024-09-10'),
(2, 208, 'Blom', 'Daan', '1974-03-29', 'Vegetarisch', '2024-09-09'),
(1, 109, 'Ruiter', 'Sanne', '1965-02-11', 'Lactosevrij', '2024-09-08'),
(1, 110, 'Kuipers', 'Milan', '1989-01-01', 'Vegan', '2024-09-07'),
(3, 307, 'Wolters', 'Sophie', '1950-10-14', 'Dieet', '2024-09-06'),
(3, 308, 'Jansen', 'Max', '1976-07-30', 'Normaal', '2024-09-05'),
(2, 209, 'Klaassen', 'Niels', '1994-02-22', 'Glutenvrij', '2024-09-04'),
(2, 210, 'Schoenmakers', 'Emma', '1982-11-03', 'Vegetarisch', '2024-09-03'),
(1, 111, 'Van Dijk', 'Yara', '1979-08-20', 'Lactosevrij', '2024-09-02'),
(1, 112, 'Meulman', 'Noah', '1996-05-06', 'Vegan', '2024-09-01');
