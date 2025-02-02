-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Feb 02, 2025 at 03:37 PM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `djg_success`
--

-- --------------------------------------------------------

--
-- Table structure for table `acd_jurusan`
--

CREATE TABLE `acd_jurusan` (
  `id` bigint(20) NOT NULL,
  `nama_jurusan` varchar(255) NOT NULL,
  `status` varchar(10) NOT NULL,
  `kode_surat` varchar(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `acd_jurusan`
--

INSERT INTO `acd_jurusan` (`id`, `nama_jurusan`, `status`, `kode_surat`) VALUES
(1, 'Ilmu Ekonomi', 'Aktif', 'JEKO'),
(2, 'Ilmu Akuntansi', 'Aktif', 'JAKN'),
(3, 'Bisnis dan Kewirausahaan', 'Aktif', 'JBDK');

-- --------------------------------------------------------

--
-- Table structure for table `acd_jurusanpejabat`
--

CREATE TABLE `acd_jurusanpejabat` (
  `id` bigint(20) NOT NULL,
  `jabatan` varchar(15) NOT NULL,
  `tgl_mulai` date NOT NULL,
  `tgl_selesai` date NOT NULL,
  `label` varchar(255) DEFAULT NULL,
  `plt` tinyint(1) DEFAULT NULL,
  `jurusan_id` bigint(20) NOT NULL,
  `pejabat_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `acd_layanan`
--

CREATE TABLE `acd_layanan` (
  `id` bigint(20) NOT NULL,
  `date_in` datetime(6) NOT NULL,
  `layanan_isi` longtext NOT NULL,
  `layanan_file` varchar(100) DEFAULT NULL,
  `status` varchar(50) NOT NULL,
  `hasil_test` longtext DEFAULT NULL,
  `hasil_file` varchar(100) DEFAULT NULL,
  `hasil_link` varchar(200) DEFAULT NULL,
  `adminp_id` int(11) DEFAULT NULL,
  `layanan_jenis_id` bigint(20) DEFAULT NULL,
  `mhs_id` int(11) DEFAULT NULL,
  `prodi_id` bigint(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `acd_layanan`
--

INSERT INTO `acd_layanan` (`id`, `date_in`, `layanan_isi`, `layanan_file`, `status`, `hasil_test`, `hasil_file`, `hasil_link`, `adminp_id`, `layanan_jenis_id`, `mhs_id`, `prodi_id`) VALUES
(1, '2025-01-29 09:13:27.736986', 'asdasdasd', 'static/layanan_files/no_photo_xQyag6I.jpg', 'Waiting', NULL, '', NULL, NULL, 1, 1001, 1),
(2, '2025-01-29 11:52:19.518288', 'saya ingin menerbitaan sk pembibning', 'static/layanan_files/6-10_Jurnal_Internasional_IoT.pdf', 'Waiting', NULL, '', NULL, NULL, 1, 1001, 1);

-- --------------------------------------------------------

--
-- Table structure for table `acd_layananjenis`
--

CREATE TABLE `acd_layananjenis` (
  `id` bigint(20) NOT NULL,
  `nama_layanan` varchar(255) NOT NULL,
  `prasyarat_layanan` longtext NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `acd_layananjenis`
--

INSERT INTO `acd_layananjenis` (`id`, `nama_layanan`, `prasyarat_layanan`) VALUES
(1, 'SK Pembimbing', 'judul diterima'),
(2, 'Seminar Proposal', 'proposal ACC');

-- --------------------------------------------------------

--
-- Table structure for table `acd_nosurat`
--

CREATE TABLE `acd_nosurat` (
  `id` bigint(20) NOT NULL,
  `tahun` varchar(5) NOT NULL,
  `date_in` date NOT NULL,
  `nomor` int(11) NOT NULL,
  `perihal` varchar(255) NOT NULL,
  `tujuan` varchar(255) NOT NULL,
  `adminp_id` int(11) NOT NULL,
  `jurusan_id` bigint(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `acd_nosurat`
--

INSERT INTO `acd_nosurat` (`id`, `tahun`, `date_in`, `nomor`, `perihal`, `tujuan`, `adminp_id`, `jurusan_id`) VALUES
(6, '2025', '2025-01-31', 1, 'asdasd', 'asdasdasd', 1, 2),
(7, '2025', '2025-01-31', 2, 'asdasd', 'asdads', 1, 2),
(8, '2025', '2025-01-31', 123, 'asdads', 'asdasd', 1, 1),
(10, '2025', '2025-01-31', 124, 'asdasd', 'asdasd', 1, 1),
(11, '2025', '2025-02-02', 125, 'asdasdasd', 'asdadasdasd', 1, 1),
(12, '2025', '2025-02-02', 126, 'dsfsdfsdf', 'sdfsdfsdfsd', 1, 1),
(13, '2025', '2025-02-02', 127, 'czsdzszs', 'zszdzsdzsd', 1, 1);

-- --------------------------------------------------------

--
-- Table structure for table `acd_prodi`
--

CREATE TABLE `acd_prodi` (
  `id` bigint(20) NOT NULL,
  `strata` varchar(5) NOT NULL,
  `nama_prodi` varchar(255) NOT NULL,
  `gelar` varchar(10) NOT NULL,
  `kode_mk` varchar(20) NOT NULL,
  `nama_mk` varchar(50) NOT NULL,
  `status` varchar(10) NOT NULL,
  `jurusan_id` bigint(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `acd_prodi`
--

INSERT INTO `acd_prodi` (`id`, `strata`, `nama_prodi`, `gelar`, `kode_mk`, `nama_mk`, `status`, `jurusan_id`) VALUES
(1, 'S1', 'Pendidikan Ekonomi', '-', '-', '-', 'Aktif', 1),
(2, 'S1', 'Pendidikan Akuntansi', '-', '-', '-', 'Aktif', 2),
(3, 'S1', 'Manajamen', '-', '-', '-', 'Aktif', 1),
(4, 'S1', 'Ekonomi Pembangunan', '-', '-', '-', 'Aktif', 1),
(5, 'S1', 'Akuntansi', '-', '-', '-', 'Aktif', 2),
(6, 'S1', 'Kewirausahaan', '-', '-', '-', 'Aktif', 3),
(7, 'S1', 'Bisnis Digital', '-', '-', '-', 'Aktif', 3),
(8, 'D4', 'Akuntansi', '-', '-', '-', 'Aktif', 2);

-- --------------------------------------------------------

--
-- Table structure for table `acd_prodipejabat`
--

CREATE TABLE `acd_prodipejabat` (
  `id` bigint(20) NOT NULL,
  `jabatan` varchar(15) NOT NULL,
  `tgl_mulai` date NOT NULL,
  `tgl_selesai` date NOT NULL,
  `label` varchar(255) DEFAULT NULL,
  `plt` tinyint(1) DEFAULT NULL,
  `pejabat_id` int(11) NOT NULL,
  `prodi_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `acd_prodipejabat`
--

INSERT INTO `acd_prodipejabat` (`id`, `jabatan`, `tgl_mulai`, `tgl_selesai`, `label`, `plt`, `pejabat_id`, `prodi_id`) VALUES
(1, 'Ketua', '2025-01-01', '2029-01-01', '-', 0, 106, 1);

-- --------------------------------------------------------

--
-- Table structure for table `acd_skripsijudul`
--

CREATE TABLE `acd_skripsijudul` (
  `id` bigint(20) NOT NULL,
  `date_in` datetime(6) NOT NULL,
  `user_id` int(11) NOT NULL,
  `prodi_id` bigint(20) DEFAULT NULL,
  `penasehat_akademik_id` int(11) DEFAULT NULL,
  `judul_1` varchar(255) NOT NULL,
  `deskripsi_judul_1` longtext DEFAULT NULL,
  `judul_2` varchar(255) DEFAULT NULL,
  `deskripsi_judul_2` longtext DEFAULT NULL,
  `judul_3` varchar(255) DEFAULT NULL,
  `deskripsi_judul_3` longtext DEFAULT NULL,
  `status` varchar(10) NOT NULL,
  `status_ket` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `acd_skripsijudul`
--

INSERT INTO `acd_skripsijudul` (`id`, `date_in`, `user_id`, `prodi_id`, `penasehat_akademik_id`, `judul_1`, `deskripsi_judul_1`, `judul_2`, `deskripsi_judul_2`, `judul_3`, `deskripsi_judul_3`, `status`, `status_ket`) VALUES
(1, '2025-01-29 11:43:17.754063', 1001, 1, 147, 'dasdasd', 'asdasdasd', 'asdasdasd', 'asdasdasd', 'asdasd', 'sdasdasd', 'Waiting', 'sdasd');

-- --------------------------------------------------------

--
-- Table structure for table `acd_userdosen`
--

CREATE TABLE `acd_userdosen` (
  `id` bigint(20) NOT NULL,
  `telp` varchar(15) NOT NULL,
  `photo` varchar(100) DEFAULT NULL,
  `gender` varchar(15) NOT NULL,
  `prodi_id` bigint(20) DEFAULT NULL,
  `user_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `acd_userdosen`
--

INSERT INTO `acd_userdosen` (`id`, `telp`, `photo`, `gender`, `prodi_id`, `user_id`) VALUES
(1, '62', '', 'Laki-laki', 1, 101),
(2, '62', '', 'Laki-laki', 1, 102),
(3, '62', '', 'Laki-laki', 1, 103),
(4, '62', '', 'Laki-laki', 1, 104),
(5, '62', '', 'Laki-laki', 1, 105),
(6, '62', '', 'Laki-laki', 1, 106),
(7, '62', '', 'Laki-laki', 1, 107),
(8, '62', '', 'Laki-laki', 1, 108),
(9, '62', '', 'Laki-laki', 1, 109),
(10, '62', '', 'Laki-laki', 1, 110),
(11, '62', '', 'Laki-laki', 2, 111),
(12, '62', '', 'Laki-laki', 2, 112),
(13, '62', '', 'Laki-laki', 2, 113),
(14, '62', '', 'Laki-laki', 2, 114),
(15, '62', '', 'Laki-laki', 2, 115),
(16, '62', '', 'Laki-laki', 2, 116),
(17, '62', '', 'Laki-laki', 2, 117),
(18, '62', '', 'Laki-laki', 2, 118),
(19, '62', '', 'Laki-laki', 3, 119),
(20, '62', '', 'Laki-laki', 3, 120),
(21, '62', '', 'Laki-laki', 3, 121),
(22, '62', '', 'Laki-laki', 3, 122),
(23, '62', '', 'Laki-laki', 3, 123),
(24, '62', '', 'Laki-laki', 3, 124),
(25, '62', '', 'Laki-laki', 3, 125),
(26, '62', '', 'Laki-laki', 3, 126),
(27, '62', '', 'Laki-laki', 3, 127),
(28, '62', '', 'Laki-laki', 3, 128),
(29, '62', '', 'Laki-laki', 3, 129),
(30, '62', '', 'Laki-laki', 3, 130),
(31, '62', '', 'Laki-laki', 3, 131),
(32, '62', '', 'Laki-laki', 3, 132),
(33, '123', '', 'Laki-laki', 3, 133),
(34, '62', '', 'Laki-laki', 3, 134),
(35, '62', '', 'Laki-laki', 3, 135),
(36, '62', '', 'Laki-laki', 3, 136),
(37, '62', '', 'Laki-laki', 3, 137),
(38, '62', '', 'Laki-laki', 3, 138),
(39, '62', '', 'Laki-laki', 4, 139),
(40, '62', '', 'Laki-laki', 4, 140),
(41, '62', '', 'Laki-laki', 4, 141),
(42, '62', '', 'Laki-laki', 4, 142),
(43, '62', '', 'Laki-laki', 4, 143),
(44, '62', '', 'Laki-laki', 4, 144),
(45, '62', '', 'Laki-laki', 4, 145),
(46, '62', '', 'Laki-laki', 4, 146),
(47, '62', '', 'Laki-laki', 6, 147),
(48, '62', '', 'Laki-laki', 6, 148),
(49, '62', '', 'Laki-laki', 6, 149),
(50, '62', '', 'Laki-laki', 6, 150),
(51, '62', '', 'Laki-laki', 6, 151),
(52, '62', 'static/img_profile/dosen/eagle.png', 'Laki-laki', 7, 152),
(53, '62', '', 'Laki-laki', 7, 153),
(54, '62', '', 'Laki-laki', 7, 154),
(55, '62', '', 'Laki-laki', 7, 155),
(56, '62', '', 'Laki-laki', 7, 156),
(57, '62', '', 'Laki-laki', 7, 157),
(58, '62', '', 'Laki-laki', 7, 158),
(59, '62', '', 'Laki-laki', 7, 159),
(60, '62', '', 'Laki-laki', 7, 160),
(61, '62', '', 'Laki-laki', 7, 161),
(62, '62', '', 'Laki-laki', 7, 162),
(63, '62', '', 'Laki-laki', 7, 163),
(64, '62', '', 'Laki-laki', 7, 164),
(65, '62', '', 'Laki-laki', 8, 165),
(66, '62', '', 'Laki-laki', 8, 166),
(67, '62', '', 'Laki-laki', 8, 167),
(68, '62', '', 'Laki-laki', 8, 168);

-- --------------------------------------------------------

--
-- Table structure for table `acd_userfakultas`
--

CREATE TABLE `acd_userfakultas` (
  `id` bigint(20) NOT NULL,
  `telp` varchar(15) NOT NULL,
  `photo` varchar(100) DEFAULT NULL,
  `gender` varchar(15) NOT NULL,
  `user_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `acd_userfakultas`
--

INSERT INTO `acd_userfakultas` (`id`, `telp`, `photo`, `gender`, `user_id`) VALUES
(3, '0000', 'static/img_profile/fakultas/images.jpg', 'Laki-laki', 9),
(4, '0000', '', 'Laki-laki', 10);

-- --------------------------------------------------------

--
-- Table structure for table `acd_usermhs`
--

CREATE TABLE `acd_usermhs` (
  `id` bigint(20) NOT NULL,
  `telp` varchar(15) NOT NULL,
  `photo` varchar(100) DEFAULT NULL,
  `gender` varchar(15) NOT NULL,
  `prodi_id` bigint(20) DEFAULT NULL,
  `user_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `acd_usermhs`
--

INSERT INTO `acd_usermhs` (`id`, `telp`, `photo`, `gender`, `prodi_id`, `user_id`) VALUES
(1, '555', 'static/img_profile/mhs/IMG-20250202-WA0024.jpg', 'Laki-laki', 1, 1001),
(2, '555', '', 'Laki-laki', 1, 1002),
(3, '555', '', 'Laki-laki', 1, 1003),
(4, '555', '', 'Laki-laki', 1, 1004),
(5, '555', '', 'Laki-laki', 1, 1005),
(6, '555', '', 'Laki-laki', 1, 1006),
(7, '555', '', 'Laki-laki', 1, 1007),
(8, '555', '', 'Laki-laki', 1, 1008),
(9, '555', '', 'Laki-laki', 1, 1009),
(10, '555', '', 'Laki-laki', 1, 1010);

-- --------------------------------------------------------

--
-- Table structure for table `acd_userprodi`
--

CREATE TABLE `acd_userprodi` (
  `id` bigint(20) NOT NULL,
  `telp` varchar(15) NOT NULL,
  `photo` varchar(100) DEFAULT NULL,
  `gender` varchar(15) NOT NULL,
  `prodi_id` bigint(20) DEFAULT NULL,
  `user_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `acd_userprodi`
--

INSERT INTO `acd_userprodi` (`id`, `telp`, `photo`, `gender`, `prodi_id`, `user_id`) VALUES
(1, '555', 'static/img_profile/prodi/no_photo_olw7jJU.jpg', 'Laki-laki', 1, 1),
(2, '555', '', 'Laki-laki', 2, 2),
(3, '555', '', 'Laki-laki', 3, 3),
(5, '555', '', 'Laki-laki', 5, 5),
(6, '555', '', 'Laki-laki', 6, 6),
(7, '555', '', 'Laki-laki', 7, 7),
(8, '555', '', 'Laki-laki', 8, 8);

-- --------------------------------------------------------

--
-- Table structure for table `auth_group`
--

CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL,
  `name` varchar(150) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `auth_group_permissions`
--

CREATE TABLE `auth_group_permissions` (
  `id` bigint(20) NOT NULL,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `auth_permission`
--

CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `auth_permission`
--

INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES
(1, 'Can add log entry', 1, 'add_logentry'),
(2, 'Can change log entry', 1, 'change_logentry'),
(3, 'Can delete log entry', 1, 'delete_logentry'),
(4, 'Can view log entry', 1, 'view_logentry'),
(5, 'Can add permission', 2, 'add_permission'),
(6, 'Can change permission', 2, 'change_permission'),
(7, 'Can delete permission', 2, 'delete_permission'),
(8, 'Can view permission', 2, 'view_permission'),
(9, 'Can add group', 3, 'add_group'),
(10, 'Can change group', 3, 'change_group'),
(11, 'Can delete group', 3, 'delete_group'),
(12, 'Can view group', 3, 'view_group'),
(13, 'Can add user', 4, 'add_user'),
(14, 'Can change user', 4, 'change_user'),
(15, 'Can delete user', 4, 'delete_user'),
(16, 'Can view user', 4, 'view_user'),
(17, 'Can add content type', 5, 'add_contenttype'),
(18, 'Can change content type', 5, 'change_contenttype'),
(19, 'Can delete content type', 5, 'delete_contenttype'),
(20, 'Can view content type', 5, 'view_contenttype'),
(21, 'Can add session', 6, 'add_session'),
(22, 'Can change session', 6, 'change_session'),
(23, 'Can delete session', 6, 'delete_session'),
(24, 'Can view session', 6, 'view_session'),
(25, 'Can add jurusan', 7, 'add_jurusan'),
(26, 'Can change jurusan', 7, 'change_jurusan'),
(27, 'Can delete jurusan', 7, 'delete_jurusan'),
(28, 'Can view jurusan', 7, 'view_jurusan'),
(29, 'Can add layanan jenis', 8, 'add_layananjenis'),
(30, 'Can change layanan jenis', 8, 'change_layananjenis'),
(31, 'Can delete layanan jenis', 8, 'delete_layananjenis'),
(32, 'Can view layanan jenis', 8, 'view_layananjenis'),
(33, 'Can add prodi', 9, 'add_prodi'),
(34, 'Can change prodi', 9, 'change_prodi'),
(35, 'Can delete prodi', 9, 'delete_prodi'),
(36, 'Can view prodi', 9, 'view_prodi'),
(37, 'Can add user prodi', 10, 'add_userprodi'),
(38, 'Can change user prodi', 10, 'change_userprodi'),
(39, 'Can delete user prodi', 10, 'delete_userprodi'),
(40, 'Can view user prodi', 10, 'view_userprodi'),
(41, 'Can add user mhs', 11, 'add_usermhs'),
(42, 'Can change user mhs', 11, 'change_usermhs'),
(43, 'Can delete user mhs', 11, 'delete_usermhs'),
(44, 'Can view user mhs', 11, 'view_usermhs'),
(45, 'Can add user fakultas', 12, 'add_userfakultas'),
(46, 'Can change user fakultas', 12, 'change_userfakultas'),
(47, 'Can delete user fakultas', 12, 'delete_userfakultas'),
(48, 'Can view user fakultas', 12, 'view_userfakultas'),
(49, 'Can add user dosen', 13, 'add_userdosen'),
(50, 'Can change user dosen', 13, 'change_userdosen'),
(51, 'Can delete user dosen', 13, 'delete_userdosen'),
(52, 'Can view user dosen', 13, 'view_userdosen'),
(53, 'Can add skripsi judul', 14, 'add_skripsijudul'),
(54, 'Can change skripsi judul', 14, 'change_skripsijudul'),
(55, 'Can delete skripsi judul', 14, 'delete_skripsijudul'),
(56, 'Can view skripsi judul', 14, 'view_skripsijudul'),
(57, 'Can add no surat', 15, 'add_nosurat'),
(58, 'Can change no surat', 15, 'change_nosurat'),
(59, 'Can delete no surat', 15, 'delete_nosurat'),
(60, 'Can view no surat', 15, 'view_nosurat'),
(61, 'Can add layanan', 16, 'add_layanan'),
(62, 'Can change layanan', 16, 'change_layanan'),
(63, 'Can delete layanan', 16, 'delete_layanan'),
(64, 'Can view layanan', 16, 'view_layanan'),
(65, 'Can add jurusan pejabat', 17, 'add_jurusanpejabat'),
(66, 'Can change jurusan pejabat', 17, 'change_jurusanpejabat'),
(67, 'Can delete jurusan pejabat', 17, 'delete_jurusanpejabat'),
(68, 'Can view jurusan pejabat', 17, 'view_jurusanpejabat'),
(69, 'Can add prodi pejabat', 18, 'add_prodipejabat'),
(70, 'Can change prodi pejabat', 18, 'change_prodipejabat'),
(71, 'Can delete prodi pejabat', 18, 'delete_prodipejabat'),
(72, 'Can view prodi pejabat', 18, 'view_prodipejabat');

-- --------------------------------------------------------

--
-- Table structure for table `auth_user`
--

CREATE TABLE `auth_user` (
  `id` int(11) NOT NULL,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `auth_user`
--

INSERT INTO `auth_user` (`id`, `password`, `last_login`, `is_superuser`, `username`, `first_name`, `last_name`, `email`, `is_staff`, `is_active`, `date_joined`) VALUES
(1, 'pbkdf2_sha256$600000$LTuwNwFpmrTvW7vFXFVaU2$oWhCn/F1mpJEmmcqw/Vmb/lcoEUU2x9pqaua9Hg1B38=', '2025-02-02 07:23:45.432057', 1, 'admin', 'Admin Super', 'Admin Prodi', 'admin@admin.com', 1, 1, '2025-01-29 07:43:56.619121'),
(2, 'pbkdf2_sha256$600000$1qjpzULTgNgSZjE5f0dsiq$hKTmq4C7dNRYWYjJW1AuOEP5rqVop6zem78/y65Xmys=', '2025-01-29 07:44:14.979738', 0, 'admin1', 'Admin Prodi 001', 'Admin Prodi', '', 0, 1, '2025-01-29 07:43:56.619121'),
(3, 'pbkdf2_sha256$600000$G1equjL6TYqARvqGlXA8SI$zJ9yqtmNrxeh/lrtQaq3cJq/5UdxNQxF1c84vV++N64=', '2025-01-29 07:44:14.979739', 0, 'admin2', 'Admin Prodi 002', 'Admin Prodi', '', 0, 1, '2025-01-29 07:43:56.619121'),
(5, 'pbkdf2_sha256$600000$1qjpzULTgNgSZjE5f0dsiq$hKTmq4C7dNRYWYjJW1AuOEP5rqVop6zem78/y65Xmys=', '2025-01-29 07:44:14.979741', 0, 'admin4', 'Admin Prodi 004', 'Admin Prodi', '', 0, 1, '2025-01-29 07:43:56.619121'),
(6, 'pbkdf2_sha256$600000$G1equjL6TYqARvqGlXA8SI$zJ9yqtmNrxeh/lrtQaq3cJq/5UdxNQxF1c84vV++N64=', '2025-01-29 07:44:14.979742', 0, 'admin5', 'Admin Prodi 005', 'Admin Prodi', '', 0, 1, '2025-01-29 07:43:56.619121'),
(7, 'pbkdf2_sha256$600000$LTuwNwFpmrTvW7vFXFVaU2$oWhCn/F1mpJEmmcqw/Vmb/lcoEUU2x9pqaua9Hg1B38=', '2025-01-29 07:44:14.979743', 0, 'admin6', 'Admin Prodi 006', 'Admin Prodi', '', 0, 1, '2025-01-29 07:43:56.619121'),
(8, 'pbkdf2_sha256$600000$LTuwNwFpmrTvW7vFXFVaU2$oWhCn/F1mpJEmmcqw/Vmb/lcoEUU2x9pqaua9Hg1B38=', '2025-01-29 07:44:14.979744', 0, 'admin7', 'Admin Prodi 007', 'Admin Prodi', '', 0, 1, '2025-01-29 07:43:56.619121'),
(9, 'pbkdf2_sha256$600000$StfgSiLkVelzyzTC2Kyjul$Q7DzrjGSYbsbaaXEjmF9Of1t7A2uOx8K+46+PRzi440=', '2025-02-02 09:17:04.908718', 0, 'adminf1', 'Admin Fakultas 001', 'Admin Fakultas', '', 0, 1, '2025-01-29 07:43:56.000000'),
(10, 'pbkdf2_sha256$600000$G1equjL6TYqARvqGlXA8SI$zJ9yqtmNrxeh/lrtQaq3cJq/5UdxNQxF1c84vV++N64=', '2025-01-29 07:44:14.000000', 0, 'adminf2', 'Admin Fakultas 002', 'Admin Fakultas', '', 0, 1, '2025-01-29 07:43:56.000000'),
(101, 'pbkdf2_sha256$600000$LTuwNwFpmrTvW7vFXFVaU2$oWhCn/F1mpJEmmcqw/Vmb/lcoEUU2x9pqaua9Hg1B38=', '2025-01-29 07:44:14.979747', 0, '196201111987021001', 'Prof. Dr. H. Thamrin Tahir, M.Si.', 'Dosen', '', 0, 1, '2025-01-29 07:43:56.619121'),
(102, 'pbkdf2_sha256$600000$1qjpzULTgNgSZjE5f0dsiq$hKTmq4C7dNRYWYjJW1AuOEP5rqVop6zem78/y65Xmys=', '2025-01-29 07:44:14.979748', 0, '198212052006041002', 'Dr. Rahmatullah, S.Pd, M.Pd.', 'Dosen', '', 0, 1, '2025-01-29 07:43:56.619121'),
(103, 'pbkdf2_sha256$600000$1qjpzULTgNgSZjE5f0dsiq$hKTmq4C7dNRYWYjJW1AuOEP5rqVop6zem78/y65Xmys=', '2025-01-29 07:44:14.979749', 0, '198509062010121007', 'Muhammad Hasan, S.Pd., M.Pd.', 'Dosen', '', 0, 1, '2025-01-29 07:43:56.619121'),
(104, 'pbkdf2_sha256$600000$G1equjL6TYqARvqGlXA8SI$zJ9yqtmNrxeh/lrtQaq3cJq/5UdxNQxF1c84vV++N64=', '2025-01-29 07:44:14.979750', 0, '196104021986102001', 'Dr. Tuti Supatminingsih, M.Si.', 'Dosen', '', 0, 1, '2025-01-29 07:43:56.619121'),
(105, 'pbkdf2_sha256$600000$LTuwNwFpmrTvW7vFXFVaU2$oWhCn/F1mpJEmmcqw/Vmb/lcoEUU2x9pqaua9Hg1B38=', '2025-01-29 07:44:14.979751', 0, '195912171987021001', 'Muhammad Dinar, S.E., M.Si.', 'Dosen', '', 0, 1, '2025-01-29 07:43:56.619121'),
(106, 'pbkdf2_sha256$600000$1qjpzULTgNgSZjE5f0dsiq$hKTmq4C7dNRYWYjJW1AuOEP5rqVop6zem78/y65Xmys=', '2025-01-29 07:44:14.979752', 0, '197307092007011001', 'Dr. Muh. Ihsan Said, S.E., M.Si.', 'Dosen', '', 0, 1, '2025-01-29 07:43:56.619121'),
(107, 'pbkdf2_sha256$600000$G1equjL6TYqARvqGlXA8SI$zJ9yqtmNrxeh/lrtQaq3cJq/5UdxNQxF1c84vV++N64=', '2025-01-29 07:44:14.979753', 0, '197107052007011001', 'Dr. Mustari, S.E., M.Si.', 'Dosen', '', 0, 1, '2025-01-29 07:43:56.619121'),
(108, 'pbkdf2_sha256$600000$LTuwNwFpmrTvW7vFXFVaU2$oWhCn/F1mpJEmmcqw/Vmb/lcoEUU2x9pqaua9Hg1B38=', '2025-01-29 07:44:14.979754', 0, '198203242015042001', 'Nurdiana, S.E., M.Si.', 'Dosen', '', 0, 1, '2025-01-29 07:43:56.619121'),
(109, 'pbkdf2_sha256$600000$1qjpzULTgNgSZjE5f0dsiq$hKTmq4C7dNRYWYjJW1AuOEP5rqVop6zem78/y65Xmys=', '2025-01-29 07:44:14.979755', 0, '198106232007012001', 'Dr. Hj. Inanna, S.Pd., M.Pd.', 'Dosen', '', 0, 1, '2025-01-29 07:43:56.619121'),
(110, 'pbkdf2_sha256$600000$G1equjL6TYqARvqGlXA8SI$zJ9yqtmNrxeh/lrtQaq3cJq/5UdxNQxF1c84vV++N64=', '2025-01-29 07:44:14.979756', 0, '199105062019032015', 'Andi Tenri Ampa, S.Pd., M.Pd.', 'Dosen', '', 0, 1, '2025-01-29 07:43:56.619121'),
(111, 'pbkdf2_sha256$600000$LTuwNwFpmrTvW7vFXFVaU2$oWhCn/F1mpJEmmcqw/Vmb/lcoEUU2x9pqaua9Hg1B38=', '2025-01-29 07:44:14.979757', 0, '195912311986011005', 'Prof. Dr. H. Muhammad Azis, M.Si.', 'Dosen', '', 0, 1, '2025-01-29 07:43:56.619121'),
(112, 'pbkdf2_sha256$600000$1qjpzULTgNgSZjE5f0dsiq$hKTmq4C7dNRYWYjJW1AuOEP5rqVop6zem78/y65Xmys=', '2025-01-29 07:44:14.979758', 0, '195805021985031003', 'M. Yusuf A. Ngampo, M.M.', 'Dosen', '', 0, 1, '2025-01-29 07:43:56.619121'),
(113, 'pbkdf2_sha256$600000$G1equjL6TYqARvqGlXA8SI$zJ9yqtmNrxeh/lrtQaq3cJq/5UdxNQxF1c84vV++N64=', '2025-01-29 07:44:14.979759', 0, '195907081986011001', 'H. Abd. Rijal, M.Si.', 'Dosen', '', 0, 1, '2025-01-29 07:43:56.619121'),
(114, 'pbkdf2_sha256$600000$LTuwNwFpmrTvW7vFXFVaU2$oWhCn/F1mpJEmmcqw/Vmb/lcoEUU2x9pqaua9Hg1B38=', '2025-01-29 07:44:14.979760', 0, '196705141993032003', 'Dra. Sitti Hajerah Hasyim, M.Si.', 'Dosen', '', 0, 1, '2025-01-29 07:43:56.619121'),
(115, 'pbkdf2_sha256$600000$1qjpzULTgNgSZjE5f0dsiq$hKTmq4C7dNRYWYjJW1AuOEP5rqVop6zem78/y65Xmys=', '2025-01-29 07:44:14.979761', 0, '197510272000031001', 'M. Ridwan Tikollah, S.Pd., M.SA.', 'Dosen', '', 0, 1, '2025-01-29 07:43:56.619121'),
(116, 'pbkdf2_sha256$600000$G1equjL6TYqARvqGlXA8SI$zJ9yqtmNrxeh/lrtQaq3cJq/5UdxNQxF1c84vV++N64=', '2025-01-29 07:44:14.979762', 0, '197502162005011002', 'Sahade, S.Pd., M.Pd.', 'Dosen', '', 0, 1, '2025-01-29 07:43:56.619121'),
(117, 'pbkdf2_sha256$600000$LTuwNwFpmrTvW7vFXFVaU2$oWhCn/F1mpJEmmcqw/Vmb/lcoEUU2x9pqaua9Hg1B38=', '2025-01-29 07:44:14.979763', 0, '198405302015042002', 'Nuraisyiah, S.Pd., M.Pd.', 'Dosen', '', 0, 1, '2025-01-29 07:43:56.619121'),
(118, 'pbkdf2_sha256$600000$1qjpzULTgNgSZjE5f0dsiq$hKTmq4C7dNRYWYjJW1AuOEP5rqVop6zem78/y65Xmys=', '2025-01-29 07:44:14.979764', 0, '199108222019032015', 'Fajriani Azis, S.Pd., M.Si.', 'Dosen', '', 0, 1, '2025-01-29 07:43:56.619121'),
(119, 'pbkdf2_sha256$600000$G1equjL6TYqARvqGlXA8SI$zJ9yqtmNrxeh/lrtQaq3cJq/5UdxNQxF1c84vV++N64=', '2025-01-29 07:44:14.979765', 0, '195607201983031003', 'Prof. Dr. H. Amiruddin Tawe, M.S.', 'Dosen', '', 0, 1, '2025-01-29 07:43:56.619121'),
(120, 'pbkdf2_sha256$600000$LTuwNwFpmrTvW7vFXFVaU2$oWhCn/F1mpJEmmcqw/Vmb/lcoEUU2x9pqaua9Hg1B38=', '2025-01-29 07:44:14.979766', 0, '196212031988031001', 'Prof. Dr. Chalid Imran Musa, M.Si.', 'Dosen', '', 0, 1, '2025-01-29 07:43:56.619121'),
(121, 'pbkdf2_sha256$600000$1qjpzULTgNgSZjE5f0dsiq$hKTmq4C7dNRYWYjJW1AuOEP5rqVop6zem78/y65Xmys=', '2025-01-29 07:44:14.979767', 0, '196307151988111001', 'Prof. Dr. Romansyah Sahabuddin, S.E., M.Si.', 'Dosen', '', 0, 1, '2025-01-29 07:43:56.619121'),
(122, 'pbkdf2_sha256$600000$G1equjL6TYqARvqGlXA8SI$zJ9yqtmNrxeh/lrtQaq3cJq/5UdxNQxF1c84vV++N64=', '2025-01-29 07:44:14.979768', 0, '196012312000121001', 'Prof. Dr. Anwar Ramli, S.E., M.Si.', 'Dosen', '', 0, 1, '2025-01-29 07:43:56.619121'),
(123, 'pbkdf2_sha256$600000$LTuwNwFpmrTvW7vFXFVaU2$oWhCn/F1mpJEmmcqw/Vmb/lcoEUU2x9pqaua9Hg1B38=', '2025-01-29 07:44:14.979769', 0, '196712152002122001', 'Dr. Hj. Siti Hasbiah, M.Si.', 'Dosen', '', 0, 1, '2025-01-29 07:43:56.619121'),
(124, 'pbkdf2_sha256$600000$1qjpzULTgNgSZjE5f0dsiq$hKTmq4C7dNRYWYjJW1AuOEP5rqVop6zem78/y65Xmys=', '2025-01-29 07:44:14.979770', 0, '197304052003121002', 'Dr. Abdi Akbar, S.T., M.M.', 'Dosen', '', 0, 1, '2025-01-29 07:43:56.619121'),
(125, 'pbkdf2_sha256$600000$G1equjL6TYqARvqGlXA8SI$zJ9yqtmNrxeh/lrtQaq3cJq/5UdxNQxF1c84vV++N64=', '2025-01-29 07:44:14.979771', 0, '197104232005011002', 'Dr. Agung Widhi Kurniawan, S.T., M.M.', 'Dosen', '', 0, 1, '2025-01-29 07:43:56.619121'),
(126, 'pbkdf2_sha256$600000$LTuwNwFpmrTvW7vFXFVaU2$oWhCn/F1mpJEmmcqw/Vmb/lcoEUU2x9pqaua9Hg1B38=', '2025-01-29 07:44:14.979772', 0, '198011262007101001', 'Ikhwan Maulana Haeruddin, S.E., MHRMgt, Ph.D.', 'Dosen', '', 0, 1, '2025-01-29 07:43:56.619121'),
(127, 'pbkdf2_sha256$600000$1qjpzULTgNgSZjE5f0dsiq$hKTmq4C7dNRYWYjJW1AuOEP5rqVop6zem78/y65Xmys=', '2025-01-29 07:44:14.979773', 0, '198204262007101001', 'Dr. Anwar, S.E., M.Si.', 'Dosen', '', 0, 1, '2025-01-29 07:43:56.619121'),
(128, 'pbkdf2_sha256$600000$G1equjL6TYqARvqGlXA8SI$zJ9yqtmNrxeh/lrtQaq3cJq/5UdxNQxF1c84vV++N64=', '2025-01-29 07:44:14.979774', 0, '196104181983021002', 'Dr. Burhanuddin, S.Sos., S.E., M.M.', 'Dosen', '', 0, 1, '2025-01-29 07:43:56.619121'),
(129, 'pbkdf2_sha256$600000$LTuwNwFpmrTvW7vFXFVaU2$oWhCn/F1mpJEmmcqw/Vmb/lcoEUU2x9pqaua9Hg1B38=', '2025-01-29 07:44:14.979775', 0, '197102162007011001', 'Ichwan Musa, S.E., M.Si.', 'Dosen', '', 0, 1, '2025-01-29 07:43:56.619121'),
(130, 'pbkdf2_sha256$600000$1qjpzULTgNgSZjE5f0dsiq$hKTmq4C7dNRYWYjJW1AuOEP5rqVop6zem78/y65Xmys=', '2025-01-29 07:44:14.979776', 0, '197411102008011017', 'Nurman, S.E., M.Si.', 'Dosen', '', 0, 1, '2025-01-29 07:43:56.619121'),
(131, 'pbkdf2_sha256$600000$G1equjL6TYqARvqGlXA8SI$zJ9yqtmNrxeh/lrtQaq3cJq/5UdxNQxF1c84vV++N64=', '2025-01-29 07:44:14.979777', 0, '198009082008012011', 'Dr. Hety Budianty, S.E., M. Ak.', 'Dosen', '', 0, 1, '2025-01-29 07:43:56.619121'),
(132, 'pbkdf2_sha256$600000$LTuwNwFpmrTvW7vFXFVaU2$oWhCn/F1mpJEmmcqw/Vmb/lcoEUU2x9pqaua9Hg1B38=', '2025-01-29 07:44:14.979778', 0, '198303192015041001', 'Uhud Darmawan Natsir, S.E., M.M.', 'Dosen', '', 0, 1, '2025-01-29 07:43:56.619121'),
(133, 'pbkdf2_sha256$600000$EoafoGWeimG8hwNN5LOkU3$wOwSUM+TNObUcpmRgAsq/mJuxwI5IerXHT5hoAuXlLs=', NULL, 0, '198303192015041001a', 'Ilham Wardhana Haeuddin, S.E., MMktMgt', 'Dosen', '', 0, 1, '2025-01-29 08:57:44.000000'),
(134, 'pbkdf2_sha256$600000$G1equjL6TYqARvqGlXA8SI$zJ9yqtmNrxeh/lrtQaq3cJq/5UdxNQxF1c84vV++N64=', '2025-01-29 07:44:14.979780', 0, '195712311986011005', 'Drs. M. Taslim Dangnga, M.Si.', 'Dosen', '', 0, 1, '2025-01-29 07:43:56.619121'),
(135, 'pbkdf2_sha256$600000$LTuwNwFpmrTvW7vFXFVaU2$oWhCn/F1mpJEmmcqw/Vmb/lcoEUU2x9pqaua9Hg1B38=', '2025-01-29 07:44:14.979781', 0, '197510102006041002', 'Zainal Ruma, S.Pd., M.M.', 'Dosen', '', 0, 1, '2025-01-29 07:43:56.619121'),
(136, 'pbkdf2_sha256$600000$1qjpzULTgNgSZjE5f0dsiq$hKTmq4C7dNRYWYjJW1AuOEP5rqVop6zem78/y65Xmys=', '2025-01-29 07:44:14.979782', 0, '195803181987021001', 'Ahmad Ali, S.E., M.Ak., CA.', 'Dosen', '', 0, 1, '2025-01-29 07:43:56.619121'),
(137, 'pbkdf2_sha256$600000$G1equjL6TYqARvqGlXA8SI$zJ9yqtmNrxeh/lrtQaq3cJq/5UdxNQxF1c84vV++N64=', '2025-01-29 07:44:14.979783', 0, '197411132002122001', 'Tenri Sayu Puspitaningsih Dipoatmodjo, S.E., M.M.', 'Dosen', '', 0, 1, '2025-01-29 07:43:56.619121'),
(138, 'pbkdf2_sha256$600000$LTuwNwFpmrTvW7vFXFVaU2$oWhCn/F1mpJEmmcqw/Vmb/lcoEUU2x9pqaua9Hg1B38=', '2025-01-29 07:44:14.979784', 0, '198703282018032001', 'Andi Mustika Amin, S.E., M.Si.', 'Dosen', '', 0, 1, '2025-01-29 07:43:56.619121'),
(139, 'pbkdf2_sha256$600000$1qjpzULTgNgSZjE5f0dsiq$hKTmq4C7dNRYWYjJW1AuOEP5rqVop6zem78/y65Xmys=', '2025-01-29 07:44:14.979785', 0, '197312122005011001', 'Dr. Abd. Rahim, S.P., M.Si.', 'Dosen', '', 0, 1, '2025-01-29 07:43:56.619121'),
(140, 'pbkdf2_sha256$600000$G1equjL6TYqARvqGlXA8SI$zJ9yqtmNrxeh/lrtQaq3cJq/5UdxNQxF1c84vV++N64=', '2025-01-29 07:44:14.979786', 0, '197401092005011001', 'Dr. Basri Bado, S.Pd., M.Si.', 'Dosen', '', 0, 1, '2025-01-29 07:43:56.619121'),
(141, 'pbkdf2_sha256$600000$LTuwNwFpmrTvW7vFXFVaU2$oWhCn/F1mpJEmmcqw/Vmb/lcoEUU2x9pqaua9Hg1B38=', '2025-01-29 07:44:14.979787', 0, '197804112008012014', 'Dr. Sri Astuti, S.E., M.Si.', 'Dosen', '', 0, 1, '2025-01-29 07:43:56.619121'),
(142, 'pbkdf2_sha256$600000$1qjpzULTgNgSZjE5f0dsiq$hKTmq4C7dNRYWYjJW1AuOEP5rqVop6zem78/y65Xmys=', '2025-01-29 07:44:14.979788', 0, '197307162008011007', 'Abdul Hakim, S.Ag., M.Ag.', 'Dosen', '', 0, 1, '2025-01-29 07:43:56.619121'),
(143, 'pbkdf2_sha256$600000$G1equjL6TYqARvqGlXA8SI$zJ9yqtmNrxeh/lrtQaq3cJq/5UdxNQxF1c84vV++N64=', '2025-01-29 07:44:14.979789', 0, '197901262014042001', 'Dr. Diah Retno Dwi Hastuti, S.P., M.Si.', 'Dosen', '', 0, 1, '2025-01-29 07:43:56.619121'),
(144, 'pbkdf2_sha256$600000$LTuwNwFpmrTvW7vFXFVaU2$oWhCn/F1mpJEmmcqw/Vmb/lcoEUU2x9pqaua9Hg1B38=', '2025-01-29 07:44:14.979790', 0, '198403022014041001', 'Andi Samsir, S.Pd., M.Si.', 'Dosen', '', 0, 1, '2025-01-29 07:43:56.619121'),
(145, 'pbkdf2_sha256$600000$1qjpzULTgNgSZjE5f0dsiq$hKTmq4C7dNRYWYjJW1AuOEP5rqVop6zem78/y65Xmys=', '2025-01-29 07:44:14.979791', 0, '198605302015041002', 'Muhammad Imam Ma?ruf, S.P., M.Sc.', 'Dosen', '', 0, 1, '2025-01-29 07:43:56.619121'),
(146, 'pbkdf2_sha256$600000$G1equjL6TYqARvqGlXA8SI$zJ9yqtmNrxeh/lrtQaq3cJq/5UdxNQxF1c84vV++N64=', '2025-01-29 07:44:14.979792', 0, '197201072000032005', 'Citra Ayni Kamaruddin, S.P., M.Si.', 'Dosen', '', 0, 1, '2025-01-29 07:43:56.619121'),
(147, 'pbkdf2_sha256$600000$LTuwNwFpmrTvW7vFXFVaU2$oWhCn/F1mpJEmmcqw/Vmb/lcoEUU2x9pqaua9Hg1B38=', '2025-01-29 07:44:14.979793', 0, '197608102007011001', 'Dr. Agus Syam, S.Pd., M.Si.', 'Dosen', '', 0, 1, '2025-01-29 07:43:56.619121'),
(148, 'pbkdf2_sha256$600000$1qjpzULTgNgSZjE5f0dsiq$hKTmq4C7dNRYWYjJW1AuOEP5rqVop6zem78/y65Xmys=', '2025-01-29 07:44:14.979794', 0, '197312312000031004', 'Dr. Muhammad Rakib, S.Pd., M.Si.', 'Dosen', '', 0, 1, '2025-01-29 07:43:56.619121'),
(149, 'pbkdf2_sha256$600000$G1equjL6TYqARvqGlXA8SI$zJ9yqtmNrxeh/lrtQaq3cJq/5UdxNQxF1c84vV++N64=', '2025-01-29 07:44:14.979795', 0, '196307211989032000', 'Dr. Ir. Hj. Marhawati, M.Si.', 'Dosen', '', 0, 1, '2025-01-29 07:43:56.619121'),
(150, 'pbkdf2_sha256$600000$LTuwNwFpmrTvW7vFXFVaU2$oWhCn/F1mpJEmmcqw/Vmb/lcoEUU2x9pqaua9Hg1B38=', '2025-01-29 07:44:14.979796', 0, 'lb001', 'Asmayanti, S.E., M.M.', 'Dosen', '', 0, 1, '2025-01-29 07:43:56.619121'),
(151, 'pbkdf2_sha256$600000$1qjpzULTgNgSZjE5f0dsiq$hKTmq4C7dNRYWYjJW1AuOEP5rqVop6zem78/y65Xmys=', '2025-01-29 07:44:14.979797', 0, 'lb002', 'Dr. Muhammad Djufri, M.Pd.', 'Dosen', '', 0, 1, '2025-01-29 07:43:56.619121'),
(152, 'pbkdf2_sha256$600000$geD3abqY2GGERt9pSkxlEa$L3pszDi6QzpGQxh1LJ8fDicLu5NtoH06EfbWiPBcyWE=', '2025-01-29 11:41:37.628894', 0, '198010252015041004', 'Syamsu Alam, S.Si., M.Si.', 'Dosen', '', 0, 1, '2025-01-29 07:43:56.619121'),
(153, 'pbkdf2_sha256$600000$LTuwNwFpmrTvW7vFXFVaU2$oWhCn/F1mpJEmmcqw/Vmb/lcoEUU2x9pqaua9Hg1B38=', '2025-01-29 07:44:14.979799', 0, '198509102019032010', 'Stefani Inggrid Gorap, S.E., M.M.', 'Dosen', '', 0, 1, '2025-01-29 07:43:56.619121'),
(154, 'pbkdf2_sha256$600000$1qjpzULTgNgSZjE5f0dsiq$hKTmq4C7dNRYWYjJW1AuOEP5rqVop6zem78/y65Xmys=', '2025-01-29 07:44:14.979800', 0, 'lb003', 'Dr. Valentino Aris, S.Kom., M.M.', 'Dosen', '', 0, 1, '2025-01-29 07:43:56.619121'),
(155, 'pbkdf2_sha256$600000$G1equjL6TYqARvqGlXA8SI$zJ9yqtmNrxeh/lrtQaq3cJq/5UdxNQxF1c84vV++N64=', '2025-01-29 07:44:14.979801', 0, 'lb004', 'Muh. Jamil, S.E., M.Si.', 'Dosen', '', 0, 1, '2025-01-29 07:43:56.619121'),
(156, 'pbkdf2_sha256$600000$LTuwNwFpmrTvW7vFXFVaU2$oWhCn/F1mpJEmmcqw/Vmb/lcoEUU2x9pqaua9Hg1B38=', '2025-01-29 07:44:14.979802', 0, 'lb005', 'Dr. Muhammad Ashdaq, S.T., M.Si.', 'Dosen', '', 0, 1, '2025-01-29 07:43:56.619121'),
(157, 'pbkdf2_sha256$600000$1qjpzULTgNgSZjE5f0dsiq$hKTmq4C7dNRYWYjJW1AuOEP5rqVop6zem78/y65Xmys=', '2025-01-29 07:44:14.979803', 0, 'lb006', 'Muhammad Taufik, S.E., M.Si.', 'Dosen', '', 0, 1, '2025-01-29 07:43:56.619121'),
(158, 'pbkdf2_sha256$600000$G1equjL6TYqARvqGlXA8SI$zJ9yqtmNrxeh/lrtQaq3cJq/5UdxNQxF1c84vV++N64=', '2025-01-29 07:44:14.979804', 0, 'lb007', 'Dr. Andi Ruslan, S.E., M.Si.', 'Dosen', '', 0, 1, '2025-01-29 07:43:56.619121'),
(159, 'pbkdf2_sha256$600000$LTuwNwFpmrTvW7vFXFVaU2$oWhCn/F1mpJEmmcqw/Vmb/lcoEUU2x9pqaua9Hg1B38=', '2025-01-29 07:44:14.979805', 0, 'lb008', 'Syahrul, S.Pd.,M.Pd', 'Dosen', '', 0, 1, '2025-01-29 07:43:56.619121'),
(160, 'pbkdf2_sha256$600000$1qjpzULTgNgSZjE5f0dsiq$hKTmq4C7dNRYWYjJW1AuOEP5rqVop6zem78/y65Xmys=', '2025-01-29 07:44:14.979806', 0, 'lb009', 'Farida Islamiah, S.Si., M.Si', 'Dosen', '', 0, 1, '2025-01-29 07:43:56.619121'),
(161, 'pbkdf2_sha256$600000$G1equjL6TYqARvqGlXA8SI$zJ9yqtmNrxeh/lrtQaq3cJq/5UdxNQxF1c84vV++N64=', '2025-01-29 07:44:14.979807', 0, 'lb010', 'Nur Isra\' Ahmad, M. Pd.I', 'Dosen', '', 0, 1, '2025-01-29 07:43:56.619121'),
(162, 'pbkdf2_sha256$600000$LTuwNwFpmrTvW7vFXFVaU2$oWhCn/F1mpJEmmcqw/Vmb/lcoEUU2x9pqaua9Hg1B38=', '2025-01-29 07:44:14.979808', 0, 'lb011', 'Muh. Qardawi Hamzah, S.Pd., M.Si.', 'Dosen', '', 0, 1, '2025-01-29 07:43:56.619121'),
(163, 'pbkdf2_sha256$600000$1qjpzULTgNgSZjE5f0dsiq$hKTmq4C7dNRYWYjJW1AuOEP5rqVop6zem78/y65Xmys=', '2025-01-29 07:44:14.979809', 0, 'lb012', 'Fadil Muhammad S.Kel., M.Sc', 'Dosen', '', 0, 1, '2025-01-29 07:43:56.619121'),
(164, 'pbkdf2_sha256$600000$G1equjL6TYqARvqGlXA8SI$zJ9yqtmNrxeh/lrtQaq3cJq/5UdxNQxF1c84vV++N64=', '2025-01-29 07:44:14.979810', 0, 'lb013', 'Sri Asmirani, S.Hut., M.Geo', 'Dosen', '', 0, 1, '2025-01-29 07:43:56.619121'),
(165, 'pbkdf2_sha256$600000$LTuwNwFpmrTvW7vFXFVaU2$oWhCn/F1mpJEmmcqw/Vmb/lcoEUU2x9pqaua9Hg1B38=', '2025-01-29 07:44:14.979811', 0, '196809091993032002', 'Dra. Hariany Idris, M.Si.', 'Dosen', '', 0, 1, '2025-01-29 07:43:56.619121'),
(166, 'pbkdf2_sha256$600000$1qjpzULTgNgSZjE5f0dsiq$hKTmq4C7dNRYWYjJW1AuOEP5rqVop6zem78/y65Xmys=', '2025-01-29 07:44:14.979812', 0, '196508011998022001', 'Hj. Masnawaty S, S.E., Ak., M.Si., Ph.D., CA., CPAL.', 'Dosen', '', 0, 1, '2025-01-29 07:43:56.619121'),
(167, 'pbkdf2_sha256$600000$G1equjL6TYqARvqGlXA8SI$zJ9yqtmNrxeh/lrtQaq3cJq/5UdxNQxF1c84vV++N64=', '2025-01-29 07:44:14.979813', 0, '197712042014042001', 'Samsinar, S.Pd., S.E., M.Si., Ak.', 'Dosen', '', 0, 1, '2025-01-29 07:43:56.619121'),
(168, 'pbkdf2_sha256$600000$LTuwNwFpmrTvW7vFXFVaU2$oWhCn/F1mpJEmmcqw/Vmb/lcoEUU2x9pqaua9Hg1B38=', '2025-01-29 07:44:14.979814', 0, '199112122019032027', 'Nurjannah, S.Pd., M.Pd.', 'Dosen', '', 0, 1, '2025-01-29 07:43:56.619121'),
(1001, 'pbkdf2_sha256$600000$5ngaZGWFGniypWM58iS6lE$h8kzL5tAFMxn8fZp0J9ExAhlh7LQn+txfWRc5HBr4N4=', '2025-01-29 12:35:47.298450', 0, 'mhs001', 'Mahasiswa 001', 'Mahasiswa', '', 0, 1, '2025-01-29 07:43:56.619121'),
(1002, 'pbkdf2_sha256$600000$G1equjL6TYqARvqGlXA8SI$zJ9yqtmNrxeh/lrtQaq3cJq/5UdxNQxF1c84vV++N64=', '2025-01-29 07:44:14.979816', 0, 'mhs002', 'Mahasiswa 002', 'Mahasiswa', '', 0, 1, '2025-01-29 07:43:56.619121'),
(1003, 'pbkdf2_sha256$600000$LTuwNwFpmrTvW7vFXFVaU2$oWhCn/F1mpJEmmcqw/Vmb/lcoEUU2x9pqaua9Hg1B38=', '2025-01-29 07:44:14.979817', 0, 'mhs003', 'Mahasiswa 003', 'Mahasiswa', '', 0, 1, '2025-01-29 07:43:56.619121'),
(1004, 'pbkdf2_sha256$600000$1qjpzULTgNgSZjE5f0dsiq$hKTmq4C7dNRYWYjJW1AuOEP5rqVop6zem78/y65Xmys=', '2025-01-29 07:44:14.979818', 0, 'mhs004', 'Mahasiswa 004', 'Mahasiswa', '', 0, 1, '2025-01-29 07:43:56.619121'),
(1005, 'pbkdf2_sha256$600000$G1equjL6TYqARvqGlXA8SI$zJ9yqtmNrxeh/lrtQaq3cJq/5UdxNQxF1c84vV++N64=', '2025-01-29 07:44:14.979819', 0, 'mhs005', 'Mahasiswa 005', 'Mahasiswa', '', 0, 1, '2025-01-29 07:43:56.619121'),
(1006, 'pbkdf2_sha256$600000$LTuwNwFpmrTvW7vFXFVaU2$oWhCn/F1mpJEmmcqw/Vmb/lcoEUU2x9pqaua9Hg1B38=', '2025-01-29 07:44:14.979820', 0, 'mhs006', 'Mahasiswa 006', 'Mahasiswa', '', 0, 1, '2025-01-29 07:43:56.619121'),
(1007, 'pbkdf2_sha256$600000$1qjpzULTgNgSZjE5f0dsiq$hKTmq4C7dNRYWYjJW1AuOEP5rqVop6zem78/y65Xmys=', '2025-01-29 07:44:14.979821', 0, 'mhs007', 'Mahasiswa 007', 'Mahasiswa', '', 0, 1, '2025-01-29 07:43:56.619121'),
(1008, 'pbkdf2_sha256$600000$G1equjL6TYqARvqGlXA8SI$zJ9yqtmNrxeh/lrtQaq3cJq/5UdxNQxF1c84vV++N64=', '2025-01-29 07:44:14.979822', 0, 'mhs008', 'Mahasiswa 008', 'Mahasiswa', '', 0, 1, '2025-01-29 07:43:56.619121'),
(1009, 'pbkdf2_sha256$600000$LTuwNwFpmrTvW7vFXFVaU2$oWhCn/F1mpJEmmcqw/Vmb/lcoEUU2x9pqaua9Hg1B38=', '2025-01-29 07:44:14.979823', 0, 'mhs009', 'Mahasiswa 009', 'Mahasiswa', '', 0, 1, '2025-01-29 07:43:56.619121'),
(1010, 'pbkdf2_sha256$600000$LTuwNwFpmrTvW7vFXFVaU2$oWhCn/F1mpJEmmcqw/Vmb/lcoEUU2x9pqaua9Hg1B38=', '2025-01-29 07:44:14.979824', 0, 'mhs010', 'Mahasiswa 010', 'Mahasiswa', '', 0, 1, '2025-01-29 07:43:56.619121');

-- --------------------------------------------------------

--
-- Table structure for table `auth_user_groups`
--

CREATE TABLE `auth_user_groups` (
  `id` bigint(20) NOT NULL,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `auth_user_user_permissions`
--

CREATE TABLE `auth_user_user_permissions` (
  `id` bigint(20) NOT NULL,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `django_admin_log`
--

CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext DEFAULT NULL,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) UNSIGNED NOT NULL CHECK (`action_flag` >= 0),
  `change_message` longtext NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `django_admin_log`
--

INSERT INTO `django_admin_log` (`id`, `action_time`, `object_id`, `object_repr`, `action_flag`, `change_message`, `content_type_id`, `user_id`) VALUES
(1, '2025-01-29 07:47:05.739911', '1', 'Ketua Jurusan Ilmu Ekonomi', 1, '[{\"added\": {}}]', 7, 1),
(2, '2025-01-29 08:06:54.582466', '2', 'ahmad - ', 1, '[{\"added\": {}}]', 4, 1),
(3, '2025-01-29 08:07:48.875809', '3', 'dsn1 - ', 1, '[{\"added\": {}}]', 4, 1),
(4, '2025-01-29 08:26:52.721702', '1', 'Ketua Jurusan Ilmu Ekonomi', 2, '[{\"changed\": {\"fields\": [\"Kajur\", \"Sekjur\"]}}]', 7, 1),
(5, '2025-01-29 08:27:58.320601', '2', 'Ilmu Akuntansi', 1, '[{\"added\": {}}]', 7, 1),
(6, '2025-01-29 08:28:06.038564', '1', 'Ilmu Ekonomi', 2, '[{\"changed\": {\"fields\": [\"Nama jurusan\"]}}]', 7, 1),
(7, '2025-01-29 08:28:41.572592', '3', 'Bisnis dan Kewirausahaan', 1, '[{\"added\": {}}]', 7, 1),
(8, '2025-01-29 08:34:47.880679', '3', 'Bisnis dan Kewirausahaan', 2, '[{\"changed\": {\"fields\": [\"Kalab\"]}}]', 7, 1),
(9, '2025-01-29 08:34:53.276017', '3', 'Bisnis dan Kewirausahaan', 2, '[]', 7, 1),
(10, '2025-01-29 08:35:04.245473', '2', 'Ilmu Akuntansi', 2, '[{\"changed\": {\"fields\": [\"Sekjur\", \"Kalab\"]}}]', 7, 1),
(11, '2025-01-29 08:35:08.430057', '1', 'Ilmu Ekonomi', 2, '[{\"changed\": {\"fields\": [\"Kalab\"]}}]', 7, 1),
(12, '2025-01-29 08:36:47.358965', '1', 'Pendidikan Ekonomi - S1', 1, '[{\"added\": {}}]', 9, 1),
(13, '2025-01-29 08:37:18.078524', '2', 'Pendidikan Akuntansi - S1', 1, '[{\"added\": {}}]', 9, 1),
(14, '2025-01-29 08:37:59.818458', '3', 'Manajamen - S1', 1, '[{\"added\": {}}]', 9, 1),
(15, '2025-01-29 08:38:28.328913', '4', 'Ekonomi Pembangunan - S1', 1, '[{\"added\": {}}]', 9, 1),
(16, '2025-01-29 08:41:02.693321', '5', 'Akuntansi - S1', 1, '[{\"added\": {}}]', 9, 1),
(17, '2025-01-29 08:41:43.719652', '6', 'Kewirausahaan - S1', 1, '[{\"added\": {}}]', 9, 1),
(18, '2025-01-29 08:42:09.266612', '7', 'Bisnis Digital - S1', 1, '[{\"added\": {}}]', 9, 1),
(19, '2025-01-29 08:42:33.216251', '8', 'Akuntansi - D4', 1, '[{\"added\": {}}]', 9, 1),
(20, '2025-01-29 08:57:45.321197', '1011', '198303192015041001a - ', 1, '[{\"added\": {}}, {\"added\": {\"name\": \"user dosen\", \"object\": \"198303192015041001a\"}}]', 4, 1),
(21, '2025-01-29 09:01:39.681241', '133', '198303192015041001a - Ilham Wardhana Haeuddin, S.E., MMktMgt', 2, '[{\"changed\": {\"fields\": [\"First name\"]}}, {\"added\": {\"name\": \"user dosen\", \"object\": \"198303192015041001a\"}}]', 4, 1),
(22, '2025-01-29 09:08:14.272028', '9', 'adminf1 - Admin Fakultas 001', 2, '[{\"added\": {\"name\": \"user fakultas\", \"object\": \"adminf1\"}}]', 4, 1),
(23, '2025-01-29 09:08:29.900931', '10', 'adminf2 - Admin Fakultas 002', 2, '[{\"added\": {\"name\": \"user fakultas\", \"object\": \"adminf2\"}}]', 4, 1),
(24, '2025-01-29 09:12:46.893637', '1', 'SK Pembimbing', 1, '[{\"added\": {}}]', 8, 1),
(25, '2025-01-29 09:12:57.072340', '2', 'Seminar Proposal', 1, '[{\"added\": {}}]', 8, 1),
(26, '2025-01-31 06:40:43.068032', '3', 'Bisnis dan Kewirausahaan', 2, '[{\"changed\": {\"fields\": [\"Kode surat\"]}}]', 7, 1),
(27, '2025-01-31 06:41:15.340313', '2', 'Ilmu Akuntansi', 2, '[{\"changed\": {\"fields\": [\"Kode surat\"]}}]', 7, 1),
(28, '2025-01-31 06:41:25.754873', '1', 'Ilmu Ekonomi', 2, '[{\"changed\": {\"fields\": [\"Kode surat\"]}}]', 7, 1);

-- --------------------------------------------------------

--
-- Table structure for table `django_content_type`
--

CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `django_content_type`
--

INSERT INTO `django_content_type` (`id`, `app_label`, `model`) VALUES
(7, 'acd', 'jurusan'),
(17, 'acd', 'jurusanpejabat'),
(16, 'acd', 'layanan'),
(8, 'acd', 'layananjenis'),
(15, 'acd', 'nosurat'),
(9, 'acd', 'prodi'),
(18, 'acd', 'prodipejabat'),
(14, 'acd', 'skripsijudul'),
(13, 'acd', 'userdosen'),
(12, 'acd', 'userfakultas'),
(11, 'acd', 'usermhs'),
(10, 'acd', 'userprodi'),
(1, 'admin', 'logentry'),
(3, 'auth', 'group'),
(2, 'auth', 'permission'),
(4, 'auth', 'user'),
(5, 'contenttypes', 'contenttype'),
(6, 'sessions', 'session');

-- --------------------------------------------------------

--
-- Table structure for table `django_migrations`
--

CREATE TABLE `django_migrations` (
  `id` bigint(20) NOT NULL,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `django_migrations`
--

INSERT INTO `django_migrations` (`id`, `app`, `name`, `applied`) VALUES
(1, 'contenttypes', '0001_initial', '2025-01-29 07:42:55.854289'),
(2, 'auth', '0001_initial', '2025-01-29 07:42:56.133091'),
(3, 'acd', '0001_initial', '2025-01-29 07:42:56.954166'),
(4, 'admin', '0001_initial', '2025-01-29 07:42:57.027326'),
(5, 'admin', '0002_logentry_remove_auto_add', '2025-01-29 07:42:57.039532'),
(6, 'admin', '0003_logentry_add_action_flag_choices', '2025-01-29 07:42:57.051959'),
(7, 'contenttypes', '0002_remove_content_type_name', '2025-01-29 07:42:57.098747'),
(8, 'auth', '0002_alter_permission_name_max_length', '2025-01-29 07:42:57.138674'),
(9, 'auth', '0003_alter_user_email_max_length', '2025-01-29 07:42:57.156028'),
(10, 'auth', '0004_alter_user_username_opts', '2025-01-29 07:42:57.168357'),
(11, 'auth', '0005_alter_user_last_login_null', '2025-01-29 07:42:57.200250'),
(12, 'auth', '0006_require_contenttypes_0002', '2025-01-29 07:42:57.202983'),
(13, 'auth', '0007_alter_validators_add_error_messages', '2025-01-29 07:42:57.215230'),
(14, 'auth', '0008_alter_user_username_max_length', '2025-01-29 07:42:57.232309'),
(15, 'auth', '0009_alter_user_last_name_max_length', '2025-01-29 07:42:57.255153'),
(16, 'auth', '0010_alter_group_name_max_length', '2025-01-29 07:42:57.277904'),
(17, 'auth', '0011_update_proxy_permissions', '2025-01-29 07:42:57.290697'),
(18, 'auth', '0012_alter_user_first_name_max_length', '2025-01-29 07:42:57.307257'),
(19, 'sessions', '0001_initial', '2025-01-29 07:42:57.330633'),
(20, 'acd', '0002_alter_jurusan_kalab_alter_jurusan_sekjur_and_more', '2025-01-29 08:31:02.804493'),
(21, 'acd', '0003_alter_jurusan_kalab_alter_jurusan_sekjur_and_more', '2025-01-29 08:33:45.671277'),
(22, 'acd', '0004_alter_jurusan_kalab_alter_jurusan_sekjur_and_more', '2025-01-29 08:34:40.000429'),
(23, 'acd', '0005_skripsijudul_prodi', '2025-01-29 12:35:22.680537'),
(24, 'acd', '0006_remove_nosurat_kode_nosurat_jurusan', '2025-01-29 12:40:53.547883'),
(25, 'acd', '0007_alter_nosurat_tahun', '2025-01-29 13:07:00.459040'),
(26, 'acd', '0002_alter_nosurat_nomor', '2025-01-31 06:51:59.999213'),
(27, 'acd', '0003_remove_jurusan_kajur_remove_jurusan_kalab_and_more', '2025-02-02 06:10:04.883213'),
(28, 'acd', '0004_remove_prodi_kaprodi_remove_prodi_sekprodi_and_more', '2025-02-02 06:29:19.978185');

-- --------------------------------------------------------

--
-- Table structure for table `django_session`
--

CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `django_session`
--

INSERT INTO `django_session` (`session_key`, `session_data`, `expire_date`) VALUES
('3t88pm9wdibixt3b3w0km2cp6yw22o3q', '.eJxVjEEOwiAQRe_C2hAYSgWX7nsGMgODVA0kpV0Z765NutDtf-_9lwi4rSVsnZcwJ3ERXpx-N8L44LqDdMd6azK2ui4zyV2RB-1yaomf18P9OyjYy7cGTwNRhhEsWA2KnSEmk6zKHM-jUUNEp523hNmjUykOQIAelGadIYr3B-KrN-0:1teW6C:RvOV76gsW--urv0mpKyxxznaKc5jK3JgYeeAykCmxHM', '2025-02-16 09:17:04.911378');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `acd_jurusan`
--
ALTER TABLE `acd_jurusan`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `acd_jurusanpejabat`
--
ALTER TABLE `acd_jurusanpejabat`
  ADD PRIMARY KEY (`id`),
  ADD KEY `acd_jurusanpejabat_jurusan_id_94da934c_fk_acd_jurusan_id` (`jurusan_id`),
  ADD KEY `acd_jurusanpejabat_pejabat_id_b6567989_fk_auth_user_id` (`pejabat_id`);

--
-- Indexes for table `acd_layanan`
--
ALTER TABLE `acd_layanan`
  ADD PRIMARY KEY (`id`),
  ADD KEY `acd_layanan_adminp_id_f854797a_fk_auth_user_id` (`adminp_id`),
  ADD KEY `acd_layanan_layanan_jenis_id_3bc6f332_fk_acd_layananjenis_id` (`layanan_jenis_id`),
  ADD KEY `acd_layanan_mhs_id_58c0caec_fk_auth_user_id` (`mhs_id`),
  ADD KEY `acd_layanan_prodi_id_277ab83d_fk_acd_prodi_id` (`prodi_id`);

--
-- Indexes for table `acd_layananjenis`
--
ALTER TABLE `acd_layananjenis`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `acd_nosurat`
--
ALTER TABLE `acd_nosurat`
  ADD PRIMARY KEY (`id`),
  ADD KEY `acd_nosurat_adminp_id_42f54c35_fk_auth_user_id` (`adminp_id`),
  ADD KEY `acd_nosurat_jurusan_id_81deb859_fk_acd_jurusan_id` (`jurusan_id`);

--
-- Indexes for table `acd_prodi`
--
ALTER TABLE `acd_prodi`
  ADD PRIMARY KEY (`id`),
  ADD KEY `acd_prodi_jurusan_id_2ab7a996_fk_acd_jurusan_id` (`jurusan_id`);

--
-- Indexes for table `acd_prodipejabat`
--
ALTER TABLE `acd_prodipejabat`
  ADD PRIMARY KEY (`id`),
  ADD KEY `acd_prodipejabat_pejabat_id_f9826ce7_fk_auth_user_id` (`pejabat_id`),
  ADD KEY `acd_prodipejabat_prodi_id_0d1797d8_fk_acd_prodi_id` (`prodi_id`);

--
-- Indexes for table `acd_skripsijudul`
--
ALTER TABLE `acd_skripsijudul`
  ADD PRIMARY KEY (`id`),
  ADD KEY `acd_skripsijudul_penasehat_akademik_id_e0506ab5_fk_auth_user_id` (`penasehat_akademik_id`),
  ADD KEY `acd_skripsijudul_user_id_af626db6_fk_auth_user_id` (`user_id`),
  ADD KEY `acd_skripsijudul_prodi_id_90ea14db_fk_acd_prodi_id` (`prodi_id`);

--
-- Indexes for table `acd_userdosen`
--
ALTER TABLE `acd_userdosen`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `user_id` (`user_id`),
  ADD KEY `acd_userdosen_prodi_id_acc8346e_fk_acd_prodi_id` (`prodi_id`);

--
-- Indexes for table `acd_userfakultas`
--
ALTER TABLE `acd_userfakultas`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `user_id` (`user_id`);

--
-- Indexes for table `acd_usermhs`
--
ALTER TABLE `acd_usermhs`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `user_id` (`user_id`),
  ADD KEY `acd_usermhs_prodi_id_b01769fc_fk_acd_prodi_id` (`prodi_id`);

--
-- Indexes for table `acd_userprodi`
--
ALTER TABLE `acd_userprodi`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `user_id` (`user_id`),
  ADD KEY `acd_userprodi_prodi_id_324faf10_fk_acd_prodi_id` (`prodi_id`);

--
-- Indexes for table `auth_group`
--
ALTER TABLE `auth_group`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `name` (`name`);

--
-- Indexes for table `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  ADD KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`);

--
-- Indexes for table `auth_permission`
--
ALTER TABLE `auth_permission`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`);

--
-- Indexes for table `auth_user`
--
ALTER TABLE `auth_user`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`);

--
-- Indexes for table `auth_user_groups`
--
ALTER TABLE `auth_user_groups`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_user_groups_user_id_group_id_94350c0c_uniq` (`user_id`,`group_id`),
  ADD KEY `auth_user_groups_group_id_97559544_fk_auth_group_id` (`group_id`);

--
-- Indexes for table `auth_user_user_permissions`
--
ALTER TABLE `auth_user_user_permissions`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` (`user_id`,`permission_id`),
  ADD KEY `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` (`permission_id`);

--
-- Indexes for table `django_admin_log`
--
ALTER TABLE `django_admin_log`
  ADD PRIMARY KEY (`id`),
  ADD KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  ADD KEY `django_admin_log_user_id_c564eba6_fk_auth_user_id` (`user_id`);

--
-- Indexes for table `django_content_type`
--
ALTER TABLE `django_content_type`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`);

--
-- Indexes for table `django_migrations`
--
ALTER TABLE `django_migrations`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `django_session`
--
ALTER TABLE `django_session`
  ADD PRIMARY KEY (`session_key`),
  ADD KEY `django_session_expire_date_a5c62663` (`expire_date`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `acd_jurusan`
--
ALTER TABLE `acd_jurusan`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `acd_jurusanpejabat`
--
ALTER TABLE `acd_jurusanpejabat`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `acd_layanan`
--
ALTER TABLE `acd_layanan`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `acd_layananjenis`
--
ALTER TABLE `acd_layananjenis`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `acd_nosurat`
--
ALTER TABLE `acd_nosurat`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=14;

--
-- AUTO_INCREMENT for table `acd_prodi`
--
ALTER TABLE `acd_prodi`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT for table `acd_prodipejabat`
--
ALTER TABLE `acd_prodipejabat`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `acd_skripsijudul`
--
ALTER TABLE `acd_skripsijudul`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `acd_userdosen`
--
ALTER TABLE `acd_userdosen`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=71;

--
-- AUTO_INCREMENT for table `acd_userfakultas`
--
ALTER TABLE `acd_userfakultas`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `acd_usermhs`
--
ALTER TABLE `acd_usermhs`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT for table `acd_userprodi`
--
ALTER TABLE `acd_userprodi`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT for table `auth_group`
--
ALTER TABLE `auth_group`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `auth_permission`
--
ALTER TABLE `auth_permission`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=73;

--
-- AUTO_INCREMENT for table `auth_user`
--
ALTER TABLE `auth_user`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=1012;

--
-- AUTO_INCREMENT for table `auth_user_groups`
--
ALTER TABLE `auth_user_groups`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `auth_user_user_permissions`
--
ALTER TABLE `auth_user_user_permissions`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `django_admin_log`
--
ALTER TABLE `django_admin_log`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=29;

--
-- AUTO_INCREMENT for table `django_content_type`
--
ALTER TABLE `django_content_type`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=19;

--
-- AUTO_INCREMENT for table `django_migrations`
--
ALTER TABLE `django_migrations`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=29;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `acd_jurusanpejabat`
--
ALTER TABLE `acd_jurusanpejabat`
  ADD CONSTRAINT `acd_jurusanpejabat_jurusan_id_94da934c_fk_acd_jurusan_id` FOREIGN KEY (`jurusan_id`) REFERENCES `acd_jurusan` (`id`),
  ADD CONSTRAINT `acd_jurusanpejabat_pejabat_id_b6567989_fk_auth_user_id` FOREIGN KEY (`pejabat_id`) REFERENCES `auth_user` (`id`);

--
-- Constraints for table `acd_layanan`
--
ALTER TABLE `acd_layanan`
  ADD CONSTRAINT `acd_layanan_adminp_id_f854797a_fk_auth_user_id` FOREIGN KEY (`adminp_id`) REFERENCES `auth_user` (`id`),
  ADD CONSTRAINT `acd_layanan_layanan_jenis_id_3bc6f332_fk_acd_layananjenis_id` FOREIGN KEY (`layanan_jenis_id`) REFERENCES `acd_layananjenis` (`id`),
  ADD CONSTRAINT `acd_layanan_mhs_id_58c0caec_fk_auth_user_id` FOREIGN KEY (`mhs_id`) REFERENCES `auth_user` (`id`),
  ADD CONSTRAINT `acd_layanan_prodi_id_277ab83d_fk_acd_prodi_id` FOREIGN KEY (`prodi_id`) REFERENCES `acd_prodi` (`id`);

--
-- Constraints for table `acd_nosurat`
--
ALTER TABLE `acd_nosurat`
  ADD CONSTRAINT `acd_nosurat_adminp_id_42f54c35_fk_auth_user_id` FOREIGN KEY (`adminp_id`) REFERENCES `auth_user` (`id`),
  ADD CONSTRAINT `acd_nosurat_jurusan_id_81deb859_fk_acd_jurusan_id` FOREIGN KEY (`jurusan_id`) REFERENCES `acd_jurusan` (`id`);

--
-- Constraints for table `acd_prodi`
--
ALTER TABLE `acd_prodi`
  ADD CONSTRAINT `acd_prodi_jurusan_id_2ab7a996_fk_acd_jurusan_id` FOREIGN KEY (`jurusan_id`) REFERENCES `acd_jurusan` (`id`);

--
-- Constraints for table `acd_prodipejabat`
--
ALTER TABLE `acd_prodipejabat`
  ADD CONSTRAINT `acd_prodipejabat_pejabat_id_f9826ce7_fk_auth_user_id` FOREIGN KEY (`pejabat_id`) REFERENCES `auth_user` (`id`),
  ADD CONSTRAINT `acd_prodipejabat_prodi_id_0d1797d8_fk_acd_prodi_id` FOREIGN KEY (`prodi_id`) REFERENCES `acd_prodi` (`id`);

--
-- Constraints for table `acd_skripsijudul`
--
ALTER TABLE `acd_skripsijudul`
  ADD CONSTRAINT `acd_skripsijudul_penasehat_akademik_id_e0506ab5_fk_auth_user_id` FOREIGN KEY (`penasehat_akademik_id`) REFERENCES `auth_user` (`id`),
  ADD CONSTRAINT `acd_skripsijudul_prodi_id_90ea14db_fk_acd_prodi_id` FOREIGN KEY (`prodi_id`) REFERENCES `acd_prodi` (`id`),
  ADD CONSTRAINT `acd_skripsijudul_user_id_af626db6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Constraints for table `acd_userdosen`
--
ALTER TABLE `acd_userdosen`
  ADD CONSTRAINT `acd_userdosen_prodi_id_acc8346e_fk_acd_prodi_id` FOREIGN KEY (`prodi_id`) REFERENCES `acd_prodi` (`id`),
  ADD CONSTRAINT `acd_userdosen_user_id_cd48baea_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Constraints for table `acd_userfakultas`
--
ALTER TABLE `acd_userfakultas`
  ADD CONSTRAINT `acd_userfakultas_user_id_3b637f8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Constraints for table `acd_usermhs`
--
ALTER TABLE `acd_usermhs`
  ADD CONSTRAINT `acd_usermhs_prodi_id_b01769fc_fk_acd_prodi_id` FOREIGN KEY (`prodi_id`) REFERENCES `acd_prodi` (`id`),
  ADD CONSTRAINT `acd_usermhs_user_id_43ef8219_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Constraints for table `acd_userprodi`
--
ALTER TABLE `acd_userprodi`
  ADD CONSTRAINT `acd_userprodi_prodi_id_324faf10_fk_acd_prodi_id` FOREIGN KEY (`prodi_id`) REFERENCES `acd_prodi` (`id`),
  ADD CONSTRAINT `acd_userprodi_user_id_1acbf879_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Constraints for table `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  ADD CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  ADD CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`);

--
-- Constraints for table `auth_permission`
--
ALTER TABLE `auth_permission`
  ADD CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`);

--
-- Constraints for table `auth_user_groups`
--
ALTER TABLE `auth_user_groups`
  ADD CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  ADD CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Constraints for table `auth_user_user_permissions`
--
ALTER TABLE `auth_user_user_permissions`
  ADD CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  ADD CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Constraints for table `django_admin_log`
--
ALTER TABLE `django_admin_log`
  ADD CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  ADD CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
