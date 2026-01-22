-- =============================================================================
-- Donnees de PRODUCTION pour l'application Suivi Colis IUT
-- =============================================================================
--
-- Ce fichier contient UNIQUEMENT :
-- - Les departements de l'IUT (referentiel)
-- - Les fournisseurs habituels (referentiel)
-- - UN compte admin pour demarrer
--
-- Pour utiliser ce fichier au lieu des donnees de test :
-- 1. Modifier docker-compose.yml ligne ~47 :
--    REMPLACER : ./app/database/donnees_de_test.sql:/docker-entrypoint-initdb.d/02-data.sql
--    PAR :       ./app/database/donnees_production.sql:/docker-entrypoint-initdb.d/02-data.sql
-- 2. Supprimer le volume MySQL : docker-compose down -v
-- 3. Relancer : docker-compose up --build
--
-- Compte admin par defaut :
-- - Email : admin@iutv.univ-paris13.fr
-- - Mot de passe : admin2025!
--
-- =============================================================================

SET NAMES utf8mb4;
SET CHARACTER SET utf8mb4;

-- -----------------------------------------------------------------------------
-- DEPARTEMENTS : Les 6 departements de l'IUT de Villetaneuse
-- -----------------------------------------------------------------------------
INSERT INTO departement (nom_departement, lieu_livraison) VALUES
('Informatique', 'Batiment A - 2eme etage - Secretariat'),
('GEA', 'Batiment B - RDC - Accueil'),
('GEII', 'Batiment C - 1er etage - Bureau 105'),
('R&T', 'Batiment A - 3eme etage - Salle reseau'),
('CJ', 'Batiment B - 2eme etage - Secretariat'),
('SD', 'Batiment C - RDC - Bureau 001');

-- -----------------------------------------------------------------------------
-- FOURNISSEURS : Entreprises partenaires typiques
-- -----------------------------------------------------------------------------
INSERT INTO fournisseur (nom_societe, contact_nom, telephone, email, notes_internes) VALUES
('LDLC Pro', 'Service Pro', '04 27 46 60 00', 'pro@ldlc.com', 'Materiel informatique. Delai 3-5 jours.'),
('Amazon Business', 'Service Client', '0 800 84 77 15', 'business@amazon.fr', 'Livraison rapide. Attention colis multiples.'),
('Bureau Vallee', NULL, '01 49 38 75 00', 'contact@bureauvallee.fr', 'Fournitures de bureau.'),
('RS Components', NULL, '03 44 10 15 00', 'commandes@rs-components.fr', 'Composants electroniques.'),
('Manutan', NULL, '01 34 53 35 35', 'service.client@manutan.fr', 'Mobilier et equipement.'),
('Dell France', 'Support Entreprise', '0 805 54 08 34', 'support.fr@dell.com', 'Ordinateurs et serveurs.');

-- -----------------------------------------------------------------------------
-- COMPTE ADMINISTRATEUR UNIQUE
-- -----------------------------------------------------------------------------
-- IMPORTANT : Changer le mot de passe apres la premiere connexion !
-- Mot de passe actuel : admin2025!
INSERT INTO utilisateur (email, mot_de_passe, nom, prenom, role, id_departement, est_actif) VALUES
('admin@iutv.univ-paris13.fr', 'admin2025!', 'Administrateur', 'Systeme', 'admin', NULL, TRUE);

-- =============================================================================
-- FIN - Aucune commande, colis ou donnee de test
-- L'admin peut maintenant creer les utilisateurs via /admin/utilisateurs
-- =============================================================================
