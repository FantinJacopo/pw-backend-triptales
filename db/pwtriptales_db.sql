-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Creato il: Mag 24, 2025 alle 09:38
-- Versione del server: 10.4.32-MariaDB
-- Versione PHP: 8.0.30

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `pwtriptales_db`
--
CREATE DATABASE IF NOT EXISTS `pwtriptales_db` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE `pwtriptales_db`;

-- --------------------------------------------------------

--
-- Struttura della tabella `auth_group`
--

CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL,
  `name` varchar(150) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Struttura della tabella `auth_group_permissions`
--

CREATE TABLE `auth_group_permissions` (
  `id` bigint(20) NOT NULL,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Struttura della tabella `auth_permission`
--

CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dump dei dati per la tabella `auth_permission`
--

INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES
(1, 'Can add permission', 1, 'add_permission'),
(2, 'Can change permission', 1, 'change_permission'),
(3, 'Can delete permission', 1, 'delete_permission'),
(4, 'Can view permission', 1, 'view_permission'),
(5, 'Can add group', 2, 'add_group'),
(6, 'Can change group', 2, 'change_group'),
(7, 'Can delete group', 2, 'delete_group'),
(8, 'Can view group', 2, 'view_group'),
(9, 'Can add content type', 3, 'add_contenttype'),
(10, 'Can change content type', 3, 'change_contenttype'),
(11, 'Can delete content type', 3, 'delete_contenttype'),
(12, 'Can view content type', 3, 'view_contenttype'),
(13, 'Can add user', 4, 'add_user'),
(14, 'Can change user', 4, 'change_user'),
(15, 'Can delete user', 4, 'delete_user'),
(16, 'Can view user', 4, 'view_user'),
(17, 'Can add badge', 5, 'add_badge'),
(18, 'Can change badge', 5, 'change_badge'),
(19, 'Can delete badge', 5, 'delete_badge'),
(20, 'Can view badge', 5, 'view_badge'),
(21, 'Can add group membership', 6, 'add_groupmembership'),
(22, 'Can change group membership', 6, 'change_groupmembership'),
(23, 'Can delete group membership', 6, 'delete_groupmembership'),
(24, 'Can view group membership', 6, 'view_groupmembership'),
(25, 'Can add trip group', 7, 'add_tripgroup'),
(26, 'Can change trip group', 7, 'change_tripgroup'),
(27, 'Can delete trip group', 7, 'delete_tripgroup'),
(28, 'Can view trip group', 7, 'view_tripgroup'),
(29, 'Can add post', 8, 'add_post'),
(30, 'Can change post', 8, 'change_post'),
(31, 'Can delete post', 8, 'delete_post'),
(32, 'Can view post', 8, 'view_post'),
(33, 'Can add comment', 9, 'add_comment'),
(34, 'Can change comment', 9, 'change_comment'),
(35, 'Can delete comment', 9, 'delete_comment'),
(36, 'Can view comment', 9, 'view_comment'),
(37, 'Can add user badge', 10, 'add_userbadge'),
(38, 'Can change user badge', 10, 'change_userbadge'),
(39, 'Can delete user badge', 10, 'delete_userbadge'),
(40, 'Can view user badge', 10, 'view_userbadge'),
(41, 'Can add post like', 11, 'add_postlike'),
(42, 'Can change post like', 11, 'change_postlike'),
(43, 'Can delete post like', 11, 'delete_postlike'),
(44, 'Can view post like', 11, 'view_postlike');

-- --------------------------------------------------------

--
-- Struttura della tabella `backendtriptales_badge`
--

CREATE TABLE `backendtriptales_badge` (
  `id` bigint(20) NOT NULL,
  `name` varchar(50) NOT NULL,
  `badge_image_url` varchar(200) NOT NULL,
  `description` longtext NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dump dei dati per la tabella `backendtriptales_badge`
--

INSERT INTO `backendtriptales_badge` (`id`, `name`, `badge_image_url`, `description`) VALUES
(1, 'Primo Post', 'https://example.com/badges/first_post.png', 'Hai pubblicato il tuo primo post! Benvenuto nella community di TripTales!'),
(2, 'Fabrizio Corona', 'https://example.com/badges/photographer.png', 'Sei un vero paparazzo! Hai condiviso 10 foto con i tuoi compagni di viaggio.'),
(3, 'Primo Commento', 'https://example.com/badges/first_comment.png', 'Hai lasciato il tuo primo commento! Grazie per aver partecipato alla conversazione.'),
(4, 'Kanye West', 'https://example.com/badges/talkative.png', 'Sei un vero chiacchierone! Hai scritto 20 commenti... non ti bastava X?'),
(5, 'Fondatore', 'https://example.com/badges/founder.png', 'Hai creato il tuo primo gruppo! Sei un vero leader e organizzatore di avventure.'),
(6, 'Nico B', 'https://example.com/badges/star.png', 'Ti sei unito a molteplici gruppi, sei proprio il Main Character!!!'),
(7, 'PLC', 'https://example.com/badges/explorer.png', 'Esploratore certificato! Hai condiviso 5 post con geolocalizzazione.'),
(8, 'm-niky', 'https://example.com/badges/ai_master.png', 'Maestro dell\'intelligenza artificiale! Hai utilizzato tutte le funzionalità AI dell\'app.'),
(9, 'Cucippo', 'https://example.com/badges/cool.png', 'Badge leggendario per i membri più cool della community!');

-- --------------------------------------------------------

--
-- Struttura della tabella `backendtriptales_comment`
--

CREATE TABLE `backendtriptales_comment` (
  `id` bigint(20) NOT NULL,
  `content` text DEFAULT NULL,
  `created_at` datetime(6) NOT NULL,
  `post_id` bigint(20) NOT NULL,
  `user_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Struttura della tabella `backendtriptales_groupmembership`
--

CREATE TABLE `backendtriptales_groupmembership` (
  `id` bigint(20) NOT NULL,
  `joined_at` datetime(6) NOT NULL,
  `group_id` bigint(20) NOT NULL,
  `user_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Struttura della tabella `backendtriptales_post`
--

CREATE TABLE `backendtriptales_post` (
  `id` bigint(20) NOT NULL,
  `image` varchar(100) DEFAULT NULL,
  `smart_caption` varchar(255) DEFAULT NULL,
  `latitude` double DEFAULT NULL,
  `longitude` double DEFAULT NULL,
  `created_at` datetime(6) NOT NULL,
  `ocr_text` text DEFAULT NULL,
  `object_tags` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL CHECK (json_valid(`object_tags`)),
  `trip_group_id` bigint(20) NOT NULL,
  `user_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Struttura della tabella `backendtriptales_postlike`
--

CREATE TABLE `backendtriptales_postlike` (
  `id` bigint(20) NOT NULL,
  `liked_at` datetime(6) NOT NULL,
  `post_id` bigint(20) NOT NULL,
  `user_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Struttura della tabella `backendtriptales_tripgroup`
--

CREATE TABLE `backendtriptales_tripgroup` (
  `id` bigint(20) NOT NULL,
  `group_name` varchar(100) DEFAULT NULL,
  `group_image` varchar(100) DEFAULT NULL,
  `description` text DEFAULT NULL,
  `invite_code` varchar(5) NOT NULL,
  `qr_code` varchar(100) DEFAULT NULL,
  `created_at` datetime(6) NOT NULL,
  `creator_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Struttura della tabella `backendtriptales_user`
--

CREATE TABLE `backendtriptales_user` (
  `id` bigint(20) NOT NULL,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  `profile_image` varchar(100) DEFAULT NULL,
  `name` varchar(100) DEFAULT NULL,
  `email` varchar(254) NOT NULL,
  `registration_date` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Struttura della tabella `backendtriptales_userbadge`
--

CREATE TABLE `backendtriptales_userbadge` (
  `id` bigint(20) NOT NULL,
  `assigned_at` datetime(6) NOT NULL,
  `badge_id` bigint(20) NOT NULL,
  `user_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Struttura della tabella `backendtriptales_user_groups`
--

CREATE TABLE `backendtriptales_user_groups` (
  `id` bigint(20) NOT NULL,
  `user_id` bigint(20) NOT NULL,
  `group_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Struttura della tabella `backendtriptales_user_user_permissions`
--

CREATE TABLE `backendtriptales_user_user_permissions` (
  `id` bigint(20) NOT NULL,
  `user_id` bigint(20) NOT NULL,
  `permission_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Struttura della tabella `django_content_type`
--

CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dump dei dati per la tabella `django_content_type`
--

INSERT INTO `django_content_type` (`id`, `app_label`, `model`) VALUES
(2, 'auth', 'group'),
(1, 'auth', 'permission'),
(5, 'backendtriptales', 'badge'),
(9, 'backendtriptales', 'comment'),
(6, 'backendtriptales', 'groupmembership'),
(8, 'backendtriptales', 'post'),
(11, 'backendtriptales', 'postlike'),
(7, 'backendtriptales', 'tripgroup'),
(4, 'backendtriptales', 'user'),
(10, 'backendtriptales', 'userbadge'),
(3, 'contenttypes', 'contenttype');

-- --------------------------------------------------------

--
-- Struttura della tabella `django_migrations`
--

CREATE TABLE `django_migrations` (
  `id` bigint(20) NOT NULL,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dump dei dati per la tabella `django_migrations`
--

INSERT INTO `django_migrations` (`id`, `app`, `name`, `applied`) VALUES
(1, 'contenttypes', '0001_initial', '2025-05-24 07:36:15.564376'),
(2, 'contenttypes', '0002_remove_content_type_name', '2025-05-24 07:36:15.722407'),
(3, 'auth', '0001_initial', '2025-05-24 07:36:16.509159'),
(4, 'auth', '0002_alter_permission_name_max_length', '2025-05-24 07:36:16.694774'),
(5, 'auth', '0003_alter_user_email_max_length', '2025-05-24 07:36:16.715095'),
(6, 'auth', '0004_alter_user_username_opts', '2025-05-24 07:36:16.733872'),
(7, 'auth', '0005_alter_user_last_login_null', '2025-05-24 07:36:16.752662'),
(8, 'auth', '0006_require_contenttypes_0002', '2025-05-24 07:36:16.765720'),
(9, 'auth', '0007_alter_validators_add_error_messages', '2025-05-24 07:36:16.786214'),
(10, 'auth', '0008_alter_user_username_max_length', '2025-05-24 07:36:16.814609'),
(11, 'auth', '0009_alter_user_last_name_max_length', '2025-05-24 07:36:16.836771'),
(12, 'auth', '0010_alter_group_name_max_length', '2025-05-24 07:36:16.873227'),
(13, 'auth', '0011_update_proxy_permissions', '2025-05-24 07:36:16.889508'),
(14, 'auth', '0012_alter_user_first_name_max_length', '2025-05-24 07:36:16.905295'),
(15, 'backendtriptales', '0001_initial', '2025-05-24 07:36:20.343013'),
(16, 'backendtriptales', '0002_alter_tripgroup_invite_code', '2025-05-24 07:36:20.587273');

--
-- Indici per le tabelle scaricate
--

--
-- Indici per le tabelle `auth_group`
--
ALTER TABLE `auth_group`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `name` (`name`);

--
-- Indici per le tabelle `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  ADD KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`);

--
-- Indici per le tabelle `auth_permission`
--
ALTER TABLE `auth_permission`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`);

--
-- Indici per le tabelle `backendtriptales_badge`
--
ALTER TABLE `backendtriptales_badge`
  ADD PRIMARY KEY (`id`);

--
-- Indici per le tabelle `backendtriptales_comment`
--
ALTER TABLE `backendtriptales_comment`
  ADD PRIMARY KEY (`id`),
  ADD KEY `backendtriptales_com_post_id_44e8dd2f_fk_backendtr` (`post_id`),
  ADD KEY `backendtriptales_com_user_id_85b3504a_fk_backendtr` (`user_id`);

--
-- Indici per le tabelle `backendtriptales_groupmembership`
--
ALTER TABLE `backendtriptales_groupmembership`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `backendtriptales_groupmembership_group_id_user_id_cc03384c_uniq` (`group_id`,`user_id`),
  ADD KEY `backendtriptales_gro_user_id_b97b3076_fk_backendtr` (`user_id`);

--
-- Indici per le tabelle `backendtriptales_post`
--
ALTER TABLE `backendtriptales_post`
  ADD PRIMARY KEY (`id`),
  ADD KEY `backendtriptales_pos_trip_group_id_eff0fcc5_fk_backendtr` (`trip_group_id`),
  ADD KEY `backendtriptales_pos_user_id_5de4672b_fk_backendtr` (`user_id`);

--
-- Indici per le tabelle `backendtriptales_postlike`
--
ALTER TABLE `backendtriptales_postlike`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `backendtriptales_postlike_user_id_post_id_90d1efd5_uniq` (`user_id`,`post_id`),
  ADD KEY `backendtriptales_pos_post_id_c86df15a_fk_backendtr` (`post_id`);

--
-- Indici per le tabelle `backendtriptales_tripgroup`
--
ALTER TABLE `backendtriptales_tripgroup`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `invite_code` (`invite_code`),
  ADD KEY `backendtriptales_tri_creator_id_3ebafec2_fk_backendtr` (`creator_id`);

--
-- Indici per le tabelle `backendtriptales_user`
--
ALTER TABLE `backendtriptales_user`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`),
  ADD UNIQUE KEY `email` (`email`);

--
-- Indici per le tabelle `backendtriptales_userbadge`
--
ALTER TABLE `backendtriptales_userbadge`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `backendtriptales_userbadge_user_id_badge_id_a932b681_uniq` (`user_id`,`badge_id`),
  ADD KEY `backendtriptales_use_badge_id_01abfc82_fk_backendtr` (`badge_id`);

--
-- Indici per le tabelle `backendtriptales_user_groups`
--
ALTER TABLE `backendtriptales_user_groups`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `backendtriptales_user_groups_user_id_group_id_1cd7e65a_uniq` (`user_id`,`group_id`),
  ADD KEY `backendtriptales_user_groups_group_id_c5cbd10e_fk_auth_group_id` (`group_id`);

--
-- Indici per le tabelle `backendtriptales_user_user_permissions`
--
ALTER TABLE `backendtriptales_user_user_permissions`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `backendtriptales_user_us_user_id_permission_id_99aadc66_uniq` (`user_id`,`permission_id`),
  ADD KEY `backendtriptales_use_permission_id_fda7e98d_fk_auth_perm` (`permission_id`);

--
-- Indici per le tabelle `django_content_type`
--
ALTER TABLE `django_content_type`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`);

--
-- Indici per le tabelle `django_migrations`
--
ALTER TABLE `django_migrations`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT per le tabelle scaricate
--

--
-- AUTO_INCREMENT per la tabella `auth_group`
--
ALTER TABLE `auth_group`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT per la tabella `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT per la tabella `auth_permission`
--
ALTER TABLE `auth_permission`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=45;

--
-- AUTO_INCREMENT per la tabella `backendtriptales_badge`
--
ALTER TABLE `backendtriptales_badge`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

--
-- AUTO_INCREMENT per la tabella `backendtriptales_comment`
--
ALTER TABLE `backendtriptales_comment`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT per la tabella `backendtriptales_groupmembership`
--
ALTER TABLE `backendtriptales_groupmembership`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT per la tabella `backendtriptales_post`
--
ALTER TABLE `backendtriptales_post`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT per la tabella `backendtriptales_postlike`
--
ALTER TABLE `backendtriptales_postlike`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT per la tabella `backendtriptales_tripgroup`
--
ALTER TABLE `backendtriptales_tripgroup`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT per la tabella `backendtriptales_user`
--
ALTER TABLE `backendtriptales_user`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT per la tabella `backendtriptales_userbadge`
--
ALTER TABLE `backendtriptales_userbadge`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT per la tabella `backendtriptales_user_groups`
--
ALTER TABLE `backendtriptales_user_groups`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT per la tabella `backendtriptales_user_user_permissions`
--
ALTER TABLE `backendtriptales_user_user_permissions`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT per la tabella `django_content_type`
--
ALTER TABLE `django_content_type`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=12;

--
-- AUTO_INCREMENT per la tabella `django_migrations`
--
ALTER TABLE `django_migrations`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=17;

--
-- Limiti per le tabelle scaricate
--

--
-- Limiti per la tabella `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  ADD CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  ADD CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`);

--
-- Limiti per la tabella `auth_permission`
--
ALTER TABLE `auth_permission`
  ADD CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`);

--
-- Limiti per la tabella `backendtriptales_comment`
--
ALTER TABLE `backendtriptales_comment`
  ADD CONSTRAINT `backendtriptales_com_post_id_44e8dd2f_fk_backendtr` FOREIGN KEY (`post_id`) REFERENCES `backendtriptales_post` (`id`),
  ADD CONSTRAINT `backendtriptales_com_user_id_85b3504a_fk_backendtr` FOREIGN KEY (`user_id`) REFERENCES `backendtriptales_user` (`id`);

--
-- Limiti per la tabella `backendtriptales_groupmembership`
--
ALTER TABLE `backendtriptales_groupmembership`
  ADD CONSTRAINT `backendtriptales_gro_group_id_367eea3c_fk_backendtr` FOREIGN KEY (`group_id`) REFERENCES `backendtriptales_tripgroup` (`id`),
  ADD CONSTRAINT `backendtriptales_gro_user_id_b97b3076_fk_backendtr` FOREIGN KEY (`user_id`) REFERENCES `backendtriptales_user` (`id`);

--
-- Limiti per la tabella `backendtriptales_post`
--
ALTER TABLE `backendtriptales_post`
  ADD CONSTRAINT `backendtriptales_pos_trip_group_id_eff0fcc5_fk_backendtr` FOREIGN KEY (`trip_group_id`) REFERENCES `backendtriptales_tripgroup` (`id`),
  ADD CONSTRAINT `backendtriptales_pos_user_id_5de4672b_fk_backendtr` FOREIGN KEY (`user_id`) REFERENCES `backendtriptales_user` (`id`);

--
-- Limiti per la tabella `backendtriptales_postlike`
--
ALTER TABLE `backendtriptales_postlike`
  ADD CONSTRAINT `backendtriptales_pos_post_id_c86df15a_fk_backendtr` FOREIGN KEY (`post_id`) REFERENCES `backendtriptales_post` (`id`),
  ADD CONSTRAINT `backendtriptales_pos_user_id_7fb572b9_fk_backendtr` FOREIGN KEY (`user_id`) REFERENCES `backendtriptales_user` (`id`);

--
-- Limiti per la tabella `backendtriptales_tripgroup`
--
ALTER TABLE `backendtriptales_tripgroup`
  ADD CONSTRAINT `backendtriptales_tri_creator_id_3ebafec2_fk_backendtr` FOREIGN KEY (`creator_id`) REFERENCES `backendtriptales_user` (`id`);

--
-- Limiti per la tabella `backendtriptales_userbadge`
--
ALTER TABLE `backendtriptales_userbadge`
  ADD CONSTRAINT `backendtriptales_use_badge_id_01abfc82_fk_backendtr` FOREIGN KEY (`badge_id`) REFERENCES `backendtriptales_badge` (`id`),
  ADD CONSTRAINT `backendtriptales_use_user_id_eaff7005_fk_backendtr` FOREIGN KEY (`user_id`) REFERENCES `backendtriptales_user` (`id`);

--
-- Limiti per la tabella `backendtriptales_user_groups`
--
ALTER TABLE `backendtriptales_user_groups`
  ADD CONSTRAINT `backendtriptales_use_user_id_3de529f7_fk_backendtr` FOREIGN KEY (`user_id`) REFERENCES `backendtriptales_user` (`id`),
  ADD CONSTRAINT `backendtriptales_user_groups_group_id_c5cbd10e_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`);

--
-- Limiti per la tabella `backendtriptales_user_user_permissions`
--
ALTER TABLE `backendtriptales_user_user_permissions`
  ADD CONSTRAINT `backendtriptales_use_permission_id_fda7e98d_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  ADD CONSTRAINT `backendtriptales_use_user_id_e2c835f0_fk_backendtr` FOREIGN KEY (`user_id`) REFERENCES `backendtriptales_user` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
