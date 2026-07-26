-- ============================================================
-- Event Management System - Sample Data
-- Run this AFTER schema.sql
-- ============================================================

USE event_management;

-- ============================================================
-- Admin (password: admin123)
-- ============================================================
INSERT INTO admins (name, email, password, phone) VALUES
('System Admin', 'admin@events.com', 'admin123', '9876543210');

-- ============================================================
-- Users (password: user123)
-- ============================================================
INSERT INTO users (name, email, password, phone, city, bio) VALUES
('John Doe', 'john@email.com', 'user123', '9876543211', 'Mumbai', 'Software enthusiast and event lover.'),
('Jane Smith', 'jane@email.com', 'user123', '9876543212', 'Delhi', 'Full-stack developer and tech speaker.'),
('Alex Johnson', 'alex@email.com', 'user123', '9876543213', 'Bangalore', 'UI/UX designer and creative thinker.'),
('Priya Patel', 'priya@email.com', 'user123', '9876543214', 'Ahmedabad', 'Data science enthusiast and blogger.'),
('Rahul Verma', 'rahul@email.com', 'user123', '9876543215', 'Pune', 'Cloud computing and DevOps explorer.'),
('Sneha Reddy', 'sneha@email.com', 'user123', '9876543216', 'Hyderabad', 'Machine learning student and hackathon participant.'),
('Amit Singh', 'amit@email.com', 'user123', '9876543217', 'Jaipur', 'Mobile app developer and open-source contributor.'),
('Neha Gupta', 'neha@email.com', 'user123', '9876543218', 'Lucknow', 'Cybersecurity enthusiast and CTF player.');

-- ============================================================
-- Categories
-- ============================================================
INSERT INTO categories (name, description, icon) VALUES
('Technology', 'Events related to technology, programming, and innovation', 'bi-laptop'),
('Workshop', 'Hands-on learning sessions and skill-building workshops', 'bi-tools'),
('Seminar', 'Educational talks and knowledge-sharing sessions', 'bi-mic'),
('Cultural', 'Cultural festivals, performances, and celebrations', 'bi-music-note'),
('Sports', 'Sports tournaments and athletic competitions', 'bi-trophy'),
('Networking', 'Professional networking and career development events', 'bi-people'),
('Hackathon', 'Coding competitions and innovation challenges', 'bi-code-slash'),
('Conference', 'Industry conferences and professional summits', 'bi-easel');

-- ============================================================
-- Events
-- ============================================================
INSERT INTO events (title, description, category_id, event_date, event_time, venue, organizer, max_participants, registration_deadline, status, created_by) VALUES
('Tech Summit 2026',
'Annual technology summit featuring industry leaders discussing AI, blockchain, cloud computing, and the future of software engineering. Join us for keynote sessions, panel discussions, and networking opportunities.',
1, CURDATE() + INTERVAL 15 DAY, '09:00:00', 'Main Auditorium, Tech University', 'Tech University', 500, CURDATE() + INTERVAL 10 DAY, 'Upcoming', 1),

('Python Workshop for Beginners',
'Hands-on workshop covering Python fundamentals, data structures, OOP concepts, and basic web development with Flask. Perfect for beginners who want to start their programming journey.',
2, CURDATE() + INTERVAL 7 DAY, '10:00:00', 'Lab 3, Computer Science Building', 'Code Academy', 60, CURDATE() + INTERVAL 5 DAY, 'Upcoming', 1),

('AI & Machine Learning Seminar',
'Expert-led seminar on the latest advances in artificial intelligence and machine learning. Topics include deep learning, NLP, computer vision, and real-world applications.',
3, CURDATE() + INTERVAL 20 DAY, '14:00 Seminar Hall', 'Seminar Hall B, Engineering Block', 'AI Research Lab', 200, CURDATE() + INTERVAL 18 DAY, 'Upcoming', 1),

('Annual Cultural Fest - Spectrum',
'Spectacular three-day cultural festival featuring music, dance, drama, fashion show, and art exhibition. Teams from colleges across the country compete for the trophy.',
4, CURDATE() + INTERVAL 30 DAY, '16:00:00', 'Open Air Theatre, Main Campus', 'Cultural Committee', 1000, CURDATE() + INTERVAL 25 DAY, 'Upcoming', 1),

('Inter-College Cricket Tournament',
'Cricket tournament between engineering colleges. Group stages followed by semi-finals and grand final. Teams of 11 players per side.',
5, CURDATE() + INTERVAL 25 DAY, '07:00:00', 'Sports Complex, Main Campus', 'Sports Committee', 200, CURDATE() + INTERVAL 20 DAY, 'Upcoming', 1),

('Career Connect Networking Event',
'Professional networking event with alumni, recruiters, and industry professionals. Resume review, mock interviews, and career guidance sessions included.',
6, CURDATE() + INTERVAL 12 DAY, '11:00:00', 'Conference Room A, Management Block', 'Placement Cell', 150, CURDATE() + INTERVAL 10 DAY, 'Upcoming', 1),

('48-Hour Hackathon - CodeStorm',
'Intense 48-hour hackathon where teams build innovative solutions for real-world problems. Mentors from top tech companies will guide participants. Prizes worth Rs. 1 Lakh.',
7, CURDATE() + INTERVAL 18 DAY, '10:00:00', 'Innovation Hub, Tech Park', 'Innovation Cell', 120, CURDATE() + INTERVAL 16 DAY, 'Upcoming', 1),

('International Tech Conference 2026',
'Global technology conference bringing together researchers, developers, and industry leaders. Paper presentations, workshops, and exhibition stalls.',
8, CURDATE() + INTERVAL 45 DAY, '09:00:00', 'Convention Center, City Center', 'Global Tech Association', 800, CURDATE() + INTERVAL 40 DAY, 'Upcoming', 1),

('Web Development Bootcamp',
'Intensive 5-day bootcamp covering HTML, CSS, JavaScript, React, Node.js, and deployment. Build 3 projects by the end of the bootcamp.',
2, CURDATE() - INTERVAL 10 DAY, '10:00:00', 'Lab 5, Computer Science Building', 'Code Academy', 40, CURDATE() - INTERVAL 15 DAY, 'Completed', 1),

('Startup Meetup 2025',
'Monthly meetup for entrepreneurs and aspiring founders. Pitch sessions, investor talks, and networking dinner.',
6, CURDATE() - INTERVAL 30 DAY, '18:00:00', 'Cafe Innovation, Tech Park', 'Startup Cell', 80, CURDATE() - INTERVAL 35 DAY, 'Completed', 1);

-- ============================================================
-- Registrations
-- ============================================================
INSERT INTO registrations (user_id, event_id, status) VALUES
(1, 1, 'Registered'),
(1, 2, 'Registered'),
(1, 7, 'Registered'),
(2, 1, 'Registered'),
(2, 3, 'Registered'),
(2, 6, 'Registered'),
(3, 1, 'Registered'),
(3, 4, 'Registered'),
(3, 5, 'Registered'),
(4, 2, 'Registered'),
(4, 3, 'Registered'),
(5, 1, 'Registered'),
(5, 7, 'Registered'),
(5, 8, 'Registered'),
(6, 3, 'Registered'),
(6, 6, 'Registered'),
(7, 4, 'Registered'),
(7, 5, 'Registered'),
(8, 1, 'Registered'),
(8, 2, 'Registered'),
(1, 9, 'Registered'),
(2, 9, 'Registered'),
(3, 10, 'Registered'),
(4, 10, 'Registered');
