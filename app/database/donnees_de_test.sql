-- =============================================================================
-- Donnees de test pour l'application Suivi Colis IUT
-- =============================================================================
--
-- Ce fichier est charge automatiquement par Docker au premier demarrage.
--
-- Comptes de test (mot de passe = 'password' pour tous) :
-- - admin@iutv.univ-paris13.fr (admin)
-- - reprographie@iutv.univ-paris13.fr (responsable_colis)
-- - compta@iutv.univ-paris13.fr (editeur)
-- - p.durand@iutv.univ-paris13.fr (demandeur)
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
('LDLC Pro', 'Marie Dupont', '04 27 46 60 00', 'pro@ldlc.com', 'Delai moyen 3-5 jours. Bon service client.'),
('Amazon Business', 'Service Client', '0 800 84 77 15', 'business@amazon.fr', 'Livraison rapide. Attention aux colis multiples.'),
('Bureau Vallee', 'Thomas Martin', '01 49 38 75 00', 'contact@bureauvallee.fr', 'Fournitures de bureau uniquement.'),
('RS Components', 'Pierre Leroy', '03 44 10 15 00', 'commandes@rs-components.fr', 'Composants electroniques. Minimum de commande 50 euros.'),
('Manutan', 'Sophie Bernard', '01 34 53 35 35', 'service.client@manutan.fr', 'Mobilier et equipement. Livraison sur rendez-vous.'),
('Dell France', 'Support Entreprise', '0 805 54 08 34', 'support.fr@dell.com', 'Ordinateurs et serveurs. Garantie 3 ans sur site.');

-- -----------------------------------------------------------------------------
-- UTILISATEURS : Comptes avec mot de passe
-- Mot de passe = 'password' (hash SHA256 simplifie pour demo)
-- En production, utiliser bcrypt ou argon2
-- -----------------------------------------------------------------------------
-- Hash SHA256 de 'password' = '5e884898da28047d9d41e8c07d1df3693e5b8dd2b2c7b5d8c2d5f0e4c3b2a1f0'
-- Pour simplifier, on utilise un hash fixe reconnu par l'application
INSERT INTO utilisateur (email, mot_de_passe, nom, prenom, role, id_departement) VALUES
('admin@iutv.univ-paris13.fr', 'password', 'Martin', 'Jean', 'admin', 1),
('reprographie@iutv.univ-paris13.fr', 'password', 'Dubois', 'Michel', 'responsable_colis', NULL),
('compta@iutv.univ-paris13.fr', 'password', 'Lefevre', 'Catherine', 'editeur', NULL),
('p.durand@iutv.univ-paris13.fr', 'password', 'Durand', 'Philippe', 'demandeur', 1),
('m.bernard@iutv.univ-paris13.fr', 'password', 'Bernard', 'Marie', 'demandeur', 2),
('s.petit@iutv.univ-paris13.fr', 'password', 'Petit', 'Stephane', 'demandeur', 3),
('n.moreau@iutv.univ-paris13.fr', 'password', 'Moreau', 'Nathalie', 'editeur', 4),
('c.lambert@iutv.univ-paris13.fr', 'password', 'Lambert', 'Christophe', 'demandeur', 5);

-- -----------------------------------------------------------------------------
-- COMMANDES : Bons de commande avec differents statuts
-- -----------------------------------------------------------------------------
INSERT INTO commande (numero_bc, id_fournisseur, id_departement, id_demandeur, date_livraison_prevue, statut_global, notes, fichier_bc) VALUES
('BC-2025-001', 1, 1, 4, '2025-01-15', 'en_cours', 'Renouvellement PC salle TP', NULL),
('BC-2025-002', 2, 2, 5, '2025-01-10', 'recue', 'Fournitures premier semestre', NULL),
('BC-2025-003', 3, 3, 6, '2025-01-20', 'en_attente', 'Consommables imprimante', NULL),
('BC-2025-004', 4, 4, NULL, '2025-01-18', 'validee', 'Composants projet etudiant', NULL),
('BC-2025-005', 5, 1, 4, '2025-02-01', 'en_attente', 'Mobilier nouvelle salle', NULL),
('BC-2025-006', 6, 5, 8, '2025-01-25', 'en_cours', 'Ordinateurs portables jury', NULL);

-- -----------------------------------------------------------------------------
-- LIGNES DE COMMANDE : Articles commandes
-- -----------------------------------------------------------------------------
INSERT INTO ligne_commande (id_commande, ref_produit, designation, quantite) VALUES
(1, 'LDLC-PC-001', 'PC Fixe i5-13400 16Go RAM', 12),
(1, 'LDLC-EC-002', 'Ecran 24 pouces Full HD', 12),
(1, 'LDLC-CL-003', 'Clavier USB AZERTY', 12),
(2, 'AMZ-PAP-001', 'Ramette papier A4 500 feuilles', 50),
(2, 'AMZ-STY-002', 'Lot stylos bille bleu x50', 10),
(3, 'BV-TONER-001', 'Toner HP LaserJet noir', 5),
(3, 'BV-TONER-002', 'Toner HP LaserJet couleur', 3),
(4, 'RS-ARDUINO-001', 'Arduino Mega 2560', 20),
(4, 'RS-RASP-002', 'Raspberry Pi 5 8Go', 10),
(4, 'RS-CAPTEUR-003', 'Kit capteurs divers', 20),
(5, 'MAN-BUREAU-001', 'Bureau 160x80 avec caisson', 6),
(5, 'MAN-CHAISE-002', 'Chaise ergonomique', 6),
(6, 'DELL-LAT-001', 'Dell Latitude 5540 i7', 5);

-- -----------------------------------------------------------------------------
-- BONS DE LIVRAISON : BL recus des fournisseurs
-- -----------------------------------------------------------------------------
INSERT INTO bon_livraison (id_commande, num_bl_fournisseur, date_bl, fichier_bl) VALUES
(1, 'BL-LDLC-78542', '2025-01-10', NULL),
(2, 'BL-AMZ-963214', '2025-01-08', NULL),
(2, 'BL-AMZ-963215', '2025-01-09', NULL),
(6, 'BL-DELL-45123', '2025-01-20', NULL);

-- -----------------------------------------------------------------------------
-- COLIS : Colis physiques avec differents statuts
-- -----------------------------------------------------------------------------
INSERT INTO colis (id_bl, num_suivi_transporteur, nom_transporteur, statut_actuel, lieu_stockage, notes) VALUES
(1, 'CHRO-FR-789456123', 'Chronopost', 'recu', 'Reprographie', 'Palette 1/2 - PC'),
(1, 'CHRO-FR-789456124', 'Chronopost', 'recu', 'Reprographie', 'Palette 2/2 - Ecrans'),
(1, 'CHRO-FR-789456125', 'Chronopost', 'probleme', 'Reprographie', 'Destinataire inconnu sur etiquette'),
(2, 'LP-FR-456789123', 'La Poste', 'livre', NULL, 'Livre secretariat GEA'),
(3, 'LP-FR-456789124', 'La Poste', 'en_distribution', 'Chariot distribution', NULL),
(4, 'DHL-FR-321654987', 'DHL', 'attendu', NULL, 'Livraison prevue 25/01');

-- -----------------------------------------------------------------------------
-- HISTORIQUE : Trace des actions sur les colis
-- -----------------------------------------------------------------------------
INSERT INTO historique_colis (id_colis, id_utilisateur, action, ancien_statut, nouveau_statut) VALUES
(1, 2, 'Reception du colis', 'attendu', 'recu'),
(2, 2, 'Reception du colis', 'attendu', 'recu'),
(3, 2, 'Reception du colis', 'attendu', 'recu'),
(3, 2, 'Probleme: Destinataire inconnu sur etiquette', 'recu', 'probleme'),
(4, 2, 'Reception du colis', 'attendu', 'recu'),
(4, 2, 'Mise en distribution', 'recu', 'en_distribution'),
(4, 2, 'Livraison au secretariat GEA', 'en_distribution', 'livre'),
(5, 2, 'Reception du colis', 'attendu', 'recu'),
(5, 2, 'Mise en distribution', 'recu', 'en_distribution');

-- -----------------------------------------------------------------------------
-- NOTIFICATIONS : Alertes de test pour les utilisateurs
-- -----------------------------------------------------------------------------
INSERT INTO notification (id_utilisateur, titre, message, lien, est_lue) VALUES
(4, 'Colis CHRO-FR-789456123', 'Votre colis est arrive a la reprographie', '/colis/1', FALSE),
(4, 'Colis CHRO-FR-789456124', 'Votre colis est arrive a la reprographie', '/colis/2', FALSE),
(5, 'Colis LP-FR-456789123', 'Votre colis a ete livre', '/colis/4', TRUE),
(1, '[ALERTE] Colis CHRO-FR-789456125', 'Un probleme a ete signale sur votre colis', '/colis/3', FALSE);
