/* © Numigi (tm) and all its contributors (https://numigi.com/r/home) */
/* License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl). */

odoo.define('web_visual_company_switcher.CompanySwitcherWidget', function (require) {
"use strict";

var AbstractAction = require('web.AbstractAction');
var core = require('web.core');
var Dialog = require('web.Dialog');
var rpc = require('web.rpc');
var session = require('web.session');
var SystrayMenu = require('web.SystrayMenu');
var Widget = require('web.Widget');

var QWeb = core.qweb;
var _t = core._t;

var VisualCompanySwitcher = Widget.extend({
    template: 'VisualCompanySwitcher',
    
    events: {
        'click .visual-company-switcher-icon': '_openModal',
    },

    init: function () {
        this._super.apply(this, arguments);
        this.companies_data = null;
        this.current_allowed_companies = [];
        this.current_company_id = null;
        this._cacheTime = 0;
        this.selectedAllowedIds = []; // Liste des IDs des compagnies cochées
        this.multi_select_mode = false;
        this.designatedActiveId = null; // ID de la compagnie désignée comme active
    },

    _openModal: function () {
        var self = this;
        
        // Load companies data and show modal directly
        this._loadCompaniesData().then(function () {
            self._showModal();
        }).catch(function () {
            // Error handling is already in _loadCompaniesData
        });
    },

    _loadCompaniesData: function () {
        var self = this;
        
        // *** VRAIE LOGIQUE ODOO : Lire depuis session.user_context ***
        
        // 1. Récupérer le contexte actuel de l'utilisateur depuis la session
        var user_context = session.user_context;
        
        // 2. Identifier la compagnie active (première dans allowed_company_ids)
        var active_company_id = user_context.allowed_company_ids ? user_context.allowed_company_ids[0] : null;
        
        // 3. Identifier TOUTES les compagnies sélectionnées
        var allowed_company_ids = user_context.allowed_company_ids || [];
        
        console.log("=== VRAIE LOGIQUE ODOO ===");
        console.log("Compagnie active:", active_company_id);
        console.log("Compagnies autorisées:", allowed_company_ids);
        
        // Appeler le serveur pour avoir les détails (noms, logos, hiérarchie)
        return rpc.query({
            route: '/web/visual_company_switcher/companies',
        }).then(function (result) {
            if (result.error) {
                self.displayNotification({
                    type: 'danger',
                    title: _t('Erreur'),
                    message: result.error,
                });
                return Promise.reject(result.error);
            }
            
            // Construire les données avec la VRAIE logique
            self.companies_data = result.companies || [];
            self.current_allowed_companies = allowed_company_ids;
            self.current_company_id = active_company_id;
            
            // Marquer correctement les compagnies selon la session
            self.companies_data.forEach(function(company) {
                company.current = (company.id === active_company_id);
                company.allowed = (allowed_company_ids.indexOf(company.id) !== -1);
            });
            
            console.log("Built companies data avec vraie logique:", self.companies_data);
            console.log("Current company ID:", self.current_company_id);
            console.log("Current allowed companies:", self.current_allowed_companies);
            
            return self.companies_data;
        }).catch(function (error) {
            self.displayNotification({
                type: 'danger',
                title: _t('Erreur'),
                message: _t('Impossible de charger les données des compagnies.'),
            });
            return Promise.reject(error);
        });
    },

    _showModal: function () {
        var self = this;
        
        // Remove any existing modal first
        $('#visualCompanySwitcherModal').remove();
        
        var $modal = $(QWeb.render('visual_company_switcher_modal', {}));
        $modal.appendTo($('body'));
        
        $modal.modal('show');
        
        // Initialize orgchart after modal is shown
        $modal.on('shown.bs.modal', function () {
            self._initializeOrgChart($modal);
        });
        
        // Clean up when modal is closed
        $modal.on('hidden.bs.modal', function () {
            $modal.remove();
        });
        
        // Bind events - toggle switch
        $modal.find('#multiSelectToggle').on('change', function () {
            self.multi_select_mode = $(this).prop('checked');
            self._toggleMultiSelectMode($modal);
        });
        
        $modal.find('#applySelection').on('click', function () {
            self._applyMultipleSelection($modal);
        });
        
        $modal.find('#clearSelection').on('click', function () {
            self._clearAllSelections($modal);
        });
    },

    _initializeOrgChart: function ($modal) {
        var self = this;
        var $container = $modal.find('#orgchart-container');
        
        // Show loading spinner
        $container.html('<div class="d-flex justify-content-center align-items-center h-100"><div class="spinner-border text-primary" role="status"><span class="sr-only">Chargement...</span></div></div>');
        
        // Transform data for orgchart
        var orgData = this._transformDataForOrgChart();
        
        if (orgData.length === 0) {
            $container.html('<div class="alert alert-info">Aucune compagnie disponible</div>');
            return;
        }
        
        // Clear container and initialize orgchart
        $container.empty();
        var $orgChart = $('<div id="orgchart"></div>').appendTo($container);
        
        $orgChart.orgchart({
            'data': orgData[0], // Root company
            'nodeTemplate': function (data) {
                return self._renderCompanyNode(data);
            },
            'direction': 't2b', // Top to bottom
            'pan': true,
            'zoom': true,
            'toggleSiblingsResp': false, // Disable default sibling highlighting
            'createNode': function($node, data) {
                // Mark currently allowed companies
                if (self.current_allowed_companies.indexOf(data.id) !== -1) {
                    $node.addClass('currently-allowed');
                }
                
                // Mark current active company
                if (data.current) {
                    $node.addClass('current-company');
                }
                
                // Add click handler
                $node.on('click.companyswitch', function(e) {
                    e.preventDefault();
                    e.stopPropagation();
                    
                    if (self.multi_select_mode) {
                        var clickedId = data.id;
                        
                        if (e.ctrlKey || e.metaKey) {
                            // ACTION: Désigner la compagnie active avec Ctrl+Clic
                            self.designatedActiveId = clickedId;
                            console.log("=== CTRL+CLIC DÉTECTÉ ===");
                            console.log("Compagnie désignée comme active:", clickedId);
                            console.log("designatedActiveId après:", self.designatedActiveId);
                            
                            // Assurer que la compagnie désignée est aussi cochée
                            if (self.selectedAllowedIds.indexOf(clickedId) === -1) {
                                self.selectedAllowedIds.push(clickedId);
                                console.log("Compagnie ajoutée aux cochées:", clickedId);
                            }
                            console.log("selectedAllowedIds après:", self.selectedAllowedIds);
                        } else {
                            // ACTION: Cocher / Décocher une compagnie
                            console.log("=== CLIC NORMAL DÉTECTÉ ===");
                            console.log("Compagnie cliquée:", clickedId);
                            var index = self.selectedAllowedIds.indexOf(clickedId);
                            if (index > -1) {
                                self.selectedAllowedIds.splice(index, 1); // Décocher
                                console.log("Compagnie décochée:", clickedId);
                                // Si on décoche la compagnie désignée comme active, la réinitialiser
                                if (self.designatedActiveId === clickedId) {
                                    self.designatedActiveId = null;
                                    console.log("designatedActiveId réinitialisée");
                                }
                            } else {
                                self.selectedAllowedIds.push(clickedId); // Cocher
                                console.log("Compagnie cochée:", clickedId);
                            }
                            console.log("selectedAllowedIds après:", self.selectedAllowedIds);
                            console.log("designatedActiveId après:", self.designatedActiveId);
                        }
                        
                        self._updateSelectionUI($modal);
                    } else {
                        // Mode simple : l'action est directe
                        session.setCompanies(data.id, [data.id]);
                    }
                });
                
                return $node;
            }
        });
    },

    _transformDataForOrgChart: function () {
        var companies = this.companies_data;
        var rootCompanies = companies.filter(function (company) {
            return !company.parent_id;
        });
        
        var self = this;
        function buildHierarchy(company) {
            var children = companies.filter(function (c) {
                return c.parent_id === company.id;
            });
            
            var node = {
                id: company.id,
                name: company.name,
                title: company.title,
                logo: company.logo,
                current: company.current,
                allowed: company.allowed,
            };
            
            if (children.length > 0) {
                node.children = children.map(buildHierarchy);
            }
            
            return node;
        }
        
        return rootCompanies.map(buildHierarchy);
    },

    _renderCompanyNode: function (data) {
        // Using structure inspired by OCA hr_org_chart_overview
        var nodeHtml = '<div class="company-node" data-company-id="' + data.id + '">';
        
        // Selection badge (hidden by default)
        nodeHtml += '<div class="selection-badge" style="display: none;">';
        nodeHtml += '<i class="fa fa-check-circle"></i>';
        nodeHtml += '</div>';
        
        // Current company badge (star icon)
        if (data.current) {
            nodeHtml += '<div class="current-badge">';
            nodeHtml += '<i class="fa fa-star"></i>';
            nodeHtml += '</div>';
        }
        
        // Logo section
        nodeHtml += '<span class="company-image">';
        if (data.logo) {
            nodeHtml += '<img src="data:image/png;base64,' + data.logo + '" alt="Logo ' + _.escape(data.name) + '"/>';
        } else {
            nodeHtml += '<div class="company-logo-placeholder"><i class="fa fa-building"></i></div>';
        }
        nodeHtml += '</span>';
        
        // Company info
        nodeHtml += '<div class="company-title">' + _.escape(data.name) + '</div>';
        if (data.title && data.title !== data.name) {
            nodeHtml += '<div class="company-content">' + _.escape(data.title) + '</div>';
        }
        
        nodeHtml += '</div>';
        return nodeHtml;
    },


    _toggleMultiSelectMode: function ($modal) {
        var $toggle = $modal.find('#multiSelectToggle');
        var $selectionInfo = $modal.find('#selectionInfo');
        var $applyButton = $modal.find('#applySelection');
        var $clearButton = $modal.find('#clearSelection');
        
        // Update toggle state to match mode
        $toggle.prop('checked', this.multi_select_mode);
        
        if (this.multi_select_mode) {
            // Switch to multi-select mode
            $selectionInfo.show();
            $applyButton.show();
            $clearButton.show();
            
            // Pre-select currently allowed companies
            this.selectedAllowedIds = [...this.current_allowed_companies];
            // Garder la compagnie actuellement active comme désignée
            this.designatedActiveId = this.current_company_id;
            this._updateSelectionUI($modal);
            
        } else {
            // Switch to single mode
            $selectionInfo.hide();
            $applyButton.hide();
            $clearButton.hide();
            
            // Clear all multi-selections
            this._clearAllSelections($modal);
        }
    },

    _updateSelectionUI: function ($modal) {
        var count = this.selectedAllowedIds.length;
        $modal.find('#selectionCount').text(count);
        $modal.find('#applyCount').text(count);
        
        // Enable/disable apply button
        var $applyButton = $modal.find('#applySelection');
        if (count > 0) {
            $applyButton.removeClass('btn-outline-success').addClass('btn-success');
        } else {
            $applyButton.removeClass('btn-success').addClass('btn-outline-success');
        }
        
        // Update visual selection in chart
        this._refreshChartSelection($modal);
        
        // Afficher quelle compagnie sera la principale
        this._updateActiveDesignation($modal);
    },
    
    _refreshChartSelection: function ($modal) {
        var self = this;
        
        // Clear all previous selections
        $modal.find('.company-node').removeClass('multi-selected single-selected');
        $modal.find('.selection-badge').hide();
        
        if (this.multi_select_mode) {
            // Show multi-selections
            this.selectedAllowedIds.forEach(function(company_id) {
                var $companyNode = $modal.find('.company-node[data-company-id="' + company_id + '"]');
                if ($companyNode.length) {
                    $companyNode.addClass('multi-selected');
                    $companyNode.find('.selection-badge').show();
                }
            });
        }
    },
    
    _updateActiveDesignation: function ($modal) {
        var self = this;
        
        // Déterminer quelle compagnie sera la principale selon la logique de repli
        var futureActiveId = null;
        if (this.selectedAllowedIds.length > 0) {
            if (this.designatedActiveId && this.selectedAllowedIds.indexOf(this.designatedActiveId) !== -1) {
                // Priorité 1: Compagnie explicitement désignée
                futureActiveId = this.designatedActiveId;
            } else if (this.selectedAllowedIds.indexOf(this.current_company_id) !== -1) {
                // Priorité 2: Compagnie actuellement active si cochée
                futureActiveId = this.current_company_id;
            } else {
                // Priorité 3: Première compagnie cochée
                futureActiveId = this.selectedAllowedIds[0];
            }
        }
        
        // Retirer toutes les désignations précédentes
        $modal.find('.company-node').removeClass('future-active');
        
        // Ajouter la classe pour la compagnie qui sera active
        if (futureActiveId) {
            $modal.find('.company-node[data-company-id="' + futureActiveId + '"]').addClass('future-active');
        }
    },
    
    _clearAllSelections: function ($modal) {
        this.selectedAllowedIds = [];
        this.designatedActiveId = null;
        this._updateSelectionUI($modal);
    },

    _switchToSingleCompany: function (company_id) {
        var self = this;
        
        // Find company name for confirmation
        var company = this.companies_data.find(c => c.id === company_id);
        var companyName = company ? company.name : 'Compagnie inconnue';
        
        // Show confirmation dialog
        this._showConfirmationDialog(
            'Changer de compagnie',
            `Voulez-vous basculer vers "${companyName}" ?`,
            'Confirmer',
            'btn-primary',
            function() {
                // Clic simple : cette compagnie devient active et unique
                self._updateCompanyContext(company_id, [company_id]);
            }
        );
    },

    _applyMultipleSelection: function ($modal) {
        var self = this;
        
        if (this.selectedAllowedIds.length === 0) {
            this.displayNotification({
                type: 'warning',
                title: _t('Attention'),
                message: _t('Veuillez sélectionner au moins une compagnie.'),
            });
            return;
        }
        
        // Show confirmation with company names
        var selectedNames = this.selectedAllowedIds.map(id => {
            var company = this.companies_data.find(c => c.id === id);
            return company ? company.name : `ID: ${id}`;
        });
        
        var message;
        if (this.selectedAllowedIds.length === 1) {
            message = `Utiliser "${selectedNames[0]}" comme compagnie active ?`;
        } else {
            message = `Utiliser ${this.selectedAllowedIds.length} compagnies sélectionnées ?\n\n• ${selectedNames.join('\n• ')}\n\nLa première sera la compagnie principale.`;
        }
        
        this._showConfirmationDialog(
            'Appliquer sélection',
            message,
            'Appliquer',
            'btn-success',
            function() {
                self._performMultipleSwitch();
            }
        );
    },
    
    _performMultipleSwitch: function() {
        var self = this;
        
        // Récupérer les états finaux
        let finalActive = this.designatedActiveId;
        
        if (this.selectedAllowedIds.length === 0) {
            this.displayNotification({
                type: 'warning',
                title: _t('Attention'),
                message: _t('Veuillez sélectionner au moins une compagnie.'),
            });
            return;
        }
        
        // Logique de repli : si aucune active n'est désignée OU si elle a été décochée
        if (!finalActive || this.selectedAllowedIds.indexOf(finalActive) === -1) {
            // PRIORITÉ CORRIGÉE : Prendre la PREMIÈRE compagnie sélectionnée
            // (l'ordre de sélection détermine la priorité, pas la compagnie actuellement active)
            finalActive = this.selectedAllowedIds[0];
        }
        
        // CORRECTION CLÉE : Construire finalAllowed avec la compagnie active en PREMIER
        const finalAllowed = [finalActive, ...this.selectedAllowedIds.filter(id => id !== finalActive)];
        
        // L'appel final qui ne peut pas échouer
        session.setCompanies(finalActive, finalAllowed);
    },
    

    _showConfirmationDialog: function(title, message, confirmText, confirmClass, onConfirm) {
        var $dialog = $(`
            <div class="modal fade" id="companyConfirmModal" tabindex="-1" role="dialog">
                <div class="modal-dialog modal-sm" role="document">
                    <div class="modal-content">
                        <div class="modal-header">
                            <h5 class="modal-title">${_.escape(title)}</h5>
                            <button type="button" class="close" data-dismiss="modal">
                                <span>&times;</span>
                            </button>
                        </div>
                        <div class="modal-body">
                            <p style="white-space: pre-line;">${_.escape(message)}</p>
                        </div>
                        <div class="modal-footer">
                            <button type="button" class="btn btn-secondary" data-dismiss="modal">
                                <i class="fa fa-times mr-1"></i>Annuler
                            </button>
                            <button type="button" class="btn ${confirmClass}" id="confirmAction">
                                <i class="fa fa-check mr-1"></i>${_.escape(confirmText)}
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        `);
        
        $dialog.appendTo($('body'));
        $dialog.modal('show');
        
        // Handle confirm action
        $dialog.find('#confirmAction').on('click', function() {
            $dialog.modal('hide');
            onConfirm();
        });
        
        // Clean up when closed
        $dialog.on('hidden.bs.modal', function () {
            $dialog.remove();
        });
    },
});

// Systray menu item
var SystrayCompanySwitcher = Widget.extend({
    template: 'SystrayCompanySwitcher',
    
    events: {
        'click .o_visual_company_switcher': '_openSwitcher',
    },

    _openSwitcher: function () {
        var switcher = new VisualCompanySwitcher(this);
        switcher._openModal();
    },
});

SystrayMenu.Items.push(SystrayCompanySwitcher);

return {
    VisualCompanySwitcher: VisualCompanySwitcher,
    SystrayCompanySwitcher: SystrayCompanySwitcher,
};

});