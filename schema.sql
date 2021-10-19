-- SQL Database Schema
-- You can use this file to populate a brand new database

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

CREATE TABLE `clubs` (
  `ID` bigint(20) NOT NULL,
  `Name` tinytext COLLATE utf8_bin NOT NULL,
  `ShortName` tinytext COLLATE utf8_bin,
  `Type` tinyint(4) NOT NULL,
  `Subtype` tinytext COLLATE utf8_bin,
  `Description` text COLLATE utf8_bin,
  `Website` tinytext COLLATE utf8_bin,
  `BannerImage` tinytext COLLATE utf8_bin,
  `Sponsor` tinytext COLLATE utf8_bin,
  `Leader` tinytext COLLATE utf8_bin,
  `Members` int(11) DEFAULT NULL,
  `MeetingTime` tinytext COLLATE utf8_bin,
  `LocationCampus` tinytext COLLATE utf8_bin,
  `LocationRoom` tinytext COLLATE utf8_bin,
  `SocialTwitter` tinytext COLLATE utf8_bin,
  `SocialGithub` tinytext COLLATE utf8_bin,
  `SocialDiscord` tinytext COLLATE utf8_bin,
  `SocialYoutube` tinytext COLLATE utf8_bin,
  `SocialFacebook` tinytext COLLATE utf8_bin,
  `SocialInstagram` tinytext COLLATE utf8_bin,
  `Remind` tinytext COLLATE utf8_bin,
  `Hidden` tinyint(1) NOT NULL,
  `Verified` tinyint(1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

CREATE TABLE `events` (
  `ID` bigint(20) NOT NULL,
  `Name` tinytext COLLATE utf8_bin NOT NULL,
  `ClubID` bigint(20) DEFAULT NULL,
  `StartTime` bigint(20) NOT NULL,
  `EndTime` bigint(20) NOT NULL,
  `Description` text COLLATE utf8_bin NOT NULL,
  `MaxAttendees` smallint(6) NOT NULL,
  `AttendanceCode` VARCHAR(16) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

CREATE TABLE `sessions` (
  `ID` bigint(20) NOT NULL,
  `Token` varchar(64) COLLATE utf8_bin NOT NULL,
  `Expiration` bigint(20) NOT NULL,
  `UserID` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

CREATE TABLE `users` (
  `ID` bigint(20) NOT NULL,
  `EmailAddress` varchar(128) COLLATE utf8_bin NOT NULL,
  `DisplayName` tinytext COLLATE utf8_bin NOT NULL,
  `Clubs` tinytext COLLATE utf8_bin NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

ALTER TABLE `clubs`
  ADD PRIMARY KEY (`ID`);

ALTER TABLE `events`
  ADD PRIMARY KEY (`ID`);

ALTER TABLE `sessions`
  ADD PRIMARY KEY (`ID`);

ALTER TABLE `users`
  ADD PRIMARY KEY (`ID`);

ALTER TABLE `clubs`
  MODIFY `ID` bigint(20) NOT NULL AUTO_INCREMENT;

ALTER TABLE `events`
  MODIFY `ID` bigint(20) NOT NULL AUTO_INCREMENT;

ALTER TABLE `sessions`
  MODIFY `ID` bigint(20) NOT NULL AUTO_INCREMENT;

ALTER TABLE `users`
  MODIFY `ID` bigint(20) NOT NULL AUTO_INCREMENT;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
