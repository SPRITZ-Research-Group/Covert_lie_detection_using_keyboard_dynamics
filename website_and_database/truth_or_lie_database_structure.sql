-- This code is a compliment to "Covert lie detection using keyboard dynamics".
-- Copyright (C) 2017  QianQian Li
-- See GNU General Public Licence v.3 for more details.
--  NO WARRANTY EXPRESSED OR IMPLIED. USE AT YOUR OWN RISK.

--
-- Server version: 5.5.57-0ubuntu0.14.04.1
-- PHP Version: 5.5.9-1ubuntu4.22

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Database: `truth_or_lie_2`
--

-- --------------------------------------------------------

--
-- Table structure for table `answers_long`
--

CREATE TABLE IF NOT EXISTS `answers_long` (
  `answer_id` mediumint(9) NOT NULL AUTO_INCREMENT,
  `session_id` mediumint(9) NOT NULL,
  `question_id` mediumint(9) NOT NULL,
  `text_answer` varchar(255) NOT NULL,
  `keystroke` longtext,
  `accellerometer_typing` longtext,
  `gyroscope_typing` longtext,
  `timestamp_first_digit` bigint(14) DEFAULT NULL,
  `eyetracking` longtext,
  `bci` longtext,
  `timestamp_prompted` bigint(14) DEFAULT NULL,
  `timestamp_enter` bigint(14) DEFAULT NULL,
  `gyroscope_before` longtext,
  `accellerometer_before` longtext,
  `timestamp_tap` varchar(45) DEFAULT NULL COMMENT 'on smartphone when the textbook is focus',
  PRIMARY KEY (`answer_id`),
  UNIQUE KEY `answer_id` (`answer_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=1593 ;



-- --------------------------------------------------------

--
-- Table structure for table `questions_long`
--

CREATE TABLE IF NOT EXISTS `questions_long` (
  `id` mediumint(9) NOT NULL AUTO_INCREMENT,
  `question_id` mediumint(9) NOT NULL,
  `text_short` varchar(255) NOT NULL,
  `text_large` varchar(255) DEFAULT NULL,
  `lettersnumber` tinyint(4) NOT NULL COMMENT 'this questions must be answers in letters\n0 is allow only letter\n1 is allow number &letter\n',
  `warmup` tinyint(4) NOT NULL COMMENT '1 warmup\n0 realtest',
  `language` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_UNIQUE` (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=22 ;

--
-- Dumping data for table `questions_long`
--

INSERT INTO `questions_long` (`id`, `question_id`, `text_short`, `text_large`, `lettersnumber`, `warmup`, `language`) VALUES
(1, 18, 'Qual è la tua professione? ', NULL, 1, 1, 'Italian'),
(2, 19, 'Qual è il tuo peso? (in lettere)', NULL, 0, 1, 'Italian'),
(3, 20, 'Di che colore sono i tuoi occhi?', NULL, 1, 1, 'Italian'),
(4, 0, 'Qual è il tuo sesso?', NULL, 1, 0, 'Italian'),
(5, 1, 'Qual è il colore della tua pelle?', NULL, 1, 0, 'Italian'),
(6, 2, 'Di che colore sono i tuoi capelli?', NULL, 1, 0, 'Italian'),
(7, 3, 'Che cittadinanza hai?', NULL, 1, 0, 'Italian'),
(8, 4, 'Qual è il tuo nome?', NULL, 1, 0, 'Italian'),
(9, 5, 'Qual è il tuo cognome?', NULL, 1, 0, 'Italian'),
(10, 6, 'In che anno sei nato?', NULL, 1, 0, 'Italian'),
(11, 7, 'In che mese sei nato?', NULL, 1, 0, 'Italian'),
(12, 8, 'In quale città sei nato?', NULL, 1, 0, 'Italian'),
(13, 9, 'In quale città sei residente?', NULL, 1, 0, 'Italian'),
(14, 10, 'Qual è il tuo indirizzo di residenza?', NULL, 1, 0, 'Italian'),
(15, 11, 'Qual è il tuo indirizzo e-mail?', NULL, 1, 0, 'Italian'),
(16, 12, 'Quanti anni hai? (in lettere)', NULL, 0, 0, 'Italian'),
(17, 13, 'Qual è il tuo segno zodiacale? ', NULL, 1, 0, 'Italian'),
(18, 14, 'In che regione sei nato?', NULL, 1, 0, 'Italian'),
(19, 15, 'In che provincia sei nato? ', NULL, 1, 0, 'Italian'),
(20, 16, 'In quale regione risiedi?', NULL, 1, 0, 'Italian'),
(21, 17, 'Qual è il capoluogo della tua regione di residenza?', NULL, 1, 0, 'Italian');

-- --------------------------------------------------------

--
-- Table structure for table `sessions_long`
--

CREATE TABLE IF NOT EXISTS `sessions_long` (
  `session_id` mediumint(9) NOT NULL AUTO_INCREMENT,
  `subject_id` mediumint(9) NOT NULL,
  `subject_name` varchar(50) NOT NULL COMMENT '1 truth\n0 lie\n',
  `subject_surname` varchar(50) NOT NULL COMMENT '1 truth\n0 lie\n',
  `age` int(9) NOT NULL COMMENT '1 truth\n0 lie\n',
  `sex` varchar(50) NOT NULL COMMENT '1 truth\n0 lie\n',
  `mind_condition` varchar(50) NOT NULL,
  `device_info` text,
  `question_ids_sequence` text,
  `current_question_index` int(11) DEFAULT NULL,
  `current_block_number` smallint(6) DEFAULT NULL COMMENT '0 is warmup\n1 is real test',
  `completed` tinyint(4) DEFAULT NULL COMMENT '0 unfinished\n1 finished',
  `start_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `education_level` varchar(45) NOT NULL,
  `pc_usage` varchar(45) NOT NULL,
  PRIMARY KEY (`session_id`),
  UNIQUE KEY `session_id` (`session_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=109 ;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
