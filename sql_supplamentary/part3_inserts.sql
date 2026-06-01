-- =====================================================
-- EXTRA AIRLINES
-- =====================================================
insert ignore into airline(airline_name) values
('Japan Airlines'),
('Korean Air'),
('Singapore Airlines'),
('Delta Air Lines'),
('United Airlines'),
('Air France'),
('British Airways'),
('Qatar Airways'),
('Air China'),
('China Eastern'),
('Shenzhen Airlines');

-- =====================================================
-- EXTRA AIRPORTS / LOCATIONS
-- =====================================================
insert ignore into airport(airport_name, city) values
('JFK', 'New York'),
('PVG', 'Shanghai'),
('SZX', 'Shenzhen'),
('HND', 'Tokyo'),
('NRT', 'Tokyo'),
('ICN', 'Seoul'),
('SIN', 'Singapore'),
('LAX', 'Los Angeles'),
('SFO', 'San Francisco'),
('CDG', 'Paris'),
('LHR', 'London'),
('DOH', 'Doha');

-- =====================================================
-- EXTRA AIRCRAFT
-- =====================================================
insert ignore into aircraft(aircraft_id, seat_capacity, airline_name) values
('JL-B787-001', 240, 'Japan Airlines'),
('KE-A330-001', 250, 'Korean Air'),
('SQ-A350-001', 300, 'Singapore Airlines'),
('DL-A330-001', 280, 'Delta Air Lines'),
('UA-B777-001', 310, 'United Airlines'),
('AF-B777-001', 310, 'Air France'),
('BA-B787-001', 260, 'British Airways'),
('QR-A350-001', 300, 'Qatar Airways'),
('CA-A320-002', 180, 'Air China'),
('MU-B737-011', 160, 'China Eastern'),
('ZH-A320-003', 170, 'Shenzhen Airlines');

-- =====================================================
-- MAY 2026 OPERATING FLIGHTS
-- =====================================================
insert ignore into operating_flight(
    operating_airline_name, flight_number,
    departure_time, arrival_time, price, status,
    departure_port, arrival_port, aircraft_id
) values
('Air China', 'CA501', '2026-05-01 09:00:00', '2026-05-01 15:00:00', 520.00, 'upcoming', 'JFK', 'PVG', 'CA-A320-002'),
('China Eastern', 'MU502', '2026-05-02 10:00:00', '2026-05-02 16:00:00', 500.00, 'upcoming', 'JFK', 'PVG', 'MU-B737-011'),
('Delta Air Lines', 'DL503', '2026-05-03 11:30:00', '2026-05-03 17:30:00', 540.00, 'upcoming', 'LAX', 'PVG', 'DL-A330-001'),
('United Airlines', 'UA504', '2026-05-04 13:00:00', '2026-05-04 19:00:00', 550.00, 'upcoming', 'SFO', 'PVG', 'UA-B777-001'),

('China Eastern', 'MU505', '2026-05-05 08:00:00', '2026-05-05 10:30:00', 180.00, 'upcoming', 'PVG', 'SZX', 'MU-B737-011'),
('Shenzhen Airlines', 'ZH506', '2026-05-06 09:00:00', '2026-05-06 11:30:00', 175.00, 'upcoming', 'PVG', 'SZX', 'ZH-A320-003'),
('Air China', 'CA507', '2026-05-07 12:00:00', '2026-05-07 14:30:00', 190.00, 'delayed', 'PVG', 'SZX', 'CA-A320-002'),

('Japan Airlines', 'JL508', '2026-05-08 08:00:00', '2026-05-08 11:00:00', 260.00, 'upcoming', 'PVG', 'HND', 'JL-B787-001'),
('Air China', 'CA509', '2026-05-09 09:30:00', '2026-05-09 12:30:00', 280.00, 'upcoming', 'PVG', 'HND', 'CA-A320-002'),
('China Eastern', 'MU510', '2026-05-10 11:00:00', '2026-05-10 14:00:00', 270.00, 'upcoming', 'PVG', 'NRT', 'MU-B737-011'),

('Japan Airlines', 'JL511', '2026-05-11 15:00:00', '2026-05-11 18:00:00', 300.00, 'upcoming', 'HND', 'PVG', 'JL-B787-001'),
('China Eastern', 'MU512', '2026-05-12 16:00:00', '2026-05-12 19:00:00', 285.00, 'upcoming', 'NRT', 'PVG', 'MU-B737-011'),

('Singapore Airlines', 'SQ513', '2026-05-13 08:30:00', '2026-05-13 14:00:00', 420.00, 'upcoming', 'PVG', 'SIN', 'SQ-A350-001'),
('China Eastern', 'MU514', '2026-05-14 09:30:00', '2026-05-14 15:00:00', 400.00, 'upcoming', 'PVG', 'SIN', 'MU-B737-011'),
('Air China', 'CA515', '2026-05-15 10:30:00', '2026-05-15 16:00:00', 410.00, 'delayed', 'PVG', 'SIN', 'CA-A320-002'),

('Korean Air', 'KE516', '2026-05-16 08:00:00', '2026-05-16 10:30:00', 230.00, 'upcoming', 'PVG', 'ICN', 'KE-A330-001'),
('China Eastern', 'MU517', '2026-05-17 09:00:00', '2026-05-17 11:30:00', 220.00, 'upcoming', 'PVG', 'ICN', 'MU-B737-011'),
('Korean Air', 'KE518', '2026-05-18 13:00:00', '2026-05-18 15:30:00', 235.00, 'upcoming', 'ICN', 'PVG', 'KE-A330-001'),

('Air France', 'AF519', '2026-05-19 09:00:00', '2026-05-19 20:30:00', 720.00, 'upcoming', 'PVG', 'CDG', 'AF-B777-001'),
('China Eastern', 'MU520', '2026-05-20 10:00:00', '2026-05-20 21:30:00', 700.00, 'upcoming', 'PVG', 'CDG', 'MU-B737-011'),
('Qatar Airways', 'QR521', '2026-05-21 12:00:00', '2026-05-21 22:00:00', 680.00, 'upcoming', 'PVG', 'DOH', 'QR-A350-001'),

('British Airways', 'BA522', '2026-05-22 09:00:00', '2026-05-22 21:00:00', 760.00, 'upcoming', 'PVG', 'LHR', 'BA-B787-001'),
('Air China', 'CA523', '2026-05-23 11:00:00', '2026-05-23 23:00:00', 740.00, 'upcoming', 'PVG', 'LHR', 'CA-A320-002'),

('Delta Air Lines', 'DL524', '2026-05-24 08:00:00', '2026-05-24 18:00:00', 690.00, 'upcoming', 'PVG', 'LAX', 'DL-A330-001'),
('United Airlines', 'UA525', '2026-05-25 09:00:00', '2026-05-25 19:00:00', 700.00, 'upcoming', 'PVG', 'SFO', 'UA-B777-001'),
('Air China', 'CA526', '2026-05-26 10:00:00', '2026-05-26 20:00:00', 680.00, 'upcoming', 'PVG', 'JFK', 'CA-A320-002'),

('Delta Air Lines', 'DL527', '2026-05-27 13:00:00', '2026-05-27 23:00:00', 710.00, 'upcoming', 'LAX', 'PVG', 'DL-A330-001'),
('United Airlines', 'UA528', '2026-05-28 14:00:00', '2026-05-29 00:00:00', 720.00, 'upcoming', 'SFO', 'PVG', 'UA-B777-001'),
('Air China', 'CA529', '2026-05-29 15:00:00', '2026-05-30 01:00:00', 690.00, 'upcoming', 'JFK', 'PVG', 'CA-A320-002'),

('Singapore Airlines', 'SQ530', '2026-05-30 18:00:00', '2026-05-30 23:30:00', 450.00, 'upcoming', 'SIN', 'PVG', 'SQ-A350-001'),
('Japan Airlines', 'JL531', '2026-05-31 19:00:00', '2026-05-31 22:00:00', 310.00, 'upcoming', 'HND', 'PVG', 'JL-B787-001');

-- =====================================================
-- MAY 2026 MARKETING FLIGHTS
-- =====================================================
insert ignore into marketing_flight(
    marketing_airline_name, marketing_flight_num,
    operating_airline_name, flight_number
) values
('Air China', 'CA501', 'Air China', 'CA501'),
('China Eastern', 'MU502', 'China Eastern', 'MU502'),
('Delta Air Lines', 'DL503', 'Delta Air Lines', 'DL503'),
('United Airlines', 'UA504', 'United Airlines', 'UA504'),

('China Eastern', 'MU505', 'China Eastern', 'MU505'),
('Shenzhen Airlines', 'ZH506', 'Shenzhen Airlines', 'ZH506'),
('Air China', 'CA507', 'Air China', 'CA507'),

('Japan Airlines', 'JL508', 'Japan Airlines', 'JL508'),
('Air China', 'CA509', 'Air China', 'CA509'),
('China Eastern', 'MU510', 'China Eastern', 'MU510'),

('Japan Airlines', 'JL511', 'Japan Airlines', 'JL511'),
('China Eastern', 'MU512', 'China Eastern', 'MU512'),

('Singapore Airlines', 'SQ513', 'Singapore Airlines', 'SQ513'),
('China Eastern', 'MU514', 'China Eastern', 'MU514'),
('Air China', 'CA515', 'Air China', 'CA515'),

('Korean Air', 'KE516', 'Korean Air', 'KE516'),
('China Eastern', 'MU517', 'China Eastern', 'MU517'),
('Korean Air', 'KE518', 'Korean Air', 'KE518'),

('Air France', 'AF519', 'Air France', 'AF519'),
('China Eastern', 'MU520', 'China Eastern', 'MU520'),
('Qatar Airways', 'QR521', 'Qatar Airways', 'QR521'),

('British Airways', 'BA522', 'British Airways', 'BA522'),
('Air China', 'CA523', 'Air China', 'CA523'),

('Delta Air Lines', 'DL524', 'Delta Air Lines', 'DL524'),
('United Airlines', 'UA525', 'United Airlines', 'UA525'),
('Air China', 'CA526', 'Air China', 'CA526'),

('Delta Air Lines', 'DL527', 'Delta Air Lines', 'DL527'),
('United Airlines', 'UA528', 'United Airlines', 'UA528'),
('Air China', 'CA529', 'Air China', 'CA529'),

('Singapore Airlines', 'SQ530', 'Singapore Airlines', 'SQ530'),
('Japan Airlines', 'JL531', 'Japan Airlines', 'JL531'),

-- code-share examples
('Shenzhen Airlines', 'ZH8501', 'China Eastern', 'MU505'),
('Delta Air Lines', 'DL8501', 'Air China', 'CA501'),
('Japan Airlines', 'JL8501', 'Air China', 'CA509'),
('Korean Air', 'KE8501', 'China Eastern', 'MU517'),
('Air France', 'AF8501', 'China Eastern', 'MU520'),
('British Airways', 'BA8501', 'Air China', 'CA523'),
('Qatar Airways', 'QR8501', 'Air China', 'CA526');





-- PVG to Singapore flights for one specific day
insert ignore into operating_flight(
    operating_airline_name, flight_number,
    departure_time, arrival_time, price, status,
    departure_port, arrival_port, aircraft_id
) values
('Singapore Airlines', 'SQ5601', '2026-05-10 08:30:00', '2026-05-10 14:00:00', 420.00, 'upcoming', 'PVG', 'SIN', 'SQ-A350-001'),
('China Eastern', 'MU5601', '2026-05-10 10:00:00', '2026-05-10 15:30:00', 400.00, 'upcoming', 'PVG', 'SIN', 'MU-B737-011'),
('Air China', 'CA5601', '2026-05-10 16:00:00', '2026-05-10 21:30:00', 410.00, 'delayed', 'PVG', 'SIN', 'CA-A320-002');

insert ignore into marketing_flight(
    marketing_airline_name, marketing_flight_num,
    operating_airline_name, flight_number
) values
('Singapore Airlines', 'SQ5601', 'Singapore Airlines', 'SQ5601'),
('China Eastern', 'MU5601', 'China Eastern', 'MU5601'),
('Air China', 'CA5601', 'Air China', 'CA5601'),

-- one code-share example
('Shenzhen Airlines', 'ZH8601', 'China Eastern', 'MU5601');

-- DATES FOR 2026-05-10

-- IN-PROGRESS FLIGHTS
insert ignore into operating_flight(
    operating_airline_name, flight_number,
    departure_time, arrival_time, price, status,
    departure_port, arrival_port, aircraft_id
) values
('China Eastern', 'MU5701', '2026-05-10 09:00:00', '2026-05-10 14:30:00', 405.00, 'in-progress', 'PVG', 'SIN', 'MU-B737-011'),
('Singapore Airlines', 'SQ5701', '2026-05-10 10:00:00', '2026-05-10 15:30:00', 430.00, 'in-progress', 'PVG', 'SIN', 'SQ-A350-001'),
('Air China', 'CA5701', '2026-05-10 11:00:00', '2026-05-10 16:30:00', 415.00, 'in-progress', 'PVG', 'SIN', 'CA-A320-002'),

('Japan Airlines', 'JL5701', '2026-05-10 08:00:00', '2026-05-10 11:00:00', 285.00, 'in-progress', 'PVG', 'HND', 'JL-B787-001'),
('Korean Air', 'KE5701', '2026-05-10 08:30:00', '2026-05-10 11:00:00', 235.00, 'in-progress', 'PVG', 'ICN', 'KE-A330-001');

insert ignore into marketing_flight(
    marketing_airline_name, marketing_flight_num,
    operating_airline_name, flight_number
) values
('China Eastern', 'MU5701', 'China Eastern', 'MU5701'),
('Singapore Airlines', 'SQ5701', 'Singapore Airlines', 'SQ5701'),
('Air China', 'CA5701', 'Air China', 'CA5701'),
('Japan Airlines', 'JL5701', 'Japan Airlines', 'JL5701'),
('Korean Air', 'KE5701', 'Korean Air', 'KE5701'),

-- code-share examples
('Shenzhen Airlines', 'ZH8701', 'China Eastern', 'MU5701'),
('Delta Air Lines', 'DL8701', 'Air China', 'CA5701'); 






-- inserting tickets into db
-- EXTRA TICKETS FOR EVERY MARKETING FLIGHT
insert ignore into ticket(ticket_id, marketing_airline_name, marketing_flight_num) values
('TCKT-005', 'Shenzhen Airlines', 'ZH300'),

('TCKT-006', 'Air China', 'CA501'),
('TCKT-007', 'China Eastern', 'MU502'),
('TCKT-008', 'Delta Air Lines', 'DL503'),
('TCKT-009', 'United Airlines', 'UA504'),

('TCKT-010', 'China Eastern', 'MU505'),
('TCKT-011', 'Shenzhen Airlines', 'ZH506'),
('TCKT-012', 'Air China', 'CA507'),

('TCKT-013', 'Japan Airlines', 'JL508'),
('TCKT-014', 'Air China', 'CA509'),
('TCKT-015', 'China Eastern', 'MU510'),

('TCKT-016', 'Japan Airlines', 'JL511'),
('TCKT-017', 'China Eastern', 'MU512'),

('TCKT-018', 'Singapore Airlines', 'SQ513'),
('TCKT-019', 'China Eastern', 'MU514'),
('TCKT-020', 'Air China', 'CA515'),

('TCKT-021', 'Korean Air', 'KE516'),
('TCKT-022', 'China Eastern', 'MU517'),
('TCKT-023', 'Korean Air', 'KE518'),

('TCKT-024', 'Air France', 'AF519'),
('TCKT-025', 'China Eastern', 'MU520'),
('TCKT-026', 'Qatar Airways', 'QR521'),

('TCKT-027', 'British Airways', 'BA522'),
('TCKT-028', 'Air China', 'CA523'),

('TCKT-029', 'Delta Air Lines', 'DL524'),
('TCKT-030', 'United Airlines', 'UA525'),
('TCKT-031', 'Air China', 'CA526'),

('TCKT-032', 'Delta Air Lines', 'DL527'),
('TCKT-033', 'United Airlines', 'UA528'),
('TCKT-034', 'Air China', 'CA529'),

('TCKT-035', 'Singapore Airlines', 'SQ530'),
('TCKT-036', 'Japan Airlines', 'JL531'),

-- code-share tickets
('TCKT-037', 'Shenzhen Airlines', 'ZH8501'),
('TCKT-038', 'Delta Air Lines', 'DL8501'),
('TCKT-039', 'Japan Airlines', 'JL8501'),
('TCKT-040', 'Korean Air', 'KE8501'),
('TCKT-041', 'Air France', 'AF8501'),
('TCKT-042', 'British Airways', 'BA8501'),
('TCKT-043', 'Qatar Airways', 'QR8501'),

-- PVG to Singapore specific day tickets
('TCKT-044', 'Singapore Airlines', 'SQ5601'),
('TCKT-045', 'China Eastern', 'MU5601'),
('TCKT-046', 'Air China', 'CA5601'),
('TCKT-047', 'Shenzhen Airlines', 'ZH8601'),

-- 2026-05-10 tickets
('TCKT-048', 'China Eastern', 'MU5701'),
('TCKT-049', 'Singapore Airlines', 'SQ5701'),
('TCKT-050', 'Air China', 'CA5701'),
('TCKT-051', 'Japan Airlines', 'JL5701'),
('TCKT-052', 'Korean Air', 'KE5701'),
('TCKT-053', 'Shenzhen Airlines', 'ZH8701'),
('TCKT-054', 'Delta Air Lines', 'DL8701');

INSERT INTO ticket (
    ticket_id,
    marketing_airline_name,
    marketing_flight_num
)
SELECT
    CONCAT(
        'TCKT-',
        LPAD(
            (
                SELECT COALESCE(MAX(CAST(SUBSTRING(ticket_id, 6) AS UNSIGNED)), 0)
                FROM ticket t2
            ) + ROW_NUMBER() OVER (
                ORDER BY mf.marketing_airline_name, mf.marketing_flight_num
            ),
            3,
            '0'
        )
    ) AS ticket_id,
    mf.marketing_airline_name,
    mf.marketing_flight_num
FROM marketing_flight mf
WHERE NOT EXISTS (
    SELECT 1
    FROM ticket t
    WHERE t.marketing_airline_name = mf.marketing_airline_name
      AND t.marketing_flight_num = mf.marketing_flight_num
);