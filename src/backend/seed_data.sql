-- Filling tables with test data
-- 2 surveys, each with 2 questions with 3 answer options

-- ============================================
-- Survey 1: "Development Technologies Survey"
-- ============================================
INSERT INTO surveys (id, title, description, status, created_by, end_date, responses_count, is_anonymous)
VALUES 
    ('11111111-1111-1111-1111-111111111111', 
     'Development Technologies Survey', 
     'Learn more about developers preferences in choosing technologies',
     'active',
     1,
     NOW() + INTERVAL '30 days',
     0,
     false);

-- Question 1.1: "Which programming language do you prefer?"
INSERT INTO questions (id, survey_id, question_text, question_order, allow_multiple_answers)
VALUES
    ('a1111111-1111-1111-1111-111111111111', '11111111-1111-1111-1111-111111111111', 
     'Which programming language do you prefer for backend development?', 
     1, false);

-- Answer options for question 1.1
INSERT INTO question_options (id, question_id, option_text, option_order)
VALUES
    ('b1111111-1111-1111-1111-111111111111', 'a1111111-1111-1111-1111-111111111111', 'Python', 1),
    ('b1111111-1111-1111-1111-111111111112', 'a1111111-1111-1111-1111-111111111111', 'JavaScript/TypeScript', 2),
    ('b1111111-1111-1111-1111-111111111113', 'a1111111-1111-1111-1111-111111111111', 'Go', 3);

-- Question 1.2: "Which database do you use?"
INSERT INTO questions (id, survey_id, question_text, question_order, allow_multiple_answers)
VALUES
    ('a1111111-1111-1111-1111-111111111112', '11111111-1111-1111-1111-111111111111', 
     'Which database do you most often use?', 
     2, false);

-- Answer options for question 1.2
INSERT INTO question_options (id, question_id, option_text, option_order)
VALUES
    ('b1111111-1111-1111-1111-111111111121', 'a1111111-1111-1111-1111-111111111112', 'PostgreSQL', 1),
    ('b1111111-1111-1111-1111-111111111122', 'a1111111-1111-1111-1111-111111111112', 'MongoDB', 2),
    ('b1111111-1111-1111-1111-111111111123', 'a1111111-1111-1111-1111-111111111112', 'MySQL', 3);

-- ============================================
-- Survey 2: "Operating Systems Survey"
-- ============================================
INSERT INTO surveys (id, title, description, status, created_by, end_date, responses_count, is_anonymous)
VALUES 
    ('22222222-2222-2222-2222-222222222222', 
     'Operating Systems Survey', 
     'Find out developers preferences in choosing OS and IDE',
     'active',
     1,
     NOW() + INTERVAL '30 days',
     0,
     true);

-- Question 2.1: "Which operating system do you use?"
INSERT INTO questions (id, survey_id, question_text, question_order, allow_multiple_answers)
VALUES
    ('a2222222-2222-2222-2222-222222222221', '22222222-2222-2222-2222-222222222222', 
     'Which operating system do you use for development?', 
     1, false);

-- Answer options for question 2.1
INSERT INTO question_options (id, question_id, option_text, option_order)
VALUES
    ('b2222222-2222-2222-2222-222222222211', 'a2222222-2222-2222-2222-222222222221', 'Linux', 1),
    ('b2222222-2222-2222-2222-222222222212', 'a2222222-2222-2222-2222-222222222221', 'macOS', 2),
    ('b2222222-2222-2222-2222-222222222213', 'a2222222-2222-2222-2222-222222222221', 'Windows', 3);

-- Question 2.2: "Which IDE do you prefer?"
INSERT INTO questions (id, survey_id, question_text, question_order, allow_multiple_answers)
VALUES
    ('a2222222-2222-2222-2222-222222222222', '22222222-2222-2222-2222-222222222222', 
     'Which IDE do you prefer to use?', 
     2, false);

-- Answer options for question 2.2
INSERT INTO question_options (id, question_id, option_text, option_order)
VALUES
    ('b2222222-2222-2222-2222-222222222221', 'a2222222-2222-2222-2222-222222222222', 'VS Code', 1),
    ('b2222222-2222-2222-2222-222222222222', 'a2222222-2222-2222-2222-222222222222', 'JetBrains (PyCharm/WebStorm)', 2),
    ('b2222222-2222-2222-2222-222222222223', 'a2222222-2222-2222-2222-222222222222', 'Vim/Neovim', 3);

-- ============================================
-- Survey 3: "Work Preferences Survey" (COMPLETED)
-- ============================================
INSERT INTO surveys (id, title, description, status, created_by, end_date, responses_count, is_anonymous)
VALUES 
    ('33333333-3333-3333-3333-333333333333', 
     'Work Preferences Survey', 
     'This survey has been completed. Thank you to all participants!',
     'completed',
     1,
     NOW() - INTERVAL '5 days',
     42,
     false);

-- Question 3.1: "Do you prefer remote work or office?"
INSERT INTO questions (id, survey_id, question_text, question_order, allow_multiple_answers)
VALUES
    ('a3333333-3333-3333-3333-333333333331', '33333333-3333-3333-3333-333333333333', 
     'Do you prefer remote work or office work?', 
     1, false);

-- Answer options for question 3.1
INSERT INTO question_options (id, question_id, option_text, option_order)
VALUES
    ('b3333333-3333-3333-3333-333333333311', 'a3333333-3333-3333-3333-333333333331', 'Fully remote', 1),
    ('b3333333-3333-3333-3333-333333333312', 'a3333333-3333-3333-3333-333333333331', 'Hybrid (remote + office)', 2),
    ('b3333333-3333-3333-3333-333333333313', 'a3333333-3333-3333-3333-333333333331', 'Fully office', 3);

-- Question 3.2: "How many hours per day do you code?"
INSERT INTO questions (id, survey_id, question_text, question_order, allow_multiple_answers)
VALUES
    ('a3333333-3333-3333-3333-333333333332', '33333333-3333-3333-3333-333333333333', 
     'How many hours per day do you spend coding?', 
     2, false);

-- Answer options for question 3.2
INSERT INTO question_options (id, question_id, option_text, option_order)
VALUES
    ('b3333333-3333-3333-3333-333333333321', 'a3333333-3333-3333-3333-333333333332', 'Less than 4 hours', 1),
    ('b3333333-3333-3333-3333-333333333322', 'a3333333-3333-3333-3333-333333333332', '4-6 hours', 2),
    ('b3333333-3333-3333-3333-333333333323', 'a3333333-3333-3333-3333-333333333332', 'More than 6 hours', 3);

-- Adding some sample answers for the completed survey to show results
INSERT INTO answers (id, question_id, option_id, user_id)
VALUES
    -- Question 3.1 answers (25 Fully remote, 12 Hybrid, 5 Office)
    ('c3333333-3333-3333-3333-333333333301', 'a3333333-3333-3333-3333-333333333331', 'b3333333-3333-3333-3333-333333333311', 1),
    ('c3333333-3333-3333-3333-333333333302', 'a3333333-3333-3333-3333-333333333331', 'b3333333-3333-3333-3333-333333333311', 2),
    ('c3333333-3333-3333-3333-333333333303', 'a3333333-3333-3333-3333-333333333331', 'b3333333-3333-3333-3333-333333333311', 3),
    ('c3333333-3333-3333-3333-333333333304', 'a3333333-3333-3333-3333-333333333331', 'b3333333-3333-3333-3333-333333333312', 4),
    ('c3333333-3333-3333-3333-333333333305', 'a3333333-3333-3333-3333-333333333331', 'b3333333-3333-3333-3333-333333333313', 5),
    -- Question 3.2 answers (8 Less than 4, 20 4-6 hours, 14 More than 6)
    ('c3333333-3333-3333-3333-333333333311', 'a3333333-3333-3333-3333-333333333332', 'b3333333-3333-3333-3333-333333333321', 1),
    ('c3333333-3333-3333-3333-333333333312', 'a3333333-3333-3333-3333-333333333332', 'b3333333-3333-3333-3333-333333333322', 2),
    ('c3333333-3333-3333-3333-333333333313', 'a3333333-3333-3333-3333-333333333332', 'b3333333-3333-3333-3333-333333333322', 3),
    ('c3333333-3333-3333-3333-333333333314', 'a3333333-3333-3333-3333-333333333332', 'b3333333-3333-3333-3333-333333333322', 4),
    ('c3333333-3333-3333-3333-333333333315', 'a3333333-3333-3333-3333-333333333332', 'b3333333-3333-3333-3333-333333333323', 5);
