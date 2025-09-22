Web Visual Company Switcher
===========================

Ce module fournit une interface visuelle pour naviguer et sélectionner les compagnies dans Odoo v14.

Fonctionnalités
---------------

* Interface d'organigramme hiérarchique pour visualiser les compagnies
* Sélection de compagnie unique avec changement immédiat de contexte
* Mode de sélection multiple avec cases à cocher
* Intégration dans la barre de navigation systray
* Respect de la hiérarchie parent/enfant des compagnies

Utilisation
-----------

1. Une nouvelle icône d'organigramme apparaît dans la barre de navigation
2. Cliquez sur l'icône pour ouvrir l'interface de sélection
3. **Mode simple** : Cliquez directement sur une compagnie pour basculer immédiatement
4. **Mode multiple** : Activez "Mode sélection multiple", cochez les compagnies désirées, puis cliquez "Appliquer"

Installation
------------

1. Copiez le module dans votre dossier addons
2. Redémarrez Odoo
3. Activez le mode développeur
4. Allez dans Applications et installez "Web Visual Company Switcher"

Prérequis
---------

* Odoo 14.0
* Librairie OrgChart.js (incluse dans le module)

Configuration
-------------

Aucune configuration particulière n'est requise. Le module utilise automatiquement la structure hiérarchique définie dans les compagnies (champ `parent_id`).