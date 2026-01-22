-- =============================================================================
-- Schema de la base de donnees Suivi Colis IUT
-- =============================================================================
-- 
-- Architecture :
-- - departement : Les 6 departements de l'IUT avec leur lieu de livraison
-- - fournisseur : Entreprises aupres desquelles l'IUT commande
-- - utilisateur : Personnes autorisees (authentification email/mot de passe)
-- - commande : Bons de commande (BC) passes aux fournisseurs
-- - ligne_commande : Articles d'une commande
-- - bon_livraison : BL recus des fournisseurs (une commande peut avoir plusieurs BL)
-- - colis : Colis physiques (un BL peut contenir plusieurs colis)
-- - historique_colis : Trace de toutes les actions sur un colis
-- - notification : Alertes envoyees aux utilisateurs
--
-- Relations :
-- Commande (1) --> BonLivraison (N) --> Colis (N) --> HistoriqueColis (N)
--
-- =============================================================================

-- Encodage UTF-8 pour les accents
SET NAMES utf8mb4;
SET CHARACTER SET utf8mb4;

-- Suppression des tables dans l'ordre inverse des dependances
DROP TABLE IF EXISTS notification;
DROP TABLE IF EXISTS historique_colis;
DROP TABLE IF EXISTS colis;
DROP TABLE IF EXISTS bon_livraison;
DROP TABLE IF EXISTS ligne_commande;
DROP TABLE IF EXISTS commande;
DROP TABLE IF EXISTS utilisateur;
DROP TABLE IF EXISTS fournisseur;
DROP TABLE IF EXISTS departement;

-- =============================================================================
-- DEPARTEMENTS
-- Les 6 departements de l'IUT de Villetaneuse
-- =============================================================================
CREATE TABLE departement (
    id_departement INT PRIMARY KEY AUTO_INCREMENT,
    nom_departement VARCHAR(100) NOT NULL,
    lieu_livraison VARCHAR(255)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- =============================================================================
-- FOURNISSEURS
-- Entreprises partenaires (LDLC, Amazon Business, etc.)
-- =============================================================================
CREATE TABLE fournisseur (
    id_fournisseur INT PRIMARY KEY AUTO_INCREMENT,
    nom_societe VARCHAR(150) NOT NULL,
    contact_nom VARCHAR(100),
    telephone VARCHAR(20),
    email VARCHAR(150),
    notes_internes TEXT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- =============================================================================
-- UTILISATEURS
-- Authentification par email + mot de passe
-- =============================================================================
CREATE TABLE utilisateur (
    id_utilisateur INT PRIMARY KEY AUTO_INCREMENT,
    email VARCHAR(150) UNIQUE NOT NULL,
    mot_de_passe VARCHAR(255) NOT NULL,              -- Hash du mot de passe
    nom VARCHAR(100) NOT NULL,
    prenom VARCHAR(100) NOT NULL,
    role ENUM('demandeur', 'editeur', 'responsable_colis', 'admin') DEFAULT 'demandeur',
    id_departement INT,
    est_actif BOOLEAN DEFAULT TRUE,
    date_creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_departement) REFERENCES departement(id_departement) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- =============================================================================
-- COMMANDES (Bons de Commande)
-- Statuts : en_attente, validee, non_validee, en_cours, recue, annulee
-- =============================================================================
CREATE TABLE commande (
    id_commande INT PRIMARY KEY AUTO_INCREMENT,
    numero_bc VARCHAR(50) UNIQUE NOT NULL,
    id_fournisseur INT NOT NULL,
    id_departement INT NOT NULL,
    id_demandeur INT,
    date_creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    date_livraison_prevue DATE,
    statut_global ENUM('en_attente', 'validee', 'non_validee', 'en_cours', 'recue', 'annulee') DEFAULT 'en_attente',
    notes TEXT,
    fichier_bc VARCHAR(255),
    FOREIGN KEY (id_fournisseur) REFERENCES fournisseur(id_fournisseur) ON DELETE CASCADE,
    FOREIGN KEY (id_departement) REFERENCES departement(id_departement) ON DELETE CASCADE,
    FOREIGN KEY (id_demandeur) REFERENCES utilisateur(id_utilisateur) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- =============================================================================
-- LIGNES DE COMMANDE
-- =============================================================================
CREATE TABLE ligne_commande (
    id_ligne INT PRIMARY KEY AUTO_INCREMENT,
    id_commande INT NOT NULL,
    ref_produit VARCHAR(100),
    designation VARCHAR(255) NOT NULL,
    quantite INT DEFAULT 1,
    FOREIGN KEY (id_commande) REFERENCES commande(id_commande) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- =============================================================================
-- BONS DE LIVRAISON
-- =============================================================================
CREATE TABLE bon_livraison (
    id_bl INT PRIMARY KEY AUTO_INCREMENT,
    id_commande INT NOT NULL,
    num_bl_fournisseur VARCHAR(100),
    date_bl DATE,
    fichier_bl VARCHAR(255),
    date_reception TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_commande) REFERENCES commande(id_commande) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- =============================================================================
-- COLIS
-- =============================================================================
CREATE TABLE colis (
    id_colis INT PRIMARY KEY AUTO_INCREMENT,
    id_bl INT,
    num_suivi_transporteur VARCHAR(100),
    nom_transporteur VARCHAR(100),
    statut_actuel ENUM('attendu', 'recu', 'en_distribution', 'livre', 'probleme') DEFAULT 'attendu',
    lieu_stockage VARCHAR(100),
    date_reception DATETIME,
    date_livraison DATETIME,
    notes TEXT,
    FOREIGN KEY (id_bl) REFERENCES bon_livraison(id_bl) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- =============================================================================
-- HISTORIQUE DES COLIS
-- =============================================================================
CREATE TABLE historique_colis (
    id_hist INT PRIMARY KEY AUTO_INCREMENT,
    id_colis INT NOT NULL,
    id_utilisateur INT,
    date_heure TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    action VARCHAR(255) NOT NULL,
    ancien_statut VARCHAR(50),
    nouveau_statut VARCHAR(50),
    FOREIGN KEY (id_colis) REFERENCES colis(id_colis) ON DELETE CASCADE,
    FOREIGN KEY (id_utilisateur) REFERENCES utilisateur(id_utilisateur) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- =============================================================================
-- NOTIFICATIONS
-- =============================================================================
CREATE TABLE notification (
    id_notification INT PRIMARY KEY AUTO_INCREMENT,
    id_utilisateur INT NOT NULL,
    titre VARCHAR(150) NOT NULL,
    message TEXT NOT NULL,
    lien VARCHAR(255),
    est_lue BOOLEAN DEFAULT FALSE,
    date_creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_utilisateur) REFERENCES utilisateur(id_utilisateur) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- =============================================================================
-- INDEX pour optimiser les recherches frequentes
-- =============================================================================
CREATE INDEX idx_commande_statut ON commande(statut_global);
CREATE INDEX idx_commande_fournisseur ON commande(id_fournisseur);
CREATE INDEX idx_commande_departement ON commande(id_departement);
CREATE INDEX idx_colis_statut ON colis(statut_actuel);
CREATE INDEX idx_colis_suivi ON colis(num_suivi_transporteur);
CREATE INDEX idx_utilisateur_email ON utilisateur(email);
CREATE INDEX idx_historique_colis ON historique_colis(id_colis);
CREATE INDEX idx_notification_utilisateur ON notification(id_utilisateur, est_lue);
